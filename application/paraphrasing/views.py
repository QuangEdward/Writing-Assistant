# application/paraphrasing/views.py
import os
import openai
from flask import Blueprint, Flask, render_template, redirect, url_for, request, jsonify
from application.paraphrasing.forms import InputForm

openai.api_key = os.getenv("OPENAI_API_KEY")
paraphrasing = Blueprint('paraphrasing',__name__, url_prefix='/paraphrasing')


def para(text):
    response = openai.Completion.create (
        engine="text-davinci-003",
        prompt=f"Please paraphrase my text. {text}",
        max_tokens=1000,
        n = 1,
        stop=None,
        temperature=0.6,
    )
    paraphrased_texts = [choice.text.strip() for choice in response.choices]

    return paraphrased_texts


@paraphrasing.route('/', methods =['GET','POST'])
def index():
    form = InputForm()
    paraphrase_check = None
    if form.validate_on_submit():
        input_text = form.input_text.data
        paraphrase_check = para(input_text)
        return render_template('paraphaser.html', form = form,  paraphrase_check =  paraphrase_check )
    return render_template('paraphaser.html', form = form )


