import json

import requests
from bs4 import BeautifulSoup


def parser(url):
    result = {}

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        span_element = soup.find('span', {'property': 'dc:date dc:created'})

        # Отримуємо значення атрибуту 'content' (дату)
        timestamp = span_element['content'] if span_element else None
        result['timestamp'] = timestamp[0:9]
        paragraphs = soup.find_all('strong')
        counter = 0
        for p in paragraphs[5:]:
            adder = p.get_text(strip=True)
            if len(adder) >= 10:
                result[counter] = adder
                counter += 1

    else:
        print("Не вдалося завантажити сторінку, статус:", response.status_code)

    return json.dumps(result, indent=4)

print(parser('https://www.understandingwar.org/backgrounder/russia-ukraine-warning-update-initial-russian-offensive-campaign-assessment'))