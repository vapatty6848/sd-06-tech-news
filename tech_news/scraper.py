import time
import requests
from requests.exceptions import HTTPError, ReadTimeout
from parsel import Selector

# import pprint


# Requisito 1
def fetch(url):
    """Seu código deve vir aqui"""
    time.sleep(1)
    responses = []

    try:
        response = requests.get(url, timeout=3)
    except ReadTimeout:
        return None

    try:
        response.raise_for_status()
    except HTTPError:
        return None

    responses.append(response)
    return response.text


# response = fetch(
#     "https://www.tecmundo.com.br/dispositivos-moveis/215327-pixel-5a-tera-lancamento-limitado-devido-escassez-chips.htm"
# )
# print(response)


# Requisito 2
def scrape_noticia(html_content):
    new_selector = Selector(html_content)

    element = {
        "url": new_selector.css("link::attr(href)")[20].getall()[0],
    }

    element["title"] = new_selector.css(
        ".tec--article__header__title::text"
    ).get()
    element["timestamp"] = new_selector.css(
        ".tec--timestamp__item time::attr(datetime)"
    ).get()

    writer = new_selector.css(".tec--author__info__link::text").get()
    element["writer"] = writer.strip() if writer is not None else None

    shares_count = new_selector.css(".tec--toolbar__item::text").get()
    shares_count = (
        shares_count.strip().split()[0] if shares_count is not None else 0
    )
    element["shares_count"] = int(shares_count)

    comments_count = new_selector.css("#js-comments-btn *::text").getall()
    comments_count = (
        comments_count[1].strip().split(" ")[0]
        if comments_count is not None
        else 0
    )
    element["comments_count"] = int(comments_count)

    summary = new_selector.css(
        ".tec--article__body.z--px-16.p402_premium > p:first-child *::text"
    ).getall()
    separator = ""
    summary = separator.join(summary)
    element["summary"] = summary

    sources = new_selector.css(".z--mb-16.z--px-16 a::text").getall()
    for i in range(len(sources)):
        sources[i] = sources[i].strip()
    element["sources"] = sources

    categories = new_selector.css("#js-categories a::text").getall()
    for i in range(len(categories)):
        categories[i] = categories[i].strip()
    element["categories"] = categories

    return element


# pp = pprint.PrettyPrinter(indent=4)
# file = scrape_noticia(response)
# pp.pprint(file)


# Requisito 3
def scrape_novidades(html_content):
    selector = Selector(html_content)
    url_list = selector.css(
        ".tec--main .tec--card__title a::attr(href)"
    ).getall()
    url_list = url_list if url_list is not None else []

    return url_list


scrape_novidades("https://www.tecmundo.com.br/novidades")


# Requisito 4
def scrape_next_page_link(html_content):
    """Seu código deve vir aqui"""


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
