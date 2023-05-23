from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(150),unique=True)
    password=db.Column(db.String(150))
    first_name=db.Column(db.String(150))

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_name = db.Column(db.String(120), nullable=False)
    room_language = db.Column(db.String(120), nullable=False)
    data=db.Column(db.String)
    owner_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    room_concept=db.Column(db.String(50),nullable=False)
    introduction=db.Column(db.String(5000))
    question=db.Column(db.String(5000))
    hint=db.Column(db.String(5000),default='')
    solution=db.Column(db.String(5000),default='')
    code_review=db.Column(db.String(5000),default='')
    last_pressed=db.Column(db.String(15),default='hint')
    
    