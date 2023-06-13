# application/text_completion/views.py
import os
import openai
from flask import Blueprint, Flask, render_template, redirect, url_for, request, jsonify
from application.text_completion.forms import InputForm
from application.auth.auth_decorator import login_required

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
    
    return completion_text

@completion.route('/', methods =['GET','POST'])
@login_required
def index():
    form = InputForm()
    completion = None
    if form.validate_on_submit():
        input_text = form.input_text.data
        completion = com(input_text)
    return render_template('text_completion.html', form = form,  completion =  completion )
    
