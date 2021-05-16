import requests
import time
from parsel import Selector
import re


# Requisito 1
def fetch(url):
    """função responsável por fazer a requisição HTTP para obter o HTML"""
    try:
        time.sleep(1)
        response = requests.get(url, timeout=3)
        response.raise_for_status()
        #  "método se cair "família de erro" ele literalmente joga um erro"
        #  https://docs.python-requests.org/en/master/user/quickstart/
        return response.text

    except (requests.exceptions.HTTPError, requests.ReadTimeout) as error:
        print(error)
        return None


# Requisito 2
def scrape_noticia(html_content):
    """Extrai o conteúdo HTML da página e busca as informações das notícias"""
    #  Pegar queries pelo inspecionar no browser
    selector = Selector(text=html_content)
    url = selector.css("link[rel=canonical]::attr(href)").get()
    title = selector.css(".tec--article__header__title::text").get()
    timestamp = selector.css(
        ".tec--timestamp__item time::attr(datetime)"
    ).get()

    writer = selector.css(".tec--author__info__link::text").get()
    #  Strip() -> Remova os espaços no início e no final da string
    if writer is not None:
        writer = writer.strip()

    shares_count = selector.css(".tec--toolbar__item::text").get()
    if shares_count is not None:
        #  https://docs.python.org/pt-br/3/library/re.html
        #  https://ic.unicamp.br/~mc102/aulas/aula15.pdf
        shares_count = int(re.sub("[^0-9]", "", shares_count))
    else:
        shares_count = 0

    comments_count = selector.css("#js-comments-btn::attr(data-count)").get()
    if comments_count is not None:
        comments_count = int(comments_count)

    #  Pega o texto do parágrafo e os filhos e join junta num só
    summary = "".join(
        selector.css("div.tec--article__body p:nth-child(1) *::text").getall()
    )

    sources = selector.css("div.z--mb-16 a.tec--badge::text").getall()
    #  for/in para remover os espaçosno início e no final
    sources = [source.strip() for source in sources]

    categories = selector.css("div#js-categories a::text").getall()
    categories = [categorie.strip() for categorie in categories]

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
    """A função faz scrape da pág Novidades p/ obter URLs da pág de notícias"""
    selector = Selector(text=html_content)
    urls = selector.css(".tec--list div h3 a::attr(href)").getall()
    return urls


# Requisito 4
def scrape_next_page_link(html_content):
    """Pega link do botão próxima página"""
    selector = Selector(text=html_content)
    next_page = selector.css("a.tec--btn.tec--btn--lg::attr(href)").get()
    return next_page


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
