import os
import openai
from flask import Flask, redirect, render_template, request, url_for, jsonify
from application import app

app.config['SECRET_KEY'] = 'mysecretkey'
openai.api_key = os.getenv("OPENAI_API_KEY")
app.app_context().push()



