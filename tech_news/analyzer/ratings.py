from tech_news.database import find_news


# Requisito 10
def top_5_news():
    news = find_news()
    top_five_most_popular = sorted([
        [
            int(
                act_news["shares_count"]
            )
            +
            int(
                act_news["comments_count"]
            ),
            act_news["title"],
            act_news["url"],
        ]
        for act_news in news
    ], reverse=True)
    return [(news[1], news[2]) for news in top_five_most_popular[:5]]


# Requisito 11
def top_5_categories():
    news = find_news()
    categories = set()
    for act_news in news:
        for category in act_news["categories"]:
            categories.add(category)
    return sorted(categories)[:5]
