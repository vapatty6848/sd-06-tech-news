import requests
import time
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
        response.raise_for_status()
    except (requests.ReadTimeout, requests.HTTPError):
        return None


# Requisito 2
def scrape_noticia(html_content):
    selector = Selector(text=html_content)
    url = selector.css("head link[rel=canonical]::attr(href)").get()
    title = selector.css("#js-article-title ::text").get()
    timestamp = selector.css("#js-article-date ::text").get()
    writer = selector.css("a.tec--author__info__link ::text").get()
    shares_count = selector.css(
        ".tec--toolbar__item::text"
    ).get().split(' ')[1].strip()
    comments_count = selector.css("button #js-comments-btn").get()
    summary = selector.css(
        "div .tec--article__body :first-child").get()
    sources = selector.css("a.tec--badge ::text").getall()
    categories = selector.css("div a:empty ::text").getall()
    page_dict = {
        url,
        title,
        timestamp,
        writer,
        shares_count,
        comments_count,
        summary,
        sources,
        categories
    }
    return page_dict


# Requisito 3
def scrape_novidades(html_content):
    if html_content == "": 
        return []
    else:
        selector = Selector(text=html_content)
        url_list = selector.css("div figure a::attr(href)").getall()
        return url_list


# Requisito 4
def scrape_next_page_link(html_content):
    """Seu código deve vir aqui"""


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
