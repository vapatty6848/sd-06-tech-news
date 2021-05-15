from tech_news.database import get_collection
from tech_news.analyzer.search_engine import format_results, search_news
from operator import itemgetter


# Requisito 10 usando MongoDB
# def top_5_news():
#     """Lista as cinco notícias mais populares;
#     o critério é a soma dos compartilhamentos e comentários"""
#     news_collection = get_collection()
#     db_result = list(news_collection.aggregate([
#         {
#             '$project': {
#                 'title': 1,
#                 'url': 1,
#                 'pop_rating': {
#                     '$sum': ['$shares_count', '$comments_count']
#                 }
#             }
#         },
#         {'$sort': {'pop_rating': -1}},
#         {'$limit': 5}
#     ]))
#     result = format_results(db_result)
#     return result


# Requisito 10 usando Python
def top_5_news():
    """Lista as cinco notícias mais populares;
        o critério é a soma dos compartilhamentos e comentários"""
    news_raw = search_news({})
    news_list = [
        {
            'title': result['title'],
            'url': result['url'],
            'pop_rating': result['shares_count'] + result['comments_count']
        }
        for result in news_raw
    ]
    sort_news = sorted(
        news_list,
        key=itemgetter('pop_rating'),
        reverse=True)
    get_top_5 = sort_news[:5]
    top_5_news = format_results(get_top_5)
    return top_5_news


# Requisito 11 usando Python
# def top_5_categories():
#     """Lista as cinco categorias mais populares;
#         o critério é a soma dos compartilhamentos e comentários"""
#     news_raw = search_news({})

#     categories_count = {}
#     for news in news_raw:
#         for category in news['categories']:
#             categories_count.setdefault(category, 0)
#             categories_count[category] += 1

#     categories_sort = sorted(categories_count)
#     top_5_categories = categories_sort[:5]
#     return top_5_categories


# Requisito 11 usando MongoDB
def top_5_categories():
    """Lista as cinco categorias mais populares;
        o critério é a soma dos compartilhamentos e comentários"""
    news_collection = get_collection()
    db_result = list(news_collection.aggregate([
        {'$unwind': '$categories'},
        {
            '$group': {
                '_id': '$categories',
                'count': {'$sum': 1}
            }
        },
        {'$sort': {'count': -1, '_id': 1}},
        {'$limit': 5}
    ]))
    top_5_categories = [category['_id'] for category in db_result]
    return top_5_categories
