from operator import itemgetter

from tech_news.database import find_news
from tech_news.analyzer.helpers import formatNews


MAX_NEWS_TO_RETURN = 5
LIST_START = 0


def flat_categories_list(categoires_by_news):
    flatten = [item for sublist in categoires_by_news for item in sublist]

    return flatten


def extract_categories(single_news):
    return single_news["categories"]


def get_frequencies(categories):
    frequencies = {}

    for category in categories:
        frequencies[category] = (
            frequencies[category] + 1 if category in frequencies else 1
        )

    return frequencies


def get_categories_frequency(news):
    all_categories = list(map(extract_categories, news))

    categories_list = flat_categories_list(all_categories)

    frequencies = get_frequencies(categories_list)

    return frequencies


def sort_by_frequency(categories_with_frequency):
    copy = [*categories_with_frequency]

    # if items are a tuple, python sorts the array based on its value,
    # from left to right
    copy.sort()

    return copy


def extract_categories_names(category_with_frequency):
    (category, _) = category_with_frequency

    return category


def get_categories_ordered_by_frequency(frequencies):
    list_with_frequency = frequencies.items()

    sorted_by_frequency = sort_by_frequency(list_with_frequency)

    categories = list(map(extract_categories_names, sorted_by_frequency))

    return categories


def calc_popularity(single_news):
    props_to_calc = ["shares_count", "comments_count"]

    shares, comments = itemgetter(*props_to_calc)(single_news)

    popularity = shares + comments

    return popularity


def add_popularity(single_news):
    popularity = calc_popularity(single_news)

    updated_news = {
        **single_news,
        "popularity": popularity,
    }

    return updated_news


def add_popularity_to_all_news(news):
    with_popularity = list(map(add_popularity, news))

    return with_popularity


def get_all_news_with_popularity():
    all_news = find_news()

    with_popularity = add_popularity_to_all_news(all_news)

    return with_popularity


def extract_popularity(single_news):
    return single_news["popularity"]


def sort_news_by_popularity(news):
    news_copy = [*news]

    news_copy.sort(key=extract_popularity, reverse=True)

    return news_copy


def extract_top_five(items):
    return items[LIST_START:MAX_NEWS_TO_RETURN]


# Requisito 10
def top_5_news():
    news = get_all_news_with_popularity()

    sorted_by_popularity = sort_news_by_popularity(news)

    top_news = extract_top_five(sorted_by_popularity)

    formatted = formatNews(top_news)

    return formatted


# Requisito 11
def top_5_categories():
    news = find_news()

    category_frequencies = get_categories_frequency(news)

    categories = get_categories_ordered_by_frequency(category_frequencies)

    top_categories = extract_top_five(categories)

    return top_categories
