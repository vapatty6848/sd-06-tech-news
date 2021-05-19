# Imports
import time
import requests
from parsel import Selector
from tech_news.database import create_news


# Remover espaços
def remove_spaces(list):
    return [string.strip() for string in list if len(string) > 1]


# Requisito 1
def fetch(url):
    try:
        response = requests.get(url, timeout=3)
        time.sleep(1)
        response.raise_for_status()
    except Exception:
        return None
    else:
        return response.text


# Requisito 2
def scrape_noticia(html_content):
    selector = Selector(text=html_content)
    url = selector.css("head > link[rel=canonical]::attr(href)").get()
    title = selector.css("h1.tec--article__header__title ::text").get()
    timestamp = selector.css(
        "div.tec--timestamp__item time::attr(datetime)"
    ).get()
    writer = selector.css("div.tec--author__info a::text").get()
    fixed_writer = writer.strip() if writer else None
    shares_count = selector.css("div.tec--toolbar__item::text").get()
    fixed_shares_count = int(shares_count.split()[0]) if shares_count else 0
    comments_count = selector.css("#js-comments-btn ::attr(data-count)").get()
    fixed_comments_count = int(comments_count) if comments_count else None
    summary = selector.css(
        ".tec--article__body p:first-child *::text"
    ).getall()
    fixed_summary = "".join(summary)
    sources = remove_spaces(selector.css("div.z--mb-16 div *::text").getall())
    categories = remove_spaces(
        selector.css("#js-categories a.tec--badge *::text").getall()
    )

    scraped_infos = {
        "url": url,
        "title": title,
        "timestamp": timestamp,
        "writer": fixed_writer,
        "shares_count": fixed_shares_count,
        "comments_count": fixed_comments_count,
        "summary": fixed_summary,
        "sources": sources,
        "categories": categories,
    }
    # print(scraped_infos)
    return scraped_infos


# scrape_noticia(
#     fetch(
#         "https://www.tecmundo.com.br/mobilidade-urbana-smart-cities"
#         + "/155000-musk-tesla-carros-totalmente-autonomos.htm"
#     )
# )
# Requisito 3
def scrape_novidades(html_content):
    selector = Selector(text=html_content)
    novidades = selector.css(
        ".tec--list a.tec--card__title__link::attr(href)"
    ).getall()
    return novidades


# print(scrape_novidades(fetch("https://www.tecmundo.com.br/novidades")))

# Requisito 4
def scrape_next_page_link(html_content):
    selector = Selector(text=html_content)
    next_page = selector.css("a.tec--btn ::attr(href)").get()
    return next_page


# print(scrape_next_page_link(fetch("https://www.tecmundo.com.br/novidades")))

# Requisito 5
def get_tech_news(amount):
    url = "https://www.tecmundo.com.br/novidades"
    database_news = []
    count = 0
    while True:
        request = fetch(url)
        current_page_news = scrape_novidades(request)
        for new in current_page_news:
            next_page_news = fetch(new)
            next_news = scrape_noticia(next_page_news)
            database_news.append(next_news)
            # print(f"\n Noticia {count}: {next_news}")
            count += 1
            if len(database_news) == amount:
                create_news(database_news)
                return database_news
        url = scrape_next_page_link(request)


# get_tech_news(10)
