import requests
import time
from parsel import Selector
from tech_news.database import create_news


# Requisito 1
def fetch(url):
    """Seu código deve vir aqui"""
    time.sleep(1)
    try:
        response = requests.get(url, timeout=3)
    except requests.ReadTimeout:
        return None
    if response.status_code == 200:
        return response.text
    else:
        return None


# Requisito 2
def scrape_noticia(html_content):
    """Seu código deve vir aqui"""
    selector = Selector(text=html_content)

    url_selector = selector.css("head > link:nth-child(26)::attr(href)").get()
    title_selector = selector.css("#js-article-title::text").get()
    time_stamp_selector = selector.css(
        "#js-article-date::attr(datetime)"
    ).get()
    writer_selector = selector.css(
        "#js-author-bar > div > p.z--m-none.z--truncate.z--font-bold > a::text"
    ).get()
    writer_name = writer_selector.strip() if writer_selector else None
    count_selector = selector.css(
        "#js-author-bar > nav > div:nth-child(1)::text"
    ).get()
    shares_count = int(count_selector.split()[0]) if count_selector else 0
    comments_count_selector = selector.css(
        "#js-comments-btn::attr(data-count)"
    ).get()
    comments = (
        int(comments_count_selector) if comments_count_selector else None
    )
    summary_selector = selector.css(
        "#js-main div.tec--article__body p:nth-child(1) *::text"
    ).getall()
    summary_all = "".join(summary_selector)
    sources_selector = selector.css(
        "#js-main div.tec--article__body-grid > div.z--mb-16 > div > a::text"
    ).getall()
    sources_list = [source.strip() for source in sources_selector]
    categories_selector = selector.css("#js-categories > a::text").getall()
    categories_list = [category.strip() for category in categories_selector]

    new_data = {
        "url": url_selector,
        "title": title_selector,
        "timestamp": time_stamp_selector,
        "writer": writer_name,
        "shares_count": shares_count,
        "comments_count": comments,
        "summary": summary_all,
        "sources": sources_list,
        "categories": categories_list,
    }

    return new_data


# Requisito 3
def scrape_novidades(html_content):
    """Seu código deve vir aqui"""
    selector = Selector(text=html_content)
    urls_selector = selector.css(
        "#js-main div.tec--list.tec--list--lg div > h3 > a::attr(href)"
    ).getall()
    urls_news = urls_selector if urls_selector else []
    return urls_news


# Requisito 4
def scrape_next_page_link(html_content):
    """Seu código deve vir aqui"""
    selector = Selector(text=html_content)
    next_page_selector = selector.css(
        "#js-main div.tec--list.tec--list--lg > a::attr(href)"
    ).get()
    return next_page_selector


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
    url_fetch = "https://www.tecmundo.com.br/novidades"
    news = []
    while len(news) < amount:
        page_data = fetch(url_fetch)
        urls = scrape_novidades(page_data)
        for url in urls:
            page_new_data = fetch(url)
            data = scrape_noticia(page_new_data)
            news.append(data)
            if len(news) == amount:
                create_news(news)
        url = scrape_next_page_link(page_new_data)
    return news
