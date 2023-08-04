from flask import request, jsonify, make_response
from apps.apis import bp
from apps.auth import token_required
from apps.models import db, SourceTypes
from apps.components import SourceTypeManagerForm

# # # # # # # # # # # # # # # # # # # # # # #
#       Source Types Management (Admin)     #
# # # # # # # # # # # # # # # # # # # # # # #

@bp.route('/manage/resources/add', methods=['POST'])
@token_required
def resources_add(current_user):
    
    if current_user.role_type != 1:
        return make_response(jsonify(message="Unauthorize User", status=False), 401)
    
    form = SourceTypeManagerForm(request.form)
    
    # if form.validate_on_submit():
    try:
        sc_name = form.sc_name.data
        sc_type = form.sc_type.data
        
        scin = SourceTypes(sc_name=sc_name, sc_type=sc_type)
        
        db.session.add(scin)
        db.session.commit()

    except:
        return make_response(jsonify(status=False, message="Error"), 500)
    
    return make_response(jsonify(status=True, message="Success Add New Source Type Lists"), 200)


@bp.route('/manage/resources/delete', methods=['DELETE'])
@token_required
def resources_delete(current_user):
    
    if current_user.role_type != 1:
        return make_response(jsonify(message="Unauthorize User", status=False), 401)
    
    try:
        getreq = request.get_json()
        getuid = SourceTypes.query.filter(SourceTypes.uuid==getreq['sc_uuid']).first_or_404()
        
        db.session.delete(getuid)
        db.session.commit()
    except:
        return make_response(jsonify(status=False, message="Error"), 500)
    
    return make_response(jsonify(status=True, message="Success Delete Source Type Lists"), 200)

@bp.route('/manage/resources/view', methods=['GET'])
@token_required
def resources_show(current_user):
    
    if current_user.role_type != 1:
        return make_response(jsonify(message="Unauthorize User", status=False), 401)
    
    source_types = SourceTypes.query.all()
    source_types = [{
        "sc_uuid": source_type.uuid,
        "sc_name": source_type.sc_name,
        "sc_type": source_type.sc_type, 
        } for source_type in source_types]
        
    return make_response(jsonify(data=source_types, status=True), 200)

@bp.route('/src/list', methods=['GET'])
def resources_lists():
    
    source_types = SourceTypes.query.all()
    source_types = [{
        "sc_id": source.stid,
        "sc_name": source.sc_name,
        } for source in source_types]
        
    return make_response(jsonify(data=source_types, status=True), 200)

@bp.route('/manage/resources/edit', methods=['POST'])
@token_required
def resources_edit(current_user):
    
    if current_user.role_type != 1:
        return make_response(jsonify(message="Unauthorize User", status=False), 401)

    try:
        form = SourceTypeManagerForm(request.form)
        
        source_type = SourceTypes.query.filter(SourceTypes.uuid==form.sc_uuid.data).first_or_404()
        source_type.sc_name = form.sc_name.data
        source_type.sc_type = form.sc_type.data
        
        db.session.commit()
    
    except Exception as e:
        print(e)
        return make_response(jsonify(message="Error", status=False), 501)
        
    return make_response(jsonify(message="Source Type has been updated successfully", status=True), 200)
