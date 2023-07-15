from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_alembic import Alembic
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_qrcode import QRcode


db = SQLAlchemy()
alembic = Alembic()
migrate = Migrate()
DB_NAME = "database.db"
qrcode = QRcode()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ally'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(DB_NAME)  # Fix the format string
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    alembic.init_app(app)
    migrate.init_app(app, db)
    qrcode.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix= '/')
    app.register_blueprint(auth, url_prefix= '/')


    from .models import URL, User, Click
    


    create_tables(app)


    login_manager = LoginManager()
    login_manager.login_view = 'auth.login_post'  # Use the assignment operator here
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app





def create_tables(app):
    with app.app_context():
        db.create_all()

       