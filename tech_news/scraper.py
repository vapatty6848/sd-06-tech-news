import requests
import time
from parsel import Selector


# Requisito 1
def fetch(url):
    """Seu código deve vir aqui"""

    time.sleep(1)
    try:
        response = requests.get(url, timeout=3)
    except requests.ReadTimeout:
        return None

    if (response.status_code == 200):
        return response.text
    else:
        return None


# Requisito 2
def scrape_noticia(html_content):
    """Seu código deve vir aqui"""
    selector = Selector(text=html_content)

    url = selector.css("head > link:nth-child(26)::attr(href)").get()
    title = selector.css("#js-article-title::text").get()
    time_stamp = selector.css("#js-article-date::attr(datetime)").get()
    writer = selector.css(
        "#js-author-bar > div > p.z--m-none.z--truncate.z--font-bold > a::text"
    ).get()
    writer_name = writer.strip() if writer else None
    count = selector.css(
        "#js-author-bar > nav > div:nth-child(1)::text"
    ).get()
    shares_count = int(count.split()[0]) if count else 0
    comments_count = int(
        selector.css("#js-comments-btn::attr(data-count)").get()
    )
    summary = selector.css(
        "#js-main div.tec--article__body p:nth-child(1) *::text"
    ).getall()
    summary_all = ''.join(summary)
    sources = selector.css(
        "#js-main div.z--mb-16.z--px-16 > div > a::text"
    ).getall()
    sources_list = [source.strip() for source in sources]
    categories = selector.css("#js-categories > a::text").getall()
    categories_list = [category.strip() for category in categories]

    new_data = {
        "url": url,
        "title": title,
        "timestamp": time_stamp,
        "writer": writer_name,
        "shares_count": shares_count,
        "comments_count": comments_count,
        "summary": summary_all,
        "sources": sources_list,
        "categories": categories_list
    }

    return new_data


# Requisito 3
def scrape_novidades(html_content):
    """Seu código deve vir aqui"""
    selector = Selector(text=html_content)
    urls = selector.css(
        "#js-main div.tec--list.tec--list--lg div > h3 > a::attr(href)"
    ).getall()
    urls_all = urls if urls else []
    return urls_all


# Requisito 4
def scrape_next_page_link(html_content):
    """Seu código deve vir aqui"""
    selector = Selector(text=html_content)
    next_page = selector.css(
        "#js-main div.tec--list.tec--list--lg > a::attr(href)"
    ).get()
    return next_page


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
