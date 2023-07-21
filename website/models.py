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

    # Define the relationship to URLs with a custom backref name
    urls = db.relationship('URL', back_populates='user', lazy=True)

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return f"User(id={self.id}, username='{self.username}', email='{self.email}')"


class URL(db.Model):
    __tablename__ = 'urls'

    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(200), nullable=False)
    short_url = db.Column(db.String(10), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    # clicks = db.Column(db.Integer, default=1)

    # Define the relationship to User with a custom backref name
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='urls')

    # Define the relationship to ClickTime using a backref named 'url'
    click_times = db.relationship('ClickTime', backref='url', lazy=True)

    def __repr__(self):
        return f"URL(id={self.id}, original_url='{self.original_url}', short_url='{self.short_url}', created_at='{self.created_at}')"


class ClickTime(db.Model):
    __tablename__ = 'click_times'

    id = db.Column(db.Integer, primary_key=True)
    url_id = db.Column(db.Integer, db.ForeignKey('urls.id'), nullable=False)
    click_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"ClickTime(id={self.id}, url_id={self.url_id}, click_time='{self.click_time}')"
