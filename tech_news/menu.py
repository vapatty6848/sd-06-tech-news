import sys
from tech_news.scraper import get_tech_news
from tech_news.analyzer.search_engine import (
    search_by_title,
    search_by_date,
    search_by_source,
    search_by_category,
)
from tech_news.analyzer.ratings import top_5_news, top_5_categories


def execute(user_input):
    options = [
        "Digite quantas notícias serão buscadas:",
        "Digite o título:",
        "Digite a data no formato aaaa-mm-dd:",
        "Digite a fonte:",
        "Digite a categoria:",
    ]

    menu = {
        0: get_tech_news,
        1: search_by_title,
        2: search_by_date,
        3: search_by_source,
        4: search_by_category,
        5: top_5_news,
        6: top_5_categories,
    }

    try:
        if user_input < len(options):
            chosen = input(options[user_input])

            if chosen != 0:
                print(menu[user_input](chosen))
            else:
                menu[user_input](chosen)

        else:
            print(menu[user_input]())

    except Exception:
        return sys.stderr.write("Opção inválida\n")


def analyzer_menu():
    try:
        user_input = int(
            input(
                "Selecione uma das opções a seguir:\n "
                "0 - Popular o banco com notícias;\n "
                "1 - Buscar notícias por título;\n "
                "2 - Buscar notícias por data;\n "
                "3 - Buscar notícias por fonte;\n "
                "4 - Buscar notícias por categoria;\n "
                "5 - Listar top 5 notícias;\n "
                "6 - Listar top 5 categorias;\n "
                "7 - Sair."
            )
        )
    except ValueError:
        return sys.stderr.write("Opção inválida")

    if user_input is None or user_input == 7:
        return print("Encerrando script")
    else:
        execute(user_input)
