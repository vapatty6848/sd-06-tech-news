# Requisito 1
import requests
import time
from parsel import Selector


def fetch(url):
    """Seu código deve vir aqui"""
    try:
        response = requests.get(url, timeout=2)
        time.sleep(1)
        response.raise_for_status()
    except Exception:
        return None
    else:
        return response.text


# Requisito 2
def scrape_noticia(html_content):
    """Seu código deve vir aqui"""
    page = Selector(text=html_content)
    url = page.css('[property="og:url"]::attr(content)').get()
    title = page.css(".tec--article__header__title::text").get()
    timestamp = page.css("#js-article-date::attr(datetime)").get()
    write = page.css(".tec--author__info__link::text").get().strip()
    shares_count = int(
        page.css(".tec--toolbar__item::text").get().split(" ")[1]
    )
    comments_count = int(page.css(".tec--btn::attr(data-count)").get())
    a = page.css(".tec--article__body p:nth-child(1) ::text").getall()
    summary = "".join(a)
    sourcesWithSpace = page.css(".z--mb-16 .tec--badge::text").getall()
    sources = [elemento.strip() for elemento in sourcesWithSpace]
    categoriesWithSpace = page.css(".tec--badge--primary::text").getall()
    categories = [elemento.strip() for elemento in categoriesWithSpace]
    return {
        "url": url,
        "title": title,
        "timestamp": timestamp,
        "writer": write,
        "shares_count": shares_count,
        "comments_count": comments_count,
        "summary": summary,
        "sources": sources,
        "categories": categories,
    }


# Requisito 3
def scrape_novidades(html_content):
    """Seu código deve vir aqui"""
    page = Selector(text=html_content)
    return page.css(
        "div.tec--list__item .tec--card__title__link::attr(href)"
    ).getall()


# Requisito 4
def scrape_next_page_link(html_content):
    """Seu código deve vir aqui"""
    page = Selector(text=html_content)
    return page.css(".tec--btn::attr(href)").get()


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
