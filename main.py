# Import Modules
import requests
import os
import env
import smtplib

# Constants (Location - Cork for Rain!)
api_key = os.environ.get("OWM_API_KEY")
OWM_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"
MY_LAT = 51.896893
MY_LONG = -8.486316
my_email = os.environ.get("MY_EMAIL")
email_password = os.environ.get("EMAIL_PASSWORD")
to_email = os.environ.get("TO_EMAIL")
port_num = os.environ.get("PORT")

# OW Parameters to get first 4 Forecasts
weather_parameters = {
    "lat" : MY_LAT,
    "lon" : MY_LONG,
    "appid" : api_key,
    "cnt" : 4,
}

# Function To Send Email
def send_email(heading, message):
    email_message = f"Subject:{heading}\n\n{message}."
    with smtplib.SMTP(host = "send.one.com", port = port_num) as connection:
        connection.starttls()
        connection.login(user = my_email, password = email_password)
        connection.sendmail(from_addr = my_email,
                            to_addrs = to_email,
                            msg = email_message
        )

# Request API and get in data file
response = requests.get(url = OWM_Endpoint, params= weather_parameters)
response.raise_for_status()
# print(response.status_code)
weather_data = response.json()
# print(weather_data)

# Check if raining over 4 forecasts
need_umbrella = False

for three_hour_data in weather_data["list"]:
    weather_now_code = three_hour_data["weather"][0]["id"]
    # If weather code < 700, assume rain
    if weather_now_code < 700:
        need_umbrella = True

if need_umbrella:
    email_heading = "Rain Expected Today!"
    email_message = "Rain expected in the next 12 hours.\nTake an umbrella today."
    send_email(email_heading, email_message)
    print("Take umbnrella today.")
else:
    email_heading = "No Rain Expected Today!"
    email_message = "No Rain expected in the next 12 hours.\nLeave the umbrella at home today."
    send_email(email_heading, email_message)
    print("Leave umbrella at home today.")
