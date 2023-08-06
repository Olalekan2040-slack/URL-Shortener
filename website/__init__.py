from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_alembic import Alembic
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_qrcode import QRcode
from flask_caching import Cache




# cache = Cache()
cache = Cache(config={'CACHE_TYPE': 'simple'})
db = SQLAlchemy()
alembic = Alembic()
migrate = Migrate()
DB_NAME = "database.db"
qrcode = QRcode()

dev = "ye"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ally'
    if dev == "No":
        app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://scissors_user:56UrctchR8HhrK0Vpw4LWuRCyceEyeD9@dpg-ci907at9aq0dcs9uuqk0-a.oregon-postgres.render.com/scissors"
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(DB_NAME) 

     # Fix the format string
    

    app.config['CACHE_TYPE'] = 'simple'  # Using simple cache type for demonstration purposes
    app.config['CACHE_DEFAULT_TIMEOUT'] = 300  # Cache timeout set to 300 seconds (5 minutes)
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    alembic.init_app(app)
    migrate.init_app(app, db)
    qrcode.init_app(app)
    cache.init_app(app)

    
    #connection test
    # with app.app_context():
    #     conn = psycopg2.connect(app.config['SQLALCHEMY_DATABASE_URI'])
    #     cursor = conn.cursor()
    #     cursor.execute("SELECT version();")
    #     result = cursor.fetchone()
    #     print("PostgreSQL version:", result[0])
    #     cursor.close()
    #     conn.close()

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix= '/')
    app.register_blueprint(auth, url_prefix= '/')


    from .models import URL, User, ClickTime



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

       