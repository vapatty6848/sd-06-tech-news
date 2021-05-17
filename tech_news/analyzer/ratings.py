#!/usr/bin/env python3
from tech_news.database import find_news
import collections


# Requisito 10
def top_5_news():
    """Seu código deve vir aqui"""
    # montando a estrutura para fazer uma lista com todas as news
    all_news = find_news()
    news_top_popularity = []
    for news in all_news:
        popularity = news['comments_count'] + news['shares_count']
        new = {
            'title': news['title'],
            'url': news['url'],
            'popularity': popularity
        }
        news_top_popularity.append(new)
    # montar uma estrutura para selecionar as 5 com maior pop


# Requisito 11
def top_5_categories():
    """Seu código deve vir aqui"""
    all_news = find_news()
    all_categories = []
    for news in all_news:
        for category in news["categories"]:
            all_categories.append(category)
    # preciso agora selecionar as catego mais repetidas da list all_categories
    category_top_five = collections.Counter(all_categories).most_common()
    # ordem alfabetica
    dt_cat_top_fv_with_sorted = sorted(category_top_five)
    # um map, que retorna uma lista. um elemento para cada vez que o for rodar.
    data_category_top_five = [varia[0] for varia in dt_cat_top_fv_with_sorted]
    # array[start:stop:pulando]
    list_result = data_category_top_five[:5]
    return list_result

# # como usar Count e most_comon
# array2 = collections.Counter(['a', 'b', 'c', 'a', 'b', 'b']).most_common(2)
# # sorted usado para ordem alfabetica
# array = sorted(array2)
# array_filter = [status[0] for status in array]
# print(array_filter)
