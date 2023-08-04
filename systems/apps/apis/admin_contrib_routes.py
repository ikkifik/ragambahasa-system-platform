from flask import make_response, request, jsonify, current_app
from werkzeug.utils import secure_filename

from apps.apis import bp
from apps.auth import token_required
from apps.components import PrintedDataForm, DigitalDataForm, UpdatePrintedDataForm
from apps.models import db, PrintedData, PrintedContent, DigitalData, Users, Languages

import os
import re

# # # # # # # # # # # # # # #
#     Admin Contribution    #
# # # # # # # # # # # # # # #

from datetime import datetime
import random

def generate_filename():
    today = datetime.now()
    today = datetime.strftime(today, "%Y%m%d_%H%M%S")
    
    keyword = "bhinnekaindonesiaacegaruda"
    code = str(random.randint(1,999))+str("".join(random.sample(keyword, 2)))
    code = list(code)
    random.shuffle(code)
    filename = str(today)+str("".join(code))
    
    return filename

def extension_check(filelist):
    count = 0
    permitted_ext = ['jpg', 'jpeg', 'png', 'pdf', 'doc', 'docx', 'txt', 'odt']
    for fl in filelist:
        ext = fl.filename.split(".")[-1]
        if ext not in permitted_ext:
            count+=1
    
    if count > 0:
        return False
    return True

def content_langdir(langname):
    dirname = re.sub("[^A-Z]", "_", langname,0,re.IGNORECASE)
    dirname = re.sub("_+", "_", dirname)
    dirname = dirname.lower().rstrip("_")
    
    return dirname

# # # # # # # # # # # # # # # # # # # # # # # # # # # -Routes-  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

''' Add '''
@bp.route('/su/contrib/add', methods=['POST'])
@token_required
def admin_contrib_add(current_user):
    if current_user.role_type != 1:
        return make_response(jsonify(message="Forbidden Access", status=False), 403)
    
    data_type = request.args.get('type')
    get_uinfo = db.session.execute(db.select(Users).filter_by(uuid=current_user.uuid)).scalar()
    
    try:
        if data_type.lower() == "printed":
            form = PrintedDataForm(request.form)
            
            title = form.title.data
            language = int(form.language.data)
            source = int(form.source.data)
            isbn = ""
            if form.isbn.data:
                isbn = form.isbn.data
                
            langname = db.session.execute(db.select(Languages).filter_by(lid=language)).scalar()
            if langname is None:
                    return make_response(jsonify(message="Bad request", status=False), 400)
                
            langdir = content_langdir(langname.lang_name)
            
            path = os.path.join(current_app.root_path, 'static', 'uploaded', langdir)
            os.makedirs(path, exist_ok=True)
            
            add_print = PrintedData(uid=get_uinfo.uid, lid=language, stid=source, title=title, isbn=isbn)
            db.session.add(add_print)
            db.session.flush()

            generated_filename = generate_filename()
            generated_filename = str(title.replace(" ", "_").lower())+"_"+generated_filename
            files = request.files.getlist("files") # Only Support: jpg, jpeg, png, pdf, doc, docx, txt, odt
            ext_check = extension_check(files)
            
            if not ext_check:
                return make_response(jsonify(message="Unsupported file type", status=False), 415)
            
            for fl in files:
                findex = files.index(fl)+1
                pagenum = "_page"+str(findex)+"."+fl.filename.split(".")[-1]
                file_path = os.path.join(path, generated_filename+pagenum)
                fl.save(file_path)

                path_to_save = os.path.join('static', 'uploaded', langdir, generated_filename+pagenum)
                add_content = PrintedContent(pid=add_print.pid, page_num=findex, file_path=path_to_save)
                db.session.add(add_content)

            db.session.commit()
            
        elif data_type.lower() == "digital":
            form = DigitalDataForm(request.form)
            
            title = form.title.data
            language = int(form.language.data)
            source = int(form.source.data)
            url_link = form.url_link.data
            content = form.content.data

            langname = db.session.execute(db.select(Languages).filter_by(lid=language)).scalar()
            if langname is None:
                    return make_response(jsonify(message="Bad request", status=False), 400)
            
            add_content = DigitalData(uid=get_uinfo.uid, lid=language, stid=source, title=title, 
                                    content=content, url_path=url_link)
            db.session.add(add_content)
            db.session.commit()
            
        else:
            return make_response(jsonify(message="Unsupported data type", status=False), 415)
        
        data = {
            "title": title,
            "language": language,
            "source": source,
        }
    except Exception as e:
        print(e)
        return make_response(jsonify(message="Internal Server Error", status=False), 500)    
    
    return make_response(jsonify(type=data_type, status=True, data=data), 200)


