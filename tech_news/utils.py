def get_writer(selector):
    writer = selector.css('main article .tec--author__info__link::text').get()
    if writer is not None:
        writer.strip()
    return writer


def get_something(selector):
    writer = selector.css('main article .tec--author__info__link::text').get()
    if writer is not None:
        writer.strip()
    return writer
