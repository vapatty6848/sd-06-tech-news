import time
import requests
from requests.exceptions import HTTPError, ReadTimeout
import parsel


# Requisito 1
def fetch(url):
    """Função para fazer a requisição HTTP"""
    time.sleep(1)
    try:
        response = requests.get(url, timeout=3)
    except ReadTimeout as error:
        print(f"Timeout Error: {error}.")
        return None

    try:
        response.raise_for_status()
    except HTTPError as error:
        print(f"HTTP Error: {error}.")
        return None

    return response.text


# Requisito 2
def scrape_noticia(html_content):
    """Função para fazer o scrape de noticias"""
    selector = parsel.Selector(html_content)

    url = selector.css("head link[rel=canonical]::attr(href)").get()
    title = selector.css("h1::text").get()
    timeStamp = selector.css(
        ".tec--timestamp__item"
    ).xpath("./time/@datetime").get().strip()

    writer = selector.css(".z--font-bold a::text").get().strip()
    sharesCount = selector.css(
        ".tec--toolbar__item::text"
    ).get().split(' ')[1].strip()

    commentsCount = selector.css("#js-comments-btn::attr(data-count)").get()
    summary = selector.css(
        ".tec--article__body > p:nth-child(1) *::text"
    ).getall()

    sources = selector.css(".z--mb-16 .tec--badge::text").getall()
    categories = selector.css("#js-categories > a *::text").getall()

    return {
        'url': url,
        'title': title,
        'timestamp': timeStamp,
        'writer': writer,
        'shares_count': int(sharesCount),
        'comments_count': int(commentsCount),
        'summary': ''.join(summary),
        'sources': [source.strip() for source in sources],
        'categories': [category.strip() for category in categories]
    }


# Requisito 3
def scrape_novidades(html_content):
    """Função para fazer o scrape de novidades"""
    selector = parsel.Selector(text=html_content)
    novidades = selector.css("h3.tec--card__title a::attr(href)").getall()

    return novidades if novidades else []


# Requisito 4
def scrape_next_page_link(html_content):
    """Função para fazer o scrape do link da proxima página"""
    selector = parsel.Selector(text=html_content)
    link = selector.css('.tec--list > a::attr(href)').get() or None

    return link


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
