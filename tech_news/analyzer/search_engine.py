import datetime
from tech_news.database import search_news


def format_date(date):
    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Data inválida")


# Requisito 6
def search_by_title(title):
    search_title_news = search_news(
        {"title": {"$regex": title, "$options": "i"}}
    )
    result_by_title = [(new["title"], new["url"]) for new in search_title_news]
    return result_by_title


# Requisito 7
def search_by_date(date):
    format_date(date)
    search_date_news = search_news({"timestamp": {"$regex": date}})
    result_by_date = [
        (item["title"], item["url"]) for item in search_date_news]
    return result_by_date


# Requisito 8
def search_by_source(source):
    search_source_news = search_news(
        {"sources": {"$regex": source, "$options": "i"}})
    result_by_source = [
        (item["title"], item["url"]) for item in search_source_news]
    return result_by_source


# Requisito 9
def search_by_category(category):
    search_category_news = search_news(
        {"categories": {"$regex": category, "$options": "i"}})
    result_by_category = [
        (item["title"], item["url"]) for item in search_category_news]
    return result_by_category
