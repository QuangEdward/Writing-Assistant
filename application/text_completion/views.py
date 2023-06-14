# application/text_completion/views.py
import os
import openai
from flask import Blueprint, Flask, render_template, redirect, url_for, request, jsonify
from application.text_completion.forms import InputForm
from application.auth.auth_decorator import login_required
from application.models import User
from flask_login import current_user
from application import db

openai.api_key = os.getenv("OPENAI_API_KEY")
completion = Blueprint('text_completion',__name__, url_prefix='/text_completion')

def com(text):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"I'll give you text. You'll pick up where the user left off and complete the following text with generated sentences in full with it's original text and output it longer to be more than twice the number of characters of the original text.\
                 Keep the meaning the same. Only give me the output and nothing else.\
                 Now, using the concepts above, complete the following text with generated sentences in full with it's original text. Cannot change the orginal text and respond in the same language variety or dialect of the following text: {text}",
        max_tokens=1024,
        n=3,
        stop=None,
        temperature=0.6,
    )

    completion_text = [choice.text.strip() for choice in response.choices]
    completion_text_str = "\n".join(completion_text)  # Convert list to a string

    text_completion = TextCompletion(user_id=current_user.id, input_text=text, output_text=completion_text_str)
    db.session.add(text_completion)
    db.session.commit()
    
    return completion_text

@completion.route('/', methods =['GET','POST'])
@login_required
# def index():
#     form = InputForm()
#     completion = None
#     if form.validate_on_submit():
#         input_text = form.input_text.data
#         user = User.query.filter_by(id=current_user.id).first()
#         completion_text = com(input_text)
#         completion = TextCompletion(input_text=input_text, user_id=user, output_text=output_text)
#         db.session.add(completion)
#         db.session.commit()
#     completions = TextCompletion.query.filter_by(user_id=current_user.id).order_by(TextCompletion.timestamp.desc()).all()

#     return render_template('text_completion.html', form = form,  completion =  completion )
    

# def index():
#     form = InputForm()
#     completion = None
#     if form.validate_on_submit():
#         input_text = form.input_text.data
#         completion_text = com(input_text)  # Get the completion text

#         # Create a new instance of TextCompletion and save it to the database
#         text_completion = TextCompletion(user_id=current_user.id, input_text=input_text, output_text=completion_text)
#         db.session.add(text_completion)
#         db.session.commit()

#         completion = completion_text  # Assign the completion text to the completion variable for rendering

#     return render_template('text_completion.html', form=form, completion=completion)

def index():
    form = InputForm()
    completion = None
    if form.validate_on_submit():
        input_text = form.input_text.data
        completion = com(input_text)
    return render_template('text_completion.html', form=form, completion=completion)
