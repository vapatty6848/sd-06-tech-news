# Requisito 1
import time
import requests
from parsel import Selector


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
    writer = selector.css("div.tec--author__info a::text").get().strip()
    shares_count = int(
        selector.css("div.tec--toolbar__item ::text").get()[1:3]
    )
    comments_count = int(
        selector.css("#js-comments-btn ::attr(data-count)").get()
    )
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
        "writer": writer,
        "shares_count": shares_count,
        "comments_count": comments_count,
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


# Requisito 4
def scrape_next_page_link(html_content):
    """Seu código deve vir aqui"""


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
