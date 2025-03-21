import urllib.request
import urllib.error
import json
import datetime
import re


def everyday_parsing_isw():
    today = datetime.date.today()
    month = str(today.strftime("%B")).lower()

    url = (
        f"https://www.understandingwar.org/backgrounder/"
        f"russian-offensive-campaign-assessment-{month}-{today.day}-{today.year}"
    )
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/120.0.0.0 Safari/537.36'
    }

    result = {
                'date': today,
                'content': None
              }
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            html_content = response.read().decode('utf-8')
            if html_content:
                date_pattern = re.compile(r'<span[^>]*?property="dc:date dc:created"[^>]*?content="(.*?)"', flags=re.DOTALL)
                date_match = date_pattern.search(html_content)
                if date_match:
                    date_content = date_match.group(1)
                    result['date'] = date_content[:10]
                else:
                    print("Date not found.")

                text_pattern = re.compile(r'<div class="field-items"><div class="field-item even" property="content:encoded">(.*?)<\/div>', flags=re.DOTALL)
                text_match = text_pattern.search(html_content)
                if text_match:
                    content = text_match.group(1)
                    text = re.sub(r'<script.*?</script>', '', content, flags=re.DOTALL)
                    text = re.sub(r'<style.*?</style>', '', text, flags=re.DOTALL)
                    text = re.sub(r'<[^>]+>', '', text)
                    clean_text = text.strip()
                    result['content'] = clean_text
                else:
                    print("Content not found.")

    except (urllib.error.HTTPError, urllib.error.URLError) as e:
        print(f"Error accessing the URL: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    result['date'] = str(result['date'])
    return json.dumps(result, indent=4)


if __name__ == "__main__":
    print(everyday_parsing_isw())