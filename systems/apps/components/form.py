from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
# https://flask-wtf.readthedocs.io/en/1.0.x/
from wtforms import StringField, PasswordField, SelectField
# https://wtforms.readthedocs.io/en/3.0.x/
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    domicile = StringField('Domicile', validators=[DataRequired()])
    gender = StringField('Gender', validators=[DataRequired()])

class PrintedDataForm(FlaskForm):
    content_id = StringField('Content ID', validators=[DataRequired()])
    title = StringField('Name', validators=[DataRequired()])
    language = StringField('Language', validators=[DataRequired()])
    source = StringField('Source', validators=[DataRequired()])
    isbn = StringField('ISBN', validators=[DataRequired()])
    files = FileField('Files', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'pdf', 'doc', 'docx', 'txt', 'odt'], 'Images or Documents only!'), FileRequired()])

class UpdatePrintedDataForm(FlaskForm):
    content_id = StringField('Content ID', validators=[DataRequired()])
    title = StringField('Name', validators=[DataRequired()])
    language = StringField('Language', validators=[DataRequired()])
    source = StringField('Source', validators=[DataRequired()])
    isbn = StringField('ISBN', validators=[DataRequired()])
    content = StringField('Content', validators=[DataRequired()])
    # files = FileField('Files', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!'), FileRequired()])
    
class DigitalDataForm(FlaskForm):
    content_id = StringField('Content ID', validators=[DataRequired()])
    title = StringField('Name', validators=[DataRequired()])
    language = StringField('Language', validators=[DataRequired()])
    source = StringField('Source', validators=[DataRequired()])
    url_link = StringField('Url Link', validators=[DataRequired()])
    content = StringField('Content', validators=[DataRequired()])
    # imagefile = FileField('Image File', validators=[FileAllowed(['jpg', 'png'], 'Images only!'), FileRequired()])
    

# Admin's Form Privillege
class UserManagerAddForm(RegisterForm):
    role_type = SelectField(u'Role Types', choices=[(1, 'Admin'), (2, 'User')])

class UserManagerEditForm(UserManagerAddForm):
    uuid = StringField('Uuid', validators=[DataRequired()])
    status = StringField('Status', validators=[DataRequired()])
    subscribed = StringField('Subscribed', validators=[DataRequired()])
    
class LangManagerForm(FlaskForm):
    lang_uuid = StringField('Language UUID', validators=[DataRequired()])
    lang_name = StringField('Language Name', validators=[DataRequired()])
    lang_code = StringField('Language Code', validators=[DataRequired()])

class SourceTypeManagerForm(FlaskForm):
    sc_uuid = StringField('Source UUID', validators=[DataRequired()])
    sc_name = StringField('Source Name', validators=[DataRequired()])
    sc_type = StringField('Source Type', validators=[DataRequired()])

class DomicileManagerForm(FlaskForm):
    dom_uuid = StringField('Domicile UUID', validators=[DataRequired()])
    dom_name = StringField('Domicile Name', validators=[DataRequired()])
    dom_code = StringField('Domicile Code', validators=[DataRequired()])

class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])

class ResetPasswordForm(FlaskForm):
    # token = StringField('Token', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

# class NewsletterArticleForm(FlaskForm):
#     title = StringField('Title', validators=[DataRequired()])
#     content = StringField('Content', validators=[DataRequired()])
#     thumbnail = StringField('Thumbnail', validators=[DataRequired()])
    