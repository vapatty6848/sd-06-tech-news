from tech_news.database import search_news
import datetime


# Requisito 6
def search_by_title(title):
    """Função para fazer buscas por título"""
    news = search_news(
        {"title": {"$regex": title, "$options": "i"}}
    )
    result = [(new["title"], new["url"]) for new in news]
    return result


# Requisito 7
def search_by_date(date):
    """Função para fazer buscas por data"""
    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")
        news = search_news({"timestamp": {"$regex": date}})
        result = [(new["title"], new["url"]) for new in news]
    except ValueError:
        raise ValueError("Data inválida")

    return result


# Requisito 8
def search_by_source(source):
    """Seu código deve vir aqui"""
    news = search_news({"sources": {
        "$regex": source,
        "$options": "i"
    }})
    result = [(new["title"], new["url"]) for new in news]

    return result


# Requisito 9
def search_by_category(category):
    """Seu código deve vir aqui"""
