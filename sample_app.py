import requests
import json

with open('jeffin_config.json', 'r') as file:
    config = json.load(file)


app_id = config["app_id"]
app_secret = config["app_secret"]
access_token = config["access_token"]
redirect_uri = "https://interfenestral-king-unmined.ngrok-free.dev/"




url = "https://www.instagram.com/oauth/authorize?"
url = url + f"client_id={int(app_id)}"
url = url + "&" + f"redirect_uri={redirect_uri}"
url = url + "&" + f"response_type=code"
url = url + "&" + f"scope={('instagram_business_basic, instagram_business_content_publish, instagram_business_manage_messages, instagram_business_manage_comments').replace(' ', '')}"
#print(url)

returned_url = "https://interfenestral-king-unmined.ngrok-free.dev/?code=AQB_w47pSGrDcsk-uW5QwgWJgCqrpKQnI7r--OHipso_LFf5zbKQ3xR_ksXqke7qqCLhM0f3jLBwvZSGpp8VolaPnUielVpLVU9W5ne_a2l7M8moQcrhaCzPicYeJbEUAo4YWD9dZ958LNz8cuAHkbbJUUYFGxo3555WHvMO6yEfulWBZLqEQ2He_-8qx9NoRAlQheXWfd0_E53SxJYYlf1XYu3aGFjM44ZuaO8uZJSKaw#_"


authorization_code = returned_url.replace(redirect_uri+ "?code=","")
#print(authorization_code)

"""url = "https://api.instagram.com/oauth/access_token"
form_data = {
    "client_id": int(app_id),
    "client_secret": app_secret,
    "grant_type": "authorization_code",
    "redirect_uri": redirect_uri,
    "code": authorization_code
}

response = requests.post(url, data=form_data)
data = response.json()
print(data)
user_access_token = data["access_token"]
print(user_access_token)"""


"""url = f'https://graph.instagram.com/v21.0/me'
payload = {
    "fields":"id,username,name,account_type,profile_picture_url,followers_count,follows_count,media_count",
    "access_token":access_token
}

response = requests.get(url, params=payload)
data = response.json()
print(json.dumps(data, indent=4))
print(f'App Scoped User ID: {data["id"]}')
print(f"Instagram Business Account User ID: {data['id']}")"""

url = f'https://graph.instagram.com/v21.0/me/messages'
headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
json_body = {
    "recipient": {
        "id": "1868427904096446"
    },
    "message": {
        "text": "Good Morning from Jeffin"
    }
}

response = requests.post(url, headers=headers, json=json_body)
data = response.json()
print(json.dumps(data, indent=4))


