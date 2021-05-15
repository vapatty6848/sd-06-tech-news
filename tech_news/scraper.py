import requests
import parsel
from time import sleep
from tech_news.database import create_news


# Requisito 1
def fetch(url):
    """Seu código deve vir aqui!"""
    try:
        response = requests.get(url, timeout=3)
        sleep(1)
        if response.status_code != 200:
            return None
        return response.text
    except requests.Timeout:
        return None


# Requisito 2
def scrape_noticia(html_content):
    """Seu código deve vir aqui!"""
    selector = parsel.Selector(html_content)

    URL = selector.css("head link[rel=canonical]::attr(href)").get()
    TITLE = selector.css("h1::text").get()
    TIMESTAMP = selector.css(
        ".tec--timestamp__item"
    ).xpath(
        "./time/@datetime"
    ).get()
    WRITER_MALFORMED = selector.css(
        "#js-author-bar .z--font-bold a::text"
    ).get()
    WRITER = WRITER_MALFORMED.strip() if WRITER_MALFORMED else None
    SHARES_MALFORMED = selector.css(
        ".tec--toolbar__item::text"
    ).re_first(r"\d+")
    SHARES_COUNT = int(SHARES_MALFORMED) if SHARES_MALFORMED else 0
    COMMENTS_MALFORMED = selector.css(
        "#js-comments-btn::attr(data-count)"
    ).get()
    COMMENTS_COUNT = int(COMMENTS_MALFORMED) if COMMENTS_MALFORMED else 0
    SUMMARY_MALFORMED = selector.css(
        ".tec--article__body p:nth-child(1) *::text"
    ).getall()
    SUMMARY = ''.join(SUMMARY_MALFORMED)
    GET_SOURCES = selector.css(".z--mb-16 .tec--badge::text").getall()
    SOURCES = [source.strip() for source in GET_SOURCES]
    GET_CATEGORIES = selector.css("#js-categories > a *::text").getall()
    CATEGORIES = [category.strip() for category in GET_CATEGORIES]
    result = {
        'url': URL,
        'title': TITLE,
        'timestamp': TIMESTAMP,
        'writer': WRITER,
        'shares_count': SHARES_COUNT if SHARES_COUNT else 0,
        'comments_count': COMMENTS_COUNT,
        'summary': SUMMARY,
        'sources': SOURCES,
        'categories': CATEGORIES
    }
    return result


# Requisito 3
def scrape_novidades(html_content):
    """Seu código deve vir aqui"""
    selector = parsel.Selector(html_content)
    news = selector.css("h3.tec--card__title a::attr(href)").getall()
    return news if news else []


# Requisito 4
def scrape_next_page_link(html_content):
    """Seu código deve vir aqui"""
    selector = parsel.Selector(html_content)
    next_page = selector.xpath(
        "//a[contains(text(), 'Mostrar mais notícias')]/@href"
    ).get()
    return next_page if next_page else None


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
    next_page = "https://www.tecmundo.com.br/novidades"
    result = []
    while next_page:
        response = fetch(next_page)
        news_list = scrape_novidades(response)
        for news in news_list:
            response_news = fetch(news)
            new_news = scrape_noticia(response_news)
            result.append(new_news)
            if amount == len(result):
                create_news(result)
                return result
        next_page = scrape_next_page_link(response)

