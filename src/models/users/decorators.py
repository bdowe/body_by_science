from functools import wraps

from flask import session, url_for, request
from werkzeug.utils import redirect
from src.app import app
from src.models.users.user import User


def requires_login(return_user=False):
    def real_decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            if 'email' not in session.keys() or session['email'] is None:
                return redirect(url_for('users.login', next=request.path))
            if return_user:
                user = User.getByEmail(session['email'])
                return func(user, **kwargs) #func(...) args: func(5, 6) kwargs: func(x=5, y=6)
            return func(*args, **kwargs)  # func(...) args: func(5, 6) kwargs: func(x=5, y=6)
        return decorated_function
    return real_decorator

def requires_admin_permissions(return_user=False):
    def real_decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            if 'email' not in session.keys() or session['email'] is None:
                return redirect(url_for('users.login', next=request.path))
            if session['email'] not in app.config['ADMINS']:
                return redirect(url_for('users.login'))
            if return_user:
                user = User.getByEmail(session['email'])
                return func(user, **kwargs) #func(...) args: func(5, 6) kwargs: func(x=5, y=6)
            return func(*args, **kwargs)  # func(...) args: func(5, 6) kwargs: func(x=5, y=6)
        return decorated_function
    return real_decorator
