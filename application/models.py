# application/models.py

# from application import db, login_manager
# from werkzeug.security import generate_password_hash, check_password_hash
# from flask_login import UserMixin
# from datetime import datetime

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(user_id)


# class User(db.Model, UserMixin):
#     _tablename_ = 'users'

#     id = db.Column(db.Integer,primary_key=True)
#     profile_image = db.Column(db.String(64),nullable=False,default='default_profile.png')
#     email = db.Column(db.String(64),unique=True,index=True)
#     username = db.Column(db.String(64),unique=True,index=True)
#     password_hash = db.Column(db.String(128))

#     grammarcheck = db.relationship('grammar_check',backref='author',lazy=True)
#     paraphase = db.relationship('paraphrasing',backref='author',lazy=True)
#     plagiarismcheck = db.relationship('plagiarism_check',backref='author',lazy=True)
#     textcompletion = db.relationship('text_completion',backref='author',lazy=True)

#     def __init__(self,email,username,password):
#         self.email = email
#         self.username = username
#         self.password_hash = generate_password_hash(password)

#     def check_password(self,password):
#         return check_password_hash(self.password_hash,password)

#     def __repr__(self):
#         return f"Username {self.username}"
    

# class grammar_check(db.Model):

#     users = db.relationship(User)

#     id = db.Column(db.Integer,primary_key=True)
#     user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)

#     date = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
#     title = db.Column(db.String(140),nullable=False)
#     text = db.Column(db.Text,nullable=False)
#     history = db.Column(db.Text,nullable=False)

#     def __init__(self,title,text,user_id):
#         self.title = title
#         self.text = text
#         self.user_id = user_id

#     def __repr__(self):
#         return f" ID: {self.id} -- Date: {self.date} --- {self.title}"