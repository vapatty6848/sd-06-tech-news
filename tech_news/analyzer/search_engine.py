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
    q_result = search_news({"source": {"$regex": source, "$options": "i"}})
    result = [(item['title'], item['source']) for item in q_result]

    return result


# Requisito 9
def search_by_category(category):
    """Seu código deve vir aqui"""
    q_result = search_news({"category": {"$regex": category, "$options": "i"}})
    result = [(item['title'], item['category']) for item in q_result]

    return result


search_by_source("Venture Beat")