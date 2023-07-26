from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from website import db, cache
from .models import User

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
@cache.cached(timeout=60)  # Cache the result for 60 seconds
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.', category='error')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    return redirect(url_for('views.dashboard'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
@cache.cached(timeout=60)  # Cache the result for 60 seconds
def signup_post():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()
    if user:
        flash('Username already exists',category='error')
        return redirect(url_for('auth.signup'))
    
    email_exists = User.query.filter_by(email=email).first()
    if email_exists:
        flash("This email is already registered.", category='error')
        return redirect(url_for('auth.signup'))
    

    if len(email) == 0:
        flash('Email cannot be empty', category='error')
    elif len(password) < 7:
        flash('Password must be greater than 7 characters.', category='error')
    elif len(username) == 0:
        flash('Username cannot be empty', category='error')
    elif len(username) <= 3:
        flash("Username cannot be lesser than 3 characters", category='error')
    else:
        new_user = User(username=username, email=email, password=generate_password_hash(password, method='sha256'))

        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('signup.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
