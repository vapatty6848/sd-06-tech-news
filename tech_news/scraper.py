import requests
import time
from parsel import Selector
from tech_news.database import create_news

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
    writer = writer.strip() if writer else None
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
    selector = Selector(text=html_content)
    next_page = selector.css(".tec--btn.tec--btn--lg::attr(href)").get()
    return next_page


# Requisito 5
def get_tech_news(amount):
    page_url = "https://www.tecmundo.com.br/novidades"
    news = []

    while len(news) < amount:
        response = fetch(page_url)
        url_list = scrape_novidades(response)
        for url in url_list:
            if len(news) >= amount:
                break
            new = scrape_noticia(fetch(url))
            news.append(new)

        page_url = scrape_next_page_link(response)

    create_news(news)
    return news
