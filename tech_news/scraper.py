import time
import requests
from requests.exceptions import ReadTimeout

"""
A função utiliza o método get() da biblioteca requests
A função executada com uma URL correta retorna o conteúdo html
A função, sofrendo timeout, retorna None
A função retorna None quando recebe uma resposta com código diferente de 200
A função respeita o rate limit
"""


# Requisito 1
def fetch(url):
    time.sleep(1)
    try:
        response = requests.get(url, timeout=3)
    except ReadTimeout:
        return None

    return response.text if response.status_code == 200 else None


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
