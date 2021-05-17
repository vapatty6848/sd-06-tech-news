from tech_news.database import search_news
from datetime import datetime


def validate_date(date_text):
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Data inválida")


def format_news(news):
    return [(new["title"], new["url"]) for new in news]


# Requisito 6
def search_by_title(title):
    search_query = {"title": {"$regex": title, "$options": "i"}}
    found_news = search_news(search_query)
    formatted_news = format_news(found_news)
    return formatted_news


# Requisito 7
def search_by_date(date):
    validate_date(date)
    search_query = {"timestamp": {"$regex": f"^{date}", "$options": "m"}}
    found_news = search_news(search_query)
    formatted_news = format_news(found_news)
    return formatted_news


# Requisito 8
def search_by_source(source):
    search_query = {"sources": {"$regex": source, "$options": "i"}}
    found_news = search_news(search_query)
    formatted_news = format_news(found_news)
    return formatted_news


# Requisito 9
def search_by_category(category):
    search_query = {"categories": {"$regex": category, "$options": "i"}}
    found_news = search_news(search_query)
    formatted_news = format_news(found_news)
    return formatted_news
