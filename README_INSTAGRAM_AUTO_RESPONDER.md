# Instagram Auto Responder

Automatically reply to comments and send DMs when users comment with specific keywords on your Instagram posts.

## Features

- Monitors your Instagram posts for comments containing trigger keywords
- Automatically replies to matching comments
- Sends direct messages to users who commented
- Prevents duplicate responses by tracking processed comments
- Supports continuous monitoring or single-check mode

## Requirements

- Python 3.7+
- Instagram Business Account
- Facebook App with Instagram Graph API access
- Required permissions:
  - `instagram_business_basic`
  - `instagram_business_content_publish`
  - `instagram_business_manage_messages`
  - `instagram_business_manage_comments`

## Installation

1. Install required packages:
```bash
pip install requests
```

2. Set up your configuration file (`jeffin_config.json`):
```json
{
  "app_id": "YOUR_APP_ID",
  "app_secret": "YOUR_APP_SECRET",
  "access_token": "YOUR_ACCESS_TOKEN"
}
```

## Usage

### Option 1: Run Single Check

Check your recent posts once and process any matching comments:

```python
from instagram_auto_responder import InstagramAutoResponder

responder = InstagramAutoResponder('jeffin_config.json')
responder.run_once(media_limit=5)
```

Or simply run:
```bash
python instagram_auto_responder.py
```

### Option 2: Continuous Monitoring

Monitor posts continuously (checks every 60 seconds):

```python
from instagram_auto_responder import InstagramAutoResponder

responder = InstagramAutoResponder('jeffin_config.json')
responder.monitor_and_respond(check_interval=60, media_limit=5)
```

Edit the `main()` function in `instagram_auto_responder.py`:
```python
def main():
    responder = InstagramAutoResponder('jeffin_config.json')
    # Uncomment this line for continuous monitoring:
    responder.monitor_and_respond(check_interval=60, media_limit=5)
    # Comment out this line:
    # responder.run_once(media_limit=5)
```

## Configuration

### Customize Trigger Keywords

Edit the keywords in the script:
```python
self.trigger_keywords = ["cyber", "giveaway", "books"]
```

Or modify after initialization:
```python
responder = InstagramAutoResponder('jeffin_config.json')
responder.trigger_keywords = ["custom", "keywords", "here"]
```

### Customize Messages

Edit messages in the script:
```python
# Comment reply message
self.comment_reply_message = "Your custom reply message!"

# Direct message
self.dm_message = "Your custom DM message!"
```

Or modify after initialization:
```python
responder.comment_reply_message = "Follow me for updates!"
responder.dm_message = "Thanks for your interest!"
```

## How It Works

1. **Fetch Recent Posts**: Gets your last N posts (default: 5)
2. **Check Comments**: Retrieves all comments on each post
3. **Keyword Matching**: Checks if comment contains any trigger keywords (case-insensitive)
4. **Auto Reply**: Replies to the comment with your custom message
5. **Send DM**: Sends a direct message to the commenter
6. **Track Processed**: Marks comment as processed to avoid duplicates

## Example Workflow

1. User comments "I love this cyber giveaway!" on your post
2. Script detects "cyber" and "giveaway" keywords
3. Script replies: "Thank you for your interest! Please follow me for more updates!"
4. Script sends DM: "Hi! Thanks for commenting on my post. Follow me for exciting updates and giveaways!"

## Important Notes

### Rate Limits
- Instagram has API rate limits
- Default check interval: 60 seconds (recommended)
- Don't set interval too low to avoid hitting limits

### Permissions
Ensure your access token has the required permissions:
- `instagram_business_manage_comments` - to reply to comments
- `instagram_business_manage_messages` - to send DMs
- `instagram_business_basic` - to access basic account info

### Access Token
- Get a long-lived access token (60 days)
- Refresh token before expiration
- Test token validity before running

### Testing
1. Start with `run_once()` to test functionality
2. Post a test comment with trigger keywords
3. Verify comment reply and DM are sent
4. Switch to continuous monitoring if needed

## Troubleshooting

### Error: "Access token has expired"
- Generate a new access token
- Update `jeffin_config.json`

### Error: "Insufficient permissions"
- Check your app has required permissions
- Re-authorize with correct scopes

### Comments not detected
- Verify keywords match (case-insensitive)
- Check `media_limit` includes the post
- Ensure comments are not already processed

### DM fails but comment reply works
- User may have restricted DMs
- Check `instagram_business_manage_messages` permission
- User must follow you or have accepted DMs

## Advanced Usage

### Custom Processing Logic

```python
responder = InstagramAutoResponder('jeffin_config.json')

# Get recent posts
media_posts = responder.get_recent_media(limit=10)

# Process specific post
for media in media_posts:
    comments = responder.get_media_comments(media['id'])
    for comment in comments:
        if responder.check_comment_for_keywords(comment['text']):
            # Custom logic here
            responder.reply_to_comment(comment['id'], "Custom message")
```

### Run as Background Service

Use `nohup` or `screen` on Linux/Mac:
```bash
nohup python instagram_auto_responder.py &
```

Or use a process manager like `supervisor` or `systemd`.

## License

This script is for educational and authorized use only. Ensure compliance with Instagram's Terms of Service and API usage policies.
