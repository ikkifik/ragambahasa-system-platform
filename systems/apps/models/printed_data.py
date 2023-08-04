from apps.models import db
from datetime import datetime
from uuid import uuid4

class PrintedData(db.Model):
    pid = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('users.uid'))
    lid = db.Column(db.Integer, db.ForeignKey('languages.lid'))
    stid = db.Column(db.Integer, db.ForeignKey('source_types.stid'))

    uuid = db.Column(db.String(100), unique=True, default=uuid4)
    title = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(30))
    status = db.Column(db.Integer, default=1) # 1:active/0:inactive
    # is_moved = db.Column(db.Integer, default=0) #1:moved; 0:not moved
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP)
    
    
    printed_content = db.relationship("PrintedContent")

    def __repr__(self):
        return f'<Printed Data {self.uuid}>'
