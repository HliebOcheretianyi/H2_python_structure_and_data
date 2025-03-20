import requests
from bs4 import BeautifulSoup


def scrape_isw(url):
    response = requests.get(url)
    if response.status_code != 200:
        return "error"
    soup = BeautifulSoup(response.text, 'html.parser')
    title = ""
    title_element = soup.find('h1', class_='title')
    if title_element:
        title = title_element.get_text().strip()
    date = ""
    if "assessment-" in url:
        date = url.split("assessment-")[-1]
    content = ""
    main_content = soup.find('div', class_='field-body')
    if main_content:
        paragraphs = main_content.find_all('p')
        content = "\n\n".join([p.get_text().strip() for p in paragraphs])
    return {
        "title": title,
        "date": date,
        "content": content,
        "soup": soup
    }


if __name__ == "__main__":
    url = "https://www.understandingwar.org/backgrounder/russian-offensive-campaign-assessment-march-17-2025"
    result = scrape_isw(url)
    data = {
        "title": result["title"],
        "date": result["date"],
        "content": result["content"]
    }
    soup = result["soup"] 
    with open('isw_report.txt', 'w', encoding='utf-8') as f:
        f.write(f"Title: {data['title']}\n")
        f.write(f"Date: {data['date']}\n\n")
        if not data['content']:
            body = soup.find('body')
            if body:
                f.write(body.get_text())
        else:
            f.write(data['content'])
    
    print("Report saved")