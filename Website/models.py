from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


    
class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(150),unique=True)
    email=db.Column(db.String(150),unique=True)
    password=db.Column(db.String(150))
    first_name=db.Column(db.String(150))
    
    sid = db.Column(db.String(80), unique=True, nullable=True,default=None)
    is_admin = db.Column(db.Boolean, default=False)
    is_AFK = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    
    
class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invite_code = db.Column(db.String(120))
    room_name = db.Column(db.String(120), unique=True, nullable=False)
    room_language = db.Column(db.String(120), nullable=False, default="python")
    data=db.Column(db.LargeBinary)
    sid = db.Column(db.String(120),nullable=True,default=None)
    
    def room_members(self):
        return [self.owner,] + [User.query.filter_by(email=i.email_address).first() for i in self.invited_users]

class InvitedUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String(150),nullable=False)
    room_id=db.Column(db.Integer,db.ForeignKey('room.id'),nullable=False)