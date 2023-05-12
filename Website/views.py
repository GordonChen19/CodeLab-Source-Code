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