import requests
import time
from parsel import Selector
from requests.exceptions import HTTPError, ReadTimeout
from tech_news.database import create_news


# Requisito 1
def fetch(url):
    time.sleep(1)

    try:
        response = requests.get(url, timeout=3)
        response.raise_for_status()
        page_content = response.text
    except (ReadTimeout, HTTPError) as error:
        print(error)
        return None

    return page_content


# Requisito 2
def scrape_noticia(html_content):
    selector = Selector(text=html_content)

    url = selector.css('link[rel=canonical]::attr(href)').get()
    title = selector.css('h1.tec--article__header__title::text').get()
    timestamp = selector.css('time::attr(datetime)').get()
    writer_selector = selector.css('a.tec--author__info__link::text').get()
    writer = writer_selector.strip() if (writer_selector) else None
    shares_count_selector = selector.css('div.tec--toolbar__item::text').get()
    shares_count = int(
        shares_count_selector.strip().split()[0]
    ) if (shares_count_selector) else 0
    comments_count_selector = "".join(
        selector.css('button.tec--btn *::text').getall()
    ).strip().split()
    comments_count = int(comments_count_selector[0]) if (
        len(comments_count_selector) != 0
    ) else 0
    summary = "".join(
        selector.css('div.tec--article__body p:nth-child(1) *::text').getall()
    )
    sources = [source.strip() for source in selector.css(
        'div.z--mb-16 div a::text'
    ).getall()]
    categories = [category.strip() for category in selector.css(
        '#js-categories a::text'
    ).getall()]

    return {
        "url": url,
        "title": title,
        "timestamp": timestamp,
        "writer": writer,
        "shares_count": shares_count,
        "comments_count": comments_count,
        "summary": summary,
        "sources": sources,
        "categories": categories
    }


# Requisito 3
def scrape_novidades(html_content):
    selector = Selector(text=html_content)
    return selector.css('.tec--card__info h3 a::attr(href)').getall()


# Requisito 4
def scrape_next_page_link(html_content):
    selector = Selector(text=html_content)
    return selector.css('.tec--btn::attr(href)').get()


# Requisito 5
def get_tech_news(amount):
    url = "https://www.tecmundo.com.br/novidades"

    array_of_news = []

    while len(array_of_news) < amount:
        html_content = fetch(url)
        first_page = scrape_novidades(html_content)

        for news in first_page:
            detailed_news = fetch(news)
            complete_news = scrape_noticia(detailed_news)
            array_of_news.append(complete_news)
            if len(array_of_news) == amount:
                create_news(array_of_news)
                return array_of_news

        url = scrape_next_page_link(html_content)

    return array_of_news
