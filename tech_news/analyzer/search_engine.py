from tech_news.database import search_news
import re
from datetime import datetime


# Requisito 6
def search_by_title(title):
    """Faz buscas nas notícias por título no DB"""
    try:
        search = title.lower()
    except AttributeError:
        print('Please use a valid string.')
        return None

    regex = re.compile(rf'{search}', re.IGNORECASE)
    query = {'title': {'$regex': regex}}
    results_raw = search_news(query)
    results = [(result['title'], result['url']) for result in results_raw]
    return results


# Requisito 7
def search_by_date(date):
    """Faz buscas nas notícias por data no DB"""
    try:
        search = date.split('-')
        ano = int(search[0])
        mes = int(search[1])
        dia = int(search[2])
        start = datetime(ano, mes, dia).isoformat()
        end = datetime(ano, mes, dia, 23, 59, 59).isoformat()
    except Exception:
        raise ValueError('Data inválida')

    query = {
        'timestamp': {
            '$gte': start,
            '$lte': end
        }
    }
    results_raw = search_news(query)
    results = [(result['title'], result['url']) for result in results_raw]
    return results


# Requisito 8
def search_by_source(source):
    """Seu código deve vir aqui"""


# Requisito 9
def search_by_category(category):
    """Seu código deve vir aqui"""
