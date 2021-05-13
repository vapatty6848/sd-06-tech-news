from parsel import Selector
import requests
import time

# Requisito 1
def fetch(url):
    """Seu código deve vir aqui"""
    time.sleep(1)
    try:
        response = requests.get(url, timeout=3)
        print(response.status_code)
    except requests.Timeout:
        print("deu erro")
        return None
    if response.status_code == 200:
        # print(response.text)
        return response.text
    return None
# print(fetch("https://httpbin.org/delay/5"))

# def value_default(value, default):
#     if (value):
#         return default


# Requisito 2
def scrape_noticia(html_content):
    """Seu código deve vir aqui"""
    selector = Selector(text=html_content)
    print(selector.css('#js-categories a::text').getall())
    # print(selector.css('button.tec--btn *::text').get())
    url = selector.css('link[rel="canonical"]::attr(href)').get().strip()
    title = selector.css('h1.tec--article__header__title::text').get().strip()
    timestamp = selector.css('div.tec--timestamp__item time::attr(datetime)').get().strip()

    get_writer = selector.css('a.tec--author__info__link::text').get()
    # print('get_writer', get_writer)
    writer = get_writer.strip() if (get_writer) else None

    get_shares_count = selector.css('div.tec--toolbar__item::text').get()
    # print('get_shares_count', get_shares_count)
    shares_count = get_shares_count.strip().split()[0] if (get_shares_count) else 0

    # comments_count = selector.css('button.tec--btn *::text').get().strip().split()[0]

    summary = selector.css('div.tec--article__body.z--px-16.p402_premium p *::text').get().strip()
    sources = [source.strip() for source in selector.css('div.z--mb-16.z--px-16 div a::text').getall()]
    categories = [category.strip() for category in selector.css('#js-categories a::text').getall()]
    return {
        "url": url,
        "title": title,
        "timestamp": timestamp,
        "writer": writer,
        "shares_count": shares_count,
        "comments_count": "",
        "summary": summary,
        "sources": sources,
        "categories": categories
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
