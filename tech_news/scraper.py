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
    get_url = selector.css("head link[rel=canonical]::attr(href)").get()
    get_title = selector.css("#js-article-title::text").get()
    get_timestamp = selector.css("#js-article-date::attr(datetime)").get()
    get_writer = (
        selector.css("#js-author-bar > div > p > a::text").get().strip()
    )
    get_shares_count = selector.css(
        "#js-author-bar > nav > div:nth-child(1)::text"
    ).re_first(r"\d+")
    shares = int(get_shares_count) if get_shares_count else 0
    get_comments_count = int(
        selector.css("#js-comments-btn::text").re_first(r"\d+")
    )
    summary = selector.css(
        ".tec--article__body > p:nth-child(1) *::text"
    ).getall()
    get_summary = "".join(summary)
    get_sources = selector.css(".z--mb-16 .tec--badge::text").getall()
    sources = [source.strip() for source in get_sources]
    get_categories = selector.css("#js-categories > a *::text").getall()
    categories = [category.strip() for category in get_categories]
    dic_news = {
        "url": get_url,
        "title": get_title,
        "timestamp": get_timestamp,
        "writer": get_writer,
        "shares_count": shares,
        "comments_count": get_comments_count,
        "summary": get_summary,
        "sources": sources,
        "categories": categories,
    }
    return dic_news


# Requisito 3
def scrape_novidades(html_content):
    if html_content == '':
        return []
    else:
        selector = Selector(text=html_content)
        news = selector.css('.tec--card__info h3 a::attr(href)').getall()
        return news


# Requisito 4
def scrape_next_page_link(html_content):
    selector = Selector(text=html_content)
    next_url = selector.css(
        "#js-main > div > div > .z--w-2-3 > div.tec--list--lg > a::attr(href)"
    ).get()
    return next_url


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""


if __name__ == "__main__":
    URL = "https://www.tecmundo.com.br/novidades"
    response = fetch(URL)
    news = scrape_next_page_link(response)
    print(news)
