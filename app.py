import json
import requests
import os
import pathlib
import secrets
import hmac
import hashlib
from datetime import datetime
from flask import Flask, request, send_file, jsonify, render_template_string, session, abort, redirect
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests

load_dotenv()

app = Flask(__name__)

# Secret key for session management — must be set via SECRET_KEY env var in production
_secret_key = os.getenv('SECRET_KEY')
if not _secret_key:
    _secret_key = secrets.token_hex(32)
    print("WARNING: SECRET_KEY env var not set. Using a random key — sessions will not persist across restarts. Set SECRET_KEY in production.")
app.secret_key = _secret_key

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///instagram_automation.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Google OAuth Configuration
# Allow HTTP (non-HTTPS) only when explicitly opted in for local development
if os.getenv('OAUTHLIB_INSECURE_TRANSPORT') == '1':
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
if not GOOGLE_CLIENT_ID:
    print("WARNING: GOOGLE_CLIENT_ID env var not set. Google OAuth token verification will fail.")
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

# Check if client_secret.json exists before creating flow
if os.path.exists(client_secrets_file):
    flow = Flow.from_client_secrets_file(
        client_secrets_file=client_secrets_file,
        scopes=["https://www.googleapis.com/auth/userinfo.profile",
                "https://www.googleapis.com/auth/userinfo.email",
                "openid"],
        redirect_uri=os.getenv('GOOGLE_REDIRECT_URI', "http://127.0.0.1:5003/callback")
    )
else:
    flow = None
    print("Warning: client_secret.json not found. Google OAuth will not work.")

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

def login_is_required(function):
    """Decorator to protect routes that require authentication"""
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function(*args, **kwargs)
    wrapper.__name__ = function.__name__
    return wrapper


@app.route("/")
def home():
    return send_file('index.html')


@app.route("/styles.css")
def styles():
    return send_file('styles.css', mimetype='text/css')


@app.route("/script.js")
def script():
    return send_file('script.js', mimetype='application/javascript')


@app.route("/script_auth.js")
def script_auth():
    return send_file('script_auth.js', mimetype='application/javascript')


@app.route("/login")
def login():
    """Initiate Google OAuth login flow"""
    if flow is None:
        return jsonify({"success": False, "message": "Google OAuth not configured"}), 500

    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@app.route("/callback")
def callback():
    """Handle Google OAuth callback"""
    if flow is None:
        return jsonify({"success": False, "message": "Google OAuth not configured"}), 500

    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    # Store user information in session
    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    session["email"] = id_info.get("email")
    session["picture"] = id_info.get("picture")

    # Optionally, save user to database
    # You can create a User model and save the user here

    return redirect("/")


@app.route("/logout")
def logout():
    """Clear user session and logout"""
    session.clear()
    return redirect("/")


@app.route("/api/user", methods=["GET"])
def get_user():
    """Get current logged-in user information"""
    if "google_id" in session:
        return jsonify({
            "success": True,
            "logged_in": True,
            "user": {
                "google_id": session.get("google_id"),
                "name": session.get("name"),
                "email": session.get("email"),
                "picture": session.get("picture")
            }
        }), 200
    else:
        return jsonify({
            "success": True,
            "logged_in": False
        }), 200

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
@login_is_required
def get_subscribers():
    """Get all email subscribers (admin endpoint — requires authentication)"""
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
        return jsonify({"success": False, "message": "An internal error occurred."}), 500


