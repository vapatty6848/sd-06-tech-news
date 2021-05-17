from tech_news.database import search_news
from datetime import datetime


# Requisito 6
# https://docs.mongodb.com/manual/reference/operator/query/regex/
def search_by_title(title):
    try:
        news = search_news({"title": {"$regex": title, "$options": "i"}})
        return [(item["title"], item["url"]) for item in news]
    except ValueError:
        raise ValueError('')


# Requisito 7
def search_by_date(date):
    try:
        datetime.strptime(date, "%Y-%m-%d")
        news = search_news({"timestamp": {"$regex": date}})
        return [(item["title"], item["url"]) for item in news]
    except ValueError:
        raise ValueError('Data inválida')


# Requisito 8
def search_by_source(source):
    try:
        news = search_news({"sources": {"$regex": source, "$options": "i"}})
        return [(item["title"], item["url"]) for item in news]
    except ValueError:
        raise ValueError('')


# Requisito 9
def search_by_category(category):
    try:
        news = search_news(
            {"categories": {"$regex": category, "$options": "i"}}
            )
        return [(item["title"], item["url"]) for item in news]
    except ValueError:
        raise ValueError('')
