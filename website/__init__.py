from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_alembic import Alembic
from flask_migrate import Migrate


db = SQLAlchemy()
alembic = Alembic()
migrate = Migrate()
DB_NAME = "database.db"
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY']= 'ally'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:/// {DB_NAME}'  # change this to your desired database filename and path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    alembic.init_app(app)
    migrate.init_app(app, db)
    


    # app.config.from_object(website.config)

    # import website.models



    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix= '/')
    app.register_blueprint(auth, url_prefix= '/')

    from .models import URL, User, Click


    create_tables(app)
    return app




def create_tables(app):
    with app.app_context():
        db.create_all()

       