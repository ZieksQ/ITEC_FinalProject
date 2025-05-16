from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import length, EqualTo, DataRequired, ValidationError, Email
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/sign_up_user', methods=['POST', 'GET'])
def sign_in():

    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            password=form.password1.data
        )
        try:
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

class RegistrationForm(FlaskForm):

    def validate_username(self, username_check):
        user = User.query.filter_by(username=username_check.data).first()
        if user:
            raise ValidationError('Username already exists!')
        
    def validate_email(self, email_check):
        user = User.query.filter_by(email=email_check.data).first()
        if user:
            raise ValidationError('Email already exists!')

    username = StringField(label='Username : ', validators=[DataRequired(), length(min=2, max=20)])
    email = StringField(label='Email : ', validators=[DataRequired(), Email()])
    first_name = StringField(label='First Name : ', validators=[DataRequired(), length(min=2, max=30)])
    last_name = StringField(label='Last Name : ', validators=[DataRequired(), length(min=2, max=30)])
    password1 = PasswordField(label='Password : ', validators=[DataRequired(), length(min=7)])
    password2 = PasswordField(label='Confirm Password : ', validators=[DataRequired(), EqualTo('password1')])
    submit = SubmitField(label='Create Account')

class LoginForm(FlaskForm):
    email = StringField(label='Email : ', validators=[DataRequired()])
    password = PasswordField(label='Password : ', validators=[DataRequired()])
    submit = SubmitField(label='Login')

"""
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
"""