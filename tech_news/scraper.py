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

    return response.text if response.status_code == 200 else None


# Requisito 2
def scrape_noticia(html_content):
    selector = Selector(text=html_content)

    URL = selector.css("head link[rel=canonical]::attr(href)").get()
    TITLE = selector.css("#js-article-title::text").get()
    TIMESTAMP = selector.css("#js-article-date::attr(datetime)").get()
    WRITER = selector.css("#js-author-bar > div > p > a::text").get().strip()
    GET_SHARES_COUNT = selector.css(
        "#js-author-bar > nav > div:nth-child(1)::text"
    ).re_first(r"\d+")
    SHARES_COUNT = int(GET_SHARES_COUNT) if GET_SHARES_COUNT else 0
    COMMENTS_COUNT = int(
        selector.css("#js-comments-btn::text").re_first(r"\d+")
    )
    SUMMARY = selector.css(
        ".tec--article__body > p:nth-child(1) *::text"
    ).getall()
    SUMMARY_TEXT = "".join(SUMMARY)
    GET_SOURCES = selector.css(".z--mb-16 .tec--badge::text").getall()
    SOURCES = [source.strip() for source in GET_SOURCES]
    GET_CATEGORIES = selector.css("#js-categories > a *::text").getall()
    CATEGORIES = [categorie.strip() for categorie in GET_CATEGORIES]
    dic_news = {
        "url": URL,
        "title": TITLE,
        "timestamp": TIMESTAMP,
        "writer": WRITER,
        "shares_count": SHARES_COUNT,
        "comments_count": COMMENTS_COUNT,
        "summary": SUMMARY_TEXT,
        "sources": SOURCES,
        "categories": CATEGORIES,
    }
    # print(dic_news)
    return dic_news


# Requisito 3
def scrape_novidades(html_content):
    if html_content == "":
        return []
    else:
        selector = Selector(text=html_content)
        list_News = selector.css(".tec--card__info h3 a::attr(href)").getall()
        return list_News


# Requisito 4
def scrape_next_page_link(html_content):
    selector = Selector(text=html_content)
    next_page = selector.css(
        "#js-main > div > div > .z--w-2-3 > div.tec--list--lg > a::attr(href)"
    ).get()
    return next_page


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""


if __name__ == "__main__":
    URL = "https://www.tecmundo.com.br/novidades"
    response = fetch(URL)
    news = scrape_next_page_link(response)
    print(news)
