import requests
import time
from parsel import Selector


# Requisito 1
def fetch(url):
    try:
        time.sleep(1)
        response = requests.get(url, timeout=3)
        return response.text
    except requests.ReadTimeout:
        response = requests.get(url, timeout=3)
        return None
    return response.text if response.status_code == 200 else None


# Requisito 2
def scrape_noticia(html_content):
    response = requests.get(html_content)
    selector = Selector(text=response.text)
    all_urls = selector.css("link::attr(href)").getall()
    url = all_urls[-2]
    title = selector.css(".tec--article__header__title::text").get()
    timestamp = selector.css(".tec--timestamp__item time ::attr(datetime)").get()
    writer = selector.css(".tec--author__info__link::text").get()
    shares = selector.css(".tec--toolbar__item::text").get()
    shares_count = shares[0:3]
    comments = selector.css(".tec--btn::attr(data-count)").get()
    not_clean_summary = selector.css("div.tec--article__body > p:nth-child(1) *::text").getall()
    summary = "".join(not_clean_summary)
    all_sources = selector.css(".tec--badge::text").getall()
    sources = all_sources[0:1]
    categories = all_sources[1:5]
    return {
        "url": url,
        "title": title,
        "timestamp": timestamp,
        "writer": writer,
        "shares_count": int(shares_count),
        "comments_count": int(comments),
        "summary": summary,
        "sources": list(sources),
        "categories": list(categories),
    }


# Requisito 3
def scrape_novidades(html_content):
    """Seu código deve vir aqui"""


# Requisito 4
def scrape_next_page_link(html_content):
    """Seu código deve vir aqui"""


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
