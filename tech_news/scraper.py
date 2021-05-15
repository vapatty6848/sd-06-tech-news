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
        r.raise_for_status() # Raises exception if status != 200
        page = r.text
    except (requests.HTTPError, requests.ReadTimeout) as e:
        # As seen on Stackoverflow: https://tinyurl.com/yb4pnwa6
        # Returns None if exceptions are raised
        print(e)
        return None
    return page


# Requisito 2
def scrape_noticia(html_content):
    """Seu código deve vir aqui"""


# Requisito 3
def scrape_novidades(html_content):
    """Seu código deve vir aqui"""


# Requisito 4
def scrape_next_page_link(html_content):
    """Seu código deve vir aqui"""


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
