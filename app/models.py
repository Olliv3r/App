from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Tool(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    author = db.Column(db.String(120), nullable=False)
    alias = db.Column(db.String(120), nullable=False)
    custom_alias = db.Column(db.String(), nullable=True)
    name_repository = db.Column(db.String(), nullable=True)

    link = db.Column(db.String(), nullable=True)
    type_install = db.Column(db.String(), nullable=False)
    category = db.Column(db.String(), nullable=False)
    dependencies = db.Column(db.String(), nullable=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    modified = db.Column(db.DateTime, default=datetime.utcnow)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), nullable=False, unique=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
