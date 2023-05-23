from flask import Blueprint, render_template, request, url_for, redirect, jsonify, flash
from flask_login import login_required, current_user
from .models import *
import json
import sqlite3 as sql
from . import runcode
from .chatgpt import chatgpt
conn=sql.connect('database.db')
c=conn.cursor()

views=Blueprint('views',__name__)


'''
routing
'''

@views.route('/',methods=['GET','POST'])
def home():
    return render_template("home.html",user=current_user)



@views.route("/projects",methods=['GET','POST'])
@login_required
def view_invitations():
    if request.method=='POST': #newroom
        room_name=request.form.get('room_name')
        concept_name=request.form.get('concept_name')
        if len(room_name)==0:
            flash('Please input a name for the room',category='error')
        if len(concept_name)==0:
            flash('Please input a valid concept ',category='error')
        room_language=request.form.get('room_language')
        
        RoomByName = Room.query.filter_by(room_name=room_name,owner_id=current_user.id).first()
        
        language_code={'python':default_python_code,'C':default_c_code,'Cpp':default_cpp_code}
        if RoomByName:
            flash('Room Name already exists.', category='error')
        else:
            introduction=chatgpt("Explain"+str(concept_name)+"with the aid of code written in"+str(room_language)+". Begin with explanation")
            question=chatgpt("Ask a question about" + str(concept_name) + "that requires me to write code. Begin with Question")
            new_room=Room(room_name=room_name,
                          owner_id=current_user.id,
                          room_language=room_language,
                          room_concept=concept_name,
                          data=language_code[room_language],
                          introduction=introduction,
                          question=question)
            
            db.session.add(new_room)
            db.session.commit() 

    room=Room.query.filter_by(owner_id=current_user.id).all()
    
    #Project name #Room Langugae 
    return render_template('projects.html',user=current_user,room=room) 

@views.route('/projects', methods=['DELETE'])
@login_required
def deleteRoom():
    room = json.loads(request.data)
    roomId = room['roomId']
    room = Room.query.get(roomId)
    if room:
        if room.owner_id == current_user.id:
            db.session.delete(room)
            db.session.commit()  
    return jsonify({})


'''
code editor navigation
'''


default_c_code = """
#include <stdio.h>

int main(int argc, char **argv)
{
    printf("Hello C World!!\\n");
    return 0;
}

    
"""

default_cpp_code = """
#include <iostream>

using namespace std;

int main(int argc, char **argv)
{
    cout << "Hello C++ World" << endl;
    return 0;
}


"""

default_python_code = """
import sys
import os

if __name__ == "__main__":
    print ("Hello Python World!!")
    
    
"""

default_rows = "15"
default_cols = "60"




@views.route("/session/<room_id>/python",methods=['POST','GET'])
@login_required
def enter_room_python(room_id): 
    
    if(request.method=='POST'):
        code = request.form['code'] #preserves indentation
        index=code.find("Output")
        code=code[:index]
        print(code)
        
        if 'launch-button' in request.form:
            run = runcode.RunPyCode(code)
            rescompil, resrun = run.run_py_code()
            if resrun== '':
                resrun = 'No result!'
            code = code + 'Output: ' + '\n' + resrun  + '\n' + 'Compilation: ' + '\n' + rescompil

            
        elif 'save-button' in request.form:
            print("executed")
            room=Room.query.filter_by(id=room_id).first()
            room.data=code
            db.session.commit()
            return redirect(url_for('views.view_invitations'))
        
        elif 'Hint' in request.form:
            print("hint detected")
            room=Room.query.filter_by(id=room_id).first()
            room.hint=chatgpt("give a hint for solving the "+room.question+" .Begin with 'hint:'")
            room.last_pressed='hint'
            print("printing hint")
            print(room.hint)
            room.data=code
            db.session.commit()
            return redirect(url_for('views.enter_room_python',room_id=room_id))
        elif 'Solution' in request.form:
            print("solution detected")
            print("hello")
            room=Room.query.filter_by(id=room_id).first()
            room.solution=chatgpt("give the solution code written in" + room.room_language + "to the" + room.question + " Begin with code:")
            room.last_pressed='solution'
            room.data=code
            print("printing solution")
            print(room.solution)
            db.session.commit()
            return redirect(url_for('views.enter_room_python',room_id=room_id))
        elif 'Review Code' in request.form:
            print("review code detected")
            room=Room.query.filter_by(id=room_id).first()
            room.code_review=chatgpt("Given the question" + room.question + "Give suggestions to how to improve the follow code to answer the question." + code)
            room.last_pressed='code_review'
            print("code_review")
            print(room.code_review)
            room.data=code
            db.session.commit()
            return redirect(url_for('views.enter_room_python',room_id=room_id))
        
    else:
        room=Room.query.filter_by(id=room_id).first()
        code = room.data
        print(room.data)
        print("printing room data")
        run = runcode.RunPyCode(code)
        rescompil, resrun = run.run_py_code()

    room=Room.query.filter_by(id=room_id).first()
    room_name=room.room_concept
    introduction=room.introduction
    question=room.question
    
    prompt=getattr(room,room.last_pressed)
    
    
    return render_template('code_editor.html',
                           user=current_user,
                           code=code,
                           target=url_for('views.enter_room_python',room_id=room_id),
                           resrun=resrun,
                           rescomp=rescompil,
                           rows=default_rows,
                           cols=default_cols,
                           room_id=room_id,
                           introduction=introduction,
                           question=question,
                           room_name=room_name,
                           prompt=prompt,
                           h_reference=f'/session/{room_id}/python')

