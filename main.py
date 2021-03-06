import os # for running on pythonanywhere w/free twilio account
import requests
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient # for running on pythonanywhere w/free twilio account

# CONSTS LAT & LNG set for New Orleans
# OPEN_WEATHER
END_POINT = "https://api.openweathermap.org/data/2.5/onecall"
LAT = 29.951065  # Change to your latitude
LNG = -90.071533  # Change to your longitude
EXCLUDE = "current,minutely,daily"
API_KEY = "_YOUR_OPEN_WEATHER_MAP_API_HERE_"  # your input here
# Twilio
SID = "_YOUR_TWILIO_SID_GOES_HERE_"  # your input here
AUTH_TOKEN = "_YOUR_TWILIO_AUTH_TOKEN_GOES_HERE_"  # your input here
PHONE = "_YOUR_TWILIO_PHONE_HERE_"  # your input here

# Params
location = {
    "lat": LAT,
    "lon": LNG,
    "exclude": EXCLUDE,
    "appid": API_KEY,
    "units": "standard",  # can change
}

# API OPEN_WEATHER
response = requests.get(
    url=f"{END_POINT}", params=location)
response.raise_for_status()
data = response.json()


# checks the condition
def precipitation():
    hourly_list = data["hourly"][0:13]
    for item in hourly_list:
        if item["weather"][0]["id"] < 700:
            return True
        else:
            return False


# prints based on condition
if precipitation():
    proxy_client = TwilioHttpClient() # for running on pythonanywhere w/free twilio account
    proxy_client.session.proxies = {'https': os.environ['https_proxy']} # for running on pythonanywhere w/free twilio account
    client = Client(SID, AUTH_TOKEN)
    message = client.messages \
        .create(body="It's gonna rain!🌧", from_=PHONE, to="_YOUR_VERIFIED_RECIPIENT_")
    print(message.status)
else:
    proxy_client = TwilioHttpClient() # for running on pythonanywhere w/free twilio account
    proxy_client.session.proxies = {'https': os.environ['https_proxy']} # for running on pythonanywhere w/free twilio account
    client = Client(SID, AUTH_TOKEN, http_client=proxy_client)
    message = client.messages \
        .create(body="Clear skies!", from_=PHONE, to="+15042648349")
    print(message.status)