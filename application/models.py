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
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    profile_image = db.Column(db.String(64), nullable=False, default='default_profile.png')
    google_id = db.Column(db.String(64), unique=True, index=True)

    def __init__(self, email=None, username=None, password=None, google_id=None):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password) if password else None
        self.google_id = google_id

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"Username {self.username}"


class TextCompletion(db.Model):
    __tablename__ = 'text_completions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    input_text = db.Column(db.Text, nullable=False)
    output_text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    

    user = db.relationship('User', backref=db.backref('text_completions', lazy=True))

    def __init__(self, user_id, input_text, output_text):
        self.user_id = user_id
        self.input_text = input_text
        self.output_text = output_text

    def __repr__(self):
        return f"TextCompletion - User: {self.user.username}, Input Text: {self.input_text}"
    

# class Grammarcheck(db.Model):
#     __tablename__ = 'grammar_check'

#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     input_text = db.Column(db.Text, nullable=False)
#     output_text = db.Column(db.Text, nullable=False)
#     timestamp = db.Column(db.DateTime, default=datetime.utcnow)


#     user = db.relationship('User', backref=db.backref('grammar_check', lazy=True))

#     def __init__(self, user_id, input_text, output_text):
#         self.user_id = user_id
#         self.input_text = input_text
#         self.output_text = output_text

#     def __repr__(self):
#         return f"TextCompletion - User: {self.user.username}, Input Text: {self.input_text}"
    

# class paraphrasing(db.Model):
#     __tablename__ = 'paraphrasing'
#     users = db.relationship(User)

#     id = db.Column(db.Integer,primary_key=True)
#     user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)

#     input_text = db.Column(db.String(1024), nullable=False)
#     output_text = db.Column(db.String(1024), nullable=False)

#     date = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)

#     def __init__(self,input_text,output_text,user_id):
#         self.input_text = input_text
#         self.output_text = output_text
#         self.user_id = user_id

#     def __repr__(self):
#         return f" ID: {self.id} -- Date: {self.date} "


# class plagiarism_check(db.Model):
#     __tablename__ = 'plagiarism_check'
#     users = db.relationship(User)

#     id = db.Column(db.Integer,primary_key=True)
#     user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)

#     input_text = db.Column(db.String(1024), nullable=False)
#     output_text = db.Column(db.String(1024), nullable=False)

#     date = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)

#     def __init__(self,input_text,output_text,user_id):
#         self.input_text = input_text
#         self.output_text = output_text
#         self.user_id = user_id

#     def __repr__(self):
#         return f" ID: {self.id} -- Date: {self.date} "


# class text_completion(db.Model):
#     __tablename__ = 'text_completion'
#     users = db.relationship(User)

#     id = db.Column(db.Integer,primary_key=True)
#     user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)

#     input_text = db.Column(db.String(1024), nullable=False)
#     output_text = db.Column(db.String(1024), nullable=False)

#     date = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)

#     def __init__(self,input_text,output_text,user_id):
#         self.input_text = input_text
#         self.output_text = output_text
#         self.user_id = user_id

#     def __repr__(self):
#         return f" ID: {self.id} -- Date: {self.date} "