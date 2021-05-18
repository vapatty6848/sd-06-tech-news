import requests
import time
from parsel import Selector


# Requisito 1
def fetch(url):
    """Seu código deve vir aqui"""
    time.sleep(1)
    try:
        response = requests.get(url, timeout=3)
    except requests.ReadTimeout:
        return None
    if response.status_code != 200:
        return None
    return response.text


# Requisito 2
def scrape_noticia(html_content):
    """Seu código deve vir aqui"""
    selector = Selector(html_content)
    url = selector.css("head link[rel=canonical]::attr(href)").get()
    title = selector.css(".tec--article__header__title::text").get()
    timestamp = selector.css("#js-article-date::attr(datetime)").get()
    get_writer = selector.css(".tec--author__info__link::text").get()
    writer = get_writer.strip() if get_writer else None
    get_shares_count = selector.css(".tec--toolbar__share::text").get()
    share_count = int(get_shares_count.split()[0]) if get_shares_count else 0
    comments_count = int(
        selector.css("#js-comments-btn::attr(data-count)").get()
    )
    get_summary = selector.css(
        ".tec--article__body p:first-child *::text"
    ).getall()
    summary = "".join(get_summary)
    get_sources = selector.css(".z--mb-16 .tec--badge::text").getall()
    sources = [source.strip() for source in get_sources]
    get_categories = selector.css("#js-categories > a *::text").getall()
    categories = [category.strip() for category in get_categories]
    News = {
        "url": url,
        "title": title,
        "timestamp": timestamp,
        "writer": writer,
        "shares_count": share_count,
        "comments_count": comments_count,
        "summary": summary,
        "sources": sources,
        "categories": categories,
    }

    return News


# Requisito 3
def scrape_novidades(html_content):
    """Seu código deve vir aqui"""
    selector = Selector(text=html_content)
    news = selector.css(
        "h3.tec--card__title a.tec--card__title__link::attr(href)"
    ).getall()
    return news


# Requisito 4
def scrape_next_page_link(html_content):
    """Seu código deve vir aqui"""


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
