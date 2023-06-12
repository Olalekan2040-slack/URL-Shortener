from datetime import datetime
from flask_login import UserMixin
from . import db
from werkzeug.security import generate_password_hash, check_password_hash



class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    urls = db.relationship('URL', backref='user', lazy=True)

    def get_id(self):
        return str(self.id)


class URL(db.Model):
    __tablename__ = 'urls'

    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(200), nullable=False)
    short_url = db.Column(db.String(10), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    clicks = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    owner = db.relationship('User', backref='owner_urls')

    def __repr__(self):
        return f"URL('{self.original_url}', '{self.short_url}', '{self.created_at}')"

class Click(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    url_id = db.Column(db.Integer, db.ForeignKey('urls.id'), nullable=False)


class Barcode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.LargeBinary, nullable=False)  # Binary representation of the barcode image
    url_id = db.Column(db.Integer, db.ForeignKey('urls.id'), nullable=False)
    url = db.relationship('URL', backref='barcodes', lazy=True)


