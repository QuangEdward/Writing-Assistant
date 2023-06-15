import os
import openai
from flask import Blueprint, render_template, redirect, url_for, session, request
from application.text_completion.forms import InputForm
from application.auth.auth_decorator import login_required
from application.models import User, TextCompletion, Grammarcheck, Paraphrasing, Plagiarismcheck
from flask_login import current_user
from application import db


openai.api_key = os.getenv("OPENAI_API_KEY")
dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard.route('/text_completion')
@login_required
def textcompletion():
    page = request.args.get('page', 1, type=int)
    # Retrieve the input_text and output_text from the database
    user_completions = TextCompletion.query.order_by(TextCompletion.timestamp.desc()).paginate(page=page, per_page=10)

    # Pass the data to the HTML template for rendering
    return render_template('completion_dashboard.html', user_completions = user_completions)


@dashboard.route('/grammar_check')
@login_required
def grammarcheck():
    page = request.args.get('page', 1, type=int)
    # Retrieve the input_text and output_text from the database
    user_grammarcheck = Grammarcheck.query.order_by(Grammarcheck.timestamp.desc()).paginate(page=page, per_page=10)

    # Pass the data to the HTML template for rendering
    return render_template('grammar_dashboard.html', user_grammarcheck = user_grammarcheck)


@dashboard.route('/paraphase')
@login_required
def paraphasing():
    page = request.args.get('page', 1, type=int)
    # Retrieve the input_text and output_text from the database
    user_paraphase = Paraphrasing.query.order_by(Paraphrasing.timestamp.desc()).paginate(page=page, per_page=10)

    # Pass the data to the HTML template for rendering
    return render_template('paraphase_dashboard.html', user_paraphase = user_paraphase)

@dashboard.route('/plagiarism')
@login_required
def plagiarism():
    page = request.args.get('page', 1, type=int)
    # Retrieve the input_text and output_text from the database
    user_plagiarism = Plagiarismcheck.query.order_by(Plagiarismcheck.timestamp.desc()).paginate(page=page, per_page=10)

    # Pass the data to the HTML template for rendering
    return render_template('plagiarism_dashboard.html', user_plagiarism = user_plagiarism)



