from apps.models import db
from datetime import datetime
from uuid import uuid4

class ExtractedContent(db.Model):
    ecid = db.Column(db.Integer, primary_key=True)
    pcid = db.Column(db.Integer, db.ForeignKey('printed_content.pcid'))
    # did = db.Column(db.Integer, db.ForeignKey('digital_data.did'))
    
    uuid = db.Column(db.String(100), unique=True, default=uuid4)
    
    content = db.Column(db.String(100), nullable=False)
    types = db.Column(db.String(50), nullable=False)

    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)

    def __repr__(self):
        return f'<Extracted Content {self.uuid}>'
