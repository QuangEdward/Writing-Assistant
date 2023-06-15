import os
import openai
from flask import Blueprint, render_template, redirect, url_for, session, request
from application.text_completion.forms import InputForm
from application.auth.auth_decorator import login_required
from application.models import User, TextCompletion
from flask_login import current_user
from application import db


openai.api_key = os.getenv("OPENAI_API_KEY")
dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard.route('/dashboard')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    # Retrieve the input_text and output_text from the database
    user_completions = TextCompletion.query.order_by(TextCompletion.timestamp.desc()).paginate(page=page, per_page=10)

    # Pass the data to the HTML template for rendering
    return render_template('dashboard.html', user_completions = user_completions)



