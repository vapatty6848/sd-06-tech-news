import requests
import time
from parsel import Selector


def fetch(url):
    time.sleep(1)
    try:
        response = requests.get(url, timeout=3)
    except requests.ReadTimeout:
        return None
    if response.status_code == 200:
        return response.text
    else:
        return None


def scrape_noticia(html_content):
    selector = Selector(text=html_content)
    title = selector.css(".tec--article__header__title::text").get()
    url = selector.css('[rel="canonical"]::attr(href)').get(),
    timestamp = selector.css("#js-article-date::attr(datetime)")
    shares_count = int(
        selector.css(".tec--toolbar__item::text").get().split()[0]) or 0
    comments_count = int(
        selector.css(".tec--toolbar__item *::text").get().split()[0])

    return {
        "url": url,
        "title": title,
        "timestamp": timestamp,
        "shares_count": shares_count,
        "comments_count": comments_count
    }


# Requisito 3
def scrape_novidades(html_content):
    """Seu código deve vir aqui"""


# Requisito 4
def scrape_next_page_link(html_content):
    """Seu código deve vir aqui"""


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
