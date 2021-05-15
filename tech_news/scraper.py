import requests
import time
from tech_news.database import create_news
from parsel import Selector


# Requisito 1
def fetch(url):
    try:
        time.sleep(1)
        response = requests.get(url, timeout=3)
        response.raise_for_status()
        return response.text
    except requests.ReadTimeout as error:
        print(f"Server not responding, timeout reached: {error}")
        return None
    except requests.exceptions.ConnectionError as error:
        print(f"Request error: {error}")
        return None
    except Exception:
        return None


# Requisito 2
def scrape_noticia(html_content):
    selector = Selector(text=html_content)
    url = selector.css("link[rel=canonical]::attr(href)").get()
    title = selector.css("#js-article-title::text").get()
    timestamp = selector.css("time::attr(datetime)").get()
    selector.xpath('//figure[@class="tec--author__avatar"]').remove()
    writer = selector.css(".tec--author__info__link::text").get()
    writer = writer.strip() if writer is not None else None
    shares_info = selector.css(".tec--toolbar__item::text").re_first(r"\d+")
    shares_count = int(shares_info) if shares_info is not None else 0
    comments_info = selector.css("#js-comments-btn::text").re_first(r"\d+")
    comments_count = int(comments_info) if comments_info is not None else 0
    summary = "".join(
        selector.css("div.tec--article__body p:nth-child(1) *::text").getall()
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


def check_enough_news(amount, news_length):
    return news_length == amount


def save_news_to_mongoDB(news):
    create_news(news)


def get_tech_news(amount):
    initial_url = "https://www.tecmundo.com.br/novidades"
    current_url = initial_url
    news = []
    while True:
        current_news_list_html = fetch(current_url)
        current_links = scrape_novidades(current_news_list_html)

        for link in current_links:
            single_news_html = fetch(link)
            single_news = scrape_noticia(single_news_html)
            print(single_news)
            news.append(single_news)
            enough_news = check_enough_news(amount, len(news))
            if enough_news is True:
                save_news_to_mongoDB(news)
                return news
        current_url = scrape_next_page_link(current_news_list_html)
