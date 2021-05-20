from tech_news.database import db


# Requisito 10
def top_5_news():
    list_notices = []
    data_response = db.news.aggregate([
      {
        "$project": {
          "_id": 0,
          "title": 1,
          "url": 1,
          "total": {"$add": ["$shares_count", "$comments_count"]},
        }
      },
      {
        "$sort": {"total": -1, "title": 1}
      },
      {
        "$limit": 5
      }
    ])
    for new in data_response:
        list_notices.append((new["title"], new["url"]))
    return list_notices


# Requisito 11
def top_5_categories():
    list_categories = []
    data_response = db.news.aggregate([
      {
       "$unwind": "$categories"
      },
      {
        "$group": {
          "_id": "$categories",
          "count": {"$sum": 1}
        }
      },
      {
        "$sort": {"count": -1, "_id": 1}
      },
      {
        "$limit": 5
      }
    ])
    for categorie in data_response:
        list_categories.append(categorie["_id"])
    return list_categories
