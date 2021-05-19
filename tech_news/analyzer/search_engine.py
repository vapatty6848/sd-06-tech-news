from tech_news.database import db
from datetime import datetime

from pymongo import MongoClient


# Requisito 6
def search_by_title(title):
    client = MongoClient("mongodb://localhost:27017/")
    db = client.tech_news
    list_notices = []
    for new in db.news.find({"title": {"$regex": title}}):
        list_notices.append((new["title"], new["url"]))
    print(list_notices)
    return list_notices


# Requisito 7
def search_by_date(date):
    client = MongoClient("mongodb://localhost:27017/")
    db = client.tech_news
    try:
        new_date = datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        return "Data inválida"
    else:
        list_notices = []
        print(new_date)
        for new in db.news.find({"timestamp": {"$regex": date}}):
            list_notices.append((new["title"], new["_id"]))
        print(list_notices)

search_by_date("201-05-19")


# Requisito 8
def search_by_source(source):
    """Seu código deve vir aqui"""


# Requisito 9
def search_by_category(category):
    """Seu código deve vir aqui"""
