import requests
import time
from requests.exceptions import ReadTimeout
from parsel import Selector


# Requisito 1
def fetch(url):
    time.sleep(1)
    try:
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except ReadTimeout:
        return None


def get_url(content):
    selector = Selector(text=content)
    return selector.css("link[rel=canonical]::attr(href)").get()


def get_shares_info(html_content):
    selector = Selector(text=html_content)
    shares_info = selector.css("div.tec--toolbar__item::text").get()
    shares_suffix = " Compartilharam"
    shares_mutated = 0
    if shares_info:
        shares_mutated = int(shares_info[1:-len(shares_suffix)])

    return shares_mutated


def get_writer_info(html_content):
    selector = Selector(text=html_content)
    writer_info = selector.css("a.tec--author__info__link::text").get()
    writer_mutated = ""
    if writer_info:
        writer_mutated = writer_info[1:len(writer_info) - 1]
    else:
        writer_mutated = None

    return writer_mutated


# Requisito 2
def scrape_noticia(html_content):
    selector = Selector(text=html_content)

    url_info = get_url(html_content)

    title_info = selector.css("h1#js-article-title::text").get()

    time_info = selector.css("time::attr(datetime)").get()

    writer_info = get_writer_info(html_content)

    shares_info = get_shares_info(html_content)

    comments_info = selector.css("button::attr(data-count)").get()
    comments_mutated = 0
    if comments_info:
        comments_mutated = int(comments_info)

    summary_info = selector.css(
        "div.tec--article__body > p:nth-child(1) *::text"
    ).getall()
    summary_mutated = "".join(summary_info)

    sources_info = selector.css("div.z--mb-16 div *::text").getall()
    sources_mutated = []
    index = 0
    while index < len(sources_info):
        indexed_source = sources_info[index]
        indexed_source_mutated = indexed_source[1:len(indexed_source) - 1]
        if len(indexed_source_mutated) > 1:
            sources_mutated.append(indexed_source_mutated)
        index += 1

    categories_info = selector.css("a.tec--badge--primary *::text").getall()
    categories_mutated = []
    index = 0
    while index < len(categories_info):
        indexed_category = categories_info[index]
        categories_mutated.append(
            indexed_category[1:len(indexed_category) - 1]
        )
        index += 1

    return {
        "url": url_info,
        "title": title_info,
        "timestamp": time_info,
        "writer": writer_info,
        "shares_count": shares_info,
        "comments_count": comments_mutated,
        "summary": summary_mutated,
        "sources": sources_mutated,
        "categories": categories_mutated,
    }


# Requisito 3
def scrape_novidades(html_content):
    """Seu código deve vir aqui"""


# Requisito 4
def scrape_next_page_link(html_content):
    """Seu código deve vir aqui"""


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
