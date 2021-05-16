from parsel import Selector
import requests
import re
import time


# Requisito 1
def fetch(url):
    # Rate limit respected by waiting 1 second between successive requests
    time.sleep(1)
    try:
        r = requests.get(url, timeout=3)
        r.raise_for_status()  # Raises exception if status != 200
        page = r.text
    except (requests.HTTPError, requests.ReadTimeout) as e:
        # As seen on Stackoverflow: https://tinyurl.com/yb4pnwa6
        # Returns None if exceptions are raised
        print(e)
        return None
    return page


# Requisito 2
def scrape_noticia(html_content):
    selector = Selector(text=html_content)
    title = selector.css('h1::text').get()
    url = selector.xpath('//link[contains(@rel, "canonical")]/@href').get()
    writer_css = selector.css('p > a::text').get()
    writer = writer_css.strip() if not None else None
    timestamp = selector.css('#js-article-date::attr(datetime)').get()
    shares_count = int(selector.xpath(
        '//nav/div[contains(., "Compartilharam")]/text()'
        ).get().strip().split()[0])
    comments_count = int(selector.css(
        '#js-comments-btn::text'
        ).getall()[1].strip().split()[0])
    dirty_summary = selector.css('.tec--article__body p').get()
    cleaner = re.compile('<.*?>')
    summary = re.sub(cleaner, '', dirty_summary)
    dirty_sources = selector.css('.z--mb-16 .tec--badge::text').getall()
    sources = []
    for s in dirty_sources:
        sources.append(s.strip())
    dirty_categories = selector.css('#js-categories a::text').getall()
    categories = []
    for a in dirty_categories:
        categories.append(a.strip())
    news = {
        'url': url,
        'title': title,
        'writer': writer,
        'summary': summary,
        'timestamp': timestamp,
        'shares_count': shares_count,
        'comments_count': comments_count,
        'sources': sources,
        'categories': categories,
    }
    return news


# Requisito 3
def scrape_novidades(html_content):
    """Seu código deve vir aqui"""


# Requisito 4
def scrape_next_page_link(html_content):
    """Seu código deve vir aqui"""


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
