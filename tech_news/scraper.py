import time
import requests
from requests.exceptions import HTTPError, ReadTimeout
import parsel
from tech_news.database import create_news


# Requisito 1
def fetch(url):
    """Função para fazer a requisição HTTP"""
    time.sleep(1)
    try:
        response = requests.get(url, timeout=3)
    except ReadTimeout as error:
        print(f"Timeout Error: {error}.")
        return None

    try:
        response.raise_for_status()
    except HTTPError as error:
        print(f"HTTP Error: {error}.")
        return None

    return response.text


# Requisito 2
def scrape_noticia(html_content):
    """Função para fazer o scrape de noticias"""
    selector = parsel.Selector(html_content)

    url = selector.css("head link[rel=canonical]::attr(href)").get()
    title = selector.css("h1::text").get()
    timeStamp = selector.css(
        ".tec--timestamp__item"
    ).xpath("./time/@datetime").get()

    writer = selector.css("#js-author-bar .z--font-bold a::text").get()
    sharesCount = selector.css(
        ".tec--toolbar__item::text"
    ).re_first(r"\d+")

    commentsCount = selector.css("#js-comments-btn::attr(data-count)").get()
    summary = selector.css(
        ".tec--article__body p:nth-child(1) *::text"
    ).getall()

    sources = selector.css(".z--mb-16 .tec--badge::text").getall()
    categories = selector.css("#js-categories > a *::text").getall()

    return {
        'url': url,
        'title': title,
        'timestamp': timeStamp,
        'writer': writer.strip() if writer else None,
        'shares_count': int(sharesCount) if sharesCount else 0,
        'comments_count': int(commentsCount) if commentsCount else 0,
        'summary': ''.join(summary),
        'sources': [source.strip() for source in sources],
        'categories': [category.strip() for category in categories]
    }


# Requisito 3
def scrape_novidades(html_content):
    """Função para fazer o scrape de novidades"""
    if html_content == "":
        return []
    else:
        selector = parsel.Selector(html_content)
        novidades = selector.css(
            "div.tec--card__info h3 a::attr(href)"
        ).getall()

        return novidades


# Requisito 4
def scrape_next_page_link(html_content):
    """Função para fazer o scrape do link da proxima página"""
    selector = parsel.Selector(html_content)
    link = selector.xpath(
        "//*[@id='js-main']/div/div/div[1]/div[2]/a/@href"
    ).get() or None

    return link


# Requisito 5
def get_tech_news(amount):
    """Função para fazer obter todas as noticias"""
    url = "https://www.tecmundo.com.br/novidades"
    result = []
    while url:
        urlResponse = fetch(url)
        news = scrape_novidades(urlResponse)
        for new in news:
            newResponse = fetch(new)
            newResult = scrape_noticia(newResponse)
            result.append(newResult)

            if amount == len(result):
                create_news(result)
                return result

        url = scrape_next_page_link(urlResponse)
