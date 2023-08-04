from apps.models import db
from uuid import uuid4

class Languages(db.Model):
    lid = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(100), unique=True, default=uuid4)
    lang_name = db.Column(db.String(100))
    lang_code = db.Column(db.String(10))

    def __repr__(self):
        return f'<Languages {self.lang_name}>'