@app.route("/api/test-dm", methods=["POST"])
def test_dm():
    """Test DM bot functionality - scan posts and send DMs for trigger keywords"""
    try:
        # Check if user is authenticated
        if "google_id" not in session:
            return jsonify({
                "success": False,
                "message": "User not authenticated. Please sign in with Google first."
            }), 401

        data = request.get_json()
        keywords = data.get('keywords', ['cyber', 'books', 'project'])

        # Log the test request
        print(f"\n{'='*60}")
        print(f"DM Test started by: {session.get('name')} ({session.get('email')})")
        print(f"Trigger keywords: {keywords}")
        print(f"{'='*60}\n")

        # Import the InstagramAutoResponder
        try:
            from instagram_auto_responder import InstagramAutoResponder
        except ImportError as e:
            return jsonify({
                "success": False,
                "message": "Instagram auto-responder module not found. Please check instagram_auto_responder.py exists."
            }), 500

        # Initialize the auto responder
        try:
            responder = InstagramAutoResponder('jeffin_config.json')

            # Update trigger keywords to match the requested ones
            responder.trigger_keywords = keywords

            print(f"Instagram Account ID: {responder.ig_account_id}")
            print(f"Scanning recent posts for comments with keywords: {keywords}\n")

        except FileNotFoundError:
            return jsonify({
                "success": False,
                "message": "Configuration file 'jeffin_config.json' not found. Please ensure your Instagram credentials are configured."
            }), 500
        except Exception as e:
            return jsonify({
                "success": False,
                "message": f"Failed to initialize Instagram bot: {str(e)}"
            }), 500

        # Get recent media posts
        media_posts = responder.get_recent_media(limit=5)

        if not media_posts:
            return jsonify({
                "success": False,
                "message": "No Instagram posts found. Please ensure your account has posts."
            }), 404

        # Track results
        total_comments = 0
        matching_comments = 0
        replies_sent = 0
        dms_sent = 0
        processed_comments_list = []

        # Process each post
        for media in media_posts:
            media_id = media['id']
            media_url = media.get('permalink', 'N/A')

            # Get comments for this post
            comments = responder.get_media_comments(media_id)
            total_comments += len(comments)

            # Process each comment
            for comment in comments:
                comment_id = comment['id']
                comment_text = comment['text']
                username = comment.get('username', 'Unknown')
                commenter_id = comment.get('from', {}).get('id')

                # Check if comment contains trigger keywords
                if responder.check_comment_for_keywords(comment_text):
                    matching_comments += 1

                    print(f"✓ Match found!")
                    print(f"  Post: {media_url}")
                    print(f"  @{username}: {comment_text}")

                    # Skip if already processed
                    if comment_id in responder.processed_comments:
                        print(f"  Already processed - skipping")
                        continue

                    # Reply to comment
                    reply_success = responder.reply_to_comment(comment_id)
                    if reply_success:
                        replies_sent += 1

                    # Send DM
                    dm_success = False
                    if commenter_id:
                        dm_success = responder.send_direct_message(commenter_id)
                        if dm_success:
                            dms_sent += 1

                    # Mark as processed
                    responder.processed_comments.add(comment_id)

                    # Track this comment
                    processed_comments_list.append({
                        'username': username,
                        'comment': comment_text[:50] + ('...' if len(comment_text) > 50 else ''),
                        'reply_sent': reply_success,
                        'dm_sent': dm_success
                    })

                    print(f"  Reply: {'✓' if reply_success else '✗'} | DM: {'✓' if dm_success else '✗'}\n")

        # Prepare response
        print(f"{'='*60}")
        print(f"Scan complete!")
        print(f"Total comments scanned: {total_comments}")
        print(f"Matching keywords: {matching_comments}")
        print(f"Replies sent: {replies_sent}")
        print(f"DMs sent: {dms_sent}")
        print(f"{'='*60}\n")

        return jsonify({
            "success": True,
            "message": f"Scan complete! Found {matching_comments} comments with trigger keywords.",
            "stats": {
                "total_posts_scanned": len(media_posts),
                "total_comments": total_comments,
                "matching_comments": matching_comments,
                "replies_sent": replies_sent,
                "dms_sent": dms_sent
            },
            "processed_comments": processed_comments_list,
            "config": {
                "keywords": keywords,
                "status": "active"
            },
            "user": {
                "name": session.get("name"),
                "email": session.get("email")
            }
        }), 200

    except Exception as e:
        print(f"Error in DM test: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "success": False,
            "message": "An internal error occurred. Please check server logs."
        }), 500


def _verify_instagram_signature(raw_body: bytes, signature_header: str) -> bool:
    """Verify the Instagram webhook X-Hub-Signature-256 header using HMAC-SHA256."""
    if not signature_header or not signature_header.startswith('sha256='):
        return False
    received_sig = signature_header[len('sha256='):]
    secret = os.getenv('INSTAGRAM_APP_SECRET', config.get('app_secret', ''))
    expected_sig = hmac.new(
        secret.encode('utf-8'),
        raw_body,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected_sig, received_sig)


@app.route("/webhook", methods=["GET","POST"])
def webhook():
    """Instagram webhook endpoint for real-time events"""
    if request.method == "POST":
        try:
            raw_body = request.get_data()
            sig_header = request.headers.get('X-Hub-Signature-256', '')
            if not _verify_instagram_signature(raw_body, sig_header):
                print("Webhook signature verification failed")
                return jsonify({"success": False}), 403

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

        verify_token = os.getenv('VERIFY_TOKEN')
        if not verify_token:
            print("ERROR: VERIFY_TOKEN env var not set. Webhook verification will fail.")
            return "Webhook not configured", 500

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
    debug_mode = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(port=5003, debug=debug_mode)