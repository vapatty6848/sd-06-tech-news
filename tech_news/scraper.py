import requests
from parsel import Selector
import time
from tech_news.database import create_news


# Requisito 1
def fetch(url):
    try:
        response = requests.get(url, timeout=3)
        time.sleep(1)

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
    news = {
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
    return news


# Requisito 3
def scrape_novidades(html_content):
    selector = Selector(text=html_content)
    urls = selector.css(
        ".tec--list a.tec--card__title__link::attr(href)"
    ).getall()
    return urls


# Requisito 4
def scrape_next_page_link(html_content):
    selector = Selector(text=html_content)
    url = selector.css('.tec--list > a::attr(href)').get() or None
    return url


# Requisito 5
def get_tech_news(amount):
    url = "https://www.tecmundo.com.br/novidades"
    news_inserted = []
    while True:
        response = fetch(url)
        news_current_page = scrape_novidades(response)
        for new in news_current_page:
            news_next_page = fetch(new)
            next_news = scrape_noticia(news_next_page)
            news_inserted.append(next_news)
            if len(news_inserted) == amount:
                create_news(news_inserted)
                return news_inserted
        url = scrape_next_page_link(response)
