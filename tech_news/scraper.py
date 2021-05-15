import requests
import time
import re
from parsel import Selector
from tech_news.database import create_news


# Requisito 1
def fetch(url):
    """Pega as notícias através da URL informada e retorna como html/txt"""
    try:
        time.sleep(1)
        response = requests.get(url, timeout=3)
        response.raise_for_status()
        return response.text
    except requests.exceptions.ConnectionError as error:
        print(f"Erro na requisição: {error}.")
        return None
    except requests.exceptions.ReadTimeout as error:
        print(f"Sem resposta do servidor: {error}.")
        return None
    except Exception:
        return None


# Requisito 2
def scrape_noticia(html_content):
    """
    Recebe o conteúdo html/txt de uma página e
    busca notícias para preencher um dicionário
    """
    selector = Selector(text=html_content)
    url = selector.css("link[rel=canonical]::attr(href)").get()
    title = selector.css(".tec--article__header__title::text").get()
    timestamp = selector.css(
        ".tec--timestamp__item time::attr(datetime)"
    ).get()
    writer = selector.css(".tec--author__info__link::text").get()
    shares_count = selector.css(".tec--toolbar__item::text").get()
    if shares_count != None:
        shares_count = re.sub("[^0-9]", "", shares_count)
    comments_count = selector.css("#js-comments-btn::attr(data-count)").get()
    summary = "".join(
        selector.css("div.tec--article__body p:nth-child(1) *::text").getall()
    )
    sources = selector.css("div.z--mb-16 a.tec--badge::text").getall()
    sources = [source.strip() for source in sources]
    categories = selector.css("div#js-categories a::text").getall()
    categories = [categorie.strip() for categorie in categories]
    return {
        "url": url,
        "title": title,
        "timestamp": timestamp,
        "writer": None if writer == None else writer.strip(),
        "shares_count": 0 if shares_count == None else int(shares_count),
        "comments_count": int(comments_count),
        "summary": summary,
        "sources": sources,
        "categories": categories,
    }


# Requisito 3
def scrape_novidades(html_content):
    """
    Fará o scrape da página Novidades para obter
    as URLs das páginas de notícias.
    """
    selector = Selector(text=html_content)
    links = selector.css(
        "div.tec--list__item .tec--card__title__link::attr(href)"
    ).getall()
    return links


# Requisito 4
def scrape_next_page_link(html_content):
    """
    Faz o scrape do link da próxima página
    """
    selector = Selector(text=html_content)
    link = selector.css("a.tec--btn.tec--btn--lg::attr(href)").get()
    return link


# Requisito 5
def get_tech_news(amount):
    """
    Pega notícias de acordo com a quantidade passada pelo parâmetro
    """
    url = "https://www.tecmundo.com.br/novidades"
    data = []
    while True:
        html_content = fetch(url)
        news_urls = scrape_novidades(html_content)
        for news_url in news_urls:
            news = scrape_noticia(fetch(news_url))
            data.append(news)
            if len(data) == amount:
                create_news(data)
                return data
        url = scrape_next_page_link(html_content)
