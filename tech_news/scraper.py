from parsel import Selector
import requests
import time
from tech_news.database import create_news


# Requisito 1
def fetch(url):
    """Seu código deve vir aqui"""
    time.sleep(1)
    try:
        response = requests.get(url, timeout=3)
    except requests.Timeout:
        return None
    if response.status_code == 200:
        return response.text
    return None


# Requisito 2
def scrape_noticia(html_content):
    """Seu código deve vir aqui"""
    selector = Selector(text=html_content)
    url = selector.css('link[rel="canonical"]::attr(href)').get()
    title = selector.css('h1.tec--article__header__title::text').get()
    timestamp = selector.css('time::attr(datetime)').get()

    get_writer = selector.css('a.tec--author__info__link::text').get()
    writer = get_writer.strip() if (get_writer) else None

    get_shares_count = selector.css('div.tec--toolbar__item::text').get()
    shares_count = int(
        get_shares_count.strip().split()[0]
    ) if (get_shares_count) else 0

    get_comments_count = "".join(
        selector.css('button.tec--btn *::text').getall()
    ).strip().split()
    comments_count = int(get_comments_count[0]) if (
        len(get_comments_count) != 0
    ) else 0

    summary = "".join(selector.css(
        'div.tec--article__body p:first-child *::text'
    ).getall())
    sources = [source.strip() for source in selector.css(
        'div.z--mb-16 div a::text'
    ).getall()]
    categories = [category.strip() for category in selector.css(
        '#js-categories a::text'
    ).getall()]
    return {
        "url": url,
        "title": title,
        "timestamp": timestamp,
        "writer": writer,
        "shares_count": shares_count,
        "comments_count": comments_count,
        "summary": summary,
        "sources": sources,
        "categories": categories
    }


# Requisito 3
def scrape_novidades(html_content):
    """Seu código deve vir aqui"""
    selector = Selector(text=html_content)
    return selector.css(
        'h3.tec--card__title a.tec--card__title__link::attr(href)'
    ).getall()


# Requisito 4
def scrape_next_page_link(html_content):
    """Seu código deve vir aqui"""
    selector = Selector(text=html_content)
    return selector.css('a.tec--btn::attr(href)').get()


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
    html_content = fetch("https://www.tecmundo.com.br/novidades")

    links_novidades = scrape_novidades(html_content)

    news = []

    index = 0
    while len(news) < amount:
        if index == len(links_novidades):
            next_page_link = scrape_next_page_link(html_content)
            html_content = fetch(next_page_link)
            links_novidades = scrape_novidades(html_content)
            index = 0
        html_content_noticia = fetch(links_novidades[index])
        news.append(scrape_noticia(html_content_noticia))
        index += 1
    create_news(news)
    return news
