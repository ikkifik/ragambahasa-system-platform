from uuid import uuid4
from apps.models import db
from datetime import datetime
from uuid import uuid4

class PrintedContent(db.Model):
    pcid = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.Integer, db.ForeignKey('printed_data.pid'))
    
    uuid = db.Column(db.String(100), unique=True, default=uuid4)
    page_num = db.Column(db.Integer)
    file_path = db.Column(db.String(200))
    moved_path = db.Column(db.String(200))
    
    content_1 = db.Column(db.Text)
    content_2 = db.Column(db.Text)
    content_3 = db.Column(db.Text)
    
    is_moved = db.Column(db.Integer, default=0) #1:moved; 0:not moved
    moved_date = db.Column(db.TIMESTAMP)

    def __repr__(self):
        return f'<Printed Content {self.uuid}>'
