import os
from dotenv import load_dotenv
import requests
from datetime import datetime, timedelta

load_dotenv()
RSA_KEY = os.getenv("RSA_KEY", "")

def generate_forecast(location: str):
    url_base = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"

    start_time = datetime.now()
    end_time = start_time + timedelta(hours=24)
    current_hour = start_time.replace(minute=0, second=0, microsecond=0)

    day_keys = [
        "datetime", "datetimeEpoch", "tempmax", "tempmin", "temp", "dew", "humidity",
        "precip", "precipcover", "solarradiation", "solarenergy", "uvindex",
        "sunrise", "sunset", "moonphase"
    ]
    hour_keys = [
        "datetime", "datetimeEpoch", "temp", "humidity", "dew", "precip", "precipprob",
        "snow", "snowdepth", "preciptype", "windgust", "windspeed", "winddir",
        "pressure", "visibility", "cloudcover", "uvindex", "conditions"
    ]

    params = {
        "unitGroup": "metric",
        "include": "hours",
        "key": RSA_KEY,
        "contentType": "json",
        "tz": "Europe/Kiev"
    }

    url = f"{url_base}/{location}/{start_time.strftime('%Y-%m-%d')}/{end_time.strftime('%Y-%m-%d')}"
    response = requests.get(url, params=params)
    if response.status_code != requests.codes.ok:
        raise Exception(f"ERROR: {response.text}: {response.status_code}")

    data = response.json()

    results = []
    for day in data.get("days", []):
        day_data = {f"day_{k}": day.get(k) for k in day_keys}

        for hour in day.get("hours", []):
            hour_time = datetime.strptime(hour["datetime"], "%H:%M:%S").time()
            full_hour_time = datetime.combine(datetime.strptime(day["datetime"], "%Y-%m-%d"), hour_time)
            if full_hour_time >= current_hour:
                hour_data = {f"hour_{k}": hour.get(k) for k in hour_keys}
                results.append({"city_resolvedAddress": data.get("resolvedAddress"),
                                **day_data, **hour_data})

    return results