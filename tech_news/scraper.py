from parsel import Selector
from tech_news.database import create_news
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
    writer_css = selector.css('.tec--author__info > p > a::text').get()
    writer = writer_css.strip() if writer_css else None
    timestamp = selector.css('#js-article-date::attr(datetime)').get()
    shares_count = selector.xpath(
        '//nav/div[contains(., "Compartilharam")]/text()'
        ).get()
    shares_count = int(re.findall(
        r'\d+', shares_count)[0]
        ) if shares_count is not None else 0
    comments_count = int(selector.css(
        '#js-comments-btn::text'
        ).getall()[1].strip().split()[0])
    dirty_summary = selector.css('.tec--article__body p').get()
    cleaner = re.compile('<.*?>')
    summary = re.sub(cleaner, '', dirty_summary).replace('&amp;', '&')
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
    selector = Selector(text=html_content)
    links = selector.css('h3 .tec--card__title__link').xpath('@href').getall()
    return links


# Requisito 4
def scrape_next_page_link(html_content):
    selector = Selector(text=html_content)
    next_page = selector.xpath('//a[contains(., "Mostrar mais")]/@href').get()
    return next_page


# Requisito 5
def get_tech_news(amount):
    base_url = 'https://www.tecmundo.com.br/novidades'
    news_qty = int(amount)

    links = []
    while len(links) < news_qty:
        news_list_html = fetch(base_url)
        links.extend(scrape_novidades(news_list_html))
        base_url = scrape_next_page_link(news_list_html)

    news_list = []
    for i in range(len(links) - 1):
        while len(news_list) < news_qty:
            news_html = fetch(links[i])
            scraped = scrape_noticia(news_html)
            news_list.append(scraped)
            i += 1

    create_news(news_list)

    return news_list


# %%
# from tech_news.scraper import fetch, scrape_novidades, scrape_next_page_link, scrape_noticia
# base_url = fetch('https://www.tecmundo.com.br/novidades?page=')
# news_qty = 30

# links = scrape_novidades(page)
# news = []
# for news_article in links:
#     news_html = fetch(news_article)
#     scraped = scrape_noticia(news_html)
#     print(scraped['url'])
#     news.append(scraped)
# create_news(news)

# %%
# from tech_news.scraper import fetch, scrape_novidades, scrape_next_page_link, scrape_noticia, get_tech_news

# get_tech_news(30)
# %%
