from tech_news.database import search_news
import re
from datetime import datetime


# Requisito 6
def search_by_title(title):
    """Seu código deve vir aqui"""
    regxTitle = re.compile(title, re.IGNORECASE)
    result_news = search_news({"title": regxTitle})
    return [(new["title"], new["url"]) for new in result_news]


# Requisito 7
def search_by_date(date):
    """Seu código deve vir aqui"""
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Data inválida")
    regxDate = re.compile(f"^{date}")
    result_news = search_news({"timestamp": regxDate})
    return [(new["title"], new["url"]) for new in result_news]


# Requisito 8
def search_by_source(source):
    """Seu código deve vir aqui"""
    regxSource = re.compile(f"^{source}$", re.IGNORECASE)
    result_news = search_news({"sources": regxSource})
    return [(new["title"], new["url"]) for new in result_news]


# Requisito 9
def search_by_category(category):
    """Seu código deve vir aqui"""
    regxCategory = re.compile(f"^{category}$", re.IGNORECASE)
    result_news = search_news({"categories": regxCategory})
    return [(new["title"], new["url"]) for new in result_news]
