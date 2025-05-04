import requests
import os
from dotenv import load_dotenv

load_dotenv()
ALERT_KEY = os.getenv("ALERT_KEY", "")

ordered_region_names = [
    "Автономна Республіка Крим",
    "Волинська область",
    "Вінницька область",
    "Дніпропетровська область",
    "Донецька область",
    "Житомирська область",
    "Закарпатська область",
    "Запорізька область",
    "Івано-Франківська область",
    "Київ",
    "Київська область",
    "Кіровоградська область",
    "Луганська область",
    "Львівська область",
    "Миколаївська область",
    "Одеська область",
    "Полтавська область",
    "Рівненська область",
    "м. Севастополь",
    "Сумська область",
    "Тернопільська область",
    "Харківська область",
    "Херсонська область",
    "Хмельницька область",
    "Черкаська область",
    "Чернівецька область",
    "Чернігівська область"
]

def get_alerts():
    url = "https://api.alerts.in.ua/v1/iot/active_air_raid_alerts_by_oblast.json"
    headers = {
        "Authorization": f"Bearer {ALERT_KEY}"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"API error: {response.status_code} - {response.text}")

    status_string = response.json()

    status_list_of_dicts = [
        {"region": region, "status": status}
        for region, status in zip(ordered_region_names, status_string)
    ]

    return status_list_of_dicts