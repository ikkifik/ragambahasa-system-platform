from flask import request, jsonify, make_response
from apps.apis import bp
from apps.auth import token_required
from apps.models import db, Languages
from apps.components import LangManagerForm

# # # # # # # # # # # # # # # # # # # # #
#       Language Management (Admin)     #
# # # # # # # # # # # # # # # # # # # # #

@bp.route('/manage/lang/add', methods=['POST'])
@token_required
def languages_add(current_user):
    
    if current_user.role_type != 1:
        return make_response(jsonify(message="Unauthorize User", status=False), 401)
    
    form = LangManagerForm(request.form)
    
    # if form.validate_on_submit():
    try:
        lang_name = form.lang_name.data
        lang_code = form.lang_code.data
        
        langin = Languages(lang_name=lang_name, lang_code=lang_code)
        
        db.session.add(langin)
        db.session.commit()

    except Exception as e:
        print(e)
        return make_response(jsonify(status=False, message="Internal Error"), 500)
    
    return make_response(jsonify(status=True, message="Success Add New Language Lists"), 200)


@bp.route('/manage/lang/delete', methods=['DELETE'])
@token_required
def languages_delete(current_user):
    
    if current_user.role_type != 1:
        return make_response(jsonify(message="Unauthorize User", status=False), 401)
    
    try:
        getreq = request.get_json()
        getuid = Languages.query.filter(Languages.uuid==getreq['lang_uuid']).first_or_404()
        
        db.session.delete(getuid)
        db.session.commit()
    except Exception as e:
        print(e)
        return make_response(jsonify(status=False, message="Internal Error"), 500)
    
    return make_response(jsonify(status=True, message="Success Delete Language Lists"), 200)

@bp.route('/manage/lang/view', methods=['GET'])
@token_required
def languages_show(current_user):
    
    if current_user.role_type != 1:
        return make_response(jsonify(message="Unauthorize User", status=False), 401)
    
    languages = Languages.query.all()
    languages = [{
        "lang_uuid": language.uuid,
        "lang_name": language.lang_name,
        "lang_code": language.lang_code, 
        } for language in languages]
        
    return make_response(jsonify(data=languages, status=True), 200)

@bp.route('/lang/list', methods=['GET'])
def language_lists():
    
    languages = Languages.query.all()
    languages = [{
        "lang_id": language.lid,
        "lang_name": language.lang_name,
        } for language in languages]
        
    return make_response(jsonify(data=languages, status=True), 200)

@bp.route('/manage/lang/edit', methods=['POST'])
@token_required
def languages_edit(current_user):
    
    if current_user.role_type != 1:
        return make_response(jsonify(message="Unauthorize User", status=False), 401)

    try:
        form = LangManagerForm(request.form)
        
        language = Languages.query.filter(Languages.uuid==form.lang_uuid.data).first_or_404()
        language.lang_name = form.lang_name.data
        language.lang_code = form.lang_code.data
        
        db.session.commit()
    
    except Exception as e:
        print(e)
        return make_response(jsonify(message="Error", status=False), 501)
        
    return make_response(jsonify(message="Language has been update successfully", status=True), 200)
