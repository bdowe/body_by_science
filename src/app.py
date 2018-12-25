from flask import Flask, render_template, session, jsonify, request
import json

from src.database import Database
from src.lesscss import lesscss
from src.models.posts.post import Post
from src.utils import Utils

app = Flask(__name__) # '__main__'
app.config.from_object('src.config')
app.secret_key = 'Brian'
lesscss(app)

from src.models.users.views import user_blueprint
app.register_blueprint(user_blueprint, url_prefix="/users")

from src.models.posts.views import post_blueprint
app.register_blueprint(post_blueprint, url_prefix="/resources")

@app.before_first_request
def initialize_database():
    Database.initialize()

@app.context_processor
def isAdmin():
    email = ''
    if session:
        email = session['email']
    isAdmin = email in app.config['ADMINS']
    return dict(isAdmin=isAdmin)

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html')

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/submit-contact-form', methods=['POST'])
def submitContactForm():
    name = request.form['name']
    email = request.form['email']
    body = request.form['message']
    status = "Error"
    message = "Error: email not sent"
    try:
        email_sent = Utils.send_contact_message(name, email, body)
        if email_sent:
            status = "OK"
            message = "Success! You have been logged in!"
        else:
            session['email'] = None
        return jsonify({"status": status, "message": message, "email": email})
    except Exception as e:
        return message


app.add_template_global(jsonify, name='jsonify')
app.add_template_global(json.dumps, name='jsonDumps')
app.add_template_global(json.loads, name='jsonLoads')