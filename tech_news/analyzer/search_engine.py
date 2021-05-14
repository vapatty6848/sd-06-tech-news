from tech_news.database import search_news
import re


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
    """Seu código deve vir aqui"""


# Requisito 8
def search_by_source(source):
    """Seu código deve vir aqui"""


# Requisito 9
def search_by_category(category):
    """Seu código deve vir aqui"""
