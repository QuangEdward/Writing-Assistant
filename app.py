# import os

# import openai
# from flask import Flask, redirect, render_template, request, url_for

# app = Flask(__name__)
# openai.api_key = os.getenv("OPENAI_API_KEY")


# @app.route("/", methods=("GET", "POST"))
# def index():
#     if request.method == "POST":
#         animal = request.form["animal"]
#         response = openai.Completion.create(
#             model="text-davinci-003",
#             prompt=generate_prompt(animal),
#             temperature=0.6,
#         )
#         return redirect(url_for("index", result=response.choices[0].text))

#     result = request.args.get("result")
#     return render_template("index.html", result=result)


# def generate_prompt(animal):
#     return """Suggest three names for an animal that is a superhero.

# Animal: Cat
# Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
# Animal: Dog
# Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
# Animal: {}
# Names:""".format(
#         animal.capitalize()
#     )

from flask import Flask, redirect, request, session, url_for
from google.oauth2 import id_token
from google.auth.transport import requests
import os

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev')

GOOGLE_CLIENT_ID = os.environ['GOOGLE_CLIENT_ID']
GOOGLE_CLIENT_SECRET = os.environ['GOOGLE_CLIENT_SECRET']
GOOGLE_DISCOVERY_URL = 'https://accounts.google.com/.well-known/openid-configuration'

@app.route('/login')
def login():
    session['state'] = os.urandom(24).hex()
    authorization_endpoint = requests.get(GOOGLE_DISCOVERY_URL).json()["authorization_endpoint"]
    redirect_uri = url_for('callback', _external=True)
    params = {
        'client_id': GOOGLE_CLIENT_ID,
        'redirect_uri': redirect_uri,
        'scope': 'openid email profile',
        'response_type': 'code',
        'state': session['state'],
    }
    return redirect(authorization_endpoint + '?' + urlencode(params))

@app.route('/callback')
def callback():
    code = request.args.get('code')
    state = request.args.get('state')
    if state != session['state']:
        return 'Invalid state parameter', 400
    token_endpoint = requests.get(GOOGLE_DISCOVERY_URL).json()["token_endpoint"]
    redirect_uri = url_for('callback', _external=True)
    data = {
        'code': code,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code',
        'client_id': GOOGLE_CLIENT_ID,
        'client_secret': GOOGLE_CLIENT_SECRET,
    }
    response = requests.post(token_endpoint, data=data)
    token_data = response.json()
    id_info = id_token.verify_oauth2_token(
        token_data['id_token'], requests.Request(), GOOGLE_CLIENT_ID)
    session['user'] = id_info['sub']
    return redirect(url_for('home'))

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return wrapper

@app.route('/')
@login_required
def home():
    return 'Hello, ' + session['user']
