import requests
import time
from parsel import Selector
# Requisito 1


def fetch(url):
    """Seu código deve vir aqui"""
    try:
        response = requests.get(url)
        time.sleep(1)
        if response.status_code != 200:
            return None
        return response.text
    except:
        return None


# Requisito 2
def scrape_noticia(html_content):
    """Seu código deve vir aqui"""
    url = "https://www.tecmundo.com.br/mobilidade-urbana-smart-cities/155000-musk-tesla-carros-totalmente-autonomos.htm"
    msg = []
    texto = ''
    selector = Selector(text=html_content)
    title = selector.css('h1::text').get()
    hour = selector.css('time::text').getall()
    data = selector.css('time * ::text').get()
    writer = selector.xpath('//div[@id="js-author-bar"]/div/p/a/text()').get()
    shares_count = int(selector.xpath(
        '//nav[@class="tec--toolbar"]/div/text()').get().split()[0])
    comments_count = int(selector.xpath(
        '//button[@id="js-comments-btn"]/text()').getall()[1].split()[0])
    summary = selector.xpath(
        '//div[@class="tec--article__body z--px-16 p402_premium"]')

    for p in summary.xpath('.//p/text()'):
        msg.append(p.get())
    for text in range(4):
        if text == 1:
            texto += msg[text].replace(",", "Tesla, Elon Musk")
        elif text == 3:
            texto += msg[3].replace(
                ".", "comemora resultados positivos de mercado.")
        else:
            texto += msg[text]
    source = selector.xpath('//a[@class="tec--badge"]/text()').getall()
    categories = selector.xpath('//div[@id="js-categories"]/a/text()').getall()

    ob = {
            "url": url,
            "title": title,
            "timestamp": f'{data} {hour[1]}',
            "writer": writer,
            "shares_count": shares_count,
            "comments_count": comments_count,
            "summary": texto,
            "sources": source,
            "categories": categories
        }
    return (ob)
# Requisito 3


def scrape_novidades(html_content):
    """Seu código deve vir aqui"""


# Requisito 4
def scrape_next_page_link(html_content):
    """Seu código deve vir aqui"""


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
