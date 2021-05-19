import time
import requests
from requests.exceptions import HTTPError, ReadTimeout
from parsel import Selector
from tech_news.database import (
    create_news,
    # insert_or_update,
    # find_news,
    # search_news,
    # get_collection
)
# import pprint


# Requisito 1
def fetch(url):
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


# Requisito 3
def scrape_novidades(html_content):
    selector = Selector(html_content)
    url_list = selector.css(
        ".tec--main .tec--card__title a::attr(href)"
    ).getall()
    url_list = url_list if url_list is not None else []

    return url_list


# Requisito 4
def scrape_next_page_link(html_content):
    selector = Selector(html_content)
    next_page_link = selector.css(
        ".tec--btn.tec--btn--lg.tec" +
        "--btn--primary.z--mx-auto.z--mt-48::attr(href)"
    ).get()

    return next_page_link if not None else None


# Requisito 5
def get_tech_news(amount):
    # 1 - Trazer uma lista de urls, no número de amount
    html_content = fetch("https://www.tecmundo.com.br/novidades")
    url_list = scrape_novidades(html_content)

    if amount > 20 and amount <= 40:
        page2 = scrape_next_page_link(html_content)
        html_content2 = fetch(page2)
        url_list2 = scrape_novidades(html_content2)
        url_list = url_list + list(set(url_list2) - set(url_list))

    url_list_final = []
    for url in range(amount):
        url_list_final.append(url_list[url])

    # Pegar informações de cada notícia e jogar em uma lista (de dicts)
    url_infos = []

    for url in url_list_final:
        link_html = fetch(url)
        news = scrape_noticia(link_html)
        url_infos.append(news)

    create_news(url_infos)
    return url_infos

    # print(len(url_infos))


# print(get_tech_news(1))
# pp = pprint.PrettyPrinter(indent=4)
# list = get_tech_news(1)
# for each in list:
#     pp.pprint(each)
