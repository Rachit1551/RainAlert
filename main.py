import os
import requests
from twilio.rest import Client

# Clear terminal screen (optional for local debugging)
os.system('cls' if os.name == 'nt' else 'clear')

# ----------------------------- Configuration -----------------------------

# Twilio credentials
account_sid = "YOUR_TWILIO_ACCOUNT_SID"
auth_token = "YOUR_TWILIO_AUTH_TOKEN"

# Twilio phone numbers
twilio_phone_number = "YOUR_TWILIO_PHONE_NUMBER"
destination_phone_number = "DESTINATION_PHONE_NUMBER"

# OpenWeatherMap API key
api_key = "YOUR_OPENWEATHERMAP_API_KEY"

# Location coordinates
latitude = YOUR_LATITUDE      # Example: 28.6139
longitude = YOUR_LONGITUDE    # Example: 77.2090

# ----------------------------- API Request ------------------------------

weather_api_url = "https://api.openweathermap.org/data/2.5/forecast"
weather_params = {
    "lat": latitude,
    "lon": longitude,
    "appid": api_key,
    "cnt": 4  # Next 4 time blocks (~12 hours)
}

response = requests.get(weather_api_url, params=weather_params)
response.raise_for_status()

# ----------------------------- Rain Detection ----------------------------

will_rain = False
rain_time = ""

for forecast in response.json().get('list', []):
    weather_id = forecast['weather'][0]['id']
    if int(weather_id) < 700:
        will_rain = True
        rain_time = forecast['dt_txt']
        break

# ----------------------------- SMS Notification --------------------------

if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=f"Rain Alert: Rain is forecasted around {rain_time}. Please take necessary precautions.",
        from_=twilio_phone_number,
        to=destination_phone_number
    )
    print(f"SMS sent: Message SID {message.sid}")
else:
    print("No rain expected in the next few hours.")
