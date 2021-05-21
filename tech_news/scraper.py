import requests
import time
from parsel import Selector
from requests.exceptions import Timeout
from tech_news.database import create_news


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


# Requisito 2
def scrape_noticia(html_content):
    selector = Selector(text=html_content)
    url = selector.css("head link[rel=canonical]::attr(href)").get()
    title = selector.css("#js-article-title ::text").get()
    timestamp = selector.css("#js-article-date::attr(datetime)").get()
    writer = selector.css("a.tec--author__info__link ::text").get().strip()
    shares_count = int(selector.css(
        ".tec--toolbar__item::text"
    ).get().split(' ')[1].strip())
    comments_count = int(selector.css(
        "#js-comments-btn::attr(data-count)"
    ).get())
    summary = selector.css(
        "div.tec--article__body p:nth-child(1) *::text").getall()
    all_summary = "".join(summary)
    source_list = selector.css("div div.z--mb-16 a.tec--badge ::text").getall()
    source = [word.strip() for word in source_list]
    categories_list = selector.css("div#js-categories a::text").getall()
    categories = [category.strip() for category in categories_list]
    page_dict = {
        "url": url,
        "title": title,
        "timestamp": timestamp,
        "writer": writer,
        "shares_count": shares_count,
        "comments_count": comments_count,
        "summary": all_summary,
        "sources": source,
        "categories": categories
    }
    return page_dict


# Requisito 3
def scrape_novidades(html_content):
    if html_content == "":
        return []
    else:
        selector = Selector(text=html_content)
        url_list = selector.css(".tec--card__info h3 a::attr(href)").getall()
        return url_list


# Requisito 4
def scrape_next_page_link(html_content):
    selector = Selector(text=html_content)
    next_page = selector.css(
        "#js-main div > div > .z--col > div.tec--list > a::attr(href)"
    ).get()
    if next_page == "":
        return None
    else:
        return next_page


# Requisito 5
def get_tech_news(amount):
    url = "https://www.tecmundo.com.br/novidades"
    page_news = []
    while True:
        response = fetch(url)
        # scrap da pag novidades
        list_news = scrape_novidades(response)
        for news in list_news:
            # scrap de cada noticia da pag novidades
            next_page = fetch(news)
            next_news = scrape_noticia(next_page)
            # adiciona a prox noticia na lista page_news
            page_news.append(next_news)
            if len(list_news) == amount:
                create_news(page_news)
                return page_news
        # se precisar ir para prox pag de novidades,
        # recebe a url da prox pagina
        url = scrape_next_page_link(response)


if __name__ == '__main__':
    news = get_tech_news(21)
