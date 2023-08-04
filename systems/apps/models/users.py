from apps.models import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from uuid import uuid4
import enum

class GenderType(enum.Enum):
    male = "M"
    female = "F"

class StatusType(enum.Enum):
    block = 0
    active = 1
    inactive = 2

class Subscribe(enum.Enum):
    no = 0
    yes = 1

class Users(UserMixin, db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(100), unique=True, default=uuid4)
    
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200))
    domicile = db.Column(db.String(100))
    gender = db.Column(db.Enum(GenderType), default=GenderType.male)
    status = db.Column(db.Enum(StatusType), default=StatusType.inactive)
    subscribed = db.Column(db.Enum(Subscribe), default=Subscribe.no)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP)
    
    printed_data = db.relationship("PrintedData")
    digital_data = db.relationship("DigitalData")
    role_type = db.Column(db.Integer, db.ForeignKey('roles.rid'))
    # role_type = db.Column(db.Enum(RoleType))

    def __repr__(self):
        return f'<Users {self.name}>'
    
    def set_password(self, password):
        self.password = generate_password_hash(password=password, method="pbkdf2:sha256:1000")
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
