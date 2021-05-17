from tech_news.database import search_news
import re


# Requisito 6
def search_by_title(title):
    """A função deve buscar as notícias do banco de dados por título"""

    #  para atender o case insensitive
    #  re.IGNORECASE permite a correspondência sem distinção entre
    #  maiúsculas e minúsculas da Expressão Regular com a string fornecida
    #  https://www.geeksforgeeks.org/name-validation-using-ignorecase-in-python-regex/
    #  https://www.tutorialspoint.com/How-to-write-a-case-insensitive-Python-regular-expression-without-re-compile
    #  avaliar outra alternativa era transformar .lower()
    query = {"title": {"$regex": re.compile(title, re.IGNORECASE)}}
    search_in_db = search_news(query)
    news_founded = [(news["title"], news["url"]) for news in search_in_db]
    return news_founded


# Requisito 7
def search_by_date(date):
    """Seu código deve vir aqui"""


# Requisito 8
def search_by_source(source):
    """Seu código deve vir aqui"""


# Requisito 9
def search_by_category(category):
    """Seu código deve vir aqui"""
