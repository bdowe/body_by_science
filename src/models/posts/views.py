import math

import src.models.posts.errors as PostErrors
from flask import Blueprint, request, render_template, jsonify, url_for
from src.models.posts.post import Post
import src.models.users.decorators as user_decorators
from werkzeug.utils import redirect
import datetime
import src.models.posts.constants as POST_CONSTANTS

post_blueprint = Blueprint('posts', __name__)


@post_blueprint.route('/', methods=['GET'], defaults={'tag': None})
@post_blueprint.route('/<tag>')
def all(tag):
    if tag is not None:
        posts = list(reversed(list(Post.getManyByTag(tag))))
    else:
        tag = 'all'
        posts = list(reversed(list(Post.getAll())))
    num_pages = math.ceil(len(posts) / POST_CONSTANTS.MAX_RESOURCES_PER_PAGE)
    max_pages_shown = POST_CONSTANTS.MAX_PAGES_SHOWN if num_pages >= POST_CONSTANTS.MAX_PAGES_SHOWN else num_pages
    page = 1
    if 'page' in request.args.keys():
        if int(request.args['page']) <= num_pages:
            page = int(request.args['page'])
        else:
            page = num_pages
    first_index = (page - 1) * POST_CONSTANTS.MAX_RESOURCES_PER_PAGE
    last_index = page * POST_CONSTANTS.MAX_RESOURCES_PER_PAGE
    posts = posts[first_index:last_index]
    tags = list(Post.getAllTags())
    for i in range(len(tags)):
        tags[i] = tags[i]['tag'].capitalize()
    css = [{'prefix': 'css/compiled/', 'name': 'resources'}]
    return render_template('resources.html', posts=posts, tags=tags, css=css, selectedTag=tag, page=page, max_per_page=POST_CONSTANTS.MAX_RESOURCES_PER_PAGE, num_pages=num_pages, max_pages_shown=max_pages_shown)

@post_blueprint.route('/view/<id>', methods=['GET'])
def view(id):
    post = Post.getOneById(id)
    if post:
        css = [{'prefix': 'css/compiled/', 'name': 'resource'}]
        return render_template('resource.html', post=post, css=css)

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



@post_blueprint.route('/search/', methods=['GET'])
def search():
    input_tag = request.args['input-tag'] if 'input-tag' in request.args else None
    select_tag = request.args['select-tag'] if 'select-tag' in request.args else None
    tag = None
    status = "No Good"
    message = "We're having trouble loading our resources right now! Please try again later."
    try:
        if input_tag is not None:
            tag = input_tag
        elif select_tag is not None:
            tag = select_tag
        if tag is not None and tag != "all":
            tag = tag.lower()
            posts = list(reversed(list(Post.getManyByTag(tag))))
        else:
            posts = list(reversed(list(Post.getAll())))

        num_pages = math.ceil(len(posts) / POST_CONSTANTS.MAX_RESOURCES_PER_PAGE)
        max_pages_shown = POST_CONSTANTS.MAX_PAGES_SHOWN if num_pages >= POST_CONSTANTS.MAX_PAGES_SHOWN else num_pages
        posts = posts[:POST_CONSTANTS.MAX_RESOURCES_PER_PAGE]

        if posts is not None:
            status = "OK"
            message = "Success!!!"
            for post in posts:
                post['_id'] = str(post['_id'])
                post['user_id'] = str(post['user_id'])
        return jsonify({"status": status, "message": message, "posts": posts, "num_pages": num_pages, "max_pages_shown": max_pages_shown})
    except Exception:
        return jsonify({"status": status, "message": message})

@post_blueprint.route('/paginate/', methods=['GET'])
def paginate():
    page = int(request.args['page'])
    tag = request.args['tag']
    status = 'No good'
    message = "We're having trouble loading our resources right now! Please try again later."
    try:
        if tag is not None and tag != "all":
            tag = tag.lower()
            posts = list(reversed(list(Post.getManyByTag(tag))))
        else:
            posts = list(reversed(list(Post.getAll())))

        first_index = (page - 1) * POST_CONSTANTS.MAX_RESOURCES_PER_PAGE
        last_index = page * POST_CONSTANTS.MAX_RESOURCES_PER_PAGE
        posts = posts[first_index:last_index]
        if posts is not None:
            status = "OK"
            message = "Success!!!"
            for post in posts:
                post['_id'] = str(post['_id'])
                post['user_id'] = str(post['user_id'])
        return jsonify({"status": status, "message": message, "posts": posts, "page": page})
    except Exception as e:
        if len(str(e)) != 0:
            message = str(e)
        return jsonify({"status": status, "message": message})



@post_blueprint.route('/tag-editor/', methods=['GET'])
@user_decorators.requires_admin_permissions(return_user=False)
def tagEditor():
    tags = list(Post.getAllTags())
    for i in range(len(tags)):
        tags[i] = tags[i]['tag']
    css = [{'prefix': 'css/compiled/', 'name': 'tag-editor'}]
    return render_template('posts/tag-editor.html', tags=tags, css=css)

@post_blueprint.route('/add-tag/', methods=['GET', 'POST'])
@user_decorators.requires_admin_permissions(return_user=False)
def addTag():
    if request.method == 'POST':
        tag = request.form['tag'].lower()
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
