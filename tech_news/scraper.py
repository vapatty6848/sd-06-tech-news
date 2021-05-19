# Requisito 1
import requests
import time
import re
from parsel import Selector


def fetch(url):
    time.sleep(1)
    response = ""
    try:
        response = requests.get(url, timeout=3)
        if response.status_code != 200:
            return None
    except requests.ReadTimeout:
        return None

    return response.text


# Requisito 2
def scrape_noticia(html_content):
    selector = Selector(html_content)

    url = selector.css("head > link[rel=canonical]::attr(href)").get()
    title = selector.css(".tec--article__header__title::text").get().strip()
    timestamp = selector.css("#js-article-date ::attr(datetime)").get().strip()
    check_writer = selector.css(".tec--author p a::text").get().strip()
    if (check_writer) is not None:
        writer = check_writer
    else:
        writer = None
    check_shares_count = int(
        (selector.css(".tec--toolbar__item::text").get().split()[0])
    )
    if (check_shares_count) is not None:
        shares_count = int(check_shares_count)
    else:
        shares_count = None
    comments_count = int(
        selector.css("#js-comments-btn ::attr(data-count)").get().strip()
    )
    get_summary = " ".join(
        selector.css(".tec--article__body p:nth-child(1) ::text").getall()
    )
    no_comma = re.sub(r'\s+([?,!"])', r"\1", get_summary)
    summary = no_comma.replace("  ", " ")

    list_sources = selector.css(
        "#js-main div.z--mb-16.z--px-16 a::text"
    ).getall()
    sources = []
    for source in list_sources:
        sources.append(source.strip())

    list_categories = selector.css("#js-categories a::text").getall()
    categories = []
    for categorie in list_categories:
        categories.append(categorie.strip())

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


# Requisito 3
def scrape_novidades(html_content):
    selector = Selector(html_content)

    list_urls = selector.css(
        ".tec--list--lg .tec--card__info h3 a::attr(href)"
    ).getall()

    return list_urls

# Requisito 4
def scrape_next_page_link(html_content):
    """Seu código deve vir aqui"""


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
