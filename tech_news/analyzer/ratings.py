from collections import Counter
from tech_news.database import find_news

# Requisito 10
def top_5_news():
    """Seu código deve vir aqui"""


# Requisito 11
def top_5_categories():
    all_news = find_news()
    categories_list = [(item['categories']) for item in all_news]
    top_categories = Counter(categories_list)
    sorted_categories = sorted(top_categories)
    sorted_list = [(item[0]) for item in sorted_categories]
    top_five_categories = sorted_list[:5]
    return top_five_categories
