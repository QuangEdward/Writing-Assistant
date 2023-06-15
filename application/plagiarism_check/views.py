import os
import openai
from flask import Blueprint, Flask, render_template, redirect, url_for, request, jsonify, session
from application.plagiarism_check.forms import InputForm
from googlesearch import search
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
from application.auth.auth_decorator import login_required
from flask_login import current_user
from application import db
from application.models import Plagiarismcheck
import json
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)

openai.api_key = os.getenv("OPENAI_API_KEY")
plagiarism = Blueprint('plagiarism_check', __name__, url_prefix='/plagiarism_check')


def search_documents(query):
    search_results = search(query, num=5) 
    return search_results

def compare_texts(input_text, document):
    input_words = set(word_tokenize(input_text.lower()))
    document_words = set(word_tokenize(document.lower()))
    similarity = len(input_words.intersection(document_words)) / len(input_words.union(document_words))
    percentage = similarity * 100
    return percentage

@plagiarism.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = InputForm()
    plagiarism_check = None
    total = 0
    doc = 0
    if form.validate_on_submit():
        input_text = form.input_text.data
        search_results = list(search_documents(input_text))
        scores = []

        for result in search_results:
            document = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f"compare text '{input_text[:900]}' with text from url '{result}'",
                max_tokens=1024,
                stop=None,
                temperature=0.6
            )["choices"][0]["text"].strip()

            similarity = compare_texts(input_text, document)
            scores.append((result, similarity))
            total += similarity
            doc += 1
        scores.sort(key=lambda x: x[1], reverse=True)
        if doc > 0:
            sum_percentage = total / doc
        else:
            sum_percentage = 0
        plagiarism_check = (input_text, scores)

        # Convert plagiarism_check to string representation
        output = "\n".join(plagiarism_check)

        if current_user.is_authenticated:
            user_id = current_user.id
            auth_id = None
        elif 'profile' in session:
            user_id = None
            auth_id = current_user.auth.id if hasattr(current_user, 'auth') else None
        else:
            user_id = None
            auth_id = None

        for i, output_text in enumerate(plagiarism_check):
            plagiarism_text = Plagiarismcheck(
                user_id=user_id,
                auth_id=auth_id,
                input_text=input_text,
                output_text=output_text
            )
            db.session.add(plagiarism_text)
        db.session.add(plagiarism_text)
        db.session.commit()

        plagiarism_check = output

        return render_template('plagiarism_check.html', form=form, plagiarism_check=plagiarism_check, total=sum_percentage)
    return render_template('plagiarism_check.html', form=form, plagiarism_check=plagiarism_check, total=total)
