def formatNews(news):
    return list(map(lambda x: (x["title"], x["url"]), news))
