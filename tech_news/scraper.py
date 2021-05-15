import requests
import time
from requests.exceptions import ReadTimeout
from requests.models import HTTPError
from parsel import Selector


# Requisito 1
def fetch(url):
    time.sleep(1)
    try:
        response = requests.get(url, timeout=3)
        response.raise_for_status()

    except (ReadTimeout, HTTPError):
        return None

    if response.status_code == 200:
        return response.text
    else:
        return None


# Requisito 2
def scrape_noticia(html_content):
    selector = Selector(text=html_content)
    url = selector.css("head link[rel=canonical]::attr(href)").get()
    title = selector.css("#js-article-title::text").get()
    timestamp = selector.css("#js-article-date::attr(datetime)").get()
    writer = selector.css(".tec--author__info__link::text").get()
    shares_count = selector.css(".tec--toolbar__item::text").get()
    comments_count = selector.css("#js-comments-btn::text").getall()[1]
    summary = selector.css(
        "div.tec--article__body > p:nth-child(1) *::text"
    ).getall()
    sources = [
        source.strip()
        for source in selector.css(
            "div.z--mb-16.z--px-16 > div > a::text"
        ).getall()
    ]
    categories = [
        category.strip()
        for category in selector.css("#js-categories > a::text").getall()
    ]

    return {
        "url": url,
        "title": title,
        "timestamp": timestamp,
        "writer": writer.strip(),
        "shares_count": int(shares_count.split(" ")[1]),
        "comments_count": int(comments_count.split(" ")[1]),
        "summary": "".join(summary),
        "sources": sources,
        "categories": categories,
    }


# Requisito 3
def scrape_novidades(html_content):
    selector = Selector(text=html_content)
    url_list = selector.css("h3.tec--card__title > a::attr(href)").getall()

    return url_list


# Requisito 4
def scrape_next_page_link(html_content):
    """Seu código deve vir aqui"""


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""


if __name__ == "__main__":
    url = "https://www.tecmundo.com.br/novidades"
    content = fetch(url)
    result = scrape_novidades(content)
    print(result)
