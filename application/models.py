# application/models.py

from application import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128)) 
    profile_image = db.Column(db.String(64), nullable=False, default='default_profile.png')
    is_active = db.Column(db.Boolean, default=True)
    completions = db.relationship('TextCompletion', backref='user', lazy='dynamic')
    grammarcheck = db.relationship('Grammarcheck', backref='user', lazy='dynamic')
    paraphase = db.relationship('Paraphrasing', backref='user', lazy='dynamic')
    plagiarismcheck = db.relationship('Plagiarismcheck', backref='user', lazy='dynamic')

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"Username {self.username}"


class Auth(db.Model):
    __tablename__ = 'auth'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)

    completions = db.relationship('TextCompletion', backref='auth', lazy='dynamic')
    grammarcheck = db.relationship('Grammarcheck', backref='auth', lazy='dynamic')
    paraphase = db.relationship('Paraphrasing', backref='auth', lazy='dynamic')
    plagiarismcheck = db.relationship('Plagiarismcheck', backref='auth', lazy='dynamic')

    def __init__(self, email, name):
        self.email = email
        self.name = name

    def __repr__(self):
        return f'<User {self.email}>'


class TextCompletion(db.Model):
    __tablename__ = 'text_completions'

    id = db.Column(db.Integer, primary_key=True)
    input_text = db.Column(db.Text, nullable=False)
    output_text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    auth_id = db.Column(db.Integer, db.ForeignKey('auth.id'))

    def __init__(self, input_text, output_text, user_id = None, auth_id = None):
        self.input_text = input_text
        self.output_text = output_text
        self.user_id = user_id 
        self.auth_id = auth_id 

    def __repr__(self):
        return f"TextCompletion - User: {self.user.username}, Input Text: {self.input_text}"
    


class Grammarcheck(db.Model):
    __tablename__ = 'grammar_check'

    id = db.Column(db.Integer, primary_key=True)
    input_text = db.Column(db.Text, nullable=False)
    output_text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    auth_id = db.Column(db.Integer, db.ForeignKey('auth.id'))

    def __init__(self, input_text, output_text, user_id = None, auth_id = None):
        self.input_text = input_text
        self.output_text = output_text
        self.user_id = user_id
        self.auth_id = auth_id  

    def __repr__(self):
        return f"Grammarcheck - User: {self.user.username}, Input Text: {self.input_text}"


class Paraphrasing(db.Model):
    __tablename__ = 'paraphrasing'

    id = db.Column(db.Integer, primary_key=True)
    input_text = db.Column(db.Text, nullable=False)
    output_text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    auth_id = db.Column(db.Integer, db.ForeignKey('auth.id'))

    def __init__(self, input_text, output_text, user_id = None, auth_id = None):
        self.input_text = input_text
        self.output_text = output_text
        self.user_id = user_id
        self.auth_id = auth_id  

    def __repr__(self):
        return f"Paraphase - User: {self.user.username}, Input Text: {self.input_text}"


class Plagiarismcheck(db.Model):
    __tablename__ = 'plagiarism'

    id = db.Column(db.Integer, primary_key=True)
    input_text = db.Column(db.Text, nullable=False)
    output_text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    auth_id = db.Column(db.Integer, db.ForeignKey('auth.id'))

    def __init__(self, input_text, output_text, user_id = None, auth_id = None):
        self.input_text = input_text
        self.output_text = output_text
        self.user_id = user_id
        self.auth_id = auth_id  

    def __repr__(self):
        return f"Plagiarism - User: {self.user.username}, Input Text: {self.input_text}"

