import requests
import time
from requests.exceptions import HTTPError, ReadTimeout


# Requisito 1
def fetch(url):
    """faz a requisição HTTP"""
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
