import src.models.posts.errors as PostErrors
from flask import Blueprint, request, session, render_template, jsonify
from src.models.posts.post import Post
from src.models.users.user import User
import src.models.users.decorators as user_decorators
from werkzeug.utils import redirect
import datetime

post_blueprint = Blueprint('posts', __name__)

@post_blueprint.route('/new/', methods=['GET'])
@user_decorators.requires_admin_permissions(return_user=False)
def new():
    email = session['email']
    if email:
        tags = list(Post.getAllTags())
        for i in range(len(tags)):
            tags[i] = tags[i]['tag']
        return render_template('posts/new.html', tags=tags)
    return render_template('users/login')


@post_blueprint.route('/create/', methods=['POST'])
@user_decorators.requires_admin_permissions(return_user=False)
def create():
    title = request.form['title']
    description = request.form['description']
    body = request.form['body']
    tag = request.form['tag']
    status = "No Good"
    message = "Error: item not inserted"
    try:
        post_added = Post.new(title, description, body, tag)
        if post_added:
            status = "OK"
            message = "Success!!!"
        return jsonify({"status": status, "message": message, "body": body, "tag": tag, "timestamp": datetime.datetime.now()})
    except PostErrors.PostError as e:
        return e.message


@post_blueprint.route('/search/', methods=['POST'])
@user_decorators.requires_login(return_user=False)
def search():
    input_tag = request.form['input-tag'] if 'input-tag' in request.form else None
    select_tag = request.form['select-tag'] if 'select-tag' in request.form else None
    tag = None
    user_id = User.getByEmail(session['email'])['_id']
    status = "No Good"
    message = "Error: search failed"
    try:
        if input_tag is not None:
            tag = input_tag
        elif select_tag is not None:
            tag = select_tag

        if tag is not None and tag is not "0":
            posts = list(reversed(list(Post.getManyByTag(tag))))
        else:
            posts = list(reversed(list(Post.getAll())))

        print(tag)
        if posts is not None:
            status = "OK"
            message = "Success!!!"
            for post in posts:
                post['_id'] = str(post['_id'])
                post['user_id'] = str(user_id)
        return jsonify({"status": status, "message": message, "posts": posts, "timestamp": datetime.datetime.now()})
    except PostErrors.PostError as e:
        return e.message

@post_blueprint.route('/search/', methods=['GET'])
@user_decorators.requires_admin_permissions(return_user=False)
def addTag():
    email = session['email']
    if email:
        return render_template('posts/add-tag.html')
    return render_template('users/login')

@post_blueprint.route('/insertTag/', methods=['POST'])
@user_decorators.requires_admin_permissions(return_user=False)
def insertTag():
    tag = request.form['tag']
    status = "No Good"
    message = "Error: tag not inserted"
    try:
        tag_added = Post.addTag(tag)
        if tag_added:
            status = "OK"
            message = "Success!!!"
        return jsonify(
            {"status": status, "message": message, "tag": tag, "timestamp": datetime.datetime.now()})
    except PostErrors.PostError as e:
        return e.message