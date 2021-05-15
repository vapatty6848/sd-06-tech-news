import time
import requests
from requests.exceptions import HTTPError, ReadTimeout
from parsel import Selector


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


response = fetch("https://www.tecmundo.com.br/novidades")
# print(response)


# Requisito 2
def scrape_noticia(html_content):
    """Seu código deve vir aqui"""
    selector = Selector(html_content)
    # Isso é pra uma noticia. Faz um for em todas
    element = {
        "url": selector.css(".tec--card__title__link::attr(href)")[0].get(),
        "title": selector.css(".tec--card__title__link::text")[0]
        .get().strip(),
    }

    # faz uma busca pelo html de dentro da noticia
    news_details = fetch(element['url'])
    new_selector = Selector(news_details)
    element['timestamp'] = new_selector.css(
        ".tec--timestamp__item time::attr(datetime)").get()
    element['writer'] = new_selector.css(
        ".tec--author__info__link::text").get() or None
    element['shares_count'] = int(new_selector.css(
        ".tec--toolbar__item::text").get().strip().split()[0]) or 0
    element['comments_count'] = int(new_selector.css(
        "#js-comments-btn::text").getall()[1].strip().split()[0])
    time.sleep(1)
    element['summary'] = new_selector.css(
        ".tec--article__body.z--px-16.p402_premium p::text").getall()[1]
    element['sources'] = new_selector.css(
        ".z--mb-16.z--px-16 a::text").getall()
    for item in element['sources']:
        item = item.strip()
    element['categories'] = new_selector.css(
        "#js-categories a::text").getall()
    print(element)


file = scrape_noticia(response)
# print(file)


# Requisito 3
def scrape_novidades(html_content):
    """Seu código deve vir aqui"""


# Requisito 4
def scrape_next_page_link(html_content):
    """Seu código deve vir aqui"""


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
