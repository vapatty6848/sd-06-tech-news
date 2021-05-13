import requests
import time
from parsel import Selector


# Requisito 1
def fetch(url):
    time.sleep(1)
    try:
        response = requests.get(url, timeout=3)
        response.raise_for_status()
        return response.text
    except requests.exceptions.ReadTimeout:
        return None
    except requests.exceptions.HTTPError:
        return None


# Requisito 2
def scrape_noticia(html_content):
    selector = Selector(html_content)
    # cardTitleSelector = "h3.tec--card__title"
    timeStampSelector = "div.tec--timestamp__item::text"
    # url = selector.css(f"{cardTitleSelector} a::attr(href)").getall()
    # title = selector.css(f"{cardTitleSelector} a::text").getall()
    timestamp = selector.css(f"{timeStampSelector}").getall()
    print(timestamp)


# Requisito 3
def scrape_novidades(html_content):
    """Seu código deve vir aqui"""


# Requisito 4
def scrape_next_page_link(html_content):
    """Seu código deve vir aqui"""


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""


if __name__ == "__main__":
    scrape_noticia(fetch("https://www.tecmundo.com.br/novidades"))
