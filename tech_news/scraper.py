import requests
import time
from tech_news.database import create_news
from parsel import Selector


# Requisito 1
def fetch(url):
    time.sleep(1)
    try:
        response = requests.get(url, timeout=3)
        response.raise_for_status()

    except Exception:
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
    writer = selector.css(".tec--author__info *::text").get()
    shares_count = selector.css(".tec--toolbar__item::text").get()
    comments_count = selector.css(".tec--toolbar__item *::text").getall()
    summary = selector.css(
        "div.tec--article__body > p:first-child *::text"
    ).getall()
    sources = [
        source.strip()
        for source in selector.css("div.z--mb-16 > div > a::text").getall()
    ]
    categories = [
        category.strip()
        for category in selector.css("#js-categories > a::text").getall()
    ]

    if shares_count is not None:
        shares_count = int(shares_count.split()[0])
    else:
        shares_count = 0

    if len(comments_count) == 3:
        comments_count = int(comments_count[2].split()[0])
    else:
        comments_count = int(comments_count[1].split()[0])

    if not writer:
        writer = selector.css(
            "div.tec--timestamp__item.z--font-bold > a::text"
        ).get()

    writer = writer.strip() if writer else None

    return {
        "url": url,
        "title": title,
        "timestamp": timestamp,
        "writer": writer,
        "shares_count": shares_count,
        "comments_count": comments_count,
        "summary": "".join(summary),
        "sources": sources,
        "categories": categories,
    }


# Requisito 3
def scrape_novidades(html_content):
    return (
        Selector(text=html_content)
        .css("h3.tec--card__title > a::attr(href)")
        .getall()
    )


# Requisito 4
def scrape_next_page_link(html_content):
    return Selector(text=html_content).css("a.tec--btn::attr(href)").get()


# Requisito 5
def get_tech_news(amount):
    news_to_save = []
    url = "https://www.tecmundo.com.br/novidades"

    while len(news_to_save) < amount:
        news_page = fetch(url)
        News_list = scrape_novidades(news_page)

        for news in News_list:
            news_html = fetch(news)
            news_to_save.append(scrape_noticia(news_html))
            if len(news_to_save) == amount:
                break

        url = scrape_next_page_link(news_page)

    create_news(news_to_save)

    return news_to_save


if __name__ == "__main__":
    url = ""
    # content = fetch(url)
    # result = scrape_next_page_link(content)
    # print(result)
