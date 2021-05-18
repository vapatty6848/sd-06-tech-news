from tech_news.database import search_news_aggregation


# Requisito 10
def top_5_news():
    """Seu código deve vir aqui"""
    result_news = search_news_aggregation([
        {
            "$project": {
                "_id": 0,
                "title": 1,
                "url": 1,
                "popularity": {"$add": ["$shares_count", "$comments_count"]}
            }
        },
        {
            "$sort": {"popularity": -1, "title": 1}
        },
        {"$limit": 5}
    ])
    return [(new["title"], new["url"]) for new in result_news]


# Requisito 11
def top_5_categories():
    """Seu código deve vir aqui"""
    result_news = search_news_aggregation([
        {
            "$project": {
                "_id": 0,
                "categories": 1
            }
        },
        {"$unwind": "$categories"},
        {
            "$group": {
                "_id": "$categories",
                "count": {"$sum": 1}
            }
        },
        {
            "$sort": {"count": -1, "_id": 1}
        },
        {"$limit": 5}
    ])
    return [new["_id"] for new in result_news]
