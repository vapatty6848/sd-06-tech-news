from tech_news.database import find_news


# Requisito 10
def top_5_news():
    """Lista as cinco notícias mais populares."""
    news_list = find_news()
    popularity_list = [
        [
            int(news["shares_count"]) + int(news["comments_count"]),
            news["title"],
            news["url"],
        ]
        for news in news_list
    ]
    ordered_list = sorted(popularity_list, reverse=True)
    result = [
        (ordere_news[1], ordere_news[2]) for ordere_news in ordered_list[:5]
    ]
    return result


# Requisito 11
def top_5_categories():
    """Seu código deve vir aqui"""
