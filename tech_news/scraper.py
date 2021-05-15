import requests
import time
from parsel import Selector


# Requisito 1
def fetch(url):
    try:
        response = requests.get(url, timeout=3)
        time.sleep(1)
        if(response.status_code != 200):
            return None
        return response.text
    except requests.ReadTimeout:
        return None


# Requisito 2
def scrape_noticia(html_content):
    selector = Selector(text=html_content)
    url_content = str(selector.css("head meta").getall()[4]).split("content=")
    title_content = selector.css("h1::text").get()
    timestamp = str(selector.css("time[datetime]").get())[16:35]
    writer_content = selector.css("a.tec--author__info__link::text").get()
    shares = str(selector.css("div.tec--toolbar__item::text").get()).split()[0]
    coments_count = selector.css("div.tec--toolbar__item button::text")
    coments = str(coments_count.getall()[1]).split()[0]

    summary = selector.css("div.tec--article__body p:first-child *::text")
    summary_content = summary.getall()
    summary_join = "".join(str(item) for item in summary_content)

    def remove_blanks(item):
        return item[1:-1]

    sources_content = selector.css("div.z--mb-16 a.tec--badge::text").getall()
    sources = []
    for item in sources_content:
        sources.append(remove_blanks(item))

    categories_content = selector.css("a.tec--badge--primary::text").getall()
    categories = []
    for item in categories_content:
        categories.append(remove_blanks(item))

    new_dict = {
        "url": url_content[1][1:-2],
        "title": title_content,
        "timestamp": timestamp,
        "writer": writer_content[1:-1],
        "shares_count": int(shares),
        "comments_count": int(coments),
        "summary": summary_join,
        "sources": sources,
        "categories": categories
    }

    return(new_dict)


# Requisito 3
def scrape_novidades(html_content):
    """Seu código deve vir aqui"""


# Requisito 4
def scrape_next_page_link(html_content):
    """Seu código deve vir aqui"""


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
