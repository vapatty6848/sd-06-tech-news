from tech_news.database import search_news


# Requisito 6
def search_by_title(title):
    get_news_by_title = search_news(
        {"title": {"$regex": title, "$options": "-i"}}
    )
    news = [(new["title"], new["url"]) for new in get_news_by_title]
    return news


# Requisito 7
def search_by_date(date):
    """Seu código deve vir aqui"""


# Requisito 8
def search_by_source(source):
    """Seu código deve vir aqui"""


# Requisito 9
def search_by_category(category):
    """Seu código deve vir aqui"""


if __name__ == "__main__":
    by_title = search_by_title("Musk")
    # by_date = search_by_date("")
    # by_source = search_by_source("")
    # by_category = search_by_category("")
    print(by_title)
