from flask import jsonify, request, redirect, url_for, current_app, make_response
from flask_login import login_user, logout_user
from functools import wraps
from datetime import datetime, timedelta
from jinja2 import Environment, FileSystemLoader, select_autoescape

from apps.auth import bp
from apps.components import RegisterForm, ForgotPasswordForm, ResetPasswordForm
from apps.models import db, PasswordResetToken
from apps.models.users import Users, check_password_hash
from apps.helper import Mail
import jwt


def token_required(f):
   @wraps(f)
   def decorator(*args, **kwargs):
       token = None
       if 'x-access-tokens' in request.headers:
           token = request.headers['x-access-tokens']
 
       if not token:
           return make_response(jsonify({'message': 'a valid token is missing'}), 403)
       try:
           data = jwt.decode(token, current_app.secret_key, algorithms=["HS256"])
           current_user = Users.query.filter_by(uuid=data['uuid']).first()
       except:
           return make_response(jsonify({'message': 'token is invalid'}), 403)

       return f(current_user, *args, **kwargs)
   return decorator

def get_reset_token(token, expires):
    return jwt.encode({'reset_password': token, 'exp': expires}, 
                      current_app.secret_key, "HS256")

def redirect_page():
    env = Environment(
        loader= FileSystemLoader(searchpath="apps/static/mail_content"),
        autoescape=select_autoescape(['html', 'xml'])
    )
    return env

def get_confirm_token(token, expires):
    return jwt.encode({'confirmation_code': token, 'exp': expires}, 
                      current_app.secret_key, "HS256")

@bp.route('/register', methods=['POST'])
async def register():
    form = RegisterForm(request.form)
    
    # Email Availability Check
    check = Users.query.filter(Users.email==form.email.data).first()
    if check is not None and check.email == form.email.data:
        return make_response(jsonify(message="Email has already registered"), 400)
    
    name = form.name.data
    email = form.email.data
    password = form.password.data
    domicile = form.domicile.data
    gender = form.gender.data

    
    uin = Users(name=name, email=email, gender=gender, domicile=domicile, role_type=2)
    uin.set_password(password)
    
    db.session.add(uin)
    db.session.commit()

    try:    
        # Confirmation
        user_uuid = uin.uuid
        expires_time = datetime.utcnow()+timedelta(days=3)
        # confirmation token for email confirmation
        get_token = get_confirm_token(token=user_uuid, expires=expires_time)
        # throw it to email 

        if current_app.config['PRODUCTION']:
            root_url = current_app.config['HOST_DOMAIN']
        else:
            root_url = request.root_url[:-1]

        redirect_url = root_url+url_for('auth.register_confirm', token=get_token)
        
        mail = Mail()
        mail.account_confirmation_mail(name=name, recepient_mail=email, redirect_url=redirect_url)
    except:
        db.session.delete(uin)
        db.session.commit()
        
    return make_response(jsonify(message="User has been added successfully"), 201)

@bp.route('/register/confirm/<token>', methods=['GET'])
async def register_confirm(token):
    
    token = jwt.decode(token, current_app.secret_key, algorithms=["HS256"])
    user = db.session.execute(db.select(Users).filter_by(uuid=token['confirmation_code'])).scalar()
    
    user.status = "active"
    user.subscribed = "yes"
    db.session.add(user)
    db.session.commit()
    
    # Ganti dengan static website sederhana
    env = redirect_page()
    page = env.get_template("email_redirected_page.html")
    
    return page.render()
    # return make_response(jsonify(message="User has been activated"), 200)


@bp.route('/auth', methods=['POST'])
async def login():
    # form = LoginForm(request.form)
    auth = request.authorization
    
    if not auth or not auth.username or not auth.password: 
       return make_response('could not verify', 401, {'Authentication': 'Login Required'})   
 
    user = Users.query.filter_by(email=auth.username).first()  
    if user is not None and check_password_hash(user.password, auth.password):

        if user.status.name != "active":
            if user.status.name == "blocked":
                return make_response(jsonify(message="Your account has been blocked", status=False), 400)
            elif user.status.name == "inactive":
                return make_response(jsonify(message="Please activate your account", status=False), 400)
        
        token = jwt.encode({'uuid': user.uuid, 'roles': user.role_type, 'exp': datetime.utcnow()+timedelta(days=14)}, 
                           current_app.secret_key, "HS256")
    
        return make_response(jsonify({'token' : token}), 201)
    
    return make_response('Could Not Verify',  401, {'Authentication': 'Wrong username/password'})


