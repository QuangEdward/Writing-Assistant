# application/grammar_check/views.py
import os
import openai
from flask import Blueprint, Flask, render_template, redirect, url_for, request, jsonify
from application.grammar_check.forms import InputForm
import spacy
openai.api_key = os.getenv("OPENAI_API_KEY")
grammar_check = Blueprint('grammar_check',__name__, url_prefix='/grammar_check')


# nlp = spacy.load("en_core_web_sm")

# def highlight_errors(text, suggestion):
#     # initialize the input sentence and suggestion as spacy Doc objects
#     doc = nlp(text)
#     suggestion_doc = nlp(suggestion)

#     # initialize lists to hold the errors and the highlighted words
#     errors = []
#     highlighted_words = []

#     # loop through the tokens in the input sentence
#     for i, token in enumerate(doc):
#         # compare the token to the corresponding token in the suggestion
#         if i < len(suggestion_doc) and token.text.lower() != suggestion_doc[i].text.lower():
#             # if the tokens don't match, check if they have the same part of speech and dependency
#             suggestion_token = suggestion_doc[i]
#             if token.pos_ == suggestion_token.pos_ and token.dep_ == suggestion_token.dep_:
#                 # if the tokens have the same part of speech and dependency, assume it's a spelling error
#                 errors.append(token.text)
#                 highlighted_words.append(f'<mark>{token.text}</mark>')
#             else:
#                 # otherwise, assume it's a grammatical error
#                 highlighted_words.append(f'<strong><mark>{token.text}</mark></strong>')
#         else:
#             # if the tokens match, add them to the highlighted words
#             highlighted_words.append(token.text)

#     # join the highlighted words back into a string
#     highlighted_text = ' '.join(highlighted_words)

#     return highlighted_text



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
        prompt=f"Please check my grammar and highlight it. {text}",
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.6,
    )

    suggestion = response.choices[0].text.strip()

    highlighted_text, errors = highlight_errors(text, suggestion)

    return highlighted_text, errors

def spell_check(text):
    # response = openai.Completio n.create(
    #     engine="text-davinci-003",
    #     prompt=f"Please give me suggestion to fix word. {text}",
    #     max_tokens=60,
    #     n=1,
    #     stop=None,
    #     temperature=0.6,
    # )
    response = openai.Completion.create(
    model="text-davinci-003",
    # prompt="Correct this to standard English:\n\nShe no went to the market.",
    prompt=f"Correct this to standard English {text}",
    temperature=0,
    max_tokens=60,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0
    )

    suggestion = response.choices[0].text.strip()

    highlighted_text, errors = highlight_errors(text, suggestion)

    return highlighted_text, errors

@grammar_check.route('/', methods =['GET','POST'])
def index():
    form = InputForm()
    highlighted_text = None
    grammar_errors = None
    spell_errors = None

    if form.validate_on_submit():
        input_text = form.input_text.data

        # perform grammar check
        highlighted_text, grammar_errors = gram(input_text)

        # perform spell check
        highlighted_text, spell_errors = spell_check(highlighted_text)

        return render_template('grammar_check.html', form=form, highlighted_text=highlighted_text, grammar_errors=grammar_errors, spell_errors=spell_errors)

    return render_template('grammar_check.html', form=form)
