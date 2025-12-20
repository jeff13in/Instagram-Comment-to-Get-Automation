# 3p99 - Instagram Comment-Bot Automation

![3P99 Logo.png](3P99.png)

Automate Instagram comment responses with intelligent keyword detection. Grow your engagement effortlessly with real-time auto-replies and direct messaging.

## 🚀 Features

- ✅ **Keyword Detection** - Automatically detect trigger words in comments
- ✅ **Auto-Reply** - Send customized replies to comments instantly
- ✅ **Direct Message Automation** - Follow up with users via DM
- ✅ **Multi-Post Monitoring** - Track comments across all recent posts
- ✅ **Real-Time Processing** - Webhook-based instant notifications
- ✅ **Duplicate Prevention** - Smart tracking ensures no spam
- ✅ **Professional Landing Page** - Beautiful UI for showcasing features
- ✅ **Email Collection** - Built-in subscriber management system

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Landing Page](#landing-page)
- [API Endpoints](#api-endpoints)
- [Deployment](#deployment)
- [Documentation](#documentation)
- [License](#license)

## ⚡ Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/3p99.git
cd 3p99
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env with your Instagram credentials
```

### 4. Run the Application

#### Option A: Landing Page + API (Recommended)
```bash
python app.py
```
Access landing page at: http://localhost:5003

#### Option B: Auto-Responder Only
```bash
python instagram_auto_responder.py
```

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- Instagram Business or Creator account
- Facebook Developer account
- Meta App with Instagram permissions

### System Requirements

```
Python >= 3.8
Flask >= 3.0.0
Flask-SQLAlchemy >= 3.1.1
SQLAlchemy >= 2.0.23
requests >= 2.31.0
python-dotenv >= 1.0.0
```

### Install from Requirements

```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

### 1. Create Meta App

1. Go to [developers.facebook.com](https://developers.facebook.com)
2. Create a new app
3. Add Instagram product
4. Configure OAuth redirect URIs
5. Add required permissions:
   - `instagram_business_basic`
   - `instagram_business_manage_comments`
   - `instagram_business_manage_messages`
   - `instagram_business_content_publish`

### 2. Get Access Token

Run the authentication helper:

```bash
python sample_app.py
```

Follow the prompts to obtain your long-lived access token (valid for 60 days).

### 3. Configure Environment Variables

Edit `.env` file:

```env
INSTAGRAM_ACCESS_TOKEN=your_long_lived_token
INSTAGRAM_APP_SECRET=your_app_secret
INSTAGRAM_ACCOUNT_ID=your_instagram_account_id
VERIFY_TOKEN=my_secret_webhook_token_123
DATABASE_URL=sqlite:///instagram_automation.db
```

### 4. Configure Keywords and Messages

Edit `jeffin_config.json`:

```json
{
  "app_id": "your_app_id",
  "app_secret": "your_app_secret",
  "access_token": "your_long_lived_token",
  "trigger_keywords": ["giveaway", "cyber", "books"],
  "comment_reply": "Thanks for your interest! 🎉",
  "dm_message": "Check your inbox for details!"
}
```

## 🎯 Usage

### Polling Mode (Testing)

Checks Instagram API every 60 seconds for new comments:

```python
from instagram_auto_responder import InstagramAutoResponder

bot = InstagramAutoResponder('jeffin_config.json')

# Run once (for testing)
bot.run_once()

# Continuous monitoring
bot.monitor_and_respond()
```

### Webhook Mode (Production)

Receives real-time events from Instagram:

```bash
python app.py
```

Configure webhook in Meta App settings:
- **Callback URL**: `https://yourdomain.com/webhook`
- **Verify Token**: Set in `.env`
- **Subscribe to**: comments, messages

## 🌐 Landing Page

The project includes a professional landing page with:

- Hero section with CTA
- Features showcase
- How it works guide
- Demo video section
- Use cases
- Pricing tiers
- FAQ section
- Email subscription form

### Pages Available

- **Home**: `/` - Landing page
- **Documentation**: `/docs` - Complete documentation
- **Privacy Policy**: `/privacy_policy` - Privacy policy
- **API**: `/api/subscribe` - Email subscription endpoint

### Customization

Edit the following files to customize your landing page:

- `index.html` - Structure and content
- `styles.css` - Styling and design
- `script.js` - Interactivity and animations

## 🔌 API Endpoints

### Email Subscription

**Endpoint**: `POST /api/subscribe`

**Request**:
```json
{
  "email": "user@example.com"
}
```

**Response**:
```json
{
  "success": true,
  "message": "Thanks for subscribing! We'll be in touch soon."
}
```

### Get Subscribers (Admin)

**Endpoint**: `GET /api/subscribers`

**Response**:
```json
{
  "success": true,
  "count": 42,
  "subscribers": [
    {
      "id": 1,
      "email": "user@example.com",
      "created_at": "2025-01-15T10:30:00",
      "source": "landing_page"
    }
  ]
}
```

### Webhook Endpoint

**Endpoint**: `GET/POST /webhook`

- **GET**: Webhook verification
- **POST**: Instagram event receiver

## 🚀 Deployment

### Deploy to Railway

1. Connect your GitHub repository to Railway
2. Add environment variables from `.env`
3. Railway will auto-deploy using `Procfile`

### Deploy to Heroku

```bash
heroku create your-app-name
heroku config:set INSTAGRAM_ACCESS_TOKEN=your_token
heroku config:set INSTAGRAM_APP_SECRET=your_app_secret
heroku config:set VERIFY_TOKEN=your_verify_token
```

### Environment Variables for Production

```env
INSTAGRAM_ACCESS_TOKEN=your_long_lived_token
INSTAGRAM_APP_SECRET=your_app_secret
VERIFY_TOKEN=your_webhook_verify_token
DATABASE_URL=postgresql://user:pass@host:5432/dbname
PORT=5000
HOST=0.0.0.0
```

## 📚 Documentation

Complete documentation is available at `/docs` when running the app, or view [docs.html](docs.html).

Topics covered:
- Installation & Setup
- Authentication (OAuth 2.0)
- Configuration
- API Reference
- Webhooks
- Rate Limits
- Deployment
- Troubleshooting

## 📁 Project Structure

```
3p99/
├── app.py                          # Flask web app + API
├── instagram_auto_responder.py     # Main bot logic
├── sample_app.py                   # OAuth helper
├── message.py                      # Message utilities
├── jeffin_config.json              # Bot configuration
├── .env.example                    # Environment template
├── requirements.txt                # Python dependencies
├── Procfile                        # Deployment config
├── index.html                      # Landing page
├── docs.html                       # Documentation page
├── styles.css                      # Styling
├── script.js                       # Frontend JS
├── privacy_policy.html             # Privacy policy
└── README.md                       # This file
```

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support:
- Check the [documentation](/docs)
- Review [Instagram API docs](https://developers.facebook.com/docs/instagram-api)
- Open an issue on GitHub

## ✨ Acknowledgments

- Built with [Instagram Graph API v21.0](https://developers.facebook.com/docs/instagram-api)
- Powered by Flask and SQLAlchemy
- UI inspired by modern SaaS landing pages

---

**Made with ❤️ for Instagram automation**

Instagram Graph API v21.0 | Flask 3.0 | Python 3.8+
