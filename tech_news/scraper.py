import time
import requests

# import pandas as pd
from requests.exceptions import ReadTimeout
from parsel import Selector


# Requisito 1
def fetch(url):
    time.sleep(1)
    try:
        response = requests.get(url, timeout=3)
    except ReadTimeout:
        return None

    return response.text if response.status_code == 200 else None


# Requisito 2
def scrape_noticia(html_content):
    selector = Selector(text=html_content)
    GET_URL = selector.css("head link[rel=canonical]::attr(href)").get()
    GET_TITLE = selector.css("#js-article-title::text").get()
    GET_TIMESTAMP = selector.css("#js-article-date::attr(datetime)").get()
    GET_WRITER = selector.css("#js-author-bar > div > p > a::text").get()
    GET_SHARES_COUNT = selector.css(
        "#js-author-bar > nav > div:nth-child(1)::text"
    ).re_first(r"\d+")
    SHARES = int(GET_SHARES_COUNT) if GET_SHARES_COUNT else 0
    GET_COMMENTS_COUNT = int(
        selector.css("#js-comments-btn::text").re_first(r"\d+")
    )
    SUMMARY = selector.css(".tec--article__body > p *::text").getall()
    GET_SUMMARY = "".join(SUMMARY)
    GET_SOURCES = selector.css(".z--mb-16 .tec--badge::text").getall()
    GET_CATEGORIES = selector.css("#js-categories > a *::text").getall()
    dic_news = {
        "url": GET_URL,
        "title": GET_TITLE,
        "timestamp": GET_TIMESTAMP,
        "writer": GET_WRITER,
        "shares_count": SHARES,
        "comments_count": GET_COMMENTS_COUNT,
        "summary": GET_SUMMARY,
        "sources": GET_SOURCES,
        "categories": GET_CATEGORIES,
    }
    return dic_news


# Requisito 3
def scrape_novidades(html_content):
    """Seu código deve vir aqui"""


# Requisito 4
def scrape_next_page_link(html_content):
    """Seu código deve vir aqui"""


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""


"""
    if __name__ == "__main__":
    URL = ""
    response = fetch(URL)
    news = scrape_noticia(response)
    print(news)
"""
