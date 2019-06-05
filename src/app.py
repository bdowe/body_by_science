from flask import Flask, render_template, session, jsonify, request
import json

from src.database import Database
from src.lesscss import lesscss
from src.utils import Utils

app = Flask(__name__) # '__main__'
app.config.from_object('src.config')
app.secret_key = 'Brian'
lesscss(app)

from src.models.users.views import user_blueprint
app.register_blueprint(user_blueprint, url_prefix="/users")

from src.models.posts.views import post_blueprint
app.register_blueprint(post_blueprint, url_prefix="/resources")

from src.models.email_subscriptions.views import email_subscription_blueprint
app.register_blueprint(email_subscription_blueprint, url_prefix="/subscriptions")

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
    css = [
        {'prefix': 'css/compiled/', 'name': 'home'},
        {'prefix': 'js/slick/', 'name': 'slick-theme'},
        {'prefix': 'js/slick/', 'name': 'slick'},
        {'prefix': 'css/HoverEffectIdeas/css/', 'name': 'set1'}
    ]
    return render_template('home.html', css=css)

@app.route('/contact', methods=['GET'])
def contact():
    css = [{'prefix': 'css/compiled/', 'name': 'contact'}]
    return render_template('contact.html', css=css)

@app.route('/about', methods=['GET'])
def about():
    css = [{'prefix': 'css/compiled/', 'name': 'about'}]
    return render_template('about.html', css=css)

@app.route('/submit-contact-form', methods=['POST'])
def submitContactForm():
    name = request.form['name']
    email = request.form['email']
    body = request.form['message']
    status = "Error"
    message = "There was a problem sending your message. Please try again later"
    try:
        email_sent = Utils.send_contact_message(name, email, body)
        if email_sent:
            status = "OK"
            message = "Success! Your message has been sent"
        return jsonify({"status": status, "message": message, "email": email})
    except Exception:
        return jsonify({"status": status, "message": message})


app.add_template_global(jsonify, name='jsonify')
app.add_template_global(len, name='len')
app.add_template_global(json.dumps, name='jsonDumps')
app.add_template_global(json.loads, name='jsonLoads')