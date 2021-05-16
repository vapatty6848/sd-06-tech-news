import requests
import time
from parsel import Selector


# Requisito 1
def fetch(url):
    """Seu código deve vir aqui"""
    try:
        time.sleep(1)
        response = requests.get(url, timeout=1)

        if response.status_code != 200:
            return None

        return response.text
    except requests.ReadTimeout:
        requests.ReadTimeout


# Requisito 2
def scrape_noticia(html_content):
    """Seu código deve vir aqui"""
    s = Selector(text=html_content)
    url = s.xpath('//link[@rel="amphtml"]').get().split('href="')[1]
    url = url.split('">')[0]
    url = url.replace("amp/", "")
    title = s.css(".tec--article__header__title::text").get()
    timestamp = s.css("time").xpath("@datetime").get()
    writer = s.css(".tec--author__info__link::text").get().strip()
    shares_element = s.css(".tec--toolbar__item::text").getall()[0]
    shares_count = shares_element.split(" ")[1].split(" ")[0]
    shares_count = int(shares_count)
    comments_element = s.css("#js-comments-btn::text").getall()[1]
    comments_count = comments_element.split(" ")[1].split(" ")[0]
    comments_count = int(comments_count)
    summary_selector = "div.tec--article__body > p:nth-child(1) *::text"
    summary_content = s.css(summary_selector).getall()
    summary = "".join(summary_content)
    sources = []
    sources_list = s.css(
        ".tec--article__body-grid .z--mb-16 div a::text"
    ).getall()
    for source in sources_list:
        sources.append(source.strip())
    categories = []
    categories_list = s.css("#js-categories a::text").getall()
    for category in categories_list:
        categories.append(category.strip())
    scraped_news = {
        "url": url,
        "title": title,
        "timestamp": timestamp,
        "writer": writer,
        "shares_count": shares_count,
        "comments_count": comments_count,
        "summary": summary,
        "sources": sources,
        "categories": categories,
    }

    return scraped_news


# Requisito 3
def scrape_novidades(html_content):
    """Seu código deve vir aqui"""


# Requisito 4
def scrape_next_page_link(html_content):
    """Seu código deve vir aqui"""


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
