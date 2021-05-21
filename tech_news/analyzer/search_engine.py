from tech_news.database import search_news
from datetime import datetime


# Requisito 6
def search_by_title(title):
    result = search_news({"title": {"$regex": title, "$options": "i"}})
    if result:
        for item in result:
            return [(item["title"], item["url"])]
    return []


# Requisito 7
def search_by_date(date):
    try:
        datetime.strptime(date, "%Y-%m-%d")
        result = search_news({"timestamp": {"$regex": date}})
        if result:
            for item in result:
                return [(item["title"], item["url"])]
        return []
    except ValueError:
        raise ValueError("Data inválida")


# Requisito 8
def search_by_source(source):
    """Seu código deve vir aqui"""


# Requisito 9
def search_by_category(category):
    """Seu código deve vir aqui"""
