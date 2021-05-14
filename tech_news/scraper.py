import os
import requests
import json
from time import sleep
from requests.exceptions import ReadTimeout
from bs4 import BeautifulSoup


def fetch(url):
    try:
        sleep(1)
        r = requests.get(url, timeout=3)
        if r.status_code != 200:
            return None
    except ReadTimeout:
        return None

    return r.text


def scrape_noticia(html_content):
    soup = BeautifulSoup(html_content, "html.parser")

    link = soup.find("meta", property="og:url")
    title = soup.find("h1", class_="tec--article__header__title").get_text()
    timestamp = soup.find("time", id="js-article-date")
    write = soup.find("a", class_="tec--author__info__link").get_text().strip()
    shares = soup.find("div", class_="tec--toolbar__item").get_text().strip()
    comments = soup.find("button", id="js-comments-btn").get_text().strip()
    summary = soup.find("div", class_="tec--article__body")
    sources_and_categories = soup.find_all("a", class_="tec--badge")

    for tag in summary.children:
        p_tag = tag.get_text()
        break

    return {"url": link["content"], "title": title, "timestamp": timestamp["datetime"], "writer": write, "shares_count": int(shares[0]), "comments_count": int(comments[0]), "summary": p_tag, "sources": [t.get_text().strip() for t in sources_and_categories[0:2]], "categories": [t.get_text().strip() for t in sources_and_categories[2:]]}


def scrape_novidades(html_content):
    if html_content == "":
        return []
    
    soup = BeautifulSoup(html_content, "html.parser")
    scripts = soup.find_all("script", {"type": "application/ld+json"})    
    
    urls = json.loads("".join(scripts[1].contents))          
    return list(map(lambda x: x.get("url"), urls['itemListElement']))
  

def scrape_next_page_link(html_content):
    pass


def get_tech_news(amount):
    pass


if __name__ == "__main__":
    os.chdir("../")
    path = ("tests/assets/tecmundo_pages/novidades.html")
    folder = f"{os.getcwd()}/{path}"
    with open(folder) as f:
        html_content = f.read()

    scrape_novidades(html_content)
