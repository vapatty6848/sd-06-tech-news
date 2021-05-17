from collections import Counter
from tech_news.database import find_news


# Requisito 10
def top_5_news():
    news_list = find_news()
    news_with_popularity = []
    for news in news_list:
        popularity = news['comments_count'] + news['shares_count']
        obj = {
            'title': news['title'],
            'url': news['url'],
            'popularity': popularity
        }
        news_with_popularity.append(obj)

    def sorted_data(e):
        return e['popularity']

    news_with_popularity.sort(key=sorted_data, reverse=True)
    news_formated_in_tuples = [
        (item["title"], item["url"]) for item in news_with_popularity
    ]
    top_five = news_formated_in_tuples[0:5]
    return top_five


# Requisito 11
def top_5_categories():
    news_list = find_news()
    categories = []
    for news in news_list:
        for category in news["categories"]:
            categories.append(category)
    most_common_categories = Counter(categories).most_common()
    top_five_sorted = sorted(most_common_categories)
    top_five = [category[0] for category in top_five_sorted]
    return top_five[:5]
