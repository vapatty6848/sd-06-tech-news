import sys
from tech_news import scraper
from tech_news.analyzer import search_engine
from tech_news.analyzer import ratings


def execute(user_input):
    options = [
        "Digite quantas notícias serão buscadas:",
        "Digite o título:",
        "Digite a data no formato aaaa-mm-dd:",
        "Digite a fonte:",
        "Digite a categoria:",
    ]

    menu = {
        0: scraper.get_tech_news,
        1: search_engine.search_by_title,
        2: search_engine.search_by_date,
        3: search_engine.search_by_source,
        4: search_engine.search_by_category,
        5: ratings.top_5_news,
        6: ratings.top_5_categories,
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

    except Exception as e:
        sys.stderr.write(str(e))
        sys.exit()


def analyzer_menu():
    try:
        user_input = int(
            input(
                "Selecione uma das opções a seguir:\n"
                "0 - Popular o banco com notícias;\n"
                "1 - Buscar notícias por título;\n"
                "2 - Buscar notícias por data;\n"
                "3 - Buscar notícias por fonte;\n"
                "4 - Buscar notícias por categoria;\n"
                "5 - Listar top 5 notícias;\n"
                "6 - Listar top 5 categorias;\n"
                "7 - Sair.\n"
            )
        )
    except ValueError:
        sys.stderr.write("Opção inválida")
        sys.exit()

    if user_input == 7:
        sys.stderr.write("Encerrando script")
        sys.exit()

    else:
        execute(user_input)
