import requests
import os
from dotenv import load_dotenv
load_dotenv()
ALERT_KEY = os.getenv("ALERT_KEY", "")
city_to_uid = {
    'Khmelnytskyi Region': '3',
    'Vinnytsia Region': '4',
    'Rivne Region': '5',
    'Volyn Region': '8',
    'Dnipropetrovsk Region': '9',
    'Zhytomyr Region': '10',
    'Zakarpattia Region': '11',
    'Zaporizhzhia Region': '12',
    'Ivano-Frankivsk Region': '13',
    'Kyiv Region': '14',
    'Kirovohrad Region': '15',
    'Luhansk Region': '16',
    'Mykolaiv Region': '17',
    'Odesa Region': '18',
    'Poltava Region': '19',
    'Sumy Region': '20',
    'Ternopil Region': '21',
    'Kharkiv Region': '22',
    'Kherson Region': '23',
    'Cherkasy Region': '24',
    'Chernihiv Region': '25',
    'Chernivtsi Region': '26',
    'Lviv Region': '27',
    'Donetsk Region': '28',
    'AR Crimea': '29',
    'Kyiv': '31'
}
status = {
    'A': 'air alarm',
    'N': 'no air alarm',
    'P': 'partial air alarm'
}

def get_alert_status(city_name):
    uid = city_to_uid.get(city_name)
    if uid is None:
        return
    url = f"https://api.alerts.in.ua/v1/iot/active_air_raid_alerts/{uid}.json"
    headers = {
        "Authorization": f"Bearer {ALERT_KEY}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == requests.codes.ok:
        return status.get(response.json())
    else:
        raise Exception(f"ERROR: {response.text}: {response.status_code}")
