from apps.models import db
from uuid import uuid4

class Domiciles(db.Model):
    domid = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(100), unique=True, default=uuid4)
    dom_name = db.Column(db.String(100))
    dom_code = db.Column(db.String(10))

    def __repr__(self):
        return f'<Domiciles {self.dom_name}>'
