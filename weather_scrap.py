import os
from dotenv import load_dotenv
import requests
from datetime import datetime, timedelta

load_dotenv()
RSA_KEY = os.getenv("RSA_KEY", "")


def generate_forecast(location: str):
    url_base = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"

    elements = [
        "datetime", "name", "resolvedAddress", "latitude", "longitude",
        "temp", "feelslike", "dew", "humidity", "precip", "precipprob", "preciptype",
        "snow", "snowdepth", "windgust", "windspeed", "winddir", "pressure",
        "visibility", "cloudcover", "solarradiation", "solarenergy", "uvindex",
        "sunrise", "sunset", "moonphase", "conditions"
    ]

    start_time = datetime.now()
    current_hour = start_time.replace(minute=0, second=0, microsecond=0)

    end_time = start_time + timedelta(hours=24)

    params = {
        "unitGroup": "metric",
        "elements": ",".join(elements),
        "include": "hours",
        "key": RSA_KEY,
        "contentType": "json",
        "tz": "Europe/Kiev"
    }

    url = f"{url_base}/{location}/{start_time.strftime('%Y-%m-%d')}/{end_time.strftime('%Y-%m-%d')}"

    response = requests.get(url, params=params)

    if response.status_code == requests.codes.ok:
        data = response.json()

        hours = []
        for day in data.get("days", []):
            for hour in day.get("hours", []):
                hour_time = datetime.strptime(hour["datetime"], "%H:%M:%S").time()
                full_hour_time = datetime.combine(datetime.strptime(day["datetime"], "%Y-%m-%d"), hour_time)

                if full_hour_time >= current_hour:
                    hours.append(hour)

        return hours[:24]
    else:
        raise Exception(f"ERROR: {response.text}: {response.status_code}")
