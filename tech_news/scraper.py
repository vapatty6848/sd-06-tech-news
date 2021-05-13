import requests
import time


def fetch(url):
    try:
        response = requests.get(url, timeout=3)
        time.sleep(1)
    except Exception:
        return None
    else:
        return response.text


# Requisito 2
def scrape_noticia(html_content):
    return html_content


# Requisito 3
def scrape_novidades(html_content):
    """Seu código deve vir aqui"""


# Requisito 4
def scrape_next_page_link(html_content):
    """Seu código deve vir aqui"""


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
