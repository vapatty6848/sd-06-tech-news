from tech_news.database import search_news
import datetime


# Requisito 6
def search_by_title(title):
    """Method to search news by title"""

    query = {"title": {"$regex": title, "$options": "i"}}
    title_news = search_news(query)
    if title_news:
        for news in title_news:
            return [(news["title"], news["url"])]
    else:
        return []


# Requisito 7
def search_by_date(date):
    """Method to search news by date"""

    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Data inválida")

    query = {"timestamp": {"$regex": date}}
    query_result = search_news(query)
    result = [(news["title"], news["url"]) for news in query_result]
    return result


# Requisito 8
def search_by_source(source):
    """Seu código deve vir aqui"""


# Requisito 9
def search_by_category(category):
    """Seu código deve vir aqui"""
