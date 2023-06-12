from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from website import db
from .models import User

auth = Blueprint('auth', __name__)

login_manager = LoginManager(app)


@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    return redirect(url_for('dashboard.html'))



@auth.route('/signup')
def signup():
    return render_template('signup.html')



@auth.route('/signup', methods=['POST'])
def signup_post():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
       
        
        

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email address already exists')
            return redirect(url_for('auth.signup'))
        # password_hash = generate_password_hash(password)
        elif len(password) < 7:
            flash('Password must be greater than 7 character.', category='error')
        else:
            new_user = User(username = username, email=email, password=generate_password_hash(password, method='sha256'))

            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        return render_template('signup.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
