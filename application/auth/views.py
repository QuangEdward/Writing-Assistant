# AS simeple as possbile flask google oAuth 2.0
from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
import os
from datetime import timedelta
from application import app, oauth, OAuth
from flask import render_template,url_for,flash,redirect,request,Blueprint
from authlib.integrations.flask_client import OAuth
from application.auth.auth_decorator import login_required
from application import db
from application.models import User


auth = Blueprint('auth',__name__, url_prefix='/auth')



google = oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    client_kwargs={'scope': 'openid email profile'},
    jwks_uri='https://www.googleapis.com/oauth2/v3/certs'
)

@auth.route('/')
@login_required
def hello_world():
    email = dict(session)['profile']['email']
    name = dict(session)['profile']['name']
    profile_image = dict(session)['profile']['profile_image']  # Get the profile image URL from the session
    return render_template('google_auth.html', email=email, name=name, profile_image=profile_image)


@auth.route('/login')
def login():
    google = oauth.create_client('google')  # create the google oauth client
    redirect_uri = url_for('auth.authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


@auth.route('/authorize')
def authorize():
    google = oauth.create_client('google')  # create the google oauth client
    token = google.authorize_access_token()  # Access token from google (needed to get user info)
    resp = google.get('userinfo')  # userinfo contains stuff you specified in the scope
    user_info = resp.json()
    
    try:
        email = user_info['email']
        name = user_info['name']
        google_id = user_info['sub']  # Extract the Google ID from the response
        profile_image = user_info['picture']  # Get the profile image URL from the user_info response
        
        # Check if a user with the provided Google ID already exists in the database
        user = User.query.filter_by(google_id=google_id).first()

        if user is None:
            # If the user doesn't exist, create a new user with the Google information
            user = User(email=email, name=name, google_id=google_id)
            db.session.add(user)
            db.session.commit()

        session['profile'] = {
            'email': email,
            'name': name,
            'profile_image': profile_image  # Store the profile image URL in the session
        }
        session.permanent = True  # make the session permanent so it keeps existing after the browser gets closed
        return redirect(url_for('auth.hello_world'))
    except KeyError:
        flash('Failed to retrieve user information from Google.')
        return redirect(url_for('auth.login'))



@auth.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for("core.index"))