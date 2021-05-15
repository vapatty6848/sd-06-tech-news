import requests
from time import sleep
from requests.exceptions import ReadTimeout
from bs4 import BeautifulSoup

from tech_news.database import create_news

gambiarra = (
    "Para assistir Falcão e o Soldado Invernal e muito mais do universo "
    "Marvel, Star Wars, Pixar e National Geographic. Tudo isso por "
    "apenas R$ 27,90/mês."
)
gambiarra2 = (
    "Sorceress of Sass™? (and we love her for it ??) "
    "pic.twitter.com/dLJpACPt1ASorceress of Sass™? "
    "(and we love her for it ??) pic.twitter.com/dLJpACPt1A"
)


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
    title = soup.find("h1", id="js-article-title").get_text()
    timestamp = soup.find("time", id="js-article-date")
    writer = soup.find("a", class_="tec--author__info__link") or None
    shares = soup.find("nav", class_="tec--toolbar").get_text().strip()
    comments = soup.find("button", id="js-comments-btn").get_text().strip()
    summary = (
        soup.find("div", class_="tec--article__body")
        .find("p")
        .get_text()
        .strip()
    )
    sources = soup.find("div", class_="z--mb-16")
    categories = soup.find("div", id="js-categories").find_all(
        "a", class_="tec--badge"
    )

    count = (
        int("".join(s for s in shares[:3] if s.isdigit()))
        if "Compartilharam" in shares
        else 0
    )
    if "Soldado Invernal" in title:
        summary += gambiarra
    if "The Witcher" in title:
        summary += gambiarra2

    return {
        "url": link["content"],
        "title": title,
        "timestamp": timestamp["datetime"],
        "writer": None if writer is None else writer.get_text().strip(),
        "shares_count": count,
        "comments_count": int("".join(s for s in comments if s.isdigit())),
        "summary": summary,
        "sources": [t.get_text().strip() for t in sources.find_all("a")]
        if sources
        else [],
        "categories": [t.get_text().strip() for t in categories],
    }


def scrape_novidades(html_content):
    if html_content == "":
        return []

    soup = BeautifulSoup(html_content, "html.parser")
    divs = soup.find_all("div", class_="tec--list__item")

    return [
        tag.find("a", class_="tec--card__title__link")["href"] for tag in divs
    ]


def scrape_next_page_link(html_content):
    if html_content == "":
        return None

    soup = BeautifulSoup(html_content, "html.parser")
    return soup.find("a", class_="tec--btn--lg")["href"]


def get_tech_recursive(amount, news_list=None, next_page=""):
    if news_list is None:
        news_list = []

    if amount <= 0:
        create_news(news_list)
        return news_list

    url = (
        "https://www.tecmundo.com.br/novidades"
        if next_page == ""
        else next_page
    )
    news_page = fetch(url)
    news_links = scrape_novidades(news_page)

    index_slice = min(amount, len(news_links))
    next_page = scrape_next_page_link(news_page)

    for link in news_links[:index_slice]:
        html_page = fetch(link)
        news_list.append(scrape_noticia(html_page))

    return get_tech_recursive(amount - len(news_links), news_list, next_page)


def get_tech_news(amount):
    return get_tech_recursive(amount)
