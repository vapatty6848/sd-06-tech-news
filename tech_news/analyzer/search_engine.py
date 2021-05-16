from functools import reduce
from datetime import datetime
from tech_news.database import find_news


def search_news_param(to_search, obj_key):
    def handle_search(param):
        return (
            [n.casefold() for n in param]
            if type(param) == list
            else param.casefold()
        )

    news = find_news()
    return [
        reduce(
            lambda a, b: a + (b["title"], b["url"]),
            filter(
                lambda x: to_search.casefold() in handle_search(x[obj_key]),
                news,
            ),
            (),
        )
    ]


def search_by_title(title):
    result = search_news_param(title, "title")
    return [] if len(result[0]) == 0 else result


def search_by_date(date):
    try:
        datetime.strptime(date, "%Y-%m-%d")
        result = search_news_param(date, "timestamp")
        return [] if len(result[0]) == 0 else result
    except ValueError:
        raise ValueError("Data inválida")


def search_by_source(source):
    result = search_news_param(source, "sources")
    return [] if len(result[0]) == 0 else result


def search_by_category(category):
    result = search_news_param(category, "categories")
    return [] if len(result[0]) == 0 else result
