from flask import Flask, request, jsonify
import openai
import re

def grammar_check(text):
    # Split text into sentences
    sentences = re.split('[.!?]', text)
    # Remove empty sentences
    sentences = [sentence for sentence in sentences if len(sentence.strip()) > 0]
    # Check each sentence for grammar errors
    results = []
    for sentence in sentences:
        response = openai.Completion.create(
          engine="text-davinci-002",
          prompt=f"Please correct the grammar in the following sentence: '{sentence}'",
          max_tokens=1024,
          n=1,
          stop=None,
          temperature=0.5,
        )
        corrected_sentence = response.choices[0].text.strip()
        if corrected_sentence != sentence:
            results.append({
                "original_sentence": sentence,
                "corrected_sentence": corrected_sentence
            })
    return results



def plagiarism_check(text):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Please check for plagiarism. {text}",
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )

    matches = response.choices[0].text.strip()

    return get_links(matches)


def text_completion(text):
    response = openai.Completion.create(
        engine="davinci",
        prompt=f"Please complete my text. {text}",
        max_tokens=60,
        n=1,
        stop=None,
        temperature=0.5,
    )

    completion_text = response.choices[0].text.strip()

    return completion_text


def paraphrasing(text):
    response = openai.Completion.create (
        engine="text-davinci-002",
        prompt=f"Please paraphrase my text. {text}",
        max_tokens=60,
        n=3,
        stop=None,
        temperature=0.5,
    )
    paraphrased_texts = [choice.text.strip() for choice in response.choices]

    return paraphrased_texts

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

    return highlighted_text

def get_links(matches):
    links = []
    for match in matches:
        link = f'<a href="{match["url"]}">{match["title"]}</a>'
        links.append(link)
    return links