''' Update '''
@bp.route('/su/contrib/update', methods=['POST'])
@token_required
def admin_contrib_update(current_user):
    if current_user.role_type != 1:
        return make_response(jsonify(message="Forbidden Access", status=False), 403)
    
    data_type = request.args.get('type')
    try:
        if data_type.lower() == "printed":
            form = UpdatePrintedDataForm(request.form)
            
            content_id = form.content_id.data
            
            printed = db.session.execute(db.select(PrintedData).filter_by(uuid=content_id)).scalar()            
            if form.title.data is not None and form.title.data != "":          
                printed.title = form.title.data

            if form.language.data is not None and form.language.data != "":
                printed.lid = int(form.language.data)

            if form.source.data is not None and form.source.data != "":
                printed.source = int(form.source.data)
            
            if form.isbn.data is not None and form.isbn.data != "":
                printed.isbn = form.isbn.data
            
            # printed.content_1 = form.content_1.data
            # printed.content_2 = form.content_2.data
            # printed.content_3 = form.content_3.data
            
            db.session.add(printed)
            db.session.commit()
            
        elif data_type.lower() == "digital":
            form = DigitalDataForm(request.form)
            
            content_id = form.content_id.data
            
            digital = db.session.execute(db.select(DigitalData).filter_by(uuid=content_id)).scalar()
            if form.title.data is not None and form.title.data != "":
                digital.title = form.title.data
            
            if form.language.data is not None and form.language.data != "":
                digital.lid = int(form.language.data)
            
            if form.source.data is not None and form.source.data != "":
                digital.source = int(form.source.data)
            
            if form.url_link.data is not None and form.url_link.data != "":
                digital.url_link = form.url_link.data

            if form.content.data is not None and form.content.data != "":
                digital.content = form.content.data

            db.session.add(digital)
            db.session.commit()
            
        else:
            return make_response(jsonify(message="Unsupported data type", status=False), 415)
    except Exception as e:
        print(e)
        return make_response(jsonify(message="Internal Server Error", status=False), 500)    
    
    return make_response(jsonify(type=data_type, status=True, message="Updated Successfully"), 200)

''' Delete '''
@bp.route('/su/contrib/remove', methods=['DELETE'])
@token_required
def admin_contrib_remove(current_user):
    if current_user.role_type != 1:
        return make_response(jsonify(message="Forbidden Access", status=False), 403)
    
    try:
        getreq = request.get_json()
        
        content_id = getreq['content_id'] # uuid of content
        content_type = getreq['type']
        
        if content_id is None or content_id == "":
            return make_response(jsonify(status=401, message="Please Provide Content ID"), 401)
        
        if content_type is None or content_type == "":
            return make_response(jsonify(status=401, message="Please Provide Content Type"), 401)
        
        if content_type.lower() == "printed":
            selected_content = db.session.execute(db.select(PrintedData).filter_by(uuid=getreq["content_id"])).scalar()            
        elif content_type.lower() == "digital":
            selected_content = db.session.execute(db.select(DigitalData).filter_by(uuid=getreq["content_id"])).scalar()
        else:
            return make_response(jsonify(status=401, message="Sorry we could not understand your request :("), 401)

        # selected_content.status = 0
        db.session.delete(selected_content)
        
        db.session.commit()
    except Exception as e:
        print(e)
        return make_response(jsonify(status=500, message="Internal Server Error"), 500)
    
    return make_response(jsonify(status=200, message="Success Delete Domicile Lists"), 200)


''' View '''
@bp.route('/su/contrib/view', methods=['POST'])
@token_required
def admin_contrib_view(current_user):
    if current_user.role_type != 1:
        return make_response(jsonify(message="Forbidden Access", status=False), 403)

    data_type = request.args.get('type')
    # user_uuid = str(request.form.get('user_uuid'))
    # getreq = request.get_json()
    # getuid = Users.query.filter(Users.uuid==current_user.uuid).first_or_404()

    try:
        if data_type.lower() == "printed":
            mains = PrintedData.query.all() # filter(PrintedData.uid==getuid.uid, PrintedData.status==1)
        elif data_type.lower() == "digital":
            mains = DigitalData.query.all() # filter(DigitalData.uid==getuid.uid, DigitalData.status==1)
        else:
            return make_response(jsonify(message="Unknown data types", status=False), 400)

        mains = [{"content_id": main.uuid, "title": main.title, "created_at": str(main.created_at)} for main in mains]
    except Exception as e:
        print(e)
        return make_response(jsonify(message="Internal Server Error", status=False), 500)    

    return make_response(jsonify(type=data_type, data=mains, status=True), 200)


''' View Detail '''
@bp.route('/su/contrib/view/detail', methods=['POST'])
@token_required
def admin_contrib_view_detail(current_user):
    data_type = request.args.get('type')
    getreq = request.get_json()
    
    try:
        if data_type.lower() == "printed":
            mains = PrintedData.query \
                .filter(PrintedData.uuid == getreq['content_id'])\
                .join(PrintedContent, PrintedContent.pid==PrintedData.pid)\
                .add_columns(PrintedData.title, PrintedData.created_at, PrintedContent.uuid, PrintedContent.file_path, PrintedContent.content_1, PrintedContent.content_2, PrintedContent.content_3)
                # .join(ExtractedContent, ExtractedContent.pcid==PrintedContent.pcid, isouter=True)\
                # .add_columns(PrintedData.title, PrintedData.created_at, PrintedContent.uuid, PrintedContent.file_path, ExtractedContent.content)
            
            # http://103.82.93.95:5000/uploaded/aabinomin/majalah_berurutan2_20230503_021531i832r_page1.doc
            # file_path = main.file_path.replace(current_app.root_path, current_app)
            mains = [{"content_id": main.uuid, "title": main.title, "created_at": str(main.created_at), "content_1": main.content_1, "content_2": main.content_2, "content_3": main.content_3, "file_path": os.path.join(request.host_url, main.file_path)} for main in mains]

        elif data_type.lower() == "digital":
            mains = DigitalData.query.filter(DigitalData.uuid==getreq['content_id'])
            mains = [{"content_id": main.uuid, "title": main.title, "created_at": str(main.created_at), "content": main.content, "url_path": main.url_path} for main in mains]

        else:
            return make_response(jsonify(message="Unknown data types", status=False), 400)
    except Exception as e:
        print(e)
        return make_response(jsonify(message="Internal Server Error", status=False), 500)
    
    return make_response(jsonify(type=data_type, data=mains, status=True), 200)