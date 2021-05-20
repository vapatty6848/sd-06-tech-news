from tech_news.database import search_news


# Requisito 6
def search_by_title(title):
    """Função para fazer buscas por título"""
    news_by_title = search_news(
        {"title": {"$regex": title, "$options": "i"}}
    )
    result = [(item["title"], item["url"]) for item in news_by_title]
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
