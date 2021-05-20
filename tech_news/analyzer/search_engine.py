#!/usr/bin/env python3
from tech_news.database import search_news


# Requisito 6
def search_by_title(title):
    """Seu código deve vir aqui"""
    search_result = search_news({"title": {"$regex": title, "$options": "i"}})
    result = [(item['title'], item['url']) for item in search_result]

    return result


# Requisito 7
def search_by_date(date):
    """Seu código deve vir aqui"""


# Requisito 8
def search_by_source(source):
    """Seu código deve vir aqui"""
    q_result = search_news({"sources": {"$regex": source, "$options": "i"}})
    result = [(item['title'], item['url']) for item in q_result]

    return result


# Requisito 9
def search_by_category(category):
    """Seu código deve vir aqui"""
    q_res = search_news({"categories": {"$regex": category, "$options": "i"}})
    print(q_res)
    result = [(item['title'], item['url']) for item in q_res]

    return result
