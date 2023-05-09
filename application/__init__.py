# application/__init__.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecret'
app.app_context().push()
############################
###### DATABASE SETUP ######
############################
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

############################
###### LOGIN CONFIG ########
############################

login_manager = LoginManager()

login_manager.init_app(app)
login_manager.login_view = 'users.login'


############################
from application.core.views import core
from application.users.views import users
from application.error_pages.handlers import error_pages
from application.paraphrasing.views import paraphrasing
from application.text_completion.views import completion
from application.grammar_check.views import grammar_check
from application.plagiarism_check.views import plagiarism

app.register_blueprint(core)
app.register_blueprint(users)
app.register_blueprint(error_pages)
app.register_blueprint(paraphrasing)
app.register_blueprint(completion)
app.register_blueprint(grammar_check)
app.register_blueprint(plagiarism)
