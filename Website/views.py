from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_login import login_required, current_user
from .models import *
import json
import sqlite3 as sql


conn=sql.connect('database.db')
c=conn.cursor()

views=Blueprint('views',__name__)

@views.route('/',methods=['GET','POST'])
def home():
    return render_template("home.html",user=current_user)

# @views.route('/create_room',methods=['GET','POST'])
# @login_required
# def create_room():
#     if request.method=='POST':
#         room_name=request.form.get('room_name')
#         room_language=request.form.get('room_language')
#         new_room=Room(room_name=room_name,room_language=room_language)
#         db.session.add(new_room)
#         db.session.commit()
#         return redirect(url_for('views.view_session',room_id=new_room.id))
#     return render_template('create_session.html')

# @views.route('/invite_user',method=['GET','POST'])
# @login_required
# def invite_user(room_id):
#     if request.method=='POST':
#         email=request.form.get('email')
#         user=User.query.filter_by(email=email).first()
#         newInvite=InvitedUser(email=email,room_id=room_id)
#         db.session.add(newInvite)
#         db.session.commit()
    
        
@views.route("/session/<room_id>")
@login_required
def view_session(room_id):
    room=Room.query.filter_by(id=room_id).first()
    if not room:
        return "ROOM DOES NOT EXIST"
    return render_template('ide.html',user=current_user)
    # return render_template('code_editor.html')

@views.route("/projects",methods=['GET','POST'])
@login_required
def view_invitations():
    if request.method=='POST': #newroom
        room_name=request.form.get('room_name')
        RoomByName = Room.query.filter_by(room_name=room_name).first()
        if RoomByName:
            flash('Room Name already exists.', category='error')
        else:
            new_room=Room(room_name=room_name,owner_id=current_user.id)
            db.session.add(new_room)
            db.session.commit() 
    
    invited_rooms=InvitedUser.query.filter_by(email=current_user.email).all()
    rooms_dict={}

    created_rooms=Room.query.filter_by(owner_id=current_user.id).all()
    print(created_rooms)
    

    for rooms in invited_rooms:
        owner=User.query.filter_by(id=rooms.owner_id).first()
        rooms_dict[rooms.room_name]=[rooms.room_language,owner.first_name]
    #Project name #Room Langugae #Owner
    return render_template('projects.html',user=current_user,rooms_dict=rooms_dict,created_rooms=created_rooms) 

