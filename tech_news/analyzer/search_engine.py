import re
import datetime
from tech_news.database import search_news


# Requisito 6
def search_by_title(title):
    query = {"title": {"$regex": re.compile(title, re.IGNORECASE)}}
    result = search_news(query)
    news_found = [(news["title"], news["url"]) for news in result]
    return news_found


# Requisito 7
def search_by_date(date):
    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Data inválida")
    query = {"timestamp": {"$regex": date}}
    result = search_news(query)
    news_found = [(news["title"], news["url"]) for news in result]
    return news_found


# Requisito 8
def search_by_source(source):
    query = {"sources": {"$regex": re.compile(source, re.IGNORECASE)}}
    result = search_news(query)
    news_found = [(news["title"], news["url"]) for news in result]
    return news_found


# Requisito 9
def search_by_category(category):
    query = {"categories": {"$regex": re.compile(category, re.IGNORECASE)}}
    result = search_news(query)
    news_found = [(news["title"], news["url"]) for news in result]
    return news_found
