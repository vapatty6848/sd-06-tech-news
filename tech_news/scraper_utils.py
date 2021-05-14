from bs4 import BeautifulSoup


def get_writer(selector):
    writer_raw = selector.css(
        'main article .tec--author__info__link::text').get()

    if writer_raw is None:
        return writer_raw

    writer = writer_raw.strip()
    return writer


def get_shares_count(selector):
    shares_count = 0
    shares = selector.css('nav.tec--toolbar *::text').get()
    if shares is not None:
        shares_count = shares.split()
        if len(shares_count) > 1:
            shares_quant = shares_count[0].strip()
            return int(shares_quant)
    return 0


def get_comments_count(selector):
    comments_count = 0
    comments = selector.css(
        'nav.tec--toolbar button *::text').getall()
    if len(comments) == 0:
        return comments_count
    comments_count = comments[1].split()[0]
    return int(comments_count)


def get_url(selector):
    return selector.xpath('//meta[@property="og:url"]/@content').get()


def get_timestamp(selector):
    return selector.css('main article time::attr(datetime)').get()


def get_summary(selector):
    summary_raw = selector.css('.tec--article__body p').get()
    if summary_raw is not None:
        return BeautifulSoup(summary_raw, 'lxml').text
    return None


def get_sources(selector):
    sourcesList = []
    sources = selector.css(
        '.tec--badge:not(.tec--badge--primary)::text'
        ).getall()
    for source in sources:
        sourcesList.append(source.strip())
    return sourcesList


def get_categories(selector):
    categoriesList = []
    categories = selector.css('.tec--badge--primary::text').getall()
    for cat in categories:
        categoriesList.append(cat.strip())
    return categoriesList
