from tech_news.database import search_news
from datetime import datetime


# case_sensitive: https://stackoverflow.com/questions/1863399/
# mongodb-is-it-possible-to-make-a-case-insensitive-query
def search_by_title(title):
    find_title = search_news({"title": {"$regex": title, "$options": "i"}})

    if find_title:
        for new in find_title:
            return [(new["title"], new["url"])]
    else:
        return []


# https://www.alura.com.br/artigos/lidando-com-datas-e-horarios-no-python?gclid=Cj
# 0KCQjw4v2EBhCtARIsACan3nzjntrLxL6jVuHqOfd64JvwIuFFyEDyOKru0w9qXk01mPtH0vUCDs0aAk
# d9EALw_wcB
# Requisito 7
def search_by_date(date):
    try:
        datetime.strptime(date, "%Y-%m-%d")
        # find_date = search_news({"$contains": {"timestamp": date}})
        find_date = search_news({"timestamp": {"$regex": date}})

        if find_date:
            for new in find_date:
                return [(new["title"], new["url"])]
        else:
            return []
    except ValueError:
        raise ValueError("Data inválida")


# Requisito 8
def search_by_source(source):
    find_source = search_news({"sources": {"$regex": source, "$options": "i"}})

    if find_source:
        for new in find_source:
            return [(new["title"], new["url"])]
    else:
        return []


# Requisito 9
def search_by_category(category):
    find_category = search_news(
        {"categories": {"$regex": category, "$options": "i"}}
    )

    if find_category:
        for new in find_category:
            return [(new["title"], new["url"])]
    else:
        return []
