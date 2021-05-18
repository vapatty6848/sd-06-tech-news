from tech_news.database import search_news
from datetime import date
from tech_news.analyzer.helpers import formatNews
import re

caseInsensitive = {"$options": "-i"}


def searchAndFormat(query):
    news = search_news(query)

    formatted = formatNews(news)

    return formatted


# Requisito 6
def search_by_title(title):
    query = {"title": {"$regex": title, **caseInsensitive}}

    news = searchAndFormat(query)

    return news


# Requisito 7
def search_by_date(wanted_date):
    try:
        acceptedFormat = r"^\d{4}(-\d{2}){2}"
        correctFormat = re.match(acceptedFormat, wanted_date)

        if not (correctFormat):
            raise ValueError("X")

        date_parts = list(map(int, wanted_date.split('-')))
        date(*date_parts)

    except ValueError:
        raise ValueError("Data inválida")

    query = {"timestamp": {"$regex": wanted_date}}

    news = searchAndFormat(query)

    return news


# Requisito 8
def search_by_source(source):
    query = {"sources": {"$regex": source, **caseInsensitive}}

    news = searchAndFormat(query)

    return news


# Requisito 9
def search_by_category(category):
    query = {"categories": {"$regex": category, **caseInsensitive}}

    news = searchAndFormat(query)

    return news
