from tech_news.database import find_news


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
