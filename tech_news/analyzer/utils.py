def format_news(news):
    return [(new["title"], new["url"]) for new in news]
