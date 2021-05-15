import requests
import time
import tech_news.database as database
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
    selector.xpath('//figure[@class="tec--author__avatar"]').remove()
    writer = selector.css("a[href*=autor]::text").get().strip()
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
def get_remaining_links(amount, current):
    return amount - current


def access_new_page_from(html_content):
    next_page_url = scrape_next_page_link(html_content)
    next_html_page = fetch(next_page_url)
    more_links = scrape_novidades(next_html_page)
    return (next_html_page, more_links)


def get_tech_news(amount):
    news_links = []
    initial_url = "https://www.tecmundo.com.br/novidades"
    current_html_page = fetch(initial_url)
    current_links = scrape_novidades(current_html_page)
    news_links.extend(current_links)
    remaining_links = get_remaining_links(amount, len(news_links))

    while remaining_links > 0:
        remaining_links = get_remaining_links(amount, len(news_links))
        new_html_page, more_links = access_new_page_from(current_html_page)
        current_html_page = new_html_page
        news_links.extend(more_links)
        remaining_links = get_remaining_links(amount, len(news_links))

    remaining_links = get_remaining_links(amount, len(news_links))

    if remaining_links < 0:
        links_to_remove_count = abs(remaining_links)
        del news_links[-links_to_remove_count:]

    print(news_links)
    for link in news_links:
        html_page = fetch(link)
        data = scrape_noticia(html_page)
        print(data)
        database.insert_or_update(data)
