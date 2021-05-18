import time
import requests
from requests.exceptions import ReadTimeout, HTTPError
from parsel import Selector

with open('/home/alexander/Downloads/teste.html', 'r') as file:
    texto = file.read()


# Requisito 1
def fetch(url):
    time.sleep(1)
    response = ''

    try:
        response = requests.get(url, timeout=3)
    except ReadTimeout:
        return None
    try:
        response.raise_for_status()
    except HTTPError:
        return None

    return response.text


# Requisito 2
def scrape_noticia(html_content):
    selector = Selector(text=html_content)

    url = selector.css('[rel=canonical]::attr(href)').get()

    title = selector.css('h1::text').get()

    writer = selector.css('.tec--author__info__link::text').get().strip()

    timestamp = selector.css('time::attr(datetime)').get()

    shares = int(selector.css(
        '.tec--toolbar__item::text')[0].getall()[0].split(' ')[1])

    comments = int(selector.css(
            '.tec--btn::text').getall()[9].split(' ')[1])

    summary_fetch = selector.css(
        '.tec--article__body p:first-child *::text').getall()
    summary = "".join(summary_fetch)

    sourcesList = selector.css('a[class=tec--badge]::text').getall()
    sources = [source.strip() for source in sourcesList]

    categoriesList = selector.css('.tec--badge--primary::text').getall()
    categories = [categorie.strip() for categorie in categoriesList]

    return {
        "url": url,
        "title": title,
        "timestamp": timestamp,
        "writer": writer,
        "shares_count": shares,
        "comments_count": comments,
        "summary": summary,
        "sources": sources,
        "categories": categories
    }


# Requisito 3
def scrape_novidades(html_content):
    """Seu código deve vir aqui"""


# Requisito 4
def scrape_next_page_link(html_content):
    """Seu código deve vir aqui"""


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""


print(scrape_noticia(texto))
