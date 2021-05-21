from tech_news.database import create_news
import requests
from requests.exceptions import Timeout
import time
from parsel import Selector
import re


# Requisito 1


def fetch(url):
    time.sleep(1)
    try:
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except Timeout:
        return None


# Requisito 2


def scrape_noticia(html_content):
    selector = Selector(text=html_content)
    url = selector.css("head link[rel=canonical]::attr(href)").get()
    title = selector.css(".tec--article__header__title::text").get()
    timestamp = selector.css("#js-article-date::attr(datetime)").get()
    writer = selector.css(
        "#js-author-bar > div > p.z--m-none.z--truncate.z--font-bold > a::text"
    ).get()
    writer = selector.css(
        "#js-author-bar > div > p.z--m-none.z--truncate.z--font-bold > a::text"
    ).get()
    writer = writer.strip() if writer else None
    shares_count = selector.css(
        "#js-author-bar > nav > div:nth-child(1)::text"
    ).get()
    shares_count = shares_count.split(" ")[1] if shares_count else 0
    comments_count = selector.css("#js-comments-btn::attr(data-count)").get()
    summary = selector.css(
        ".tec--article__body p:nth-child(1) *::text"
    ).getall()
    summary = "".join(summary)
    sources = selector.css(".z--mb-16 .tec--badge::text").getall()
    sources = [source.strip() for source in sources]
    categories = selector.css("#js-categories > a.tec--badge::text").getall()
    categories = [category.strip() for category in categories]

    news = {
        "url": url,
        "title": title,
        "timestamp": timestamp,
        "writer": writer,
        "shares_count": int(shares_count),
        "comments_count": int(comments_count),
        "summary": summary,
        "sources": sources,
        "categories": categories,
    }

    return news


# Requisito 3


def scrape_novidades(html_content):
    if not html_content:
        return []
    selector = Selector(text=html_content)
    urls = selector.css(".tec--card__info > h3 > a::attr(href)").getall()
    return urls


# Requisito 4
def scrape_next_page_link(html_content):
    selector = Selector(text=html_content)
    load_more = selector.css(".tec--list.tec--list--lg > a::attr(href)").get()
    return load_more


# Requisito 5
def get_tech_news(amount):
    url = "https://www.tecmundo.com.br/novidades"
    urls = []

    while len(urls) < amount:
        request = fetch(url)
        urls.extend(scrape_novidades(request))
        url = scrape_next_page_link(request)

    news_group = urls[:amount]
    news_list = []
    for news in news_group:
        news_list.append(scrape_noticia(fetch(news)))

    try:
        create_news(news_list)

    except Exception as error:
        print(error)

    return news_list
