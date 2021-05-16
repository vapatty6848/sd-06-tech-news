import requests
import time


# Requisito 1
def fetch(url):
    """função responsável por fazer a requisição HTTP para obter o HTML"""
    try:
        time.sleep(1)
        response = requests.get(url, timeout=3)
        response.raise_for_status()
        #  https://docs.python-requests.org/en/master/user/quickstart/
        return response.text

    except (requests.exceptions.HTTPError, requests.ReadTimeout) as error:
        print(error)
        return None


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
