import requests
from parsel import Selector
import time
from tech_news.database import create_news

tech_mundo_url = "https://www.tecmundo.com.br/novidades"


def fetch(url):
    time.sleep(1)
    try:
        website = requests.get(url, timeout=3)
    except requests.ReadTimeout:
        return None
    else:
        response_status = website.status_code
        if response_status == 200:
            return website.text
        elif response_status != 200:
            return None


def remove_spaces_from_items(list_to_treat):
    return [string.strip() for string in list_to_treat if len(string) > 1]


def scrape_noticia(html_content):
    selector = Selector(text=html_content, base_url=html_content)
    url = selector.css("head > link[rel=canonical]::attr(href)").get()
    title = selector.css("h1#js-article-title::text").get()
    timestamp = selector.css("#js-article-date::attr(datetime)").get()
    writer = selector.css("a.tec--author__info__link::text").get()
    get_writer = writer.strip() if writer else None

    shares_count = selector.css("div.tec--toolbar__item::text").get()
    get_shares_count = int(shares_count.split()[0]) if shares_count else 0

    comments_count = selector.css(
        "div.tec--toolbar__item #js-comments-btn::attr(data-count)"
    ).get()
    get_comments_count = int(comments_count) if comments_count else None

    summary = selector.css(
        ".tec--article__body p:first-child *::text"
    ).getall()
    treated_summary = "".join(summary)

    sources = remove_spaces_from_items(
        selector.css("div.z--mb-16 div *::text").getall()
    )
    categories = remove_spaces_from_items(
        selector.css("#js-categories a.tec--badge *::text").getall()
    )

    scraped_infos = {
        "url": url,
        "title": title,
        "timestamp": timestamp,
        "writer": get_writer,
        "shares_count": get_shares_count,
        "comments_count": get_comments_count,
        "summary": treated_summary,
        "sources": sources,
        "categories": categories,
    }
    return scraped_infos


# Requisito 3
def scrape_novidades(html_content):
    selector = Selector(text=html_content)
    news = selector.css(
        ".tec--list a.tec--card__title__link::attr(href)"
    ).getall()
    return news


# Requisito 4
def scrape_next_page_link(html_content):
    selector = Selector(text=html_content)
    next_page_btn = selector.css(
        "#js-main > div > div > .z--w-2-3 > div.tec--list--lg > a::attr(href)"
    ).get()
    return next_page_btn


# Requisito 5
def get_tech_news(amount):
    url = "https://www.tecmundo.com.br/novidades"
    news_inserted = []
    while True:
        response = fetch(url)
        news_current_page = scrape_novidades(response)
        for new in news_current_page:
            news_next_page = fetch(new)
            next_news = scrape_noticia(news_next_page)
            news_inserted.append(next_news)
            if len(news_inserted) == amount:
                create_news(news_inserted)
                return news_inserted
        url = scrape_next_page_link(response)


# get_tech_news(20)
