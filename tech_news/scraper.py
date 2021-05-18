import requests
from parsel import Selector
from time import sleep


# Requisito 1
def fetch(url):
    sleep(1)
    try:
        response = requests.get(url, timeout=3)
    except requests.ReadTimeout:
        return None
    else:
        if response.status_code == 200:
            return response.text
        else:
            return None


# Requisito 2
def scrape_noticia(html_content):
    selector = Selector(text=html_content)
    url = selector.css("link[rel=canonical]::attr(href)").get()
    title = selector.css("#js-article-title::text").get()
    timestamp = selector.css("time::attr(datetime)").get()
    writer = selector.css(".z--m-none a::text").get().strip()
    shares_count = selector.css(".tec--toolbar__item::text").re_first(r"\d+")
    shares_count = int(shares_count) if shares_count else 0
    comments_count = int(
        selector.css("#js-comments-btn::text").re_first(r"\d+")
    )
    summary = "".join(
        selector.css(".tec--article__body p:nth-child(1) *::text").getall()
    )
    sources = selector.css(".z--mb-16 div a::text").getall()
    sources_strip = []
    for source in sources:
        sources_strip.append(source.strip())
    categories = selector.css("#js-categories a::text").getall()
    categories_strip = []
    for categorie in categories:
        categories_strip.append(categorie.strip())
    notice_infos = {
        "url": url,
        "title": title,
        "timestamp": timestamp,
        "writer": writer,
        "shares_count": shares_count,
        "comments_count": comments_count,
        "summary": summary,
        "sources": sources_strip,
        "categories": categories_strip,
    }

    return notice_infos


# Requisito 3
def scrape_novidades(html_content):
    selector = Selector(text=html_content)
    links = selector.css(".tec--list__item h3 a::attr(href)").getall()
    return links


# Requisito 4
def scrape_next_page_link(html_content):
    selector = Selector(text=html_content)
    link_next_page = selector.css(".tec--btn::attr(href)").get()
    return link_next_page
    

# Requisito 5
def get_tech_news(amount):




response = requests.get("https://www.tecmundo.com.br/novidades")
html_content = response.text
get_tech_news(html_content)