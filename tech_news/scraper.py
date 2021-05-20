import time
import requests
from parsel import Selector
from tech_news.database import create_news

def fetch(url):
    time.sleep(1)
    try:
        response = requests.get(url, timeout=3)
    except ReadTimeout:
        return None

    return response.text if response.status_code == 200 else None

def scrape_noticia(html_content):
    selector = Selector(text=html_content)

    get_url = selector.css("head link[rel=canonical]::attr(href)").get()
    get_title = selector.css("#js-article-title::text").get()
    get_timestamp = selector.css("#js-article-date::attr(datetime)").get()
    get_writer = selector.css(
        "#js-author-bar > div > p.z--m-none.z--truncate.z--font-bold "
        "> a::text"
    ).get()
    get_shares_count = selector.css(
        "#js-author-bar > nav > div:nth-child(1)::text"
    ).re_first(r"\d+")
    get_comments = selector.css("#js-comments-btn::text").re_first(r"\d+")
    get_summary = selector.css(
        ".tec--article__body p:nth-child(1) *::text"
    ).getall()
    get_sources = selector.css(".z--mb-16 .tec--badge::text").getall()
    get_categories = selector.css("#js-categories > a *::text").getall()

    writer = writer.strip() if writer else None
    shares = int(get_shares_count) if get_shares_count else 0
    comments = int(get_comments) if get_comments else None
    summary = "".join(get_summary)
    sources = [source.strip() for source in get_sources]
    categories = [category.strip() for category in get_categories]

    dic_news = {
        "url": get_url,
        "title": get_title,
        "timestamp": get_timestamp,
        "writer": writer,
        "shares_count": shares,
        "comments_count": comments,
        "summary": summary,
        "sources": sources,
        "categories": categories,
    }

    return dic_news

def scrape_novidades(html_content):
    if html_content == "":
        return []
    else:
        selector = Selector(text=html_content)
        get_news = selector.css(".tec--card__info h3 a::attr(href)").getall()
        return get_news

def scrape_next_page_link(html_content):
    selector = Selector(text=html_content)
    get_next_url = selector.css(
        "#js-main > div > div > .z--w-2-3 > div.tec--list--lg > a::attr(href)"
    ).get()
    return get_next_url

def get_tech_news(amount):
    url = "https://www.tecmundo.com.br/novidades"
    news = []
    while True:
        response = fetch(url)
        news_current_page = scrape_novidades(response)
        for new in news_current_page:
            news_next_page = fetch(new)
            next_news = scrape_noticia(news_next_page)
            news.append(next_news)
            if len(news) == amount:
                create_news(news)
                return news
        url = scrape_next_page_link(response)

if __name__ == "__main__":
    get_tech_news(15)
