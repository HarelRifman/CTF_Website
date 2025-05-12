from flask import Blueprint, redirect, url_for, session, render_template, request, jsonify
import hashlib
import re
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from firebase_handler import FirebaseHandler

# ────────────────────────────────────────────────────────────────
# Blueprint Setup
# ────────────────────────────────────────────────────────────────
auth_bp = Blueprint('auth', __name__)


# ────────────────────────────────────────────────────────────────
# Helper Functions
# ────────────────────────────────────────────────────────────────

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


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
    return (False, ", ".join(errors)) if errors else (True, "")


# ────────────────────────────────────────────────────────────────
# Custom WTForms Validators
# ────────────────────────────────────────────────────────────────

def password_strength_check(form, field):
    valid, message = validate_password(field.data)
    if not valid:
        raise ValidationError(message)


def username_length_check(form, field):
    if len(field.data) < 4:
        raise ValidationError("Username must be at least 4 characters long")


# ────────────────────────────────────────────────────────────────
# Form Definitions
# ────────────────────────────────────────────────────────────────

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
    username = StringField('Username', validators=[DataRequired(message="Username is required")])
    password = PasswordField('Password', validators=[DataRequired(message="Password is required")])


# ────────────────────────────────────────────────────────────────
# Routes
# ────────────────────────────────────────────────────────────────

@auth_bp.route('/')
def index():
    return redirect(url_for('auth.signin'))


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    # Check if it's a JSON request (for AJAX submission)
    if request.is_json:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        # Validate input
        if not username or not password or not confirm_password:
            return jsonify({
                'success': False,
                'message': 'All fields are required'
            }), 400

        # Validate username length
        if len(username) < 4:
            return jsonify({
                'success': False,
                'message': 'Username must be at least 4 characters long'
            }), 400

        # Validate password strength
        is_valid, error_message = validate_password(password)
        if not is_valid:
            return jsonify({
                'success': False,
                'message': error_message
            }), 400

        # Check password confirmation
        if password != confirm_password:
            return jsonify({
                'success': False,
                'message': 'Passwords do not match'
            }), 400

        # Check if username already exists
        user_handler = FirebaseHandler("users")
        if user_handler.get_record(username):
            return jsonify({
                'success': False,
                'message': 'Username already exists! Try a different one.'
            }), 400

        # Create user
        user_details = {
            "username": username,
            "password": hash_password(password),
            "score": 0,
            "solved_challenges": []
        }

        # Add user to database
        if user_handler.add_record(username, user_details):
            session['signup_success'] = "Sign Up Successful! You can now sign in."
            return jsonify({
                'success': True,
                'message': 'Sign Up Successful! You can now sign in.',
                'redirect': url_for('auth.signin')
            }), 201
        else:
            return jsonify({
                'success': False,
                'message': 'Error during signup. Please try again later.'
            }), 500

    # Handle traditional form submission
    form = SignUpForm()
    error_messages = []
    success_message = None

    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user_handler = FirebaseHandler("users")

        if user_handler.get_record(username):
            error_messages.append("Username already exists! Try a different one.")
        else:
            is_valid, error_message = validate_password(password)
            if not is_valid:
                error_messages.append(f"Password not strong enough: {error_message}")
            else:
                user_details = {
                    "username": username,
                    "password": hash_password(password),
                    "score": 0,
                    "solved_challenges": []
                }
                if user_handler.add_record(username, user_details):
                    session['signup_success'] = "Sign Up Successful! You can now sign in."
                    return redirect(url_for('auth.signin'))
                else:
                    error_messages.append("Error during signup. Please try again later.")

    # Collect form validation errors
    for field_errors in form.errors.values():
        error_messages.extend(field_errors)

    return render_template(
        "auth/signup.html",
        form=form,
        error_messages=error_messages,
        success_message=success_message
    )


@auth_bp.route('/signin', methods=['GET', 'POST'])
def signin():
    # Check if it's a JSON request (for AJAX submission)
    if request.is_json:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        # Validate input
        if not username or not password:
            return jsonify({
                'success': False,
                'message': 'Username and password are required'
            }), 400

        user_handler = FirebaseHandler("users")
        user = user_handler.get_record(username)

        if not user:
            return jsonify({
                'success': False,
                'message': 'Username not found. Please sign up first.'
            }), 404

        if user.get("password") != hash_password(password):
            return jsonify({
                'success': False,
                'message': 'Incorrect password. Please try again.'
            }), 401

        # Successful login
        session['username'] = username
        return jsonify({
            'success': True,
            'message': 'Sign In Successful!',
            'redirect': '/dashboard'  # Direct URL instead of url_for
        }), 200

    # Handle traditional form submission
    form = SignInForm()
    error_messages = []
    success_message = session.pop('signup_success', None)

    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user_handler = FirebaseHandler("users")
        user = user_handler.get_record(username)

        if not user:
            error_messages.append("Username not found. Please sign up first.")
        elif user.get("password") != hash_password(password):
            error_messages.append("Incorrect password. Please try again.")
        else:
            session['username'] = username
            # Use render_template for dashboard as in the original code
            return render_template(
                "main/dashboard.html",
                username=username,
                success_message="Sign In Successful!"
            )

    # Collect form validation errors
    for field_errors in form.errors.values():
        error_messages.extend(field_errors)

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
