from flask import request, jsonify, make_response
from apps.apis import bp
from apps.auth import token_required
from apps.models import db, Users
from apps.components import UserManagerAddForm, UserManagerEditForm

# # # # # # # # # # # # # # # # # # #
#       User Management (Admin)     #
# # # # # # # # # # # # # # # # # # #

@bp.route('/manage/user/add', methods=['POST'])
@token_required
def user_add(current_user):
    
    if current_user.role_type != 1:
        return make_response(jsonify(message="Unauthorize User", status=False), 401)
    
    form = UserManagerAddForm(request.form)
    
    # if form.validate_on_submit():
    try:
        name = form.name.data
        email = form.email.data
        password = form.password.data
        domicile = form.domicile.data
        gender = form.gender.data
        role_type = form.role_type.data
        
        uin = Users(name=name, email=email, gender=gender, domicile=domicile, status="active", subscribed="yes", role_type=role_type)
        uin.set_password(password)
        
        db.session.add(uin)
        db.session.commit()

    except:
        return make_response(jsonify(status=False, message="Error"), 500)
    
    return make_response(jsonify(status=True, message="Success Add User"), 200)


@bp.route('/manage/user/delete', methods=['DELETE'])
@token_required
def user_delete(current_user):
    
    if current_user.role_type != 1:
        return make_response(jsonify(message="Unauthorize User", status=False), 401)
    
    try:
        getreq = request.get_json()
        getuid = Users.query.filter(Users.uuid==getreq['uuid']).first_or_404()
        
        db.session.delete(getuid)
        db.session.commit()
    except:
        return make_response(jsonify(status=False, message="Error"), 500)
    
    return make_response(jsonify(status=True, message="Success Delete User"), 200)

@bp.route('/manage/user/view', methods=['POST'])
@token_required
def user_show(current_user):
    
    if current_user.role_type != 1:
        return make_response(jsonify(message="Unauthorize User", status=False), 401)
    
    users = Users.query.all()
    users = [{
        "user_id": user.uuid, 
        "name": user.name, 
        "email": user.email, 
        "domicile": user.domicile, 
        "gender": user.gender.name, 
        "status": user.status.name, 
        "subscribed": user.subscribed.name, 
        "role_type": user.role_type, 
        "created_at": str(user.created_at)        
        } for user in users]
        
    return make_response(jsonify(data=users, status=True), 200)

@bp.route('/manage/user/edit', methods=['POST'])
@token_required
def user_edit(current_user):
    
    if current_user.role_type != 1:
        return make_response(jsonify(message="Unauthorize User", status=False), 401)

    try:
        form = UserManagerEditForm(request.form)
        
        user = db.session.execute(db.select(Users).filter_by(uuid=form.uuid.data)).scalar()
        if user is None:
            return make_response(jsonify(message="Cannot find User", status=False), 400)
        
        # user = Users.query.filter(Users.uuid==form.uuid.data).first_or_404()
        user.name = form.name.data
        user.email = form.email.data
        user.domicile = form.domicile.data
        user.gender = form.gender.data
        user.role_type = form.role_type.data
        
        if form.status.data:
            user.status = form.status.data
        if form.subscribed.data:
            user.subscribed = form.subscribed.data
        
        if form.password.data:
            user.set_password(form.password.data)
        else:
            return make_response(jsonify(message="Password cannot empty", status=False), 400)
        
        db.session.commit()
    
    except Exception as e:
        print(e)
        return make_response(jsonify(message="Internal Error", status=False), 500)
        
    return make_response(jsonify(message="User has been update successfully", status=True), 200)
