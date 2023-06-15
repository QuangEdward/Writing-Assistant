# application/text_completion/views.py
import os
import openai
from flask import Blueprint, render_template, redirect, url_for, session
from application.text_completion.forms import InputForm
from application.auth.auth_decorator import login_required
from application.models import User, TextCompletion
from flask_login import current_user
from application import db

openai.api_key = os.getenv("OPENAI_API_KEY")
completion = Blueprint('text_completion', __name__, url_prefix='/text_completion')


def com(text):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"I'll give you text. You'll pick up where the user left off and complete the following text with generated sentences in full with its original text and output it longer to be more than twice the number of characters of the original text. \
                 Keep the meaning the same. Only give me the output and nothing else. \
                 Now, using the concepts above, complete the following text with generated sentences in full with its original text. Cannot change the original text and respond in the same language variety or dialect of the following text: {text}",
        max_tokens=1024,
        n=3,
        stop=None,
        temperature=0.6,
    )

    completion_text = [choice.text.strip() for choice in response.choices]
    # Convert list to a string
    return completion_text


@completion.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = InputForm()
    completion = None
    if form.validate_on_submit():
        input_text = form.input_text.data
        completion_text = com(input_text)
        completion_text_str = "\n".join(completion_text)

        if current_user.is_authenticated:
            user_id = current_user.id
            auth_id = None
        elif 'profile' in session:
            user_id = None
            auth_id = current_user.auth.id if hasattr(current_user, 'auth') else None
        else:
            user_id = None
            auth_id = None

        for i, output_text in enumerate(completion_text):
            text_completion = TextCompletion(
                user_id=user_id,
                auth_id=auth_id,
                input_text=input_text,
                output_text=output_text
            )
            db.session.add(text_completion)
        db.session.add(text_completion)
        db.session.commit()

        completion = completion_text

    return render_template('text_completion.html', form=form, completion=completion)
