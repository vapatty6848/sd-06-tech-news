import sys
from tech_news.analyzer.search_engine import (
    search_by_title,
    search_by_date,
    search_by_source,
    search_by_category,
)
from tech_news.scraper import get_tech_news
from tech_news.analyzer.ratings import top_5_news, top_5_categories


def end():
    sys.exit("Encerrando script\n")


OPTIONS = [
    "0 - Popular o banco com notícias;",
    "1 - Buscar notícias por título;",
    "2 - Buscar noticias por data;",
    "3 - Buscar notícias por fonte;",
    "4 - Buscar notícias por categoria;",
    "5 - Listar top 5 notícias;",
    "6 - Listar top 5 categorias;",
    "7 - Sair.",
]

INPUTS = [
    "Digite quantas notícias serão buscadas: ",
    "Digite o título: ",
    "Digite a data no formato aaaa-mm-dd: ",
    "Digite a fonte: ",
    "Digite a categoria: ",
]

ACTIONS = [
    get_tech_news,
    search_by_title,
    search_by_date,
    search_by_source,
    search_by_category,
    top_5_news,
    top_5_categories,
    end,
]


def menu_options():
    user_options = "".join([f"\n {option}" for option in OPTIONS])
    user_input = input(f"Selecione uma das opções a seguir:{user_options}")
    return int(user_input)


def check_parameter(input, choice):
    return int(input) if choice == 0 else input


def validate_option(choice):
    if choice not in range(8):
        return print("Opção inválida 1", file=sys.stderr)


def analyzer_menu():
    try:
        user_choice = menu_options()
        validate_option(user_choice)
    except ValueError:
        return print("Opção inválida", file=sys.stderr)

    if user_choice not in (5, 6, 7):
        user_action = INPUTS[user_choice]
        parameter = input(user_action)
        function_parameter = check_parameter(parameter, user_choice)
        output = ACTIONS[user_choice](function_parameter)
        return print(output)
    else:
        output = ACTIONS[user_choice]()
        print(output)


if __name__ == "__main__":
    analyzer_menu()
