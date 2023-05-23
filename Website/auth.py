from flask import Blueprint, render_template,request,flash,redirect, url_for
from werkzeug.security import generate_password_hash,check_password_hash
from .models import User
from . import db 
from . import views
from flask_login import login_user,login_required,logout_user,current_user

auth=Blueprint('auth',__name__)

@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        error = None
        email=request.form.get('email')
        print(email)
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()
        
        if user:
            if check_password_hash(user.password,password):
                # flash('Logged in successfully!',category='success')
                login_user(user,remember=True)
                return redirect(url_for('views.home'))
            else:
                error = 'Incorrect password, try again.'
                return render_template("login.html", error=error)
        else:
            error = 'Email does not exist.'
            return render_template("login.html", error=error)
        # elif 'sign up button' in request.form:
        #     print("executed")
        #     email = request.form.get('email')
        #     first_name = request.form.get('firstName')
        #     username = request.form.get('username')
        #     password1 = request.form.get('password1')
        #     password2 = request.form.get('password2')

        #     userByEmail = User.query.filter_by(email=email).first()
        #     userByUsername = User.query.filter_by(username=username).first()
        #     if userByEmail:
        #         flash('Email already exists.', category='error')
        #     elif userByUsername:
        #         flash('username already exists.', category='error')
        #     elif len(email) < 4:
        #         flash('Email must be greater than 3 characters.', category='error')
        #     elif len(first_name) < 2:
        #         flash('First name must be greater than 1 character.', category='error')
        #     elif password1 != password2:
        #         flash('Passwords don\'t match.', category='error')
        #     elif len(password1) < 7:
        #         flash('Password must be at least 7 characters.', category='error')
        #     else:
        #         new_user = User(email=email, first_name=first_name, 
        #                         username=username,
        #                         password=generate_password_hash(password1, method='sha256'))
        #         db.session.add(new_user)
        #         db.session.commit()
        #         login_user(new_user, remember=True)
        #         flash('Account created!', category='success')
                
        #         return redirect(url_for('views.home'))
   
        
        
    return render_template("login.html", user=current_user)
                
    
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        error = None
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        userByEmail = User.query.filter_by(email=email).first()
        if userByEmail:
            error = "Email already exists."
            return render_template("login.html", error=error)
        elif len(email) < 4:
            error = 'Email must be greater than 3 characters.'
            return render_template("login.html", error=error)
        elif len(first_name) < 2:
            error = 'First name must be greater than 1 character.'
            return render_template("login.html", error=error)
        elif password1 != password2:
            error = 'Passwords don\'t match.'
            return render_template("login.html", error=error)
        elif len(password1) < 7:
            error = 'Password must be at least 7 characters.'
            return render_template("login.html", error=error)
        else:
            new_user = User(email=email, first_name=first_name, 
                            password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            
            return redirect(url_for('views.home'))
    return render_template("login.html", user=current_user)
