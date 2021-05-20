import requests
from requests.exceptions import HTTPError, ReadTimeout
import time
from parsel import Selector

# Requisito 1


def fetch(url):
    """Seu código deve vir aqui"""
    time.sleep(1)
    try:
        response = requests.get(url, timeout=3)
        response.raise_for_status()
    except (ReadTimeout, HTTPError):
        return None

    if response.status_code == 200:
        return response.text
    else:
        return None


# head > link:nth-child(26)
# Requisito 2
def scrape_noticia(html_content):
    """Seu código deve vir aqui"""
    selector = Selector(text=html_content)
    return {
        "url": selector.css("head > link:nth-child(26)::attr(href)").get(),
        "title": selector.css("#js-article-title::text").get(),
        "timestamp": selector.css("#js-article-date::attr(datetime)").get(),
        "writer": selector.css(".tec--author__info__link::text").get().strip(),
        "shares_count": selector.css(".tec--toolbar__item::text").re_first(
            r"\d+"
        ),
        "comments_count": selector.css("#js-comments-btn::text").re_first(
            r"\d+"
        ),
        "summary": "".join(
            selector.css(
                "#js-main > div.z--container > article "
                + "> div.tec--article__body-grid >"
                + " div.tec--article__body.z--px-16.p402_premium "
                + " > p:nth-child(1) *::text"
            ).getall(),
        ),
        "source": selector.css(".tec--badge::text").get().strip(),
        "categories": [
            elemet.strip()
            for elemet in selector.css("#js-categories > a::text").getall()
        ],
    }


# list comprehension ou compreenção de lista em portugues

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
    url = "https://www.tecmundo.com.br/mobilidade-urbana-smart-cities/"
    +"155000-musk-tesla-carros-totalmente-autonomos.htm"
    html_content = fetch(url)
    print(scrape_noticia(html_content))
