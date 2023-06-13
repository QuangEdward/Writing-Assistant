# application/paraphrasing/views.py
import os
import openai
from flask import Blueprint, Flask, render_template, redirect, url_for, request, jsonify
from application.paraphrasing.forms import InputForm
from application.auth.auth_decorator import login_required
openai.api_key = os.getenv("OPENAI_API_KEY")
paraphrasing = Blueprint('paraphrasing',__name__, url_prefix='/paraphrasing')


def para(text):
    response = openai.Completion.create (
        engine="text-davinci-003",
        prompt=f"I will give you text content, you will rewrite it and output that in a re-worded version of my text. \
                Reword the text to convey the same meaning using different words and sentence structures.\
                Avoiding plagiarism, improving the flow and readability of the text, and ensuring that the re-written content is unique and original. \
                Keep the tone the same. Keep the meaning the same. Make sure the re-written content's number of characters is exactly the same as the original text's number of characters. Do not alter the original structure and formatting outlined in any way. Only give me the output and nothing else. Now, using the concepts above, re-write the following text.\
                Respond in the same language variety or dialect of the following text: {text}",
        max_tokens=1000,
        n = 3,
        stop=None,
        temperature=0.6,
    )
    paraphrased_texts = [choice.text.strip() for choice in response.choices]

    return paraphrased_texts


@paraphrasing.route('/', methods =['GET','POST'])
@login_required
def index():
    form = InputForm()
    paraphrase_check = None
    if form.validate_on_submit():
        input_text = form.input_text.data
        paraphrase_check = para(input_text)
        return render_template('paraphaser.html', form = form,  paraphrase_check =  paraphrase_check )
    return render_template('paraphaser.html', form = form )


