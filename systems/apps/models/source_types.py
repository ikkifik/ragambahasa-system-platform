from apps.models import db
from uuid import uuid4

class SourceTypes(db.Model):
    stid = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(100), unique=True, default=uuid4)
    sc_name = db.Column(db.String(50))
    sc_type = db.Column(db.String(50))

    printed_data = db.relationship("PrintedData")
    digital_data = db.relationship("DigitalData")

    def __repr__(self):
        return f'<Source_Types {self.sc_name}>'
