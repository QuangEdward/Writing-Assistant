# application/plagiarism_check/views.py
import os
import openai
from flask import Blueprint, Flask, render_template, redirect, url_for, request, jsonify
from application.plagiarism_check.forms import InputForm

openai.api_key = os.getenv("OPENAI_API_KEY")
plagiarism = Blueprint('plagiarism_check',__name__, url_prefix='/plagiarism_check')


def compute_plagiarism_score(text1, text2):
    # Compute the Jaccard similarity index between the two texts
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    return len(intersection) / len(union)

def perform_plagiarism_check(text):
    search_query = f"{text}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Search for articles that contain the following text: {search_query}",
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.6,
    )
    articles = response.choices[0].text.strip()
    results = []
    for article in articles:
        plagiarism_score = compute_plagiarism_score(text, article)
        results.append({"article": article.strip(), "plagiarism_score": plagiarism_score})
    return results


@plagiarism.route('/', methods =['GET','POST'])
def index():
    form = InputForm()
    plagiarism_check = None
    if form.validate_on_submit():
        input_text = form.input_text.data
        plagiarism_check = perform_plagiarism_check(input_text)
        return render_template('plagiarism_check.html', form = form,  plagiarism_check =  plagiarism_check )
    return render_template('plagiarism_check.html', form = form )


