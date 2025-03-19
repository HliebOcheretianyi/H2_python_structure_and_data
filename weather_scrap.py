import json
import os

from dotenv import load_dotenv

import requests

load_dotenv()
API_TOKEN = os.getenv("API_TOKEN", "")
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


# def json_output(data, indent=4, sort_keys=False, ensure_ascii=False, file=None):
#     """
#     Universal JSON outputter that can handle various Python objects and output them as JSON.
#
#     Parameters:
#     - data: The Python object to convert to JSON
#     - indent: Number of spaces for indentation (None for compact format)
#     - sort_keys: Whether to sort dictionary keys alphabetically
#     - ensure_ascii: Whether to escape non-ASCII characters
#     - file: Optional file object or path to write JSON to
#
#     Returns:
#     - JSON string if file is None, otherwise writes to file and returns None
#     """
#     try:
#         # If file is a string, open it as a file path
#         if isinstance(file, str):
#             with open(file, 'w', encoding='utf-8') as f:
#                 json.dump(data, f, indent=indent, sort_keys=sort_keys, ensure_ascii=ensure_ascii)
#             return f"JSON successfully written to {file}"
#
#         # If file is a file object, write to it
#         elif file is not None:
#             json.dump(data, file, indent=indent, sort_keys=sort_keys, ensure_ascii=ensure_ascii)
#             return f"JSON successfully written to file"
#
#         # Otherwise return formatted JSON string
#         else:
#             return json.dumps(data, indent=indent, sort_keys=sort_keys, ensure_ascii=ensure_ascii)
#
#     except TypeError as e:
#         # Try to handle non-serializable objects
#         if "not JSON serializable" in str(e):
#             # Create a custom encoder for common non-serializable types
#             class CustomEncoder(json.JSONEncoder):
#                 def default(self, obj):
#                     # Handle date/time objects
#                     if hasattr(obj, 'isoformat'):
#                         return obj.isoformat()
#                     # Handle sets
#                     elif isinstance(obj, set):
#                         return list(obj)
#                     # Handle bytes
#                     elif isinstance(obj, bytes):
#                         return obj.decode('utf-8', errors='replace')
#                     # Handle objects with __dict__
#                     elif hasattr(obj, '__dict__'):
#                         return obj.__dict__
#                     return str(obj)
#
#             # Try again with custom encoder
#             if isinstance(file, str):
#                 with open(file, 'w', encoding='utf-8') as f:
#                     json.dump(data, f, indent=indent, sort_keys=sort_keys,
#                               ensure_ascii=ensure_ascii, cls=CustomEncoder)
#                 return f"JSON successfully written to {file}"
#             elif file is not None:
#                 json.dump(data, file, indent=indent, sort_keys=sort_keys,
#                           ensure_ascii=ensure_ascii, cls=CustomEncoder)
#                 return f"JSON successfully written to file"
#             else:
#                 return json.dumps(data, indent=indent, sort_keys=sort_keys,
#                                   ensure_ascii=ensure_ascii, cls=CustomEncoder)
#     except Exception as e:
#         return f"Error outputting JSON: {str(e)}"
#
# print(json_output(generate_forecast("Kyiv", "2024-07-01")))