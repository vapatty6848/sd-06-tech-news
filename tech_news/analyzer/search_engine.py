#!/usr/bin/env python3
from tech_news.database import search_news


# Requisito 6
def search_by_title(title):
    """Seu código deve vir aqui"""
    post_by_title = search_news({"title": {"$regex": title, "$options": "i"}})
    # map para tirar e formatar o titulo e url do array
    post_result = [(post["title"], post["url"]) for post in post_by_title]
    return post_result


# Requisito 7
def search_by_date(date):
    """Seu código deve vir aqui"""
    # falta arranjar uma forma de converter o formato recebido p/ timestamp
    post_by_date = search_news({"source": {"$regex": date}})
    return post_by_date


# Requisito 8
def search_by_source(source):
    """Seu código deve vir aqui"""
    post_by_source = search_news({"source": {"$regex": source}})
    return post_by_source


# Requisito 9
def search_by_category(category):
    """Seu código deve vir aqui"""
    post_by_cat = search_news({"categories": {"$regex": category}})
    return post_by_cat

