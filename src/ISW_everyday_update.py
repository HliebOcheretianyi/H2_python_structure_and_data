import urllib.request
import urllib.error
import datetime
import re
import pandas as pd

def everyday_parsing_isw():
    today = datetime.date.today()
    month = str(today.strftime("%B")).lower()

    url = (
        f"https://www.understandingwar.org/backgrounder/"
        f"russian-offensive-campaign-assessment-{month}-{today.day - 2}-{today.year}"
    )
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/120.0.0.0 Safari/537.36'
    }

    result = {
        'date': [],
        'content': []
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
                    result['date'] = [date_content[:10]]
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
                    result['content'] = [clean_text]
                else:
                    print("Content not found.")

    except urllib.error.URLError as e:
        print(f"Error accessing the URL: {e}")
        return
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return

    df = pd.DataFrame(result)

    try:
        existing_df = pd.read_csv('../data/ISW.csv')
        if df['date'][0] in existing_df['date'].values:
            print("Data for this date already exists. Skipping save.")
            return
        combined_df = pd.concat([existing_df, df], ignore_index=True)
    except FileNotFoundError:
        combined_df = df
    except Exception as e:
        print(f"Error reading existing file: {e}")
        combined_df = df

    combined_df.to_csv('../data/ISW.csv', index=False)
if __name__ == "__main__":
    everyday_parsing_isw()

