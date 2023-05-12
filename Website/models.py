from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import JSON, Integer, String, LargeBinary


    
class User(db.Model,UserMixin):
    id=db.Column(Integer,primary_key=True)
    email=db.Column(String(150),unique=True)
    password=db.Column(String(150))
    first_name=db.Column(String(150))
    last_name=db.Column(String(150))

class File_relationship(db.Model):
    id=db.Column(Integer,primary_key=True)
    file_id=db.Column(Integer,db.ForeignKey('file.id'))
    user_id=db.Column(Integer,db.ForeignKey('user.id'))
    
    
class File(db.Model):
    id = db.Column(Integer, primary_key=True)
    filename = db.Column(String)
    data = db.Column(LargeBinary)



