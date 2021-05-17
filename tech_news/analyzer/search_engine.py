from tech_news.database import search_news
import re
from datetime import datetime


# Requisito 6
def search_by_title(title):
    """Seu código deve vir aqui"""
    regx = re.compile(title, re.IGNORECASE)
    result_news = search_news({'title': regx})
    return [(new["title"], new["url"]) for new in result_news]

# class ValueError(Exception):
#     pass


# Requisito 7
def search_by_date(date):
    """Seu código deve vir aqui"""
    try:
        datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Data inválida")
    ola = re.compile(f"^{date}")
    result_news = search_news({'timestamp': ola})
    return [(new["title"], new["url"]) for new in result_news]
# search_by_date("2021-05-17")

# Requisito 8
def search_by_source(source):
    """Seu código deve vir aqui"""


# Requisito 9
def search_by_category(category):
    """Seu código deve vir aqui"""
