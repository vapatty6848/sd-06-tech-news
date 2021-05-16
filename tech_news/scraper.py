# Requisito 1
def fetch(url):
    url = "https://www.tecmundo.com.br/novidades"
    try:
        response = requests.get(url, timeout=1)
    except requests.ReadTimeout:
        response = requests.get(url, timeout=2)
    finally:
        print (response.status_code)


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