@bp.route('/auth/out', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('auth.index'))

@bp.route('/forgot-password', methods=['POST'])
async def forgot_password():
    form = ForgotPasswordForm(request.form)
    
    # Email Availability Check
    check = Users.query.filter(Users.email==form.email.data).first()
    # if check is not None and check.email == form.email.data:
    if check is None:
        return make_response(jsonify(message="Thank you, please check your email for the new access and try to login again", status=True), 200)
    
    import secrets, os
    create_token = secrets.token_urlsafe()
    expires_time = datetime.utcnow()+timedelta(minutes=60*3)
    
    check_token_availability = db.session.execute(db.select(PasswordResetToken).filter_by(user_uuid=check.uuid)).scalar()
    if check_token_availability is not None:
        check_token_availability.token = create_token
        check_token_availability.token_expiry = expires_time
        db.session.add(check_token_availability)
    else:
        store_token = PasswordResetToken(user_uuid=check.uuid, token=create_token, token_expiry=expires_time)
        db.session.add(store_token)
    
    db.session.commit()
    
    # reset token for email confirmation
    get_token = get_reset_token(token=create_token, expires=expires_time)
    # throw it to email 

    if current_app.config['PRODUCTION']:
        root_url = current_app.config['HOST_DOMAIN']
    else:
        root_url = request.root_url[:-1]
        
    redirect_url = root_url+url_for('auth.reset_password', token=get_token)
    
    mail = Mail()
    mail.reset_password_mail(name=check.name, recepient_mail=check.email, redirect_url=redirect_url)
    
    return make_response(jsonify(message="Thank you, please check your email for the new access and try to login again", status=True), 200)

@bp.route('/reset-password/<token>', methods=['GET'])
async def reset_password(token):
    
    # if request.method == "GET":
    get_token = jwt.decode(token, current_app.secret_key, algorithms=["HS256"])
    check_token = db.session.execute(db.select(PasswordResetToken).filter_by(token=get_token['reset_password'])).scalar()
    if check_token is None:
        return make_response(jsonify(message="Token Invalid", status=False), 400)
    
    # return make_response(jsonify(message="Reset Token is Valid", status=True, token=token['reset_password']), 200)

    env = redirect_page()
    page = env.get_template("reset_password_page.html")
    
    if current_app.config['PRODUCTION']:
        root_url = current_app.config['HOST_DOMAIN']
    else:
        root_url = request.root_url[:-1]
    
    target_url = root_url+url_for('auth.reset_password_confirm', token=token)
    
    return page.render(target_url=target_url)
    
    # Ganti dengan redirect, bikin static page sederhana isinya form
    # return redirect(url_for())

@bp.route('/reset-password/confirm/<token>', methods=['POST'])
async def reset_password_confirm(token):
    # elif request.method == "POST":
    form = ResetPasswordForm(request.form)
    
    # Check similarity token JWT info with inputted token
    token = jwt.decode(token, current_app.secret_key, algorithms=["HS256"])
    # if token['reset_password'] != form.token.data:
    #     return make_response(jsonify(message="Invalid Token", status=False), 400)
    
    # Check if token available in database
    check = db.session.execute(db.select(PasswordResetToken).filter_by(token=token['reset_password'])).scalar()
    if check is None:
        return make_response(jsonify(message="Invalid Request", status=False), 400)
    
    # Check if user with UUID available
    get_user = db.session.execute(db.select(Users).filter_by(uuid=check.user_uuid)).scalar()
    if get_user is None:
        return make_response(jsonify(message="Invalid Request", status=False), 400)
    
    # Check if password has inputted
    if form.password.data:
        get_user.set_password(form.password.data)
    else:
        return make_response(jsonify(message="Password cannot empty", status=False), 400)
    
    db.session.delete(check)
    db.session.commit()
    
    env = redirect_page()
    page = env.get_template("reset_password_success.html")
    
    return page.render()
    
    # return make_response(jsonify(message="Password has been update successfully", status=True), 200)
    