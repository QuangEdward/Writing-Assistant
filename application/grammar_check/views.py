# application/grammar_check/views.py
import os
import openai
from flask import Blueprint, render_template, request, session
from application.grammar_check.forms import InputForm
from application.auth.auth_decorator import login_required
from application import db
from application.models import Grammarcheck, User
from flask_login import current_user

# from application.models import Grammarcheck
from flask_login import current_user
from application import db

openai.api_key = os.getenv("OPENAI_API_KEY")
grammar_check = Blueprint('grammar_check',__name__, url_prefix='/grammar_check')

def highlight_errors(text, suggestion):
    # split the input text and the suggestion into words
    words = text.split()
    suggestion_words = suggestion.split()

    # initialize lists to hold the errors and the highlighted words
    errors = []
    highlighted_words = []

    # loop through the words and compare them to the suggestion
    for i, word in enumerate(words):
        if i >= len(suggestion_words) or word.lower() != suggestion_words[i].lower():
            errors.append(word)
            highlighted_words.append(f'<mark>{word}</mark>')
        else:
            highlighted_words.append(word)

    # join the highlighted words back into a string
    highlighted_text = ' '.join(highlighted_words)

    return highlighted_text, errors

def gram(text):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"I want you to act as a brilliant grammar checker who can correct any wrong English grammars. Please correct grammar in the following texts. {text}",
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.6,
    )

    suggestion = response.choices[0].text.strip()

    highlighted_text, errors = highlight_errors(text, suggestion)

    return highlighted_text, errors

def fix(text):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"I want you to act as a brilliant grammar checker who can correct any wrong English grammars. Please rewrite all the text with the correct grammar and no paraphrase or completion text.{text}",
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.6,
    )

    suggestion = [choice.text.strip() for choice in response.choices]

    return suggestion




@grammar_check.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = InputForm()
    highlighted_text = None
    fix_errors = None
    grammar_errors = None

    if form.validate_on_submit():
        input_text = form.input_text.data

        # perform grammar check
        highlighted_text, grammar_errors = gram(input_text)
        fix_errors = fix(input_text)
        grammar_check_str = "\n".join(fix_errors)

        if current_user.is_authenticated:
            user_id = current_user.id
            auth_id = None
        elif 'profile' in session:
            user_id = None
            auth_id = current_user.auth.id if hasattr(current_user, 'auth') else None
        else:
            user_id = None
            auth_id = None

        grammar_check = Grammarcheck(
            user_id=user_id,
            auth_id=auth_id,
            input_text=input_text,
            output_text=grammar_check_str
        )

        db.session.add(grammar_check)
        db.session.commit()

        fix_errors = fix_errors

        return render_template('grammar_check.html', form=form, highlighted_text=highlighted_text,grammar_errors= grammar_errors, fix_errors=fix_errors)
    return render_template('grammar_check.html', form=form)
# def index():
#     form = InputForm()
#     highlighted_text = None
#     grammar_errors = None

#     if form.validate_on_submit():
#         input_text = form.input_text.data

#         # Perform grammar check
#         highlighted_text, grammar_errors = gram(input_text)
#         fix_errors = fix(input_text)

#         # Save input and output in the database
#         user_id = current_user.id  # Assuming you have a current_user object from authentication
#         grammar_check_entry = grammar_check(user_id=user_id, input_text=input_text, output_text=highlighted_text)
#         db.session.add(grammar_check_entry)
#         db.session.commit()

#         return render_template('grammar_check.html', form=form, highlighted_text=highlighted_text, grammar_errors=grammar_errors, fix_errors=fix_errors)

#     return render_template('grammar_check.html', form=form)