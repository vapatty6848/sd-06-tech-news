#!/usr/bin/env python3
import requests
import time
from parsel import Selector
from requests.exceptions import ReadTimeout
from tech_news.database import create_news


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
    if writer_by is None:
        writer_by = seletor.css(
            '.tec--timestamp__item.z--font-bold>a::text'
        ).get()
        if writer_by is not None:
            writer_by = writer_by.strip()
    else:
        writer_by = writer_by.strip()

    shares_count_info = seletor.css(
            '.tec--toolbar__item::text'
        ).get()
    if shares_count_info is not None:
        shares_count_info = int(shares_count_info.split()[0])
    else:
        shares_count_info = 0

    comments_count_info = seletor.css(
            '.tec--toolbar__item *::text'
        ).getall()
    if len(comments_count_info) == 3:
        comments_count_info = int(comments_count_info[2].split()[0])
    else:
        comments_count_info = int(comments_count_info[1].split()[0])

    return {
        "url": seletor.css('[rel="canonical"]::attr(href)').get(),
        "title": seletor.css('.tec--article__header__title::text').get(),
        "timestamp": seletor.css('#js-article-date::attr(datetime)').get(),
        "writer": writer_by,
        "shares_count": shares_count_info,
        "comments_count": comments_count_info,
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
    news_to_save = []
    url = "https://www.tecmundo.com.br/novidades"
    news_page = fetch(url)
    News_list = scrape_novidades(news_page)
    print(news_page)

    while len(news_to_save) < amount:
        for news in News_list:
            news_html = fetch(news)
            news_to_save.append(scrape_noticia(news_html))
            if len(news_to_save) == amount:
                break
        next_url = scrape_next_page_link(news_page)
        news_page = fetch(next_url)
        News_list = scrape_novidades(news_page)

    create_news(news_to_save)

    return news_to_save


if __name__ == "__main__":
    print(get_tech_news(3))
    # htmlgg = fetch(
    #   'https://www.tecmundo.com.br/redes-sociais/217386-encontrar-grupos-telegram.htm
    # ')
    # print(htmlgg)
    # print(scrape_noticia(htmlgg))
