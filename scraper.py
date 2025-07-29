from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json
import time

def scrape_behance_projects(username, limit=6):
    url = f"https://www.behance.net/{username}"

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--window-size=1920,1080')

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    projects = []
    articles = soup.find_all('article', limit=limit)

    for article in articles:
        title_anchor = article.find('a', class_='Title-title-lpJ')
        if not title_anchor:
            continue

        title = title_anchor.text.strip()
        project_href = title_anchor['href']
        project_url = f"https://www.behance.net{project_href}"

        img_tag = article.find('picture')
        image_url = img_tag.find('img').get('src') if img_tag and img_tag.find('img') else None

        if title and project_url and image_url:
            projects.append({
                "title": title,
                "url": project_url,
                "image": image_url
            })

    return projects
