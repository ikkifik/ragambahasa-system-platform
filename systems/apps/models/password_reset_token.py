from apps.models import db
from datetime import datetime
from uuid import uuid4

class PasswordResetToken(db.Model):
    prtid = db.Column(db.Integer, primary_key=True)
    user_uuid = db.Column(db.String(40), unique=True)
    token = db.Column(db.String(100), unique=True)
    token_created = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    token_expiry = db.Column(db.TIMESTAMP)

    def __repr__(self):
        return f'<Token Created {datetime.utcnow()}>'
