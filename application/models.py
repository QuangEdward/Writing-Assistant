# application/models.py

from application import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    _tablename_ = 'users'

    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(64),unique=True,index=True)
    username = db.Column(db.String(64),unique=True,index=True)
    password_hash = db.Column(db.String(128))
    profile_image = db.Column(db.String(64),nullable=False,default='default_profile.png')

    # This is a one-to-many relationship
    # grammarcheck = db.relationship('grammar_check',backref='users',lazy='dynamic')
    # paraphase = db.relationship('paraphrasing',backref='users',lazy='dynamic')
    # plagiarismcheck = db.relationship('plagiarism_check',backref='users',lazy='dynamic')
    # textcompletion = db.relationship('text_completion',backref='users',lazy='dynamic')

    def __init__(self,email,username,password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f"Username {self.username}"
    

# class grammar_check(db.Model):
#     __tablename__ = 'grammar_check'
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