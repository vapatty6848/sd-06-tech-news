import requests
from parsel import Selector
import time
from tech_news.database import create_news


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
    selector = Selector(html_content)

    url = selector.css("head link[rel=canonical]::attr(href)").get()
    title = selector.css(".tec--article__header__title::text").get()
    timestamp = selector.css("#js-article-date::attr(datetime)").get()

    get_writer = selector.css(".tec--author__info__link::text").get()
    writer = get_writer.strip() if get_writer else None

    get_shares_count = selector.css(
        "#js-author-bar > nav > div:nth-child(1)::text"
    ).re_first(r"\d+")
    share_count = int(get_shares_count) if get_shares_count else 0

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

    allNews = {
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
    url = "https://www.tecmundo.com.br/novidades"
    allNews = []
    while len(allNews) < amount:
        request = fetch(url)
        newsList = scrape_novidades(request)
        for item in newsList:
            newsURL = fetch(item)
            allNews.append(scrape_noticia(newsURL))
            if len(allNews) == amount:
                create_news(allNews)
                return allNews
        url = scrape_next_page_link(request)
