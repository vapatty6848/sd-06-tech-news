from tech_news.database import search_news


# Requisito 6
def search_by_title(title):
    search_title_news = search_news(
        {"title": {"$regex": title, "$options": "i"}}
    )
    result = [(new["title"], new["url"]) for new in search_title_news]
    return result


# Requisito 7
def search_by_date(date):
    """Seu código deve vir aqui"""


# Requisito 8
def search_by_source(source):
    """Seu código deve vir aqui"""


# Requisito 9
def search_by_category(category):
    """Seu código deve vir aqui"""
