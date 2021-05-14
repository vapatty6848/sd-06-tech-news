# Requisito 1
import requests
import time
from parsel import Selector


def fetch(url):
    """Seu código deve vir aqui"""
    try:
        response = requests.get(url, timeout=2)
        time.sleep(1)
        response.raise_for_status()
    except Exception:
        return None
    else:
        return response.text


# Requisito 2
def scrape_noticia(html_content):
    """Seu código deve vir aqui"""
    Selector(html_content)
    title = Selector.css(".tec--article__header__title::text").get().strip()
    timestamp = (
        Selector.css(".tec--timestamp tec--timestamp--lg::text").get().strip()
    )
    writer = Selector.css(".tec--author__info__link::text").get().strip()
    shares_count = Selector.css(".tec-toolbar__item::text").get()
    comments_count = Selector.css(".comment-count::text").get()
    summary = (
        Selector.css(".tec--article__body z--px-16 p402_premium::text")
        .get()
        .split()[0]
    )
    sources = Selector.css("tec-badge::text").get()
    categories = Selector.css("#js-categories *::text").get()
    return {
        "title": title,
        "timestamp": timestamp,
        "writer": writer,
        "shares_count": shares_count,
        "comments_count": comments_count,
        "summary": summary,
        "sources": sources,
        "categories": categories,
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
