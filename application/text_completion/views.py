# application/text_completion/views.py
import os
import openai
from flask import Blueprint, Flask, render_template, redirect, url_for, request, jsonify
from application.text_completion.forms import InputForm

openai.api_key = os.getenv("OPENAI_API_KEY")
completion = Blueprint('text_completion',__name__, url_prefix='/text_completion')

def com(text):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Please complete my text. {text}",
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.6,
    )

    completion_text = [choice.text.strip() for choice in response.choices]

    return completion_text

@completion.route('/', methods =['GET','POST'])
def index():
    form = InputForm()
    completion = None
    if form.validate_on_submit():
        input_text = form.input_text.data
        completion = com(input_text)
        return render_template('text_completion.html', form = form,  completion =  completion )
    return render_template('text_completion.html', form = form )
