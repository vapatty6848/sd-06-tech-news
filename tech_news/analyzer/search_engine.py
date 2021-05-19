import datetime
from tech_news.database import search_news


# Requisito 6
def search_by_title(title):
    """Retorna notícias buscadas por seu título"""
    news_list_by_title = search_news(
        {"title": {"$regex": title, "$options": "i"}}
    )
    return [(item["title"], item["url"]) for item in news_list_by_title]


# Requisito 7
def search_by_date(date):
    """Retorna notícias buscadas por sua data"""
    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")
        news_list_by_date = search_news({"timestamp": {"$regex": date}})
        return [(item["title"], item["url"]) for item in news_list_by_date]
    except ValueError:
        raise ValueError("Data inválida")


# Requisito 8
def search_by_source(source):
    """Retorna notícias buscadas por sua fonte"""
    news_list_by_source = search_news(
        {"sources": {"$regex": source, "$options": "i"}}
    )
    return [(item["title"], item["url"]) for item in news_list_by_source]


# Requisito 9
def search_by_category(category):
    """Retorna notícias buscadas por sua fonte"""
    news_list_by_category = search_news(
        {"categories": {"$regex": category, "$options": "i"}}
    )
    return [(item["title"], item["url"]) for item in news_list_by_category]
