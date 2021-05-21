import requests
from requests.exceptions import Timeout
import time
from parsel import Selector
import re


url = "https://www.tecmundo.com.br/novidades"

# Requisito 1


def fetch(url):
    time.sleep(1)
    try:
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except Timeout:
        return None


# {
#   "url": "https://www.tecmundo.com.br/mobilidade-urbana-smart-cities/155000-musk-tesla-carros-totalmente-autonomos.htm",
#   "title": "Musk: Tesla está muito perto de carros totalmente autônomos",
#   "timestamp": "2020-07-09T11:00:00",
#   "writer": "Nilton Kleina",
#   "shares_count": 61,
#   "comments_count": 26,
#   "summary": "O CEO da Tesla, Elon Musk, garantiu que a montadora está muito perto de atingir o chamado nível 5 de autonomia de sistemas de piloto automático de carros. A informação foi confirmada em uma mensagem enviada pelo executivo aos participantes da Conferência Anual de Inteligência Artificial (WAIC, na sigla em inglês). O evento aconteceu em Xangai, na China, onde a montadora comemora resultados positivos de mercado.",
#   "sources": ["Venture Beat"],
#   "categories": [
#     "Mobilidade Urbana/Smart Cities",
#     "Veículos autônomos",
#     "Tesla",
#     "Elon Musk"
#   ]
# }


# Requisito 2


def scrape_noticia(html_content):
    selector = Selector(text=html_content)
    url = selector.css("head link[rel=canonical]::attr(href)").get()
    title = selector.css(".tec--article__header__title::text").get()
    timestamp = selector.css("#js-article-date::attr(datetime)").get()
    writer = (
        selector.css(
            "#js-author-bar > div > p.z--m-none.z--truncate.z--font-bold > a::text"
        )
        .get()
        .strip()
    )
    shares_count = selector.css(
        "#js-author-bar > nav > div:nth-child(1)::text"
    ).get()
    shares_count = re.sub("[^0-9]", "", shares_count)
    comments_count = selector.css("#js-comments-btn::attr(data-count)").get()
    summary = selector.css(
        ".tec--article__body p:nth-child(1) *::text"
    ).getall()
    summary = "".join(summary)
    sources = selector.css(
        "#js-main > div.z--container > article > div.tec--article__body-grid > div.z--mb-16.z--px-16 > div > a.tec--badge::text"
    ).getall()
    categories = selector.css("#js-categories > a.tec--badge::text").getall()
    sources = [source.strip() for source in sources]
    categories = [category.strip() for category in categories]

    news = {
        "url": url,
        "title": title,
        "timestamp": timestamp,
        "writer": writer,
        "shares_count": int(shares_count),
        "comments_count": int(comments_count),
        "summary": summary,
        "sources": sources,
        "categories": categories,
    }

    return news


html = fetch(
    "https://www.tecmundo.com.br/mobilidade-urbana-smart-cities/155000-musk-tesla-carros-totalmente-autonomos.htm"
)
print(scrape_noticia(html))


# Requisito 3


def scrape_novidades(html_content):
    if not html_content:
        return []
    selector = Selector(text=html_content)
    urls = selector.css(".tec--card__info > h3 > a::attr(href)").getall()
    return urls


# Requisito 4
def scrape_next_page_link(html_content):
    """Seu código deve vir aqui"""


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
