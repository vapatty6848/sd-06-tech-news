#!/usr/bin/env python3
import requests
import time
from parsel import Selector


# Requisito 1
def fetch(url):
    time.sleep(1)
    try:
        response = requests.get(url, timeout=3)
        response.raise_for_status()
        return response.text
    except requests.exceptions.ReadTimeout:
        return None
    except requests.exceptions.HTTPError:
        return None


# Requisito 2
def scrape_noticia(html_content):
    selector = Selector(html_content)

    url = selector.css('[rel="canonical"]::attr(href)').get()
    title = selector.css('.tec--article__header__title::text').get()
    timestamp = selector.css('#js-article-date::attr(datetime)').get()
    shares_count = int(
        selector.css('.tec--toolbar__item::text')
        .get()
        .split()[0]
    )
    comments_count = int(
        selector.css('.tec--toolbar__item *::text')
        .getall()[2].split()[0]
    )
    summary = selector.css('.tec--article__body z--px-16 p402_premium')
    writer = selector.css('.tec--author__info__link::text').get().strip()
    url = selector.css('[rel="canonical"]::attr(href)').get()
    summary = ''.join(
        selector.css('.tec--article__body p:first-child *::text')
        .getall()
    )
    sources = [
        i.strip() for i in selector.css('[rel="noopener nofollow"]::text')
        .getall()
    ]

    categories = [
        i.strip() for i in selector.css('#js-categories a::text')
        .getall()
    ]

    result = {
        "url": url,
        "title": title,
        "timestamp": timestamp,
        "shares_count": shares_count,
        "comments_count": comments_count,
        "summary": summary,
        "writer": writer,
        "sources": sources,
        "categories": categories,
    }

    return result


# Requisito 3
def scrape_novidades(html_content):
    """Seu código deve vir aqui"""


# Requisito 4
def scrape_next_page_link(html_content):
    """Seu código deve vir aqui"""


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""


if __name__ == "__main__":
    scrape_noticia(fetch("https://www.tecmundo.com.br/mobilidade-urbana-smart-cities/155000-musk-tesla-carros-totalmente-autonomos.htm"))
