# Quick Start Guide - Instagram Auto Responder

## What This Does

Automatically monitors your Instagram posts and:
1. Detects comments with keywords like "cyber", "giveaway", "books"
2. Replies to those comments with a custom message
3. Sends a direct message to the commenter

## Setup (5 minutes)

### Step 1: Install Dependencies

```bash
pip install requests
```

### Step 2: Verify Your Config File

Make sure your `jeffin_config.json` has these fields:

```json
{
  "app_id": "YOUR_APP_ID",
  "app_secret": "YOUR_APP_SECRET",
  "access_token": "YOUR_ACCESS_TOKEN"
}
```

### Step 3: Test the Bot

Run the test script to verify everything works:

```bash
python test_instagram_bot.py
```

This will:
- Test your API connection
- Show your recent posts
- Display comments on those posts
- Identify any comments with trigger keywords
- Optionally let you test replying and sending DMs

### Step 4: Run the Bot

Once tests pass, run the main script:

```bash
python instagram_auto_responder.py
```

By default, this runs a **single check**. It will:
- Check your last 5 posts
- Find comments with keywords
- Reply and send DMs to matching comments

## Continuous Monitoring

To keep the bot running and check every 60 seconds:

1. Open `instagram_auto_responder.py`
2. Find the `main()` function at the bottom
3. Change it to:

```python
def main():
    responder = InstagramAutoResponder('jeffin_config.json')
    # Run continuous monitoring (checks every 60 seconds)
    responder.monitor_and_respond(check_interval=60, media_limit=5)
```

4. Run again:
```bash
python instagram_auto_responder.py
```

Press `Ctrl+C` to stop.

## Customization

### Change Keywords

Edit line ~24 in `instagram_auto_responder.py`:

```python
self.trigger_keywords = ["cyber", "giveaway", "books"]
```

Change to your own keywords:

```python
self.trigger_keywords = ["win", "contest", "free", "promo"]
```

### Change Messages

Edit lines ~29-32 in `instagram_auto_responder.py`:

```python
# Comment reply message
self.comment_reply_message = "Thank you! Follow me for updates!"

# Direct message
self.dm_message = "Hi! Thanks for commenting. Check out my latest posts!"
```

## Troubleshooting

### "Access token has expired"
- Your token needs to be refreshed
- Use your existing auth flow in `sample_app.py` to get a new token
- Update `jeffin_config.json` with the new token

### "Insufficient permissions"
Your app needs these permissions:
- `instagram_business_manage_comments` - to reply to comments
- `instagram_business_manage_messages` - to send DMs
- `instagram_business_basic` - to access account info

Re-authorize with these scopes (check line 20 in `sample_app.py`).

### No comments detected
- Make sure you have recent posts
- Test by commenting on your own post with keywords like "cyber" or "giveaway"
- Check the keywords match (case doesn't matter)

### Reply works but DM fails
- User must have DMs enabled
- User needs to follow you OR have accepted DM requests
- Check you have `instagram_business_manage_messages` permission

## Running in Background

### On Mac/Linux:

```bash
nohup python instagram_auto_responder.py > bot.log 2>&1 &
```

Check logs:
```bash
tail -f bot.log
```

Stop the bot:
```bash
ps aux | grep instagram_auto_responder
kill <PID>
```

### On Windows:

Use Task Scheduler or run in a separate terminal window.

## Important Notes

1. **Rate Limits**: Don't check too frequently (60 seconds is safe)
2. **API Costs**: Instagram API is free but has rate limits
3. **Token Expiry**: Tokens expire after 60 days - refresh regularly
4. **Testing**: Always test with `run_once()` before continuous monitoring
5. **Compliance**: Follow Instagram's Terms of Service

## File Overview

- `instagram_auto_responder.py` - Main bot script
- `test_instagram_bot.py` - Test suite
- `jeffin_config.json` - Your credentials (keep private!)
- `sample_app.py` - Your existing auth script
- `README_INSTAGRAM_AUTO_RESPONDER.md` - Full documentation

## Support

For issues:
1. Run `test_instagram_bot.py` to diagnose
2. Check Instagram API status
3. Verify token and permissions
4. Review error messages in console

## Next Steps

1. Run the test script: `python test_instagram_bot.py`
2. If tests pass, run single check: `python instagram_auto_responder.py`
3. Monitor the output
4. Switch to continuous mode if desired
5. Customize keywords and messages as needed

Happy automating!
