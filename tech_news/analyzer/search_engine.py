from tech_news.database import db
from datetime import datetime
import re


# Requisito 6
def search_by_title(title):
    list_notices = []
    title_ignorecase = re.compile(title, re.IGNORECASE)
    for new in db.news.find({"title": {"$regex": title_ignorecase}}):
        list_notices.append((new["title"], new["url"]))
    return list_notices


# Requisito 7
def search_by_date(date):
    try:
        new_date = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Data inválida")
    else:
        list_notices = []
        print(new_date)
        for new in db.news.find({"timestamp": {"$regex": date}}):
            list_notices.append((new["title"], new["url"]))
    return list_notices


# Requisito 8
def search_by_source(source):
    list_notices = []
    source_ignorecase = re.compile(source, re.IGNORECASE)
    for new in db.news.find({"sources": {"$regex": source_ignorecase}}):
        list_notices.append((new["title"], new["url"]))
    return list_notices


# Requisito 9
def search_by_category(category):
    list_notices = []
    category_ignorecase = re.compile(category, re.IGNORECASE)
    for new in db.news.find({"categories": {"$regex": category_ignorecase}}):
        list_notices.append((new["title"], new["url"]))
    return list_notices
