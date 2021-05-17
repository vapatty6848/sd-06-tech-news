import requests
import time
from parsel import Selector
from tech_news.database import create_news


def strip(items):
    return [item.strip() for item in items]


# Requisito 1
def fetch(url, sleep=1, timeout=3):
    time.sleep(sleep)
    try:
        response = requests.get(url, timeout=timeout)
    except requests.Timeout:
        return None
    if (response.status_code != 200):
        return None
    return response.text


# Requisito 2
def scrape_noticia(html_content):
    selector = Selector(text=html_content)
    url = selector.css('head link[rel=canonical]::attr(href)').get()
    title = selector.css('.tec--article__header__title::text').get()
    date_time = selector.css('time::attr(datetime)').get()

    writer = selector.css('.tec--author__info__link::text').get()
    verify_writer = writer.strip() if (writer) else None

    shares_count = selector.css('.tec--toolbar__item::text').get()
    verify_shares = int(shares_count.split()[0]) if (shares_count) else 0

    comments_count = int(selector.css(
        '#js-comments-btn::attr(data-count)'
        ).get())

    summary = selector.css(
        ".tec--article__body p:first-child *::text"
    ).getall()
    summary_join = "".join(summary)

    sources = strip(selector.css('.z--mb-16 a::text').getall())
    categories = strip(selector.css('#js-categories a::text').getall())

    obj = {
        "url": url,
        "title": title,
        "timestamp": date_time,
        "writer": verify_writer,
        "shares_count": verify_shares,
        "comments_count": comments_count,
        "summary": summary_join,
        "sources": sources,
        "categories": categories
    }
    return obj


# Requisito 3
def scrape_novidades(html_content):
    selector = Selector(text=html_content)
    url = selector.css("div.tec--card__info > h3 > a::attr(href)").getall()
    return url


# Requisito 4
def scrape_next_page_link(html_content):
    selector = Selector(text=html_content)
    url = selector.css('a.tec--btn::attr(href)').get()
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
                try:
                    create_news(news_inserted)
                    return news_inserted
                except ValueError:
                    raise ValueError('Database Error')
        url = scrape_next_page_link(response)
