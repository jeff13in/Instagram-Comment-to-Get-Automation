import requests
import json

with open('jeffin_config.json', 'r') as file:
    config = json.load(file)


app_id = config["app_id"]
app_secret = config["app_secret"]
redirect_uri = "https://interfenestral-king-unmined.ngrok-free.dev/"

url = f'https://graph.instagram.com/access_token'
payload = {
    "grant_type":"ig_exchange_token",
    "client_secret":app_secret,
    "access_token":"IGAAQjSjUZAegpBZAFJEN3Mxcl9vQjhMSVRNUjI1eEZACeXdtMy1fMV9wYm0weFJDV28tMXAzN2gwcHFPOEVlMjg5YWhBVzVYa3A4TktCYzIwR0xFNktTM2xfREp0R05vUHpyOE9ydGFMTHIzM3NQZAWNMZAW52RW1lbnMtNk8zeHVNWQZDZD"
}
response = requests.get(url, params=payload)
data = response.json()
print(data)
long_access_token = data["access_token"]
print(long_access_token)