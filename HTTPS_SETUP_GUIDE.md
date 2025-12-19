# HTTPS Setup Guide for Instagram Webhook Bot

Facebook **requires HTTPS** for webhooks. Here are several methods to enable HTTPS for your bot.

---

## Method 1: ngrok (Easiest - For Testing)

### What is ngrok?
ngrok creates a secure tunnel from a public HTTPS URL to your local server. Perfect for development and testing.

### Setup Steps:

#### 1. Install ngrok
```bash
# macOS (using Homebrew)
brew install ngrok

# Or download from https://ngrok.com/download
```

#### 2. Create a free account
- Go to https://ngrok.com/signup
- Get your auth token from dashboard

#### 3. Authenticate ngrok
```bash
ngrok config add-authtoken YOUR_AUTH_TOKEN
```

#### 4. Start your webhook bot
```bash
# Make sure it's running on port 5001 (as configured)
python instagram_webhook_bot.py
```

#### 5. Start ngrok tunnel
```bash
# In a new terminal
ngrok http 5001
```

#### 6. Copy the HTTPS URL
You'll see output like:
```
Forwarding  https://abc123def.ngrok-free.app -> http://localhost:5001
```

Copy the HTTPS URL (e.g., `https://abc123def.ngrok-free.app`)

#### 7. Configure Facebook Webhook
- Go to Facebook App Dashboard → Webhooks
- Callback URL: `https://abc123def.ngrok-free.app/webhook`
- Verify Token: `12345` (from your code)

### Pros & Cons:
✅ Super easy setup
✅ Instant HTTPS
✅ Great for testing
❌ URL changes every restart (free tier)
❌ Not suitable for production

### Pro Tip: Fixed Domain
Upgrade to ngrok Pro ($8/month) for a fixed domain that doesn't change.

---

## Method 2: Deploy to Render (Free HTTPS)

### What is Render?
Free cloud platform with automatic HTTPS and easy deployment.

### Setup Steps:

#### 1. Create a Render account
- Go to https://render.com/
- Sign up (free tier available)

#### 2. Create a new Web Service
- Click "New +" → "Web Service"
- Connect your GitHub repo (or deploy manually)

#### 3. Configure the service
```yaml
Name: instagram-webhook-bot
Environment: Python 3
Build Command: pip install -r requirements.txt
Start Command: gunicorn -w 4 -b 0.0.0.0:$PORT instagram_webhook_bot:app
```

#### 4. Add environment variables
```
ACCESS_TOKEN=your_token
INSTAGRAM_ACCOUNT_ID=your_id
VERIFY_TOKEN=12345
APP_SECRET=your_secret
```

#### 5. Deploy
- Click "Create Web Service"
- Render will provide an HTTPS URL automatically

#### 6. Use the URL in Facebook
Your webhook URL will be: `https://your-app.onrender.com/webhook`

### Pros & Cons:
✅ Free tier available
✅ Automatic HTTPS
✅ Fixed URL
✅ Production-ready
❌ Cold starts on free tier

---

## Method 3: Deploy to Heroku (Free HTTPS)

### Setup Steps:

#### 1. Install Heroku CLI
```bash
# macOS
brew install heroku/brew/heroku

# Or download from https://devcenter.heroku.com/articles/heroku-cli
```

#### 2. Create a Procfile
Create `/Users/jeffinsam/Desktop/3p99/Procfile`:
```
web: gunicorn instagram_webhook_bot:app
```

#### 3. Create runtime.txt
```
python-3.11.0
```

#### 4. Update your code to use environment variable for port
The bot needs to read `PORT` from environment. I'll help you fix this.

#### 5. Deploy
```bash
cd /Users/jeffinsam/Desktop/3p99

# Login to Heroku
heroku login

# Create app
heroku create instagram-webhook-bot

# Set environment variables
heroku config:set ACCESS_TOKEN=your_token
heroku config:set INSTAGRAM_ACCOUNT_ID=your_id
heroku config:set VERIFY_TOKEN=12345
heroku config:set APP_SECRET=your_secret

# Deploy
git init
git add .
git commit -m "Initial commit"
git push heroku main
```

#### 6. Your HTTPS URL
`https://instagram-webhook-bot.herokuapp.com/webhook`

### Pros & Cons:
✅ Free tier
✅ Automatic HTTPS
✅ Fixed URL
✅ Reliable
❌ Requires credit card (even for free tier)
❌ Sleep after 30 min inactivity (free tier)

---

## Method 4: Use Your Own Server with Let's Encrypt (Production)

### If you have a VPS (DigitalOcean, AWS, etc.)

#### 1. Install Certbot
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install certbot python3-certbot-nginx

# macOS
brew install certbot
```

#### 2. Get SSL Certificate
```bash
sudo certbot certonly --standalone -d yourdomain.com
```

#### 3. Install nginx
```bash
# Ubuntu
sudo apt install nginx

# macOS
brew install nginx
```

#### 4. Configure nginx as reverse proxy
Create `/etc/nginx/sites-available/webhook`:
```nginx
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### 5. Enable and restart nginx
```bash
sudo ln -s /etc/nginx/sites-available/webhook /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 6. Start your bot
```bash
gunicorn -w 4 -b 127.0.0.1:5001 instagram_webhook_bot:app
```

### Pros & Cons:
✅ Full control
✅ Production-ready
✅ Free SSL certificates
✅ Best performance
❌ Requires server management
❌ More complex setup

---

## Method 5: Railway (Easiest Production Deploy)

### Setup Steps:

#### 1. Go to https://railway.app
- Sign up with GitHub

#### 2. Click "New Project"
- Select "Deploy from GitHub repo"
- Or use "Empty Project" and upload files

#### 3. Railway auto-detects Python
No configuration needed! It will:
- Install from requirements.txt
- Auto-assign HTTPS URL
- Provide environment variables section

#### 4. Add environment variables
Click on your service → Variables:
```
ACCESS_TOKEN=your_token
INSTAGRAM_ACCOUNT_ID=your_id
VERIFY_TOKEN=12345
APP_SECRET=your_secret
```

#### 5. Deploy
- Railway auto-deploys on every push
- Provides HTTPS URL: `https://your-app.up.railway.app`

### Pros & Cons:
✅ Super easy
✅ Automatic HTTPS
✅ Fixed URL
✅ Free $5 credit/month
✅ No sleep time
✅ Production-ready
✅ Best option for production

---

## Recommended Approach

### For Testing (Today):
**Use ngrok** - 5 minute setup, instant HTTPS

### For Production (Long-term):
**Use Railway or Render** - Easy deployment, free tier, reliable

---

## Quick Start with ngrok (Recommended for Testing)

```bash
# Terminal 1: Start your bot
cd /Users/jeffinsam/Desktop/3p99
python instagram_webhook_bot.py

# Terminal 2: Start ngrok
ngrok http 5001
```

Copy the HTTPS URL from ngrok output and use it in Facebook:
- Webhook URL: `https://YOUR-NGROK-URL.ngrok-free.app/webhook`
- Verify Token: `12345`

Done! ✅

---

## Troubleshooting

### ngrok "Too many connections"
- Free tier has connection limits
- Upgrade to paid plan or use cloud deployment

### SSL Certificate Expired
- Let's Encrypt certs expire every 90 days
- Set up auto-renewal: `sudo certbot renew --dry-run`

### Webhook verification fails
- Make sure you're using HTTPS (not HTTP)
- Check verify token matches exactly
- Check that server is publicly accessible

---

## Testing Your HTTPS Setup

```bash
# Test that webhook endpoint is accessible
curl https://YOUR-URL/webhook

# Should return health check response
{"status": "active", "message": "Instagram Webhook Bot is running!", ...}

# Test webhook verification (simulate Facebook)
curl "https://YOUR-URL/webhook?hub.mode=subscribe&hub.verify_token=12345&hub.challenge=test"

# Should return: test
```

---

## Next Steps

1. Choose your HTTPS method (ngrok for quick test)
2. Start your bot
3. Get HTTPS URL
4. Configure Facebook webhook with HTTPS URL
5. Test by commenting on your Instagram post!

Need help? Check the server logs for detailed error messages.
