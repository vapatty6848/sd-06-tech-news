import requests
import time
from parsel import Selector


# Requisito 1
def fetch(url):
    try:
        time.sleep(1)
        response = requests.get(url, timeout=3)
        return response.text if response.status_code == 200 else None
    except requests.ReadTimeout:
        return None


# Requisito 2
def scrape_noticia(html_content):
    selector = Selector(text=html_content)
    url = selector.css("link[rel=canonical]::attr(href)").get()
    title = selector.css(".tec--article__header__title::text").get()
    timestamp = selector.css(".tec--timestamp__item time ::attr(datetime)").get()
    get_writer = selector.css(".tec--author__info__link::text").get()
    writer = get_writer.strip()
    shares = selector.css(".tec--toolbar__item::text").re_first(r"\d+")
    comments = selector.css(".tec--btn::attr(data-count)").get()
    uncl_summary = selector.css("div.tec--article__body > p:nth-child(1) *::text").getall()
    summary = "".join(uncl_summary)
    sources = selector.css(".z--mb-16 .tec--badge::text").getall()
    all_sources = [source.strip() for source in sources]
    categories = selector.css("#js-categories > a *::text").getall()
    all_categories = [category.strip() for category in categories]
    return {
        "url": url,
        "title": title,
        "timestamp": timestamp,
        "writer": writer,
        "shares_count": int(shares),
        "comments_count": int(comments),
        "summary": summary,
        "sources": all_sources,
        "categories": all_categories,
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
