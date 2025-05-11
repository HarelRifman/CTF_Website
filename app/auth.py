from flask import Blueprint, redirect, url_for, session, render_template
import hashlib
import re
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from firebase_handler import FirebaseHandler

# Create blueprint
auth_bp = Blueprint('auth', __name__)

# Helper function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Password validation function
def validate_password(password):
    errors = []
    if len(password) < 8:
        errors.append("Password must be at least 8 characters long")
    if not re.search(r'[A-Z]', password):
        errors.append("Password must contain at least one uppercase letter")
    if not re.search(r'[a-z]', password):
        errors.append("Password must contain at least one lowercase letter")
    if not re.search(r'[0-9]', password):
        errors.append("Password must contain at least one number")

    if errors:
        return False, ", ".join(errors)
    return True, ""

# Custom validators
def password_strength_check(form, field):
    valid, message = validate_password(field.data)
    if not valid:
        raise ValidationError(message)

def username_length_check(form, field):
    if len(field.data) < 4:
        raise ValidationError("Username must be at least 4 characters long")

# Form classes
class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(message="Username is required"),
        username_length_check
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required"),
        password_strength_check
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message="Password confirmation is required"),
        EqualTo('password', message="Passwords do not match")
    ])

class SignInForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(message="Username is required")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required")
    ])

# Routes
@auth_bp.route('/')
def index():
    return redirect(url_for('auth.signin'))

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    error_messages = []
    success_message = None

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user_handler = FirebaseHandler("users")
        existing_user = user_handler.get_record(username)

        if existing_user:
            error_messages.append("Username already exists! Try a different one.")
        else:
            is_valid, error_message = validate_password(password)
            if not is_valid:
                error_messages.append(f"Password not strong enough: {error_message}")
            else:
                hashed_password = hash_password(password)
                user_details = {
                    "username": username,
                    "password": hashed_password,
                    "score": 0,
                    "solved_challenges": []
                }
                if user_handler.add_record(username, user_details):
                    success_message = "Sign Up Successful! You can now sign in."
                    session['signup_success'] = success_message
                    return redirect(url_for('auth.signin'))
                else:
                    error_messages.append("Error during signup, please try again.")

    for field, errors in form.errors.items():
        for error in errors:
            error_messages.append(f"{error}")

    return render_template(
        "auth/signup.html",
        form=form,
        error_messages=error_messages,
        success_message=success_message
    )

@auth_bp.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SignInForm()
    error_messages = []
    success_message = None

    if 'signup_success' in session:
        success_message = session.pop('signup_success')

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user_handler = FirebaseHandler("users")
        existing_user = user_handler.get_record(username)

        if not existing_user:
            error_messages.append("Username not found. Please sign up first.")
        elif existing_user.get("password") != hash_password(password):
            error_messages.append("Incorrect password. Please try again.")
        else:
            session['username'] = username
            return render_template(
                "main/dashboard.html",
                username=username,
                success_message="Sign In Successful!"
            )

    for field, errors in form.errors.items():
        for error in errors:
            error_messages.append(f"{error}")

    return render_template(
        "auth/signin.html",
        form=form,
        error_messages=error_messages,
        success_message=success_message
    )

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.signin'))