from tech_news.database import db

# from pymongo import MongoClient


# Requisito 6
def search_by_title(title):
    # client = MongoClient("mongodb://localhost:27017/")
    # db = client.library
    list_notices = []
    for new in db.books.find({"title": {"$regex": title}}):
        list_notices.append([(new["title"], new["_id"])])
    return list_notices


# Requisito 7
def search_by_date(date):
    """Seu código deve vir aqui"""


# Requisito 8
def search_by_source(source):
    """Seu código deve vir aqui"""


# Requisito 9
def search_by_category(category):
    """Seu código deve vir aqui"""
