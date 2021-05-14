#!/usr/bin/env python3
import requests
import time
from parsel import Selector
from requests.exceptions import ReadTimeout


# Requisito 1
def fetch(url):
    """Seu código deve vir aqui"""
    time.sleep(1)
    try:
        response = requests.get(url, timeout=3)
    except ReadTimeout:
        return None
    if response.status_code == 200:
        return response.text
    else:
        return None


# Requisito 2
def scrape_noticia(html_content):
    """Seu código deve vir aqui"""
    seletor = Selector(html_content)
    writer_by = seletor.css('.tec--author__info__link::text').get()

    return {
        "url": seletor.css('[rel="canonical"]::attr(href)').get(),
        "title": seletor.css('.tec--article__header__title::text').get(),
        "timestamp": seletor.css('#js-article-date::attr(datetime)').get(),
        "writer": writer_by.strip(),
        "shares_count": int(seletor.css(
            '.tec--toolbar__item::text'
        ).get().split()[0]),
        "comments_count": int(seletor.css(
            '.tec--toolbar__item *::text'
        ).getall()[2].split()[0]),
        "summary": ''.join(seletor.css(
            '.tec--article__body p:first-child *::text'
        ).getall()),
        "sources": [i.strip() for i in seletor.css(
            '[rel="noopener nofollow"]::text'
        ).getall()],
        "categories": [i.strip() for i in seletor.css(
            '#js-categories a::text'
        ).getall()],
    }


# Requisito 3
def scrape_novidades(html_content):
    """Seu código deve vir aqui"""
    selector = Selector(html_content)
    url = selector.css("h3.tec--card__title a::attr(href)").getall()
    return url


# Requisito 4
def scrape_next_page_link(html_content):
    """Seu código deve vir aqui"""
    selector = Selector(html_content)
    urls = selector.css('div.tec--list--lg a::attr(href)').getall()
    if (len(urls) < 1):
        return None
    else:
        url = urls[len(urls) - 1]
        return url


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
    # url = 'https://www.tecmundo.com.br/novidades'
    # html_news = fetch(url)
    # lista_news = scrape_novidades(html_news)
    # news = []
    # while (len(news) < amount):
    #     html_att = fetch(lista_news[len(news)])
    #     obj_data = scrape_noticia(html_att)
    #     news.append(obj_data)
    # print(news)


# if __name__ == "__main__":
