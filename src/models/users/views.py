import src.models.users.errors as UserErrors
from flask import Blueprint, request, session, render_template, jsonify, app
from src.models.users.user import User
from src.models.posts.post import Post
import src.models.users.decorators as user_decorators
from werkzeug.utils import redirect
from src.app import app
from src.utils import Utils

user_blueprint = Blueprint('users', __name__)

@user_blueprint.route('/register/', methods=['GET'])
def register():
    return render_template('users/register.html')

@user_blueprint.route('/login/', methods=['GET'])
def login():
    return render_template('users/login.html')

@user_blueprint.route('/profile/', methods=['GET'])
@user_decorators.requires_login(return_user=True)
def profile(user):
    user_id = user['_id']
    email = session['email']
    posts = reversed(list(Post.getAllByUserId(user_id)))
    # posts = reversed(list(Post.getAll()))
    tags = list(Post.getAllTags())
    for i in range(len(tags)):
        tags[i] = tags[i]['tag']
    return render_template('users/profile.html', email=email, posts=posts, tags=tags)

@user_blueprint.route('/auth/login', methods=['POST'])
def loginUser():
    email = request.form['email']
    password = request.form['password']
    status = "No Good"
    message = "Error - information provided does not match any account"

    if not email or not password:
        return 'Email and password are required to register'

    if not Utils.email_is_valid(email):
        return 'Email format is not valid'

    if len(password) < 6:
        return 'Password must be at least 8 characters'

    if email not in app.config['ADMINS']:
        return 'This email does not have admin priviliges'

    try:
        valid = User.isLoginValid(email, password)
        if valid:
            session['email'] = email
            status = "OK"
            message = "Success! You have been logged in!"
        else:
            session['email'] = None
        return jsonify({"status": status, "message": message, "email": email})
    except UserErrors.UserError as e:
        return e.message

@user_blueprint.route('/auth/register', methods=['POST'])
def registerUser():
    email = request.form['email']
    password = request.form['password']
    status = "No Good"
    message = "An account with that email already exists"

    if not email or not password:
        return 'Email and password are required to register'

    if not Utils.email_is_valid(email):
        return 'Email format is not valid'

    if len(password) < 6:
        return 'Password must be at least 8 characters'

    if email not in app.config['ADMINS']:
        return 'This email does not have admin priviliges'

    try:
        registered = User.register(email, password)
        if registered:
            status = "OK"
            message = "Success! Your account has been registered!"

        return jsonify({"status": status, "message": message, "email": email})
    except UserErrors.UserError as e:
        return e.message


@user_blueprint.route('/auth/logout', methods=['GET'])
@user_decorators.requires_login()
def logoutUser():
    try:
        status = "No Good"
        User.logout()
        if session['email'] is None:
            return redirect('/')
        return jsonify({"status": status})
    except UserErrors.UserError as e:
        return e.message