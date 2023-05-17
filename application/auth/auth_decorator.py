from flask import session, url_for, redirect
from functools import wraps
from flask_login import current_user

# def login_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         user = dict(session).get('profile', None)
#         # You would add a check here and usethe user id or something to fetch
#         # the other data for that user/check if they exist
#         if user:
#             return f(*args, **kwargs)
#         return 'You aint logged in, no page for u!'
#     return decorated_function

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            # User is already authenticated via regular login
            return f(*args, **kwargs)
        elif 'profile' in session:
            # User is authenticated with Google
            return f(*args, **kwargs)
        else:
            return redirect(url_for("users.login"))
    return decorated_function
