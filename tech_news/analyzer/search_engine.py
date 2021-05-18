from tech_news.database import search_news
import re
import datetime


# Requisito 6
def search_by_title(title):
    query = {
        "title": {
            "$regex": re.compile(title, re.IGNORECASE)
        }
    }
    response = search_news(query)
    return [(item["title"], item["url"]) for item in response]


# Requisito 7
def search_by_date(date):
    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Data inválida")
    query = {
        "timestamp": {
            "$regex": date
        }
    }
    response = search_news(query)
    return [(item["title"], item["url"]) for item in response]


# Requisito 8
def search_by_source(source):
    query = {
        "sources": {
            "$regex": re.compile(source, re.IGNORECASE)
        }
    }
    response = search_news(query)
    return [(item["title"], item["url"]) for item in response]


# Requisito 9
def search_by_category(category):
    query = {
        "categories": {
            "$regex": re.compile(category, re.IGNORECASE)
        }
    }
    response = search_news(query)
    return [(item["title"], item["url"]) for item in response]
