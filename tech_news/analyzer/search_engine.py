from tech_news.database import search_news
import re
import datetime


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
    """Esta função irá buscar as notícias do banco de dados por data"""
    # https://stackoverflow.com/questions/55961092/how-to-use-striptime-y-m-d-hms-minus-1-minute
    # https://python.hotexamples.com/pt/examples/mx/DateTime/strptime/python-datetime-strptime-method-examples.html
    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")

    except ValueError:
        raise ValueError("Data inválida")

    query = {"timestamp": {"$regex": date}}
    search_in_db = search_news(query)
    news_founded = [(news["title"], news["url"]) for news in search_in_db]
    return news_founded


# Os 2 próximos requisitos são aprecidos com o req 6
# Requisito 8
def search_by_source(source):
    """função irá buscar as notícias por fonte"""
    query = {"sources": {"$regex": re.compile(source, re.IGNORECASE)}}
    search_in_db = search_news(query)
    news_founded = [(news["title"], news["url"]) for news in search_in_db]
    return news_founded


# Requisito 9
def search_by_category(category):
    """função irá buscar as notícias por categoria"""
    query = {"categories": {"$regex": re.compile(category, re.IGNORECASE)}}
    search_in_db = search_news(query)
    news_founded = [(news["title"], news["url"]) for news in search_in_db]
    return news_founded
