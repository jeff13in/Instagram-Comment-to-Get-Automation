import requests
import json
import time
from datetime import datetime
from typing import List, Dict, Set


class InstagramAutoResponder:
    """
    Instagram Auto Responder - Monitors comments and sends auto-replies + DMs
    """

    def __init__(self, config_path: str = 'jeffin_config.json'):
        """Initialize the auto responder with config"""
        with open(config_path, 'r') as file:
            config = json.load(file)

        self.app_id = config["app_id"]
        self.app_secret = config["app_secret"]
        self.access_token = config["access_token"]
        self.base_url = "https://graph.instagram.com/v21.0"

        # Keywords to trigger auto-response
        self.trigger_keywords = ["cyber", "giveaway", "books"]

        # Track processed comments to avoid duplicates
        self.processed_comments: Set[str] = set()

        # Auto-reply message for comments
        self.comment_reply_message = "Thank you for your interest! Please follow me for more updates!"

        # DM message template
        self.dm_message = "Hi! Thanks for commenting on my post. Follow me for exciting updates and giveaways!"

        # Get Instagram Business Account ID
        self.ig_account_id = self._get_instagram_account_id()
        print(f"Instagram Account ID: {self.ig_account_id}")

    def _get_instagram_account_id(self) -> str:
        """Get the Instagram Business Account ID"""
        url = f'{self.base_url}/me'
        params = {
            "fields": "id,username",
            "access_token": self.access_token
        }

        response = requests.get(url, params=params)
        data = response.json()

        if 'error' in data:
            raise Exception(f"Error getting account ID: {data['error']['message']}")

        return data['id']

    def get_recent_media(self, limit: int = 10) -> List[Dict]:
        """Get recent media posts"""
        url = f'{self.base_url}/{self.ig_account_id}/media'
        params = {
            "fields": "id,caption,media_type,media_url,timestamp,permalink",
            "limit": limit,
            "access_token": self.access_token
        }

        response = requests.get(url, params=params)
        data = response.json()

        if 'error' in data:
            print(f"Error getting media: {data['error']['message']}")
            return []

        return data.get('data', [])

    def get_media_comments(self, media_id: str) -> List[Dict]:
        """Get comments for a specific media post"""
        url = f'{self.base_url}/{media_id}/comments'
        params = {
            "fields": "id,text,username,timestamp,from",
            "access_token": self.access_token
        }

        response = requests.get(url, params=params)
        data = response.json()

        if 'error' in data:
            print(f"Error getting comments: {data['error']['message']}")
            return []

        return data.get('data', [])

    def check_comment_for_keywords(self, comment_text: str) -> bool:
        """Check if comment contains any trigger keywords"""
        comment_lower = comment_text.lower()
        return any(keyword.lower() in comment_lower for keyword in self.trigger_keywords)

    def reply_to_comment(self, comment_id: str, message: str = None) -> bool:
        """Reply to a specific comment"""
        if message is None:
            message = self.comment_reply_message

        url = f'{self.base_url}/{comment_id}/replies'
        params = {
            "message": message,
            "access_token": self.access_token
        }

        response = requests.post(url, params=params)
        data = response.json()

        if 'error' in data:
            print(f"Error replying to comment: {data['error']['message']}")
            return False

        print(f"Successfully replied to comment {comment_id}")
        return True

    def send_direct_message(self, recipient_id: str, message: str = None) -> bool:
        """Send a direct message to a user"""
        if message is None:
            message = self.dm_message

        url = f'{self.base_url}/me/messages'
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        json_body = {
            "recipient": {
                "id": recipient_id
            },
            "message": {
                "text": message
            }
        }

        response = requests.post(url, headers=headers, json=json_body)
        data = response.json()

        if 'error' in data:
            print(f"Error sending DM: {data['error']['message']}")
            return False

        print(f"Successfully sent DM to user {recipient_id}")
        return True

    def process_comment(self, comment: Dict, media_id: str) -> None:
        """Process a single comment - reply and send DM if keywords match"""
        comment_id = comment['id']
        comment_text = comment['text']
        username = comment.get('username', 'Unknown')
        commenter_id = comment.get('from', {}).get('id')

        # Skip if already processed
        if comment_id in self.processed_comments:
            return

        # Check if comment contains trigger keywords
        if self.check_comment_for_keywords(comment_text):
            print(f"\n[{datetime.now()}] Trigger found!")
            print(f"Media ID: {media_id}")
            print(f"Comment by @{username}: {comment_text}")

            # Reply to the comment
            reply_success = self.reply_to_comment(comment_id)

            # Send DM to the user
            if commenter_id:
                dm_success = self.send_direct_message(commenter_id)
            else:
                print(f"Could not send DM - commenter ID not available")
                dm_success = False

            # Mark as processed
            self.processed_comments.add(comment_id)

            print(f"Comment Reply: {'✓' if reply_success else '✗'}")
            print(f"DM Sent: {'✓' if dm_success else '✗'}")
        else:
            # Mark as processed even if no keywords match
            self.processed_comments.add(comment_id)

    def monitor_and_respond(self, check_interval: int = 60, media_limit: int = 5) -> None:
        """
        Continuously monitor posts for new comments and respond

        Args:
            check_interval: Time in seconds between checks (default: 60)
            media_limit: Number of recent posts to monitor (default: 5)
        """
        print(f"\n{'='*60}")
        print(f"Instagram Auto Responder Started")
        print(f"{'='*60}")
        print(f"Monitoring for keywords: {', '.join(self.trigger_keywords)}")
        print(f"Check interval: {check_interval} seconds")
        print(f"Monitoring last {media_limit} posts")
        print(f"{'='*60}\n")

        try:
            while True:
                print(f"[{datetime.now()}] Checking for new comments...")

                # Get recent media posts
                media_posts = self.get_recent_media(limit=media_limit)

                if not media_posts:
                    print("No media posts found")
                else:
                    # Check comments on each post
                    for media in media_posts:
                        media_id = media['id']
                        comments = self.get_media_comments(media_id)

                        # Process each comment
                        for comment in comments:
                            self.process_comment(comment, media_id)

                print(f"Check complete. Waiting {check_interval} seconds...\n")
                time.sleep(check_interval)

        except KeyboardInterrupt:
            print(f"\n{'='*60}")
            print("Auto Responder stopped by user")
            print(f"Total comments processed: {len(self.processed_comments)}")
            print(f"{'='*60}")

    def run_once(self, media_limit: int = 5) -> None:
        """Run a single check without continuous monitoring"""
        print(f"\n{'='*60}")
        print(f"Running single check...")
        print(f"{'='*60}\n")

        media_posts = self.get_recent_media(limit=media_limit)

        for media in media_posts:
            media_id = media['id']
            print(f"\nChecking post: {media.get('permalink', media_id)}")
            comments = self.get_media_comments(media_id)

            print(f"Found {len(comments)} comments")

            for comment in comments:
                self.process_comment(comment, media_id)

        print(f"\n{'='*60}")
        print(f"Check complete. Processed {len(self.processed_comments)} comments")
        print(f"{'='*60}")


def main():
    """Main function to run the auto responder"""
    # Create the auto responder instance
    responder = InstagramAutoResponder('jeffin_config.json')

    # Option 1: Run continuous monitoring (checks every 60 seconds)
    # responder.monitor_and_respond(check_interval=60, media_limit=5)

    # Option 2: Run a single check
    responder.run_once(media_limit=5)


if __name__ == "__main__":
    main()
