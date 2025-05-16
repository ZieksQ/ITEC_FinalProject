from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint('auth', __name__)

@auth.route('/sign_up_user', methods=['POST', 'GET'])
def sign_in():

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')

        try:
            with db.session.no_autoflush:
                new_user = User(email=email, first_name=first_name, last_name=last_name, username=username, 
                                password=generate_password_hash(password1, method='pbkdf2:sha256'))
                db.session.add(new_user)
                db.session.commit()
            flash('User created successfully!', category='success')
            return redirect(url_for('views.home'))
        except Exception as e:
            db.session.rollback()
            flash(f'Failed to create user! error:{e}', category='error')
            return render_template('signup.html')
            
    return render_template("signup.html")
        
@auth.route('/login_user', methods=['POST', 'GET'])
def login():

    return render_template("login.html")