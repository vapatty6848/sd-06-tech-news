from tech_news.database import search_news


# case_sensitive: https://stackoverflow.com/questions/1863399/
# mongodb-is-it-possible-to-make-a-case-insensitive-query
def search_by_title(title):
    find_title = search_news({"title": {"$regex": title, "$options": "i"}})

    if find_title:
        for new in find_title:
            return [(new["title"], new["url"])]
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
