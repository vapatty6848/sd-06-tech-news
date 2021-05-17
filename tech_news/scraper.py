from tech_news.database import create_news
import requests
from parsel import Selector
from time import sleep


# Requisito 1
def fetch(url):
    sleep(1)
    try:
        response = requests.get(url, timeout=3)
        if (response.status_code == 200):
            return response.text
        else:
            return None
    except requests.Timeout:
        return None


# Requisito 2
def scrape_noticia(html_content):
    selector = Selector(text=html_content)
    url = selector.css("head > link[rel=canonical]::attr(href)").get()
    title = selector.css(".tec--article__header__title::text").get()
    timestamp = selector.css("#js-article-date::attr(datetime)").get()

    writer = selector.css(".tec--author__info__link::text").get()
    writer = writer.strip() if writer else None

    shares_count = selector.css(".tec--toolbar__item::text").get()
    shares_count = int(shares_count.split()[0]) if shares_count else 0

    comments_count = int(selector.css(
        ".tec--toolbar__item #js-comments-btn::attr(data-count)"
    ).get())

    summary = "".join(selector.css(
        ".tec--article__body p:first-child *::text"
    ).getall())

    sources = selector.css(".z--mb-16 div *::text").getall()
    sources = [item.strip() for item in sources if item != ' ']

    categories = selector.css("#js-categories *::text").getall()
    categories = [
        category.strip() for category in categories if category != ' '
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
    return selector.css(
        ".tec--list .tec--card__title__link::attr(href)"
    ).getall()


# Requisito 4
def scrape_next_page_link(html_content):
    selector = Selector(text=html_content)
    return selector.css(
        ".tec--btn--primary::attr(href)"
    ).get()


# Requisito 5
def get_tech_news(amount):
    base_url = "https://www.tecmundo.com.br/novidades"
    news = []
    while True:
        response = fetch(base_url)
        news_container = scrape_novidades(response)
        for news_link in news_container:
            html_content_of_a_specific_page = fetch(news_link)
            news_data = scrape_noticia(html_content_of_a_specific_page)
            news.append(news_data)
            if len(news) == amount:
                create_news(news)
                return news
        base_url = scrape_next_page_link(response)


# html_content = fetch("https://www.tecmundo.com.br/novidades")

# print(scrape_next_page_link(html_content))
# print(get_tech_news(5))
# html_content = fetch(
#     "https://www.tecmundo.com.br/mobilidade-urbana-smart-cities/155000-musk-tesla-carros-totalmente-autonomos.htm"
# )

# print(scrape_noticia(html_content))
# print(type(int(" 0 Compartilharam".split()[0])))
