import requests
import time
from tech_news.scraper_utils import (
    get_categories,
    get_sources,
    get_writer,
    get_shares_count,
    get_comments_count,
    get_url,
    get_timestamp,
    get_summary,
)
from parsel import Selector


# Requisito 1
def fetch(url):
    """Faz a request HTTP e obtém o HTML"""
    time.sleep(1)
    try:
        response = requests.get(url, timeout=3)
        response.raise_for_status()
        contents = response.text
        # print(type(contents))
        return contents
    except (requests.exceptions.HTTPError, requests.ReadTimeout) as err:
        print(err)
        return None


# Requisito 2
def scrape_noticia(html_content):
    """Extrai dados de notícias de uma página html"""
    selector = Selector(text=html_content)

    noticia = {}
    noticia['url'] = get_url(selector)
    noticia['title'] = selector.css('main article h1::text').get()
    noticia['timestamp'] = get_timestamp(selector)
    noticia['writer'] = get_writer(selector)
    noticia['shares_count'] = get_shares_count(selector)
    noticia['comments_count'] = get_comments_count(selector)
    noticia['summary'] = get_summary(selector)
    noticia['sources'] = get_sources(selector)
    noticia['categories'] = get_categories(selector)

    return noticia


# Requisito 3
def scrape_novidades(html_content):
    """Faz o scrape do HTML para obter as URLs de cada notícia."""
    selector = Selector(text=html_content)

    noticias = selector.css('.tec--list div h3 a::attr(href)').getall()

    return noticias


# Requisito 4
def scrape_next_page_link(html_content):
    """Seu código deve vir aqui"""


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
