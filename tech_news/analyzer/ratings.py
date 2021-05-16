from tech_news.database import find_news


# Requisito 10
def top_5_news():
    """Method to get top 5 news"""

    news_list = find_news()
    popularity_list = []
    for news in news_list:
        popularity = news['comments_count'] + news['shares_count']
        obj = {
            'title': news['title'],
            'url': news['url'],
            'popularity': popularity
        }
        popularity_list.append(obj)

    def sorted_data(e):
        return e['popularity']

    popularity_list.sort(key=sorted_data, reverse=True)
    result = [
        (item["title"], item["url"]) for item in popularity_list
    ]
    top_five = result[:5]
    return top_five


# Requisito 11
def top_5_categories():
    """Method to get top 5 categories"""

    news_list = find_news()
    categories_list = set()

    for news in news_list:
        for category in news['categories']:
            categories_list.add(category)
    top_five = sorted(categories_list)[:5]
    return top_five
