import requests
import time
from parsel import Selector


def fetch(url):
    try:
        response = requests.get(url, timeout=3)
        time.sleep(1)
        response.raise_for_status()
    except Exception:
        return None
    else:
        return response.text


# Requisito 2
def scrape_noticia(html_content):
    selector = Selector(text=html_content)
    url = selector.css("head link[rel=canonical]::attr(href)").get()
    title = selector.css("#js-article-title::text").get()
    timestamp = selector.css("#js-article-date::attr(datetime)").get()
    writer = selector.css("#js-author-bar > div > p > a::text").get().strip()
    get_shares_count = selector.css(
        "#js-author-bar > nav > div:nth-child(1)::text"
    ).re_first(r"\d+")
    shares_count = int(get_shares_count) if get_shares_count else 0
    comments_count = int(
        selector.css("#js-comments-btn::text").re_first(r"\d+")
    )
    summary_list = selector.css(
        ".tec--article__body > p:nth-child(1) *::text"
    ).getall()
    summary = "".join(summary_list)
    get_sources = selector.css(".z--mb-16 .tec--badge::text").getall()
    sources = [source.strip() for source in get_sources]
    get_categories = selector.css("#js-categories > a *::text").getall()
    categories = [categorie.strip() for categorie in get_categories]
    dic_news = {
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
    return dic_news


# Requisito 3
def scrape_novidades(html_content):
    selector = Selector(text=html_content)
    get_links = selector.css(
        ".tec--list .tec--card__title__link::attr(href)"
    ).getall()
    return get_links


# Requisito 4
def scrape_next_page_link(html_content):
    selector = Selector(text=html_content)
    get_next_page_link = selector.css(".tec--list > a::attr(href)").get()
    return get_next_page_link


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""


if __name__ == "__main__":
    req2 = "https://www.tecmundo.com.br/mobilidade-urbana-smart-cities/155000-musk-tesla-carros-totalmente-autonomos.htm"
    req3 = "https://www.tecmundo.com.br/novidades"
    news = scrape_noticia(fetch(req2))
    links = scrape_novidades(fetch(req3))
    next_page = scrape_next_page_link(fetch(req3))
    print(news, links, next_page)
