#!/usr/bin/env python3
import requests
import time
from parsel import Selector
from tech_news.database import create_news


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
    shares_count = (
        selector.css('.tec--toolbar__item::text')
        .get()
    )
    comments_count = (
        selector.css('.tec--toolbar__item *::text')
        .getall()
    )
    writer = selector.css('.tec--author__info__link::text').get()
    url = selector.css('[rel="canonical"]::attr(href)').get()
    summary = ''.join(
        selector.css('.tec--article__body p:first-child *::text')
        .getall()
    )
    sources = [
        i.strip() for i in selector.css('.z--mb-16 .tec--badge::text')
        .getall()
    ]

    categories = [
        i.strip() for i in selector.css('#js-categories a::text')
        .getall()
    ]

    if (shares_count is None):
        shares_count = 0
    else:
        shares_count = shares_count.split()[0]

    if (len(comments_count) == 3):
        comments_count = int(comments_count[2].split()[0])
    else:
        comments_count = int(comments_count[1].split()[0])

    if (shares_count is None):
        shares_count = 0
    else:
        shares_count = int(shares_count)
    if (writer is not None):
        writer = writer.strip()

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
    selector = Selector(html_content)
    cardTitleSelector = "h3.tec--card__title"
    url = selector.css(f"{cardTitleSelector} a::attr(href)").getall()

    return url


# Requisito 4
def scrape_next_page_link(html_content):
    selector = Selector(html_content)
    urls = selector.css('div.tec--list--lg a::attr(href)').getall()

    if (len(urls) < 1):
        return None
    else:
        url = urls[len(urls) - 1]
        return url


# Requisito 5
def get_tech_news(amount):
    news = []
    url = "https://www.tecmundo.com.br/novidades"
    html_content = fetch(url)
    links_list = scrape_novidades(html_content)

    while len(news) != amount:
        for link in links_list:
            content_to_scrape = fetch(link)
            news.append(scrape_noticia(content_to_scrape))
            if len(news) == amount:
                break

        next_page = scrape_next_page_link(html_content)
        html_content = fetch(next_page)
        links_list = scrape_novidades(html_content)

    create_news(news)
    return news


if __name__ == "__main__":

    get_tech_news(10)
