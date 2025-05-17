from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import length, EqualTo, DataRequired, ValidationError, Email
from .models import User
from flask_login import login_user, logout_user, login_required
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/sign_in_user', methods=['POST', 'GET'])
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
            login_user(new_user)
            flash('User created successfully!', category='success')
            return redirect(url_for('views.add_product'))
        except Exception as e:
            db.session.rollback()
            flash(f'Failed to create user! error :{e}', category='error')
            return render_template('signup.html', form=form)
        
    if form.errors:
        for err_msg in form.errors.values():
            flash(f'Error in Form : {err_msg}', category='error')
            
    return render_template("signup.html", form=form)
        
@auth.route('/login_user', methods=['POST', 'GET'])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        attempted_user = User.query.filter_by(email=form.email.data).first()
        if attempted_user and attempted_user.check_password_correction(
            attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.email}', category='success')
            return redirect(url_for('views.add_product'))
        else:
            flash('Username and password are not match! Please try again', category='error')
            return render_template("login.html")

    return render_template("login.html", form=form)


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
