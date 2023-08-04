from flask import request, jsonify, make_response
from apps.apis import bp
from apps.auth import token_required
from apps.models import db, Domiciles
from apps.components import DomicileManagerForm

# # # # # # # # # # # # # # # # # # # # #
#       Domicile Management (Admin)     #
# # # # # # # # # # # # # # # # # # # # #

@bp.route('/manage/dom/add', methods=['POST'])
@token_required
def domiciles_add(current_user):
    
    if current_user.role_type != 1:
        return make_response(jsonify(message="Unauthorize User", status=False), 401)
    
    form = DomicileManagerForm(request.form)
    
    # if form.validate_on_submit():
    try:
        dom_name = form.dom_name.data
        dom_code = form.dom_code.data
        
        domin = Domiciles(dom_name=dom_name, dom_code=dom_code)
        
        db.session.add(domin)
        db.session.commit()

    except:
        return make_response(jsonify(status=False, message="Error"), 500)
    
    return make_response(jsonify(status=True, message="Success Add New Domicile Lists"), 200)


@bp.route('/manage/dom/delete', methods=['DELETE'])
@token_required
def domiciles_delete(current_user):
    
    if current_user.role_type != 1:
        return make_response(jsonify(message="Unauthorize User", status=False), 401)
    
    try:
        getreq = request.get_json()
        getuid = Domiciles.query.filter(Domiciles.uuid==getreq['dom_uuid']).first_or_404()
        
        db.session.delete(getuid)
        db.session.commit()
    except:
        return make_response(jsonify(status=False, message="Error"), 500)
    
    return make_response(jsonify(status=True, message="Success Delete Domicile Lists"), 200)

@bp.route('/manage/dom/view', methods=['GET'])
@token_required
def domiciles_show(current_user):
    
    if current_user.role_type != 1:
        return make_response(jsonify(message="Unauthorize User", status=False), 401)
    
    domiciles = Domiciles.query.all()
    domiciles = [{
        "dom_uuid": domicile.uuid,
        "dom_name": domicile.dom_name,
        "dom_code": domicile.dom_code, 
        } for domicile in domiciles]
        
    return make_response(jsonify(data=domiciles, status=True), 200)

@bp.route('/dom/list', methods=['GET'])
def domicile_lists():
    
    domiciles = Domiciles.query.all()
    domiciles = [{
        # "dom_id": domicile.did,
        "dom_name": domicile.dom_name,
        } for domicile in domiciles]
        
    return make_response(jsonify(data=domiciles, status=True), 200)

@bp.route('/manage/dom/edit', methods=['POST'])
@token_required
def domiciles_edit(current_user):
    
    if current_user.role_type != 1:
        return make_response(jsonify(message="Unauthorize User", status=False), 401)

    try:
        form = DomicileManagerForm(request.form)
        
        domicile = Domiciles.query.filter(Domiciles.uuid==form.dom_uuid.data).first_or_404()
        domicile.dom_name = form.dom_name.data
        domicile.dom_code = form.dom_code.data
        
        db.session.commit()
    
    except Exception as e:
        print(e)
        return make_response(jsonify(message="Error", status=False), 501)
        
    return make_response(jsonify(message="Domicile has been update successfully", status=True), 200)
