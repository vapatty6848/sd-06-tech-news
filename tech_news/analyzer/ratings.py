from pymongo import MongoClient
from decouple import config


DB_HOST = config("DB_HOST", default="localhost")
DB_PORT = config("DB_PORT", default="27017")

client = MongoClient(host=DB_HOST, port=int(DB_PORT))
db = client.tech_news


# Requisito 10
def top_5_news():
    top_5_news = []
    query_result = db.news.aggregate(
        [
            {
                "$project": {
                    "_id": False,
                    "title": True,
                    "url": True,
                    "popularity": {
                        "$add": ["$shares_count", "$comments_count"]
                    },
                }
            },
            {"$sort": {"popularity": -1, "title": 1}},
            {"$limit": 5},
        ]
    )
    for result in query_result:
        news_info = (result["title"], result["url"])
        top_5_news.append(news_info)
    return top_5_news


# Requisito 11
def top_5_categories():
    """Seu código deve vir aqui"""
