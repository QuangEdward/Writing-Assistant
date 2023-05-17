# application/plagiarism_check/views.py
import os
import openai
from flask import Blueprint, Flask, render_template, redirect, url_for, request, jsonify
from application.plagiarism_check.forms import InputForm
from googlesearch import search
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
from application.auth.auth_decorator import login_required
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)

openai.api_key = os.getenv("OPENAI_API_KEY")
plagiarism = Blueprint('plagiarism_check',__name__, url_prefix='/plagiarism_check')

def preprocess_text(text):
    # Tokenize the text and remove stop words and punctuations
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text.lower())
    words = [word for word in words if word.isalpha() and word not in stop_words]
    return ' '.join(words)

def search_documents(query):
    # Search for documents on the internet that match the query
    search_results = search(query, num=10)
    return search_results

def compare_texts(input_text, document):
    # Compare the input text with the document using cosine similarity
    input_tokens = set(preprocess_text(input_text).split())
    document_tokens = set(preprocess_text(document).split())
    similarity = len(input_tokens.intersection(document_tokens)) / len(input_tokens.union(document_tokens))
    return similarity


@plagiarism.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = InputForm()
    plagiarism_check = None

    if form.validate_on_submit():
        input_text = form.input_text.data
        search_results = search_documents(input_text)
        scores = []

        for result in search_results:
            document = openai.Completion.create(
                engine="text-davinci-003", 
                prompt=f"compare text '{input_text}' with text from url '{result}'", 
                max_tokens=1024,
                stop = None,
                temperature=0.6)["choices"][0]["text"].strip()
            similarity = compare_texts(input_text, document)
            scores.append((result, similarity))

        scores.sort(key=lambda x: x[1], reverse=True)
        plagiarism_check = (input_text, scores)

    return render_template('plagiarism_check.html', form=form, plagiarism_check=plagiarism_check)
