top_news_pipe = [
    {
        "$project": {
            "title": 1,
            "url": 1,
            "popularity": {"$sum": ["$shares_count", "$comments_count"]},
            "_id": 0,
        }
    },
    {"$sort": {"popularity": -1, "title": 1}},
    {"$limit": 5},
]

top_categories_pipe = [
    {"$unwind": "$categories"},
    {"$group": {"_id": "$categories", "total": {"$sum": 1}}},
    {"$sort": {"total": -1, "_id": 1}},
    {"$limit": 5},
    {"$project": {"category": "$_id", "total": 1, "_id": 0}},
]
