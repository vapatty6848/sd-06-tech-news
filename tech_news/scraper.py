import requests
import parsel
import time
from requests.exceptions import Timeout
from tech_news.database import create_news


# Requisito 1
def fetch(url):
    try:
        response = requests.get(url, timeout=3)
        time.sleep(1)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except Timeout:
        return None


# Requisito 2
def scrape_noticia(html_content):
    selector = parsel.Selector(html_content)

    URL = selector.css("head link[rel=canonical]::attr(href)").get()
    TITLE = selector.css("h1::text").get()
    TIMESTAMP = selector.css(
        ".tec--timestamp__item"
    ).xpath(
        "./time/@datetime"
    ).get()
    WRITER_UNFORMATED = selector.css(
        "#js-author-bar .z--font-bold a::text"
    ).get()
    WRITER = WRITER_UNFORMATED.strip() if WRITER_UNFORMATED else None
    SHARES_CNT_UNF = selector.css(
        ".tec--toolbar__item::text"
    ).re_first(r"\d+")
    SHARES_CNT = int(SHARES_CNT_UNF) if SHARES_CNT_UNF else 0
    COMMENTS_COUNT_UNF = selector.css(
        "#js-comments-btn::attr(data-count)"
    ).get()
    COMMENTS_COUNT = int(COMMENTS_COUNT_UNF) if COMMENTS_COUNT_UNF else 0
    SUMMARY_UNFORMATTED = selector.css(
        ".tec--article__body p:nth-child(1) *::text"
    ).getall()
    SUMMARY = ''.join(SUMMARY_UNFORMATTED)
    GET_SOURCES = selector.css(".z--mb-16 .tec--badge::text").getall()
    SOURCES = [source.strip() for source in GET_SOURCES]
    GET_CATEGORIES = selector.css("#js-categories > a *::text").getall()
    CATEGORIES = [category.strip() for category in GET_CATEGORIES]
    result_dict = {
        'url': URL,
        'title': TITLE,
        'timestamp': TIMESTAMP,
        'writer': WRITER,
        'shares_count': SHARES_CNT if SHARES_CNT else 0,
        'comments_count': COMMENTS_COUNT,
        'summary': SUMMARY,
        'sources': SOURCES,
        'categories': CATEGORIES
    }
    return result_dict


# Requisito 3
def scrape_novidades(html_content):
    if html_content == "":
        return []
    else:
        selector = parsel.Selector(html_content)
        list_urls = selector.css(
            "div.tec--card__info h3 a::attr(href)"
        ).getall()
        return list_urls


# Requisito 4
def scrape_next_page_link(html_content):
    selector = parsel.Selector(html_content)
    url_next_page = selector.xpath(
        "//*[@id='js-main']/div/div/div[1]/div[2]/a/@href"
    ).get()
    if (url_next_page == ""):
        return None
    else:
        return url_next_page


# Requisito 5
def get_tech_news(amount):
    next_page_url = "https://www.tecmundo.com.br/novidades"
    result = []
    while next_page_url:
        response = fetch(next_page_url)
        news_list = scrape_novidades(response)
        for news in news_list:
            response_news = fetch(news)
            new = scrape_noticia(response_news)
            result.append(new)

            if amount == len(result):
                create_news(result)
                return result

        next_page_url = scrape_next_page_link(response)
