import os

from dotenv import load_dotenv

import requests

load_dotenv()
RSA_KEY = os.getenv("RSA_KEY", "")


def generate_forecast(location: str, date):
    url_base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"
    elements = [
        "datetime", "name", "resolvedAddress", "latitude", "longitude",
        "temp", "feelslike", "dew", "humidity", "precip", "precipprob", "preciptype",
        "snow", "snowdepth", "windgust", "windspeed", "winddir", "pressure",
        "visibility", "cloudcover", "solarradiation", "solarenergy", "uvindex",
        "sunrise", "sunset", "moonphase", "conditions"
    ]

    params = {
        "unitGroup": "metric",
        "elements": ",".join(elements),
        "include": "hours",
        "key": RSA_KEY,
        "contentType": "json"
    }

    url = f"{url_base_url}/{location}/{date}"

    response = requests.get(url, params=params, headers={"X-Api-Key": RSA_KEY})

    if response.status_code == requests.codes.ok:
        return response.json()
    else:
        raise Exception(f"ERROR: {response.text}: {response.status_code}")
