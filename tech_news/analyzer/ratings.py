from tech_news.analyzer.utils import format_news
from tech_news.analyzer.db_pipelines import top_news_pipe, top_categories_pipe
from tech_news.database import db


# Requisito 10
def top_5_news():
    top_news = db.news.aggregate(top_news_pipe)
    formated_news = format_news(top_news)
    return formated_news


# Requisito 11
def top_5_categories():
    top_categories = db.news.aggregate(top_categories_pipe)
    return [new["category"] for new in top_categories]
