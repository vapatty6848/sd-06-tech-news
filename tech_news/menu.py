import sys
from tech_news.scraper import get_tech_news
from tech_news.analyzer.search_engine import (
    search_by_title,
    search_by_category,
    search_by_date,
    search_by_source,
    )
from tech_news.analyzer.ratings import top_5_news, top_5_categories


def validate_option(input):
    try:
        option = int(input)
    except Exception:
        return print("Opção inválida", file=sys.stderr)

    if 0 < option > 7:
        print("Opção inválida", file=sys.stderr)

    return option


# Requisito 12
def analyzer_menu():
    """Menu do programa"""

    # menu_options = """
    #     Selecione uma das opções a seguir:
    #      0 - Popular banco;
    #      1 - Buscar notícias por título;
    #      2 - Buscar notícias por data;
    #      3 - Buscar notícias por fonte;
    #      4 - Buscar notícias por categoria;
    #      5 - Listar top 5 notícias;
    #      6 - Listar top 5 categorias;
    #      7 - Sair.
    #     """

    menu_options = "Selecione uma das opções a seguir:\n"\
        " 0 - Popular banco;\n"\
        " 1 - Buscar notícias por título;\n"\
        " 2 - Buscar notícias por data;\n"\
        " 3 - Buscar notícias por fonte;\n"\
        " 4 - Buscar notícias por categoria;\n"\
        " 5 - Listar top 5 notícias;\n"\
        " 6 - Listar top 5 categorias;\n"\
        " 7 - Sair."\

    menu_input = input(menu_options)
    option = validate_option(menu_input)
    run_menu_option(option)


def run_menu_option(option):
    if option == 0:
        news_quantity = input('Digite quantas notícias serão buscadas:')
        return get_tech_news(news_quantity)
    elif option == 1:
        title = input('Digite o título:')
        query = search_by_title(title)
        print(query)
        return query
    elif option == 2:
        date = input('Digite a data no formato aaaa-mm-dd:')
        return search_by_date(date)
    elif option == 3:
        source = input('Digite a fonte:')
        return search_by_source(source)
    elif option == 4:
        category = input('Digite a categoria:')
        return search_by_category(category)
    elif option == 5:
        return top_5_news()
    elif option == 6:
        return top_5_categories()
    elif option == 7:
        return print('Encerrando script')
