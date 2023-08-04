from apps.models import Users, Roles, Domiciles, SourceTypes, Languages
from apps import app, db
from config import config

with app.app_context():
    app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
    app.config['DB_RECREATE'] = config.DB_RECREATE
    db.init_app(app)
    db.create_all()
    
    r1 = Roles(role_name="admin")
    r2 = Roles(role_name="user")
    
    db.session.add_all([r1, r2])
    db.session.flush()
    
    e1 = Users(name='userbaja', email='userbaja@example.com', status="active", subscribed="yes", role_type=r2.rid)
    e1.set_password('123')
    e2 = Users(name='useranomali', email='useranomali@example.com', status="active", subscribed="yes", role_type=r1.rid)
    e2.set_password('123')
    
    db.session.add_all([e1, e2])

    import json
    with open('initial_data/source_types.json', 'r') as f:
        for sct in json.load(f):
            sc = SourceTypes(sc_name=sct["sc_name"], sc_type=sct["sc_type"])
            db.session.add(sc)

    with open('initial_data/language_list.txt', 'r') as f:
        for ll in f.readlines():
            ls = Languages(lang_name=ll.replace("\n", ""))
            db.session.add(ls)

    with open('initial_data/region_list.txt', 'r') as f:
        for rl in f.readlines():
            rs = Domiciles(dom_name=rl.replace("\n", ""))
            db.session.add(rs)

    db.session.commit()