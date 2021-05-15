from tech_news.database import search_news


# Requisito 6
def search_by_title(title):
    """
    Fará buscas de notícias no banco de dados através do título informado.
    """
    query = {"title": title.lower()}
    result = search_news(query)
    return [] if len(result) == 0 else [(result.title, result.url)]


# Requisito 7
def search_by_date(date):
    """Seu código deve vir aqui"""


# Requisito 8
def search_by_source(source):
    """Seu código deve vir aqui"""


# Requisito 9
def search_by_category(category):
    """Seu código deve vir aqui"""
