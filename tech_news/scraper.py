from parsel import Selector
from tech_news.database import create_news
import requests
import time

tecmundo = "https://www.tecmundo.com.br/novidades"


def remove_spaces(items):
    return [item[1:-1] for item in items]


# Requisito 1
def fetch(url):
    """Seu código deve vir aqui"""
    try:
        time.sleep(1)
        result = requests.get(url, timeout=3)
    except requests.ReadTimeout:
        return None
    else:
        status = result.status_code
        if status != 200:
            return None
        return result.text


# Requisito 2
def scrape_noticia(html_content):
    """Seu código deve vir aqui"""
    selector = Selector(text=html_content)
    url = selector.css('head link[rel=canonical]::attr(href)').get()
    title = selector.css('.tec--article__header__title::text').get()
    timestamp = selector.css('time::attr(datetime)').get()
    writer_exists = selector.css('.tec--author__info__link::text').get()
    writer = writer_exists[1:-1] if writer_exists is not None else None
    shares = selector.css('.tec--toolbar__item::text').get()
    shares_count = int(shares[1] if shares is not None else 0)
    comments = selector.css('#js-comments-btn::attr(data-count)').get()
    comments_count = int(comments) if comments is not None else 0
    summary = selector.css(
        '.tec--article__body p:first-child *::text'
    ).getall()
    sources = remove_spaces(selector.css('.z--mb-16 a::text').getall())
    categories = remove_spaces(selector.css('#js-categories a::text').getall())

    obj = {
        "url": url,
        "title": title,
        "timestamp": timestamp,
        "writer": writer,
        "shares_count": shares_count,
        "comments_count": comments_count,
        "summary": ''.join(summary),
        "sources": sources,
        "categories": categories
    }
    return obj


# Requisito 3
def scrape_novidades(html_content):
    """Seu código deve vir aqui"""
    if html_content == "" or None:
        return []
    selector = Selector(text=html_content)
    urls = selector.css(
        '.tec--list__item .tec--card__title__link::attr(href)'
    ).getall()
    return urls


# Requisito 4
def scrape_next_page_link(html_content):
    """Seu código deve vir aqui"""
    selector = Selector(text=html_content)
    next_page = selector.css('.tec--btn::attr(href)').get()
    return next_page


# Requisito 5
def get_tech_news(amount):
    next_page = tecmundo
    result = []
    while next_page:
        content = fetch(next_page)
        news = scrape_novidades(content)
        for url in news:
            details_content = fetch(url)
            notice = scrape_noticia(details_content)
            result.append(notice)
            if amount == len(result):
                create_news(result)
                return result
        next_page = scrape_next_page_link(content)
