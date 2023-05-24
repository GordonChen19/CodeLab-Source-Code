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
    return render_template("home.html")



@views.route("/projects",methods=['GET','POST'])
def view_invitations():
    if request.method=='POST': #newroom
        room_name=request.form.get('room_name')
        concept_name=request.form.get('concept_name')
        if len(room_name)==0:
            flash('Please input a name for the room',category='error')
        if len(concept_name)==0:
            flash('Please input a valid concept ',category='error')
        room_language=request.form.get('room_language')
        language_code={'python':default_python_code,'C':default_c_code,'Cpp':default_cpp_code}

        introduction=chatgpt("Explain"+str(concept_name)+"with the aid of code written in"+str(room_language)+". Begin with explanation")
        question=chatgpt("Give a coding question about" + str(concept_name) + ". Begin with Question:")
        return redirect(url_for(f'views.enter_room_{room_language}',
                                room_concept=concept_name,
                                room_language=room_language,
                                code=language_code[room_language],
                                introduction=introduction,
                                question=question,
                                prompt='IM HERE TO HELP'))

    return render_template('projects.html') 


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




@views.route("/session/python",methods=['POST','GET'])
def enter_room_python(): 
    room_concept = request.args.get('room_concept')
    room_language = request.args.get('room_language')
    code = request.args.get('code')
    introduction = request.args.get('introduction')
    question= request.args.get('question')
    prompt= request.args.get('prompt')
    resrun=''
    rescompil=''
    
    if(request.method=='POST'):
        code = request.form['code'] #preserves indentation
        index=code.find("Output")
        code=code[:index]
        
        
        if 'launch-button' in request.form:
            run = runcode.RunPyCode(code)
            rescompil, resrun = run.run_py_code()

            if resrun== '':
                resrun = 'No result!'
            code = code + 'Output: ' + '\n' + resrun  + '\n' + 'Compilation: ' + '\n' + rescompil

        
        elif 'Hint' in request.form:
            prompt=chatgpt("give a hint for solving the "+question+" .Begin with 'hint:'")
            return redirect(url_for('views.enter_room_python',
                                    room_concept=room_concept,
                                    room_language=room_language,
                                    code=code,
                                    introduction=introduction,
                                    question=question,
                                    prompt=prompt))
        elif 'Solution' in request.form:
           
            
            prompt=chatgpt("give the solution code written in" + room_language + "to the" + question + " Begin with Solution:")
            return redirect(url_for('views.enter_room_python',
                                    room_concept=room_concept,
                                    room_language=room_language,
                                    code=code,
                                    introduction=introduction,
                                    question=question,
                                    prompt=prompt))
        elif 'Review Code' in request.form:

            prompt=chatgpt( "Does" + code + "answer the question:" + question)
            return redirect(url_for('views.enter_room_python',room_concept=room_concept,room_language=room_language,
                                    code=code,introduction=introduction,
                                    question=question,
                                    prompt=prompt))
        
    
    return render_template('code_editor.html',
                           code=code,
                           target=url_for('views.enter_room_python',
                                          room_concept=room_concept,
                                          room_language=room_language,
                                          code=code,introduction=introduction,
                                          question=question,
                                          prompt=prompt),
                            resrun=resrun,
                            rescomp=rescompil,
                            rows=default_rows,
                            cols=default_cols,
                            room_name=room_concept,
                            introduction=introduction,
                            question=question,
                            prompt=prompt)
    
    
    
    
    
