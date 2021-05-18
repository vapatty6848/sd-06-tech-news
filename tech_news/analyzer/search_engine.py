from tech_news.database import search_news
from datetime import datetime


# Requisito 6
def search_by_title(title):
    searched_news = search_news({"title": {"$regex": title, "$options": "i"}})

    return [(new["title"], new["url"]) for new in searched_news]


# Requisito 7
def search_by_date(date):
    try:
        datetime.strptime(date, "%Y-%m-%d")
        searched_news = search_news({"timestamp": {"$regex": date}})

        return [(new["title"], new["url"]) for new in searched_news]
    except ValueError:
        raise ValueError("Data inválida")


# Requisito 8
def search_by_source(source):
    searched_news = search_news(
        {"sources": {"$regex": source, "$options": "i"}}
    )

    return [(new["title"], new["url"]) for new in searched_news]


# Requisito 9
def search_by_category(category):
    searched_news = search_news(
        {"categories": {"$regex": category, "$options": "i"}
    })

    return [(new["title"], new["url"]) for new in searched_news]
