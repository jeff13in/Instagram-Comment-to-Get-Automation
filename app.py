import json
import requests
import os
from datetime import datetime
from flask import Flask, request, send_file, jsonify, render_template_string
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///instagram_automation.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Models
class EmailSubscriber(db.Model):
    __tablename__ = 'email_subscribers'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    source = db.Column(db.String(50), default='landing_page')

    def __repr__(self):
        return f'<EmailSubscriber {self.email}>'

# Create tables
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return send_file('index.html')

@app.route("/privacy_policy")
def privacy_policy():
    return send_file('privacy_policy.html')

@app.route("/docs")
def docs():
    return send_file('docs.html')

@app.route("/api/subscribe", methods=["POST"])
def subscribe():
    """Handle email subscription from landing page"""
    try:
        data = request.get_json()
        email = data.get('email', '').strip().lower()

        if not email:
            return jsonify({"success": False, "message": "Email is required"}), 400

        # Basic email validation
        if '@' not in email or '.' not in email.split('@')[1]:
            return jsonify({"success": False, "message": "Invalid email format"}), 400

        # Check if email already exists
        existing = EmailSubscriber.query.filter_by(email=email).first()
        if existing:
            return jsonify({"success": True, "message": "You're already subscribed!"}), 200

        # Create new subscriber
        subscriber = EmailSubscriber(email=email)
        db.session.add(subscriber)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Thanks for subscribing! We'll be in touch soon."
        }), 201

    except Exception as e:
        print(f"Error subscribing email: {str(e)}")
        return jsonify({"success": False, "message": "An error occurred. Please try again."}), 500


@app.route("/api/subscribers", methods=["GET"])
def get_subscribers():
    """Get all email subscribers (admin endpoint)"""
    try:
        subscribers = EmailSubscriber.query.order_by(EmailSubscriber.created_at.desc()).all()
        return jsonify({
            "success": True,
            "count": len(subscribers),
            "subscribers": [{
                "id": sub.id,
                "email": sub.email,
                "created_at": sub.created_at.isoformat(),
                "source": sub.source
            } for sub in subscribers]
        }), 200
    except Exception as e:
        print(f"Error fetching subscribers: {str(e)}")
        return jsonify({"success": False, "message": "An error occurred"}), 500


@app.route("/webhook", methods=["GET","POST"])
def webhook():
    """Instagram webhook endpoint for real-time events"""
    if request.method == "POST":
        try:
            payload = request.get_json()
            print("Webhook received:")
            print(json.dumps(payload, indent=4))

            # TODO: Process webhook events and trigger auto-responder
            # For now, just log the events

            return jsonify({"success": True}), 200
        except Exception as e:
            print(f"Error processing webhook: {str(e)}")
            return jsonify({"success": False}), 500

    if request.method == "GET":
        # Webhook verification
        hub_mode = request.args.get("hub.mode")
        hub_challenge = request.args.get("hub.challenge")
        hub_verify_token = request.args.get("hub.verify_token")

        verify_token = os.getenv('VERIFY_TOKEN', 'my_secret_webhook_token_123')

        if hub_mode == "subscribe" and hub_verify_token == verify_token:
            print("Webhook verified successfully!")
            return hub_challenge
        else:
            return "Verification failed", 403



with open('jeffin_config.json', 'r') as file:
    config = json.load(file)

app_id = config["app_id"]
app_secret = config["app_secret"]
redirect_uri = "https://interfenestral-king-unmined.ngrok-free.dev/"


url = "https://www.instagram.com/oauth/authorize?"
url = url + f"client_id={int(app_id)}"
url = url + "&" + f"redirect_uri={redirect_uri}"
url = url + "&" + f"response_type=code"
url = url + "&" + f"scope={('instagram_business_basic, instagram_business_content_publish, instagram_business_manage_messages, instagram_business_manage_comments').replace(' ', '')}"
url


if __name__ == "__main__":
    app.run(port=5003, debug=True)