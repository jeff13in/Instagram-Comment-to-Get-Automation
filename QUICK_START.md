

# Quick Start Guide - Instagram Webhook Bot with HTTPS

Get your Instagram webhook bot running with HTTPS in under 5 minutes!

---

## Prerequisites

- ✅ Python 3.8+
- ✅ Instagram Business/Creator Account
- ✅ Facebook Developer Account
- ✅ Facebook App with Instagram API access

---

## Step 1: Install ngrok (2 minutes)

### macOS:
```bash
brew install ngrok
```

### Other platforms:
Download from https://ngrok.com/download

### Authenticate ngrok:
1. Sign up at https://ngrok.com/signup
2. Get your auth token from dashboard
3. Run:
```bash
ngrok config add-authtoken YOUR_AUTH_TOKEN
```

---

## Step 2: Start the Bot with HTTPS (30 seconds)

### Option A: Automatic (Recommended)
```bash
cd /Users/jeffinsam/Desktop/3p99
./start_with_ngrok.sh
```

This automatically:
- Starts the webhook server
- Starts ngrok tunnel
- Provides HTTPS URL

### Option B: Manual
```bash
# Terminal 1: Start the bot
python instagram_webhook_bot.py

# Terminal 2: Start ngrok
ngrok http 5001
```

---

## Step 3: Copy Your HTTPS URL

From ngrok output, copy the HTTPS URL:
```
Forwarding  https://abc123def.ngrok-free.app -> http://localhost:5001
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
              Copy this URL!
```

---

## Step 4: Configure Facebook Webhook (2 minutes)

### 1. Go to Facebook App Dashboard
https://developers.facebook.com/apps/

### 2. Select your app → Products → Webhooks

### 3. Subscribe to Instagram
- Click **Configure** next to Instagram
- Click **Add Callback URL**

### 4. Enter webhook details:
```
Callback URL: https://YOUR-NGROK-URL.ngrok-free.app/webhook
Verify Token: 12345
```
(Replace YOUR-NGROK-URL with your actual ngrok URL)

### 5. Click "Verify and Save"
You should see ✅ "Success!" if verification works

### 6. Subscribe to fields:
Check these boxes:
- ✅ `messages` (for DMs)
- ✅ `comments` (for comments)

### 7. Click Save

---

## Step 5: Test It! (1 minute)

### Test Comments:
1. Go to your Instagram account
2. Make a comment on one of your posts
3. Say "How much does this cost?"
4. Watch the bot auto-reply! ✨

### Test DMs:
1. Send a DM to your Instagram account (from another account)
2. Say "Hello"
3. Watch the bot auto-reply! ✨

### Check Server Logs:
You should see in your terminal:
```
📬 Webhook Received!
📝 New Comment Received!
✅ Replied about pricing
```

---

## Troubleshooting

### "Callback verification failed"
- Make sure verify token is `12345` (check line 14 in instagram_webhook_bot.py)
- Make sure you copied the HTTPS URL correctly (not HTTP)
- Check that bot is running

### "Invalid signature"
- Make sure APP_SECRET is correct (line 15 in instagram_webhook_bot.py)
- Copy from Facebook App Dashboard → Settings → Basic

### Bot not auto-replying
- Check server logs for errors
- Make sure you subscribed to webhook fields
- Verify access token has correct permissions

### ngrok URL not working
- Make sure you're using HTTPS (not HTTP)
- Check that ngrok is running
- Try restarting ngrok

---

## What Happens Next?

Your bot is now:
✅ Receiving real-time webhook notifications
✅ Auto-replying to comments based on keywords
✅ Auto-replying to DMs based on keywords
✅ Using HTTPS (required by Facebook)

### When you stop ngrok:
- The URL will change next time you start it
- You'll need to update the webhook URL in Facebook
- For a permanent solution, see deployment options below

---

## Production Deployment (Optional)

For a permanent HTTPS URL that doesn't change:

### Recommended: Railway (Free tier)
1. Go to https://railway.app
2. Sign up with GitHub
3. Deploy your bot (see HTTPS_SETUP_GUIDE.md)
4. Get permanent HTTPS URL
5. Update Facebook webhook with Railway URL

### Other options:
- Render (free tier)
- Heroku (requires credit card)
- Your own server with SSL

See **HTTPS_SETUP_GUIDE.md** for detailed instructions.

---

## Current Auto-Reply Rules

### Comments:
| Keyword | Reply |
|---------|-------|
| "price", "cost", "how much" | Pricing info |
| "available", "in stock", "buy" | Availability info |
| "ship", "delivery", "shipping" | Shipping info |
| "love", "amazing", "great" | Thank you message |
| "?" (questions) | General help |
| Spam keywords | Auto-hide comment |

### DMs:
| Keyword | Reply |
|---------|-------|
| "hi", "hello", "hey" | Greeting |
| "price", "cost" | Pricing info |
| "available", "buy" | Availability info |
| "ship", "delivery" | Shipping info |
| "thanks", "thank you" | You're welcome |
| "?" (questions) | General help |

---

## Customize Auto-Replies

Edit `instagram_webhook_bot.py`:
- Line 113-137: Comment auto-reply rules
- Line 188-220: DM auto-reply rules

Add your own keywords and custom responses!

---

## Need Help?

1. Check server logs (terminal output)
2. Read WEBHOOK_SETUP_GUIDE.md for detailed setup
3. Read HTTPS_SETUP_GUIDE.md for HTTPS options
4. Check Facebook webhook logs in App Dashboard

---

## Summary of Your Setup

✅ **Webhook Server**: Running on port 5001
✅ **HTTPS Tunnel**: ngrok providing public HTTPS URL
✅ **Facebook Webhook**: Configured to send events to your bot
✅ **Auto-Replies**: Active for comments and DMs

**Your webhook is live!** 🎉

Every time someone comments or DMs, you'll get instant notification and auto-reply!
