from tech_news.database import search_news
from datetime import datetime


# Requisito 6
def search_by_title(title):
    get_news = search_news({"title": {"$regex": title, "$options": "-i"}})
    news = [(new["title"], new["url"]) for new in get_news]
    return news


# Requisito 7
def search_by_date(date):
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Data inválida")
    get_news = search_news({"timestamp": {"$regex": date}})
    news = [(new["title"], new["url"]) for new in get_news]
    return news


# Requisito 8
def search_by_source(source):
    get_news = search_news({"sources": {"$regex": source, "$options": "-i"}})
    news = [(new["title"], new["url"]) for new in get_news]
    return news


# Requisito 9
def search_by_category(category):
    get_news = search_news(
        {"categories": {"$regex": category, "$options": "-i"}}
    )
    news = [(new["title"], new["url"]) for new in get_news]
    return news


if __name__ == "__main__":
    by_title = search_by_title("Musk")
    # by_date = search_by_date("")
    # by_source = search_by_source("")
    # by_category = search_by_category("")
    print(by_title)
