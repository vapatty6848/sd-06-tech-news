from tech_news.database import find_news
from functools import reduce


def search_top_news():
    news = find_news()
    return reduce(
        lambda a, b: a + [[b["title"], b["url"]]],
        sorted(
            news,
            key=lambda x: x["shares_count"] + x["comments_count"],
            reverse=True,
        ),
        [],
    )


def search_top_categories():
    news = find_news()
    return reduce(
        lambda a, b: a + b["categories"],
        sorted(
            news,
            key=lambda x: x["categories"].count(x["categories"][0]),
            reverse=True,
        ),
        [],
    )


def top_5_news():
    top_5 = search_top_news()
    result = [tuple(n) for n in top_5 if len(top_5) != 0]
    return [] if not result else result[:5]


def top_5_categories():
    result = search_top_categories()
    result.sort()
    return [] if not result else result[:5]
