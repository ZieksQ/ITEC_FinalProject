from flask import Blueprint, render_template, request, flash, redirect, url_for, flash, get_flashed_messages, current_app
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import length, EqualTo, DataRequired, ValidationError, Email
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from PIL import Image
from . import db
import secrets
import os

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
            password=form.password1.data,
            display_password=form.password1.data
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
            flash('Username and password does not match! Please try again', category='error')
            return render_template("login.html", form=form)

    return render_template("login.html", form=form)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics/', picture_fn)

    output_size = (700, 700)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@auth.route('/profile', methods=['POST', 'GET'])
@login_required
def the_profile():

    form = UpdateForm()
    form_picture = ProfilePictureForm()

    if form_picture.validate_on_submit():
        if form_picture.picture.data:
            picture_file = save_picture(form_picture.picture.data)
            current_user.image_file = picture_file
            try:
                db.session.commit()
                flash("You have succesfully updated your profile picture", category='success')
                return redirect(url_for('auth.the_profile'))
            except Exception as e:
                db.session.rollback()
                flash(f"You have failed to update your profile picture \nERROR : {e}")
                return redirect(url_for('auth.the_profile'))

    if form.validate_on_submit():

        current_user.email = form.email.data
        current_user.username = form.username.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data

        try:
            db.session.commit()
            flash("You have succesfully updated your account", category='success')
            return redirect(url_for('auth.the_profile'))
        except Exception as e:
            db.session.rollback()
            flash(f"You have failed to update your profile \nERROR : {e}")
            return redirect(url_for('auth.the_profile'))
        
    elif request.method == "GET":
        form.email.data = current_user.email
        form.username.data = current_user.username
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)

    return render_template("profile.html", user=current_user, image_file=image_file, form=form, form_picture=form_picture)


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

class UpdateForm(FlaskForm):

    def validate_username(self, username_check):
        if username_check.data != current_user.username:
            user = User.query.filter_by(username=username_check.data).first()
            if user:
                flash('Username already exist')
                raise ValidationError('Username already exists!')
        
    def validate_email(self, email_check):
        if email_check.data != current_user.email:
            user = User.query.filter_by(email=email_check.data).first()
            if user:
                flash('Email already exist')
                raise ValidationError('Email already exists!')

    username = StringField(label='Update Username : ', validators=[DataRequired(), length(min=2, max=20)])
    email = StringField(label='Update Email : ', validators=[DataRequired(), Email()])
    first_name = StringField(label='Update First Name : ', validators=[DataRequired(), length(min=2, max=30)])
    last_name = StringField(label='Update Last Name : ', validators=[DataRequired(), length(min=2, max=30)])
    submit = SubmitField(label='Update Account')

class ProfilePictureForm(FlaskForm):
    picture = FileField(label="Update Profile Picture", validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField(label='Upload Picture')