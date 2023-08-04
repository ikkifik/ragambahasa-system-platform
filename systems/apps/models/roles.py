from apps.models import db
import enum

class RoleType(enum.Enum):
    admin = 0
    user = 1

class Roles(db.Model):
    rid = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.Enum(RoleType))
    
    user = db.relationship("Users")

    def __repr__(self):
        return f'<Roles {self.role_name}>'
