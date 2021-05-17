from tech_news.database import search_news
import re


# Requisito 6
def search_by_title(title):
    query = {
        "title": {
            "$regex": re.compile(title, re.IGNORECASE)
        }
    }
    response = search_news(query)
    return [(item["title"], item["url"]) for item in response]


# Requisito 7
def search_by_date(date):
    """Seu código deve vir aqui"""


# Requisito 8
def search_by_source(source):
    """Seu código deve vir aqui"""


# Requisito 9
def search_by_category(category):
    """Seu código deve vir aqui"""


print(search_by_title("que"))
