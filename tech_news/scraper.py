import requests
from parsel import Selector
from time import sleep


# Requisito 1
def fetch(url):
    sleep(1)
    try:
        response = requests.get(url, timeout=3)
        if (response.status_code == 200):
            return response.text
        else:
            return None
    except requests.Timeout:
        return None


# Requisito 2
def scrape_noticia(html_content):
    # Selector for the card
    selector = Selector(text=html_content)
    url = selector.css("head > link[rel=canonical]::attr(href)").get()
    title = selector.css(".tec--article__header__title::text").get()
    timestamp = selector.css("#js-article-date::attr(datetime)").get()

    # Request for the news url using card selector
    writer = selector.css(".tec--author__info__link::text").get()
    writer = writer.strip() if writer else None

    # treating the return of the counting shares of the post
    shares_count = selector.css(".tec--toolbar__item::text").get()
    shares_count = int(shares_count.split()[0]) if shares_count else 0

    comments_count = int(selector.css(
        ".tec--toolbar__item #js-comments-btn::attr(data-count)"
    ).get())

    # treating the return of the summary
    summary = "".join(selector.css(
        ".tec--article__body p:first-child *::text"
    ).getall())

    sources = selector.css(".z--mb-16 div *::text").getall()
    sources = [item.strip() for item in sources if item != ' ']

    categories = selector.css("#js-categories *::text").getall()
    categories = [
        category.strip() for category in categories if category != ' '
    ]

    return {
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


# Requisito 3
def scrape_novidades(html_content):
    selector = Selector(text=html_content)
    return selector.css(
        ".tec--list .tec--card__title__link::attr(href)"
    ).getall()
    # urls = selector.css("a.tec--card__title__link::attr(href)").getall()
    # return urls


# Requisito 4
def scrape_next_page_link(html_content):
    """Seu código deve vir aqui"""


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""


# html_content = fetch("https://www.tecmundo.com.br/novidades")

# print(scrape_novidades(html_content))
# html_content = fetch(
#     "https://www.tecmundo.com.br/mobilidade-urbana-smart-cities/155000-musk-tesla-carros-totalmente-autonomos.htm"
# )

# print(scrape_noticia(html_content))
# print(type(int(" 0 Compartilharam".split()[0])))
