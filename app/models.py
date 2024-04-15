from app import db, login
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):  # Simple User model
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128), unique=True)
    user_tasks = db.relationship('ToDo', backref='creator', lazy='dynamic')

    def __repr__(self):
        return f"User {self.username}"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class ToDo(db.Model):  # Simple task model
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    due_date = db.Column(db.Date, index=True, default=datetime.utcnow)
    status = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"Task {self.title} body {self.content}"


@login.user_loader  # Given *id*, return the associated User object
def load_user(id):
    return User.query.get(int(id))