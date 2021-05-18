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
    except requests.ReadTimeout:
        return None


# Requisito 2
def scrape_noticia(html_content):
    """Seu código deve vir aqui"""
    strip_source = []
    strip_categories = []
    texto = ''
    selector = Selector(text=html_content)
    title = selector.css('h1::text').get()
    data = selector.css('time::attr(datetime)').get()
    writer = selector.xpath(
        '//div[@id="js-author-bar"]/div/p/a/text()').get().strip()
    shares_count = int(selector.xpath(
        '//nav[@class="tec--toolbar"]/div/text()').get().split()[0])
    comments_count = int(selector.xpath(
        '//button[@id="js-comments-btn"]/text()').getall()[1].split()[0])

    summary = selector.xpath(
        '//div[@class="tec--article__body z--px-16 p402_premium"]/p').css(
            '::text').getall()
    for sum in range(7):
        texto += summary[sum]

    source = selector.xpath('//a[@class="tec--badge"]/text()').getall()
    for each in source:
        strip_source.append(each.strip())
    categories = selector.xpath('//div[@id="js-categories"]/a/text()').getall()
    for each in categories:
        strip_categories.append(each.strip())

    url = selector.xpath(
        '//link[contains(@rel, "canonical")]').css('::attr(href)').get()

    ob = {
            "url": url,
            "title": title,
            "timestamp": data,
            "writer": writer,
            "shares_count": shares_count,
            "comments_count": comments_count,
            "summary": texto,
            "sources": strip_source,
            "categories": strip_categories
        }
    return (ob)
# Requisito 3


def scrape_novidades(html_content):
    """Seu código deve vir aqui"""
    selector = Selector(text=html_content)
    try:
        url_news = selector.xpath(
            '//h3[@class="tec--card__title"]/a').css('::attr(href)').getall()
        return (url_news)
    except requests.URLRequired:
        return []


# Requisito 4
def scrape_next_page_link(html_content):
    """Seu código deve vir aqui"""
    selector = Selector(text=html_content)
    try:
        next_page = selector.xpath(
            '//a[text()=" Mostrar mais notícias "]').css('::attr(href)').get()
        return next_page
    except requests.URLRequired:
        return None


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
