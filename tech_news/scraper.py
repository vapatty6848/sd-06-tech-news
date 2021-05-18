import requests
import time
from parsel import Selector


def fetch(url):
    time.sleep(1)
    try:
        response = requests.get(url, timeout=3)
    except requests.ReadTimeout:
        return None
    if response.status_code == 200:
        return response.text
    else:
        return None


def scrape_noticia(html_content):
    selector = Selector(text=html_content)
    url = selector.css('[rel="canonical"]::attr(href)').get()
    title = selector.css(".tec--article__header__title::text").get()
    timestamp = selector.css("#js-article-date::attr(datetime)").get()
    writer = selector.css(".tec--author__info__link::text").get()
    writer = writer.strip() if writer else None
    shares_count = selector.css(".tec--toolbar__item::text").get()
    if shares_count:
        shares_count = int(shares_count.split()[0])
    else:
        shares_count = 0
    comments_count = selector.css(".tec--toolbar__item *::text").get()
    if len(comments_count) > 1:
        comments_count = int(comments_count.split()[0])
    else:
        comments_count = 0
    summary = "".join(
        selector.css(".tec--article__body p:nth-child(1) *::text").getall())
    sources_list = selector.css(".z--mb-16 div .tec--badge::text").getall()
    sources = []
    for e in sources_list:
        sources.append(e.strip())
    categories_list = selector.css("#js-categories a::text").getall()
    categories = []
    for c in categories_list:
        categories.append(c.strip())

    return {
        "url": url,
        "title": title,
        "timestamp": timestamp,
        "writer": writer,
        "shares_count": shares_count,
        "comments_count": comments_count,
        "summary": summary,
        "sources": sources,
        "categories": categories,
    }


def scrape_novidades(html_content):
    selector = Selector(html_content)
    news_list = selector.css(
        "h3.tec--card__title a.tec--card__title__link::attr(href)").getall()
    return news_list


# Requisito 4
def scrape_next_page_link(html_content):
    """Seu código deve vir aqui"""


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
