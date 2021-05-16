import requests
import time
from parsel import Selector
from tech_news.database import create_news


# Requisito 1
def fetch(url):
    time.sleep(1)
    try:
        response = requests.get(url, timeout=3)
    except requests.ReadTimeout:
        return None
    if response.status_code == 200:
        return response.text
    else:
        return None


# Requisito 2
def scrape_noticia(html_content):
    selector = Selector(html_content)
    url_get = selector.css("[rel=canonical]::attr(href)").get()
    title_get = selector.css('.tec--article__header__title::text').get()
    timestamp_get = selector.css('#js-article-date::attr(datetime)').get()
    writer_get = selector.css('.tec--author__info__link::text').get()
    writer = writer_get.strip() if writer_get else None
    shares_count_get = selector.css('.tec--toolbar__item::text').get()
    shares_count = int(shares_count_get.split()[0]) if shares_count_get else 0
    comments_count_get = selector.css(
        '.tec--toolbar__item #js-comments-btn::attr(data-count)').get()
    comments_count = int(comments_count_get) if comments_count_get else 0
    summary_getall = selector.css(
        '.tec--article__body p:first-child *::text').getall()
    summary = ''.join(summary_getall)
    sources_get = selector.css('.z--mb-16 .tec--badge::text').getall()
    sources = [source.strip() for source in sources_get]
    categories_getall = selector.css('#js-categories a::text').getall()
    categories = [categories.strip() for categories in categories_getall]

    dictionary_attributes = {
        'url': url_get,
        'title': title_get,
        'timestamp': timestamp_get,
        'writer': writer,
        'shares_count':  shares_count,
        'comments_count': comments_count,
        'summary': summary,
        'sources': sources,
        'categories': categories
    }
    return dictionary_attributes


# Requisito 3
def scrape_novidades(html_content):
    selector = Selector(html_content)
    url_lists = selector.css("h3.tec--card__title a::attr(href)").getall()
    if url_lists == "":
        return []
    return url_lists


# Requisito 4
def scrape_next_page_link(html_content):
    selector = Selector(html_content)
    next_page_url = selector.css(
        ".tec--list > a::attr(href)").get()
    if not next_page_url:
        return None
    return next_page_url


# Requisito 5
def get_tech_news(amount):
    url = "https://www.tecmundo.com.br/novidades"
    news_db = []
    while url:
        response = fetch(url)
        url_list = scrape_novidades(response)
        for news_list in url_list:
            response_news = fetch(news_list)
            new_news = scrape_noticia(response_news)
            news_db.append(new_news)
            if amount == len(news_db):
                create_news(news_db)
                return news_db
        url = scrape_next_page_link(response)
