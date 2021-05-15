import re
import datetime
from tech_news.database import search_news


# Requisito 6
def search_by_title(title):
    """
    Fará buscas de notícias no banco de dados através do título informado.
    """
    query = {"title": {"$regex": re.compile(title, re.IGNORECASE)}}
    result = search_news(query)
    news_found = [(news["title"], news["url"]) for news in result]
    return news_found


# Requisito 7
def search_by_date(date):
    """Busca as notícias do banco de dados por data."""
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
    """Busca as notícias do banco de dados por fonte."""
    query = {"sources": {"$regex": re.compile(source, re.IGNORECASE)}}
    result = search_news(query)
    news_found = [(news["title"], news["url"]) for news in result]
    return news_found


# Requisito 9
def search_by_category(category):
    """Busca as notícias do banco de dados por categoria."""
    query = {"categories": {"$regex": re.compile(category, re.IGNORECASE)}}
    result = search_news(query)
    news_found = [(news["title"], news["url"]) for news in result]
    return news_found
