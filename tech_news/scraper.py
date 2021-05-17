import requests
from parsel import Selector
import time


# Requisito 1
def fetch(url):
    try:
        response = requests.get(url, timeout=3)
        time.sleep(3)

        if response.status_code != 200:
            return None

        return response.text

    except requests.Timeout:
        return None


# Requisito 2
def scrape_noticia(html_content):
    selector = Selector(text=html_content)

    url = selector.css("head link[rel=canonical]::attr(href)").get()
    title = selector.css("#js-article-title::text").get()
    timestamp = selector.css("#js-article-date::attr(datetime)").get()
    writer = (
        selector.css("#js-author-bar > div > p > a::text").get().strip()
    )
    shares_count = selector.css(
        "#js-author-bar > nav > div:nth-child(1)::text"
    ).re_first(r"\d+")
    shares_new = int(shares_count) if shares_count else 0
    comments_count = int(
        selector.css("#js-comments-btn::text").re_first(r"\d+")
    )
    summary = selector.css(
        ".tec--article__body > p:nth-child(1) *::text"
    ).getall()

    summary_new = "".join(summary)
    sources = selector.css(".z--mb-16 .tec--badge::text").getall()
    sources_new = [source.strip() for source in sources]
    categories = selector.css("#js-categories > a *::text").getall()
    categories_new = [category.strip() for category in categories]

    allNews = {
        "url": url,
        "title": title,
        "timestamp": timestamp,
        "writer": writer,
        "shares_count": shares_new,
        "comments_count": comments_count,
        "summary": summary_new,
        "sources": sources_new,
        "categories": categories_new,
    }

    return allNews


# Requisito 3
def scrape_novidades(html_content):
    selector = Selector(text=html_content)
    newsSection = selector.css(
        '.tec--list a.tec--card__title__link::attr(href)'
    ).getall()

    return newsSection


# Requisito 4
def scrape_next_page_link(html_content):
    selector = Selector(text=html_content)
    nextPage = selector.css('.tec--list > a::attr(href)').get() or None

    return nextPage


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