@views.route("/session/C",methods=['POST','GET'])
def enter_room_C(): 
    room_concept = request.args.get('room_concept')
    room_language = request.args.get('room_language')
    code = request.args.get('code')
    introduction = request.args.get('introduction')
    question= request.args.get('question')
    prompt= request.args.get('prompt')
    resrun=''
    rescompil=''
    
    if(request.method=='POST'):
        code = request.form['code'] #preserves indentation
        index=code.find("Output")
        code=code[:index]
        
        
        if 'launch-button' in request.form:
            run = runcode.RunCCode(code)
            rescompil, resrun = run.run_c_code()

            if resrun== '':
                resrun = 'No result!'
            code = code + 'Output: ' + '\n' + resrun  + '\n' + 'Compilation: ' + '\n' + rescompil

        
        elif 'Hint' in request.form:
            prompt=chatgpt("give a hint for solving the "+question+" .Begin with 'hint:'")
            return redirect(url_for('views.enter_room_C',
                                    room_concept=room_concept,
                                    room_language=room_language,
                                    code=code,
                                    introduction=introduction,
                                    question=question,
                                    prompt=prompt))
        elif 'Solution' in request.form:
           
            
            prompt=chatgpt("give the solution code written in" + room_language + "to the" + question + " Begin with Solution:")
            return redirect(url_for('views.enter_room_C',
                                    room_concept=room_concept,
                                    room_language=room_language,
                                    code=code,
                                    introduction=introduction,
                                    question=question,
                                    prompt=prompt))
        elif 'Review Code' in request.form:

            prompt=chatgpt( "Does" + code + "answer the question:" + question)
            return redirect(url_for('views.enter_room_C',room_concept=room_concept,room_language=room_language,
                                    code=code,introduction=introduction,
                                    question=question,
                                    prompt=prompt))
        
    
    return render_template('code_editor.html',
                           code=code,
                           target=url_for('views.enter_room_C',
                                          room_concept=room_concept,
                                          room_language=room_language,
                                          code=code,introduction=introduction,
                                          question=question,
                                          prompt=prompt),
                            resrun=resrun,
                            rescomp=rescompil,
                            rows=default_rows,
                            cols=default_cols,
                            room_name=room_concept,
                            introduction=introduction,
                            question=question,
                            prompt=prompt)
    
    
    
        
    
@views.route("/session/Cpp",methods=['POST','GET'])
def enter_room_Cpp(): 
    room_concept = request.args.get('room_concept')
    room_language = request.args.get('room_language')
    code = request.args.get('code')
    introduction = request.args.get('introduction')
    question= request.args.get('question')
    prompt= request.args.get('prompt')
    resrun=''
    rescompil=''
    
    if(request.method=='POST'):
        code = request.form['code'] #preserves indentation
        index=code.find("Output")
        code=code[:index]
        
        
        if 'launch-button' in request.form:
            run = runcode.RunCppCode(code)
            rescompil, resrun = run.run_cpp_code()

            if resrun== '':
                resrun = 'No result!'
            code = code + 'Output: ' + '\n' + resrun  + '\n' + 'Compilation: ' + '\n' + rescompil

        
        elif 'Hint' in request.form:
            prompt=chatgpt("give a hint for solving the "+question+" .Begin with 'hint:'")
            return redirect(url_for('views.enter_room_Cpp',
                                    room_concept=room_concept,
                                    room_language=room_language,
                                    code=code,
                                    introduction=introduction,
                                    question=question,
                                    prompt=prompt))
        elif 'Solution' in request.form:
           
            
            prompt=chatgpt("give the solution code written in" + room_language + "to the" + question + " Begin with Solution:")
            return redirect(url_for('views.enter_room_Cpp',
                                    room_concept=room_concept,
                                    room_language=room_language,
                                    code=code,
                                    introduction=introduction,
                                    question=question,
                                    prompt=prompt))
        elif 'Review Code' in request.form:

            prompt=chatgpt( "Does" + code + "answer the question:" + question)
            return redirect(url_for('views.enter_room_Cpp',room_concept=room_concept,room_language=room_language,
                                    code=code,introduction=introduction,
                                    question=question,
                                    prompt=prompt))
        
    
    return render_template('code_editor.html',
                           code=code,
                           target=url_for('views.enter_room_Cpp',
                                          room_concept=room_concept,
                                          room_language=room_language,
                                          code=code,introduction=introduction,
                                          question=question,
                                          prompt=prompt),
                            resrun=resrun,
                            rescomp=rescompil,
                            rows=default_rows,
                            cols=default_cols,
                            room_name=room_concept,
                            introduction=introduction,
                            question=question,
                            prompt=prompt)
    
    