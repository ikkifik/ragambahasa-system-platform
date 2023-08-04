from flask import request, jsonify, make_response
from apps.apis import bp
from apps.auth import token_required
from apps.helper import Mail
from apps.models import db, Users

# # # # # # # # # # # # # # # # # # #
#         Newsletter (Admin)        #
# # # # # # # # # # # # # # # # # # #

@bp.route('/newsletter', methods=['POST'])
@token_required
def newsletter(current_user):
    
    if current_user.role_type != 1:
        return make_response(jsonify(message="Unauthorize User", status=False), 401)

    # Example request body
    # {
    #     "title": "title",
    #     "content": "content",
    #     "thumbnail": "thumbnail",
    #     "source_url": "source_url",
    #     "recipients": ["example1@gmail.com", "example2@gmail.com"]
    # }

    getreq = request.get_json()
    recptype = request.args.get('type') # single/multi
    
    subscribed_mails = db.session.execute(db.select(Users).filter_by(subscribed="yes", role_type=2)).scalars()
    subscribed_mails = [subsm.email for subsm in subscribed_mails.all()]
    
    if recptype.lower() == "single":
        recipients = getreq['recipients']
    elif recptype.lower() == "multi":
        recipients = subscribed_mails
    else:
        return make_response(jsonify(message="Bad Request", status=False), 400)
    
    try:
        mail = Mail()
        mail.newsletter_mail(
            recepient_mails=recipients,
            title=getreq['title'],
            content=getreq['content'],
            source_url=getreq['source_url'],
            image_thumbnail=getreq['thumbnail'],
        )
    except:
        return make_response(jsonify(message="Failed send newsletter", status=False), 500)
    
    return make_response(jsonify(message="Newsletter has been sent successfully", status=True), 200)