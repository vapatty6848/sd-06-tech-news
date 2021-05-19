from tech_news.database import search_news
from datetime import datetime


# Requisito 6
def search_by_title(title):
    """Seu código deve vir aqui"""
    search_title = search_news({"title": {"$regex": title, "$options": "i"}})
    if search_title:
        for item in search_title:
            return [(item["title"], item["url"])]
    return []


# Requisito 7
def search_by_date(date):
    """Seu código deve vir aqui"""
    try:
        datetime.strptime(date, "%Y-%m-%d")
        search_date = search_news({"timestamp": {"$regex": date}})
        if search_date:
            for item in search_date:
                return [(item["title"], item["url"])]
        return []
    except ValueError:
        raise ValueError("Data inválida")


# Requisito 8
def search_by_source(source):
    """Seu código deve vir aqui"""
    search_source = search_news(
        {"sources": {"$regex": source, "$options": "i"}}
    )
    if search_source:
        for item in search_source:
            return [(item["title"], item["url"])]
    return []


# Requisito 9
def search_by_category(category):
    """Seu código deve vir aqui"""
    search_category = search_news(
        {"categories": {"$regex": category, "$options": "i"}}
    )
    if search_category:
        for item in search_category:
            return [(item["title"], item["url"])]
    return []
