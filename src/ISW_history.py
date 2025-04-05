import urllib.request
import urllib.error
import datetime
import re
import pandas as pd
from tqdm import tqdm

def generate_date_range(start_date, end_date):
    current = start_date
    while current <= end_date:
        yield current
        current += datetime.timedelta(days=1)

def build_url(date_obj):
    month = date_obj.strftime("%B").lower()
    day = str(date_obj.day)
    year = date_obj.year

    if year == 2022 and date_obj.month == 2 and date_obj.day == 24:
        return ("https://www.understandingwar.org/backgrounder/"
                "russia-ukraine-warning-update-initial-russian-offensive-campaign-assessment")
    elif year == 2022 and date_obj.month == 2 and date_obj.day == 25:
        return (f"https://www.understandingwar.org/backgrounder/"
                f"russia-ukraine-warning-update-russian-offensive-campaign-assessment-{month}-{day}-{year}")
    elif year == 2022 and date_obj.month == 2 and date_obj.day != 28:
        return (f"https://www.understandingwar.org/backgrounder/"
                f"russia-ukraine-warning-update-russian-offensive-campaign-assessment-{month}-{day}")
    elif year == 2022 and date_obj.month != 2:
        return (f"https://www.understandingwar.org/backgrounder/"
                f"russian-offensive-campaign-assessment-{month}-{day}")
    else:
        return (f"https://www.understandingwar.org/backgrounder/"
                f"russian-offensive-campaign-assessment-{month}-{day}-{year}")

def try_fetch_article(date_obj, headers):
    url = build_url(date_obj)

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            html_content = response.read().decode('utf-8')

            text_pattern = re.compile(
                r'<div class="field-items"><div class="field-item even" property="content:encoded">(.*?)<\/div>',
                flags=re.DOTALL
            )
            text_match = text_pattern.search(html_content)
            if text_match:
                content = text_match.group(1)
                text = re.sub(r'<script.*?</script>', '', content, flags=re.DOTALL)
                text = re.sub(r'<style.*?</style>', '', text, flags=re.DOTALL)
                text = re.sub(r'<[^>]+>', '', text)
                clean_text = text.strip()
                return clean_text
    except urllib.error.HTTPError:
        return ""
    except Exception as e:
        print(f"[{date_obj}] Unexpected error: {e}")
        return ""

    return ""

def collect_all_isw_reports(end_date):
    start_date = datetime.date(2022, 2, 24)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/'
                      '537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    data = {
        'date': [],
        'content': []
    }

    for date_obj in tqdm(generate_date_range(start_date, end_date), desc="Downloading ISW reports"):
        content = try_fetch_article(date_obj, headers)
        data['date'].append(date_obj.strftime('%Y-%m-%d'))
        data['content'].append(content)

    df = pd.DataFrame(data)
    df.sort_values(by='date', inplace=True)

    df.to_csv('../data/ISW.csv', index=False)

    print(f"Total rows saved: {len(df)}")

if __name__ == "__main__":
    end_date = datetime.date(2025, 3, 23)
    collect_all_isw_reports(end_date)
    df = pd.read_csv('../data/ISW.csv')
    print(df[df['content'] != ""].tail(10))