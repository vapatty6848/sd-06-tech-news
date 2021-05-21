import requests
import time
from parsel import Selector

# "https://www.tecmundo.com.br/novidades"
# Requisito 1


def fetch(url):
    try:
        time.sleep(1)
        response = requests.get(url, timeout=3)
    except Exception:
        return None
    else:
        if response.status_code == 200:
            return response.text
        else:
            return None


# Requisito 2
def scrape_noticia(html_content):
    selector = Selector(text=html_content)
    url = selector.css("head link[rel=canonical]::attr(href)").get()
    title = selector.css(".tec--article__header__title::text").get()
    timestamp = selector.css(
        ".tec--timestamp__item time::attr(datetime)"
    ).get()
    writer = selector.css(".tec--author__info__link::text").get()
    writer = writer.strip()
    shares_count = selector.css(".tec--toolbar__item::text").get()
    shares_count = int(shares_count.split(" ")[1]) if shares_count else 0
    comments_count = selector.css("#js-comments-btn::attr(data-count)").get()
    comments_count = int(comments_count) if comments_count else None
    summary = selector.css(
        ".tec--article__body p:nth-child(1) *::text"
    ).getall()
    summary = "".join(summary)
    sources = selector.css(".z--mb-16 .tec--badge::text").getall()
    sources = [source.strip() for source in sources]
    categories = selector.css("#js-categories a::text").getall()
    categories = [category.strip() for category in categories]
    dic_data = {
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
    return dic_data


# Requisito 3
def scrape_novidades(html_content):
    if not html_content:
        return []
    selector = Selector(text=html_content)
    url_list = selector.css(".tec--card__info > h3 > a::attr(href)").getall()
    return url_list


# Requisito 4
def scrape_next_page_link(html_content):
    """Seu código deve vir aqui"""


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
