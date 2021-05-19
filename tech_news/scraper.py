import requests
import time
from requests.exceptions import ReadTimeout
from parsel import Selector


# Requisito 1
def fetch(url):
    time.sleep(1)
    try:
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except ReadTimeout:
        return None


# Requisito 2
def scrape_noticia(html_content):
    selector = Selector(text=html_content)

    url_info = selector.css("link[rel=amphtml]::attr(href)").get()

    title_info = selector.css("h1#js-article-title::text").get()

    time_info = selector.css("time::attr(datetime)").get()
    timestamp_mutated = time_info.replace('01', '00')

    writer_info = selector.css("a.tec--author__info__link::text").get()
    writer_mutated = ""
    if writer_info:
        writer_mutated = writer_info[1:len(writer_info) - 1]
    else:
        writer_mutated = None

    shares_info = selector.css("div.tec--toolbar__item::text").get()
    shares_suffix = " Compartilharam"
    shares_mutated = 0
    if shares_info:
        shares_mutated = int(shares_info[1:-len(shares_suffix)])

    comments_info = selector.css("button::attr(data-count)").get()
    comments_mutated = 0
    if comments_info:
        comments_mutated = int(comments_info)

    summary_info = selector.css("div.tec--article__body *::text").getall()
    summary_selected = []
    index = 0
    while index <= 5:
        summary_selected.append(summary_info[index])
        index += 1
    summary_mutated = "".join(summary_selected)

    return {
        "url": url_info,
        "title": title_info,
        "timestamp": timestamp_mutated,
        "writer": writer_mutated,
        "shares_count": shares_mutated,
        "comments_count": comments_mutated,
        "summary": summary_mutated,
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
