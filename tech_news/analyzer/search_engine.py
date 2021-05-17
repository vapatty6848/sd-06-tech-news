from tech_news.database import search_news


# Requisito 6
def search_by_title(title):
    requested_news = []
    query_result = search_news({"title": {"$regex": title, "$options": "i"}})
    for result in query_result:
        news_info = [(result["title"], result["url"])]
        requested_news.append(news_info)
    return requested_news


# Requisito 7
def search_by_date(date):
    """Seu código deve vir aqui"""


# Requisito 8
def search_by_source(source):
    """Seu código deve vir aqui"""


# Requisito 9
def search_by_category(category):
    """Seu código deve vir aqui"""
