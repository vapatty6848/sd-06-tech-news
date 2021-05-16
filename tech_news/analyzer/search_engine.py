from tech_news.database import search_news


# Requisito 6
def search_by_title(title):
    """Method to search news by title"""

    title_news = search_news({"title": {"$regex": title, "$options": "i"}})
    if title_news:
        for news in title_news:
            return [(news["title"], news["url"])]
    else:
        return []


# Requisito 7
def search_by_date(date):
    """Seu código deve vir aqui"""


# Requisito 8
def search_by_source(source):
    """Seu código deve vir aqui"""


# Requisito 9
def search_by_category(category):
    """Seu código deve vir aqui"""
