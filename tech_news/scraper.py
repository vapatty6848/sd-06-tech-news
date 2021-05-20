import requests
import time
from parsel import Selector
from tech_news.database import create_news


def fetch(url):
    time.sleep(1)
    try:
        response = requests.get(url, timeout=3)
    except requests.ReadTimeout:
        return None
    if response.status_code == 200:
        return response.text
    else:
        return None


def scrape_noticia(html_content):
    selector = Selector(text=html_content)
    url = selector.css('[rel="canonical"]::attr(href)').get()
    title = selector.css(".tec--article__header__title::text").get()
    timestamp = selector.css("#js-article-date::attr(datetime)").get()
    writer = selector.css(".tec--author__info__link::text").get()
    writer = writer.strip() if writer else None
    shares_count = selector.css(".tec--toolbar__item::text").get()
    if shares_count:
        shares_count = int(shares_count.split()[0])
    else:
        shares_count = 0
    comments_count = selector.css(".tec--toolbar__item *::text").get()
    if len(comments_count) > 1:
        comments_count = int(comments_count.split()[0])
    else:
        comments_count = 0
    summary = "".join(
        selector.css(".tec--article__body p:nth-child(1) *::text").getall())
    sources_list = selector.css(".z--mb-16 div .tec--badge::text").getall()
    sources = []
    for e in sources_list:
        sources.append(e.strip())
    categories_list = selector.css("#js-categories a::text").getall()
    categories = []
    for c in categories_list:
        categories.append(c.strip())

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


def scrape_novidades(html_content):
    selector = Selector(html_content)
    news_list = selector.css(
        "h3.tec--card__title a.tec--card__title__link::attr(href)").getall()
    return news_list


def scrape_next_page_link(html_content):
    selector = Selector(html_content)
    next_page = selector.css("a.tec--btn::attr(href)").get()
    return next_page


def get_tech_news(amount):
    base_url = "https://www.tecmundo.com.br/novidades"
    news = []
    while len(news) < amount:
        html_content = fetch(base_url)
        url_news = scrape_novidades(html_content)
        for new in url_news:
            new_content = fetch(new)
            new_data = scrape_noticia(new_content)
            news.append(new_data)
            if len(news) == amount:
                create_news(news)
                return news
        base_url = scrape_next_page_link(new_content)
    return news
