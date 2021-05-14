import requests
import time
import utils
from parsel import Selector
from bs4 import BeautifulSoup


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

    noticia['url'] = selector.xpath(
        '//meta[@property="og:url"]/@content').get()

    noticia['title'] = selector.css('main article h1::text').get()

    noticia['timestamp'] = selector.css(
        'main article time::attr(datetime)').get()

    noticia['writer'] = selector.css(
        'main article .tec--author__info__link::text').get()
    if noticia['writer'] is not None:
        noticia['writer'].strip()

    shares = selector.css(
        'nav.tec--toolbar *::text').get()
    if shares is not None:
        shares_count = shares.split()[0].strip()
        noticia['shares_count'] = int(shares_count)

    noticia['comments_count'] = 0
    comments = selector.css(
        'nav.tec--toolbar button *::text').getall()
    if len(comments) > 0:
        comments_count = comments[1].split()[0]
        noticia['comments_count'] = int(comments_count)

    raw_summary = selector.css('.tec--article__body p').getall()[0]
    noticia['summary'] = BeautifulSoup(raw_summary, 'html').text

    noticia['sources'] = []
    sources = selector.css(
        '.tec--badge:not(.tec--badge--primary)::text').getall()
    for source in sources:
        noticia['sources'].append(source.strip())

    noticia['categories'] = []
    categories = selector.css('.tec--badge--primary::text').getall()
    for cat in categories:
        noticia['categories'].append(cat.strip())

    return noticia


# Requisito 3
def scrape_novidades(html_content):
    """Seu código deve vir aqui"""


# Requisito 4
def scrape_next_page_link(html_content):
    """Seu código deve vir aqui"""


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
