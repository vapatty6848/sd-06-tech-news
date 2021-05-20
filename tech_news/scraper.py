import requests
import time
from parsel import Selector
import re
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
    url = selector.css("link[rel=canonical]::attr(href)").get()
    title = selector.css(".tec--article__header__title::text").get()
    timestamp = selector.css(
        ".tec--timestamp__item time::attr(datetime)"
    ).get()
    writer = selector.css(".tec--author__info__link::text").get()
    if writer is not None:
        writer = writer.strip()
    shares_count = selector.css(".tec--toolbar__item::text").get()
    if shares_count is not None:
        shares_count = int(re.sub("[^0-9]", "", shares_count))
    else:
        shares_count = 0
    comments_count = selector.css("#js-comments-btn::attr(data-count)").get()
    if comments_count is not None:
        comments_count = int(comments_count)
    summary_content = "".join(
      selector.css("div.tec--article__body p:nth-child(1) *::text").getall()
    )
    sources = selector.css("div.z--mb-16 a.tec--badge::text").getall()
    sources = [source.strip() for source in sources]
    categories = selector.css("div#js-categories a::text").getall()
    categories = [categorie.strip() for categorie in categories]
    return {
        "url": url,
        "title": title,
        "timestamp": timestamp,
        "writer": writer,
        "shares_count": shares_count,
        "comments_count": comments_count,
        "summary": summary_content,
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
    url = "https://www.tecmundo.com.br/novidades"
    news_list = []
    while True:
        html_content = fetch(url)
        news_urls = scrape_novidades(html_content)
        for news_url in news_urls:
            news = scrape_noticia(fetch(news_url))
            news_list.append(news)
            if len(news_list) == amount:
                create_news(news_list)
                return news_list
        url = scrape_next_page_link(html_content)
