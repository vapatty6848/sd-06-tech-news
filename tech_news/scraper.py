import requests
import time
from parsel import Selector


# Requisito 1
def fetch(url):
    time.sleep(1)
    try:
        response = requests.get(url, timeout=3)
    except requests.ReadTimeout:
        return None

    if response.status_code != 200:
        return None

    return response.text


# Requisito 2
def scrape_noticia(html_content):
    selector = Selector(text=html_content)
    url = selector.css("link[rel=canonical]::attr(href)").get()
    title = selector.css("#js-article-title::text").get()
    timestamp = selector.css("time::attr(datetime)").get()
    writer = selector.css(".tec--author__info__link::text").get().strip()
    shares = selector.css(".tec--toolbar__item::text").re_first(r"^[^A-Z]*")
    shares_count = int(shares) if shares is not None else 0
    comments_count = int(
        selector.css("#js-comments-btn::attr(data-count)").get()
    )
    summary = "".join(
        selector.css(
            "div.tec--article__body > p:nth-child(1) *::text"
        ).getall()
    )
    sources = [
        source.strip()
        for source in selector.xpath(
            "//h2[text()='Fontes']/following-sibling::div//a/text()"
        ).getall()
    ]
    categories = [
        category.strip()
        for category in selector.xpath(
            "//h2[text()='Categorias']/following-sibling::div//a/text()"
        ).getall()
    ]
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
    selector = Selector(text=html_content)
    news = selector.css("h3.tec--card__title a::attr(href)").getall()
    return news if news else []


# Requisito 4
def scrape_next_page_link(html_content):
    selector = Selector(text=html_content)
    next_page_link = selector.xpath(
        "//a[contains(text(), 'Mostrar mais notícias')]/@href"
    ).get()
    return next_page_link if next_page_link else None


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
