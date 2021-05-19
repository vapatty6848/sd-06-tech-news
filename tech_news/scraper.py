import requests
import time
from parsel import Selector
from tech_news.database import create_news


# Requisito 1
def fetch(url):
    try:
        response = requests.get(url, timeout=3)

        time.sleep(1)

        if not (response) or response.status_code != 200:
            return None

        return response.text
    except requests.exceptions.Timeout:
        return None


def stripWhiteSpaces(stringArray):
    return list(map(lambda x: x.strip(), stringArray))


def get_writter(selector):
    possible_writer_1 = selector.css(
        ".tec--author p > a.tec--author__info__link::text"
    ).get()

    possible_writer_2 = selector.css(
        ".tec--article .tec--timestamp__item > a::text"
    ).get()

    possible_writer_3 = selector.css(
        ".tec--article .tec--author__info > p:first-of-type::text"
    ).get()

    writer = possible_writer_1 or possible_writer_2 or possible_writer_3

    return writer


# Requisito 2
def scrape_noticia(html_content):
    selector = Selector(text=html_content)

    title = selector.css("h1#js-article-title::text").get()
    timestamp = selector.css("time#js-article-date::attr(datetime)").get()

    writer = get_writter(selector)

    shares_count = (
        selector.css(".tec--author nav > div:first-of-type::text").re_first(
            r"\d+"
        )
        or 0
    )

    comments_count = (
        selector.css("#js-comments-btn::text").re_first(r"\d+")
        or 0
    )

    summary_pars = selector.css(
        ".tec--article__body > p:first-of-type *::text"
    ).getall()
    summary = "".join(summary_pars)

    sources_no_trim = selector.css(
        ".tec--article__body ~ div"
        + "> h2 ~ div:not(#js-categories) > a::text"
    ).getall()
    sources = stripWhiteSpaces(sources_no_trim)

    categories_no_trim = selector.css("#js-categories > a::text").getall()
    categories = stripWhiteSpaces(categories_no_trim)

    url = selector.css("link[rel=canonical]::attr(href)").get()

    pageInfo = {
        "url": url,
        "title": title,
        "timestamp": timestamp,
        "writer": writer and writer.strip(),
        "shares_count": int(shares_count),
        "comments_count": int(comments_count),
        "summary": summary,
        "sources": sources,
        "categories": categories,
    }

    return pageInfo


# Requisito 3
def scrape_novidades(html_content):
    selector = Selector(text=html_content)

    links = selector.css(
        "main .tec--list .tec--card .tec--card__title > a::attr(href)"
    ).getall()

    return links


# Requisito 4
def scrape_next_page_link(html_content):
    selector = Selector(text=html_content)

    link = selector.css("a.tec--btn.tec--btn--primary::attr(href)").get()

    return link


# Requisito 5
def get_tech_news(amount):
    base_url = "https://www.tecmundo.com.br/novidades"
    news_amount_missing = amount

    news = []

    while news_amount_missing > 0:
        news_page_content = fetch(base_url)
        tech_news_links = scrape_novidades(news_page_content)
        base_url = scrape_next_page_link(news_page_content)
        amount_of_links = len(tech_news_links)

        if news_amount_missing < amount_of_links:
            tech_news_links = tech_news_links[0:news_amount_missing]

        for link in tech_news_links:
            page_content = fetch(link)
            news_info = scrape_noticia(page_content)
            news.append(news_info)

        news_amount_missing = news_amount_missing - len(tech_news_links)

    create_news(news)

    return news
