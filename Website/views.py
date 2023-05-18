from flask import Blueprint, render_template, request, url_for, redirect
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

@views.route('/create_room',methods=['GET','POST'])
@login_required
def create_room():
    if request.method=='POST':
        room_name=request.form.get('room_name')
        room_language=request.form.get('room_language')
        new_room=Room(room_name=room_name,room_language=room_language)
        db.session.add(new_room)
        db.session.commit()
        return redirect(url_for('views.view_session',room_id=new_room.id))
    return render_template('create_session.html')

@views.route('/invite_user',method=['GET','POST'])
@login_required
def invite_user(room_id):
    if request.method=='POST':
        email=request.form.get('email')
        user=User.query.filter_by(email=email).first()
        newInvite=InvitedUser(email=email,room_id=room_id)
        db.session.add(newInvite)
        db.session.commit()
    
        
@views.route("/session/<room_id>")
@login_required
def view_session(room_id):
    room=Room.query.filter_by(id=room_id).first()
    if not room:
        return "ROOM DOES NOT EXIST"
    return render_template('code_editor.html')

@views.route("/projects",methods=['GET','POST'])
@login_required
def view_invitations():
    if request.method=='POST':
        links=InvitedUser.query.filter_by(email=current_user.email).all()
        room_id=request.form.get('room_id')
        return redirect(url_for('views.view_session',room_id=room_id))
    return render_template('projects.html',links=links)