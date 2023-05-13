from flask import Blueprint, render_template, request, url_for, redirect
from flask_login import login_required, current_user
from .models import *
import json
import sqlite3 as sql

import subprocess

conn=sql.connect('database.db')
c=conn.cursor()

views=Blueprint('views',__name__)

@views.route('/',methods=['GET','POST'])
def home():
    return render_template("home.html",user=current_user)

@views.route('/all_projects', methods=['GET', 'POST'])
def project():
    code = request.form.get('code')
    if code:
        result = subprocess.run(code, stdout=subprocess.PIPE, shell=True)
        output = result.stdout.decode('utf-8')
        print(output)
    else:
        output = ''
    return render_template("ide.html", user=current_user)
