from tech_news.database import find_news


# Requisito 10
def top_5_news():
    """função irá listar as cinco notícias mais populares"""
    # Preciso resolver implementação do critério de popularidade
    # Deve ser parecido com o 11


# Requisito 11
def top_5_categories():
    """função irá listar as 5 categorias com maior ocorrência no BD"""
    categories = set()
    for news in find_news():
        for category in news["categories"]:
            # set() - https://www.geeksforgeeks.org/set-add-python/
            categories.add(category)
    # https://www.w3schools.com/python/ref_func_sorted.asp
    top_5 = sorted(categories)[:5]
    return top_5
