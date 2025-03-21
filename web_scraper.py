import urllib.request
import urllib.error

import re


url = "https://www.understandingwar.org/backgrounder/russia-ukraine-warning-update-initial-russian-offensive-campaign-assessment"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

req = urllib.request.Request(url, headers=headers)

with urllib.request.urlopen(req) as response:
    try:
        html_content = response.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        print(f"HTTP error {e.code}: {e.reason}")

if html_content:
    date_pattern = re.compile(r'<span[^>]*?property="dc:date dc:created"[^>]*?content="(.*?)"', re.DOTALL)
    date_match = date_pattern.search(html_content)
    if date_match:
        date_content = date_match.group(1)
        print(f"Date: {date_content}")
    else:
        print("Date not found.")

    text_pattern = re.compile(r'<div class="field-items"><div class="field-item even" property="content:encoded">(.*?)<\/div>', re.DOTALL)
    text_match = text_pattern.search(html_content)
    if text_match:
        content = text_match.group(1)
        text = re.sub(r'<script.*?</script>', '', content, flags=re.DOTALL)
        text = re.sub(r'<style.*?</style>', '', text, flags=re.DOTALL)
        text = re.sub(r'<[^>]+>', '', text)
        clean_text = text.strip()
        print(f"Content: {clean_text}")
    else:
        print("Content not found.")

