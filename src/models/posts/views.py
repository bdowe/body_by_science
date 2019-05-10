import src.models.posts.errors as PostErrors
from flask import Blueprint, request, render_template, jsonify, url_for
from src.models.posts.post import Post
import src.models.users.decorators as user_decorators
from werkzeug.utils import redirect
import datetime

post_blueprint = Blueprint('posts', __name__)


@post_blueprint.route('/', methods=['GET'])
def all():
    posts = list(reversed(list(Post.getAll())))
    tags = list(Post.getAllTags())
    for i in range(len(tags)):
        tags[i] = tags[i]['tag']
    return render_template('resources.html', posts=posts, tags=tags)

@post_blueprint.route('/<id>', methods=['GET'])
def view(id):
    post = Post.getOneById(id)
    if post:
        return render_template('resource.html', post=post)

@post_blueprint.route('/new/', methods=['GET', 'POST'])
@user_decorators.requires_admin_permissions(return_user=False)
def new():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        body = request.form['body'].strip()
        tag = request.form['tag']
        videoURL = request.form['videoURL']
        status = "No Good"
        message = "Error: item not inserted"

        if not title or not description or not tag or (not body and not videoURL):
            return {"status": status, "message": message}

        try:
            post_added = Post.new(title, description, body, tag, videoURL)
            if post_added:
                status = "OK"
                message = "Success!!!"
            return jsonify(
                {"status": status, "message": message, "body": body, "tag": tag, "videoURL": videoURL, "timestamp": datetime.datetime.now()})
        except PostErrors.PostError as e:
            return e.message
    else:
        tags = list(Post.getAllTags())
        for i in range(len(tags)):
            tags[i] = tags[i]['tag']
        return render_template('posts/new.html', tags=tags)


@post_blueprint.route('/edit/<id>', methods=['GET', 'POST'])
@user_decorators.requires_admin_permissions(return_user=False)
def update(id):
    post = Post.getOneById(id)
    post['body'] = ','.join(post['body'])
    tags = list(Post.getAllTags())
    for i in range(len(tags)):
        tags[i] = tags[i]['tag']
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        body = request.form['body']
        tag = request.form['tag']
        videoURL = request.form['videoURL']
        status = "No Good"
        message = "Error: item not inserted"

        if not title or not description or not tag or (not body and not videoURL):
            return {"status": status, "message": message}

        try:
            post_updated = Post.update(id, title, description, body, tag, videoURL)
            if post_updated:
                status = "OK"
                message = "Success!!!"
            return jsonify(
                {"status": status, "message": message, "body": body, "tag": tag, "videoURL": videoURL, "timestamp": datetime.datetime.now()})
        except PostErrors.PostError as e:
            return e.message
    else:
        return render_template('posts/edit.html', post=post, tags=tags)

@post_blueprint.route('/remove/<id>', methods=['GET'])
@user_decorators.requires_admin_permissions(return_user=False)
def delete(id):
    status = "No Good"
    message = "Error: could not delete post"
    try:
        post_deleted = Post.delete(id)
        if post_deleted:
            return redirect(url_for('posts.all'))
        return jsonify({"status": status, "message": message, "timestamp": datetime.datetime.now()})
    except PostErrors.PostError as e:
        return e.message



@post_blueprint.route('/search/', methods=['POST'])
def search():
    input_tag = request.form['input-tag'] if 'input-tag' in request.form else None
    select_tag = request.form['select-tag'] if 'select-tag' in request.form else None
    tag = None
    status = "No Good"
    message = "We're having trouble loading our resources right now! Please try again later."
    try:
        if input_tag is not None:
            tag = input_tag
        elif select_tag is not None:
            tag = select_tag
        if tag is not None and tag != "all":
            posts = list(reversed(list(Post.getManyByTag(tag))))
        else:
            posts = list(reversed(list(Post.getAll())))

        if posts is not None:
            status = "OK"
            message = "Success!!!"
            for post in posts:
                post['_id'] = str(post['_id'])
                post['user_id'] = str(post['user_id'])
        return jsonify({"status": status, "message": message, "posts": posts, "timestamp": datetime.datetime.now()})
    except Exception:
        return jsonify({"status": status, "message": message})


@post_blueprint.route('/tag-editor/', methods=['GET'])
@user_decorators.requires_admin_permissions(return_user=False)
def tagEditor():
    tags = list(Post.getAllTags())
    for i in range(len(tags)):
        tags[i] = tags[i]['tag']
    return render_template('posts/tag-editor.html', tags=tags)

@post_blueprint.route('/add-tag/', methods=['GET', 'POST'])
@user_decorators.requires_admin_permissions(return_user=False)
def addTag():
    if request.method == 'POST':
        tag = request.form['tag']
        status = "No Good"
        message = "Error: tag not inserted"

        if not tag:
            return {"status": status, "message": message}

        try:
            tag_added = Post.addTag(tag)
            if tag_added:
                status = "OK"
                message = "Success!!!"
            return jsonify(
                {"status": status, "message": message, "tag": tag, "timestamp": datetime.datetime.now()})
        except PostErrors.PostError as e:
            return e.message
    else:
        return render_template('posts/add-tag.html')

@post_blueprint.route('/remove-tag/', methods=['POST'])
@user_decorators.requires_admin_permissions(return_user=False)
def deleteTag():
    status = "No Good"
    message = "Error: could not delete post"
    tag = request.form['tag']
    try:
        tag_deleted = Post.deleteTag(tag)
        if tag_deleted:
            status = 'OK'
            message = 'Sucess!!!'
        return jsonify({"status": status, "message": message, "timestamp": datetime.datetime.now()})
    except PostErrors.PostError as e:
        return e.message
