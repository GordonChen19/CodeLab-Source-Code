from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_login import login_required, current_user
from .models import *
import json
import sqlite3 as sql
from . import runcode


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




'''
code editor navigation
'''


default_c_code = """#include <stdio.h>

int main(int argc, char **argv)
{
    printf("Hello C World!!\\n");
    return 0;
}    
"""

default_cpp_code = """#include <iostream>

using namespace std;

int main(int argc, char **argv)
{
    cout << "Hello C++ World" << endl;
    return 0;
}
"""

default_python_code = """import sys
import os

if __name__ == "__main__":
    print "Hello Python World!!"
"""

default_rows = "15"
default_cols = "60"

@views.route("/session/<room_id>/python",methods=['POST','GET'])
@login_required
def enter_room_python(room_id): 
    if(request.method=='POST'):
        code = request.form['code']
        run = runcode.RunPyCode(code)
        rescompil, resrun = run.run_py_code()
        if not resrun:
            resrun = 'No result!'
    else:
        code = default_python_code
        resrun = 'No result!'
        rescompil = 'No Compilation for Python'
    
    return render_template('code_editor.html',
                           user=current_user,
                           code=code,
                           target=url_for('views.enter_room_python',room_id=room_id),
                           resrun=resrun,
                           rescomp=rescompil,
                           rows=default_rows,
                           cols=default_cols,
                           room_id=room_id,
                            h_reference=f'/session/{room_id}/python')

@views.route("/session/<room_id>/C",methods=['POST','GET'])
@login_required
def enter_room_C(room_id): 
    if(request.method=='POST'):
        code = request.form['code']
        run = runcode.RunCCode(code)
        rescompil, resrun = run.run_c_code()
        if not resrun:
            resrun = 'No result!'
    else:
        code = default_c_code
        resrun = 'No result!'
        rescompil = ''
        
    return render_template('code_editor.html',
                           user=current_user,
                           code=code,
                           target=url_for('views.enter_room_C',room_id=room_id),
                           resrun=resrun,
                           rescomp=rescompil,
                           rows=default_rows,
                           cols=default_cols,
                           room_id=room_id,
                            h_reference=f'/session/{room_id}/C')

@views.route("/session/<room_id>/Cpp",methods=['POST','GET'])
@login_required
def enter_room_Cpp(room_id): 
    if(request.method=='POST'):
        code = request.form['code']
        run = runcode.RunCppCode(code)
        rescompil, resrun = run.run_cpp_code()
        if not resrun:
            resrun = 'No result!'
    else:
        code = default_cpp_code
        resrun = 'No result!'
        rescompil = ''
        
    return render_template('code_editor.html',
                           user=current_user,
                           code=code,
                           target=url_for('views.enter_room_Cpp',room_id=room_id),
                           resrun=resrun,
                           rescomp=rescompil,
                           rows=default_rows,
                           cols=default_cols,
                           room_id=room_id,
                           h_reference=f'/session/{room_id}/Cpp'
                           )
                    