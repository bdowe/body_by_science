from flask import Blueprint, request, session, render_template, jsonify, app

from src.models.email_subscriptions.email_subscription import EmailSubscription

email_subscription_blueprint = Blueprint('email_subscriptions', __name__)

@email_subscription_blueprint.route('/subscribe/', methods=['POST'])
def subscribe():
    email = request.form['email']
    status = "No Good"
    message = "There was an error adding your email to our subscription list."
    try:
        subscribed = EmailSubscription.new(email)
        if subscribed:
            status = "OK"
            message = "Success! Your email has been added to our subscription list!"
        return jsonify({"status": status, "message": message, "email": email})
    except Exception as e:
        return jsonify({"status": status, "message": str(e)})
