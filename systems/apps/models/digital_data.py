from apps.models import db
from datetime import datetime
from uuid import uuid4

class DigitalData(db.Model):
    did = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('users.uid'))
    lid = db.Column(db.Integer, db.ForeignKey('languages.lid'))
    stid = db.Column(db.Integer, db.ForeignKey('source_types.stid'))
    
    uuid = db.Column(db.String(100), unique=True, default=uuid4)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text)
    url_path = db.Column(db.String(200))
    status = db.Column(db.Integer, default=1) # 1:active/0:inactive
    is_moved = db.Column(db.Integer, default=0) #1:moved; 0:not moved
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP)
    
    # extracted_content = db.relationship("ExtractedContent")
    
    def __repr__(self):
        return f'<Digital Data {self.uuid}>'
