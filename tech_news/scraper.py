import requests
from time import sleep
from parsel import Selector
import re

# Requisito 1


def fetch(url):
    try:
        response = requests.get(url, timeout=3)
        sleep(1)

        if response.status_code != 200:
            return None

        return response.text

    except requests.Timeout:
        return None


# Requisito 2
def scrape_noticia(html_content):
    select = Selector(text=html_content)
    url = select.css("link[rel=canonical]::attr(href)").get()
    title = select.css(".tec--article__header__title::text").get()
    timestamp = select.css(
        ".tec--timestamp__item time::attr(datetime)"
    ).get()
    writer = select.css(".tec--author__info__link::text").get()
    if writer is not None:
        writer = writer.strip()
    shares_count = select.css(".tec--toolbar__item::text").get()
    if shares_count is not None:
        shares_count = int(re.sub("[^0-9]", "", shares_count))
    else:
        shares_count = 0
    comments_count = select.css("#js-comments-btn::attr(data-count)").get()
    if comments_count is not None:
        comments_count = int(comments_count)
    summary_content = "".join(
      select.css("div.tec--article__body p:nth-child(1) *::text").getall()
    )
    sources = select.css("div.z--mb-16 a.tec--badge::text").getall()
    sources = [source.strip() for source in sources]
    categories = select.css("div#js-categories a::text").getall()
    categories = [categorie.strip() for categorie in categories]
    return {
        "url": url,
        "title": title,
        "timestamp": timestamp,
        "writer": writer,
        "shares_count": shares_count,
        "comments_count": comments_count,
        "summary": summary_content,
        "sources": sources,
        "categories": categories,
    }


# Requisito 3
def scrape_novidades(html_content):
    select = Selector(text=html_content)
    links = select.css(
        "div.tec--list__item .tec--card__title__link::attr(href)"
    ).getall()
    return links


# Requisito 4
def scrape_next_page_link(html_content):
    """Seu código deve vir aqui"""


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