@views.route("/session/<room_id>/C",methods=['POST','GET'])
@login_required
def enter_room_C(room_id): 
    if(request.method=='POST'):
        code = request.form['code'] #preserves indentation
        index=code.find("Output")
        code=code[:index]
        
        if 'launch-button' in request.form:
            run = runcode.RunCCode(code)
            rescompil, resrun = run.run_c_code()
            if not resrun:
                resrun = 'No result!'
            code = code + 'Output: ' + '\n' + resrun  + '\n' + 'Compilation: ' + '\n' + rescompil
            
        elif 'save-button' in request.form:
            print("executed")
            room=Room.query.filter_by(id=room_id).first()
            room.data=code
            db.session.commit()
            return redirect(url_for('views.view_invitations'))
        
        elif 'Hint' in request.form:
            print("hint detected")
            room=Room.query.filter_by(id=room_id).first()
            room.hint=chatgpt("give a hint for solving the "+room.question+" .Begin with 'hint:'")
            room.last_pressed='hint'
            print("printing hint")
            print(room.hint)
            room.data=code
            db.session.commit()
            return redirect(url_for('views.enter_room_C',room_id=room_id))
        elif 'Solution' in request.form:
            print("solution detected")
            print("hello")
            room=Room.query.filter_by(id=room_id).first()
            room.solution=chatgpt("give the solution code written in" + room.room_language + "to the" + room.question + " Begin with code:")
            room.last_pressed='solution'
            print("printing solution")
            print(room.solution)
            room.data=code
            db.session.commit()
            return redirect(url_for('views.enter_room_C',room_id=room_id))
        elif 'Review Code' in request.form:
            print("review code detected")
            room=Room.query.filter_by(id=room_id).first()
            room.code_review=chatgpt("Given the question" + room.question + "Give suggestions to how to improve the follow code to answer the question." + code)
            room.last_pressed='code_review'
            print("code_review")
            print(room.code_review)
            room.data=code
            db.session.commit()
            return redirect(url_for('views.enter_room_C',room_id=room_id))
    else:
        room=Room.query.filter_by(id=room_id).first()
        code = room.data
        run = runcode.RunCCode(code)
        rescompil, resrun = run.run_c_code()
    
    room=Room.query.filter_by(id=room_id).first()
    room_name=room.room_concept
    introduction=room.introduction
    question=room.question
    
    prompt=getattr(room,room.last_pressed)
    
    return render_template('code_editor.html',
                           user=current_user,
                           code=code,
                           target=url_for('views.enter_room_C',room_id=room_id),
                           resrun=resrun,
                           rescomp=rescompil,
                           rows=default_rows,
                           cols=default_cols,
                           room_id=room_id,
                           introduction=introduction,
                           question=question,
                           room_name=room_name,
                           prompt=prompt,
                           h_reference=f'/session/{room_id}/C')

@views.route("/session/<room_id>/Cpp",methods=['POST','GET'])
@login_required
def enter_room_Cpp(room_id): 
    if(request.method=='POST'):
        code = request.form['code'] #preserves indentation
        index=code.find("Output")
        code=code[:index]
        
        if 'launch-button' in request.form:
            run = runcode.RunCppCode(code)
            rescompil, resrun = run.run_cpp_code()
            if not resrun:
                resrun = 'No result!'
            code = code + 'Output: ' + '\n' + resrun  + '\n' + 'Compilation: ' + '\n' + rescompil
        
        elif 'save-button' in request.form:
            print("executed")
            room=Room.query.filter_by(id=room_id).first()
            room.data=code
            db.session.commit()
            return redirect(url_for('views.view_invitations'))
        
        elif 'Hint' in request.form:
            print("hint detected")
            room=Room.query.filter_by(id=room_id).first()
            room.hint=chatgpt("give a hint for solving the "+room.question+" .Begin with 'hint:'")
            room.last_pressed='hint'
            print("printing hint")
            print(room.hint)
            room.data=code
            db.session.commit()
            return redirect(url_for('views.enter_room_Cpp',room_id=room_id))
        elif 'Solution' in request.form:
            print("solution detected")
            print("hello")
            room=Room.query.filter_by(id=room_id).first()
            room.solution=chatgpt("give the solution code written in" + room.room_language + "to the" + room.question + " Begin with code:")
            room.last_pressed='solution'
            print("printing solution")
            print(room.solution)
            room.data=code
            db.session.commit()
            return redirect(url_for('views.enter_room_Cpp',room_id=room_id))
        elif 'Review Code' in request.form:
            print("review code detected")
            room=Room.query.filter_by(id=room_id).first()
            room.code_review=chatgpt("Given the question" + room.question + "Give suggestions to how to improve the follow code to answer the question." + code)
            room.last_pressed='code_review'
            print("code_review")
            print(room.code_review)
            room.data=code
            db.session.commit()
            return redirect(url_for('views.enter_room_Cpp',room_id=room_id))
    
    else:
        room=Room.query.filter_by(id=room_id).first()
        code = room.data
        run = runcode.RunCppCode(code)
        rescompil, resrun = run.run_cpp_code()

    room=Room.query.filter_by(id=room_id).first()
    room_name=room.room_concept
    introduction=room.introduction
    question=room.question
    
    prompt=getattr(room,room.last_pressed)
    
    return render_template('code_editor.html',
                           user=current_user,
                           code=code,
                           target=url_for('views.enter_room_Cpp',room_id=room_id),
                           resrun=resrun,
                           rescomp=rescompil,
                           rows=default_rows,
                           cols=default_cols,
                           room_id=room_id,
                           room_name=room_name,
                           introduction=introduction,
                           question=question,
                           prompt=prompt,
                           h_reference=f'/session/{room_id}/Cpp'
                           )
    

