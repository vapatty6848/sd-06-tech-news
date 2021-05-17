import sys
from tech_news.analyzer.search_engine import (
    search_by_title,
    search_by_date,
    search_by_source,
    search_by_category,
)
from tech_news.scraper import get_tech_news
from tech_news.analyzer.ratings import top_5_news, top_5_categories


def end_script():
    sys.exit("Encerrando script")


OPTIONS = [
    {"value": "0 - Popular o banco com notícias;"},
    {"value": "1 - Buscar notícias por título;"},
    {"value": "2 - Buscar noticias por data;"},
    {"value": "3 - Buscar notícias por fonte;"},
    {"value": "4 - Buscar notícias por categoria;"},
    {"value": "5 - Listar top 5 notícias;"},
    {"value": "6 - Listar top 5 categorias;"},
    {"value": "7 - Sair."},
]

INPUTS = [
    {"user_input": "Digite quantas notícias serão buscadas: "},
    {"user_input": "Digite o título: "},
    {"user_input": "Digite a data no formato aaaa-mm-dd: "},
    {"user_input": "Digite a fonte: "},
    {"user_input": "Digite a categoria: "},
]

ACTIONS = [
    {"action": get_tech_news},
    {"action": search_by_title},
    {"action": search_by_date},
    {"action": search_by_source},
    {"action": search_by_category},
    {"action": top_5_news},
    {"action": top_5_categories},
    {"action": end_script},
]


def menu_options():
    user_options = "".join([f"\n {option['value']}" for option in OPTIONS])
    user_input = input(f"Selecione uma das opções a seguir:{user_options}\n")
    return int(user_input)


def check_parameter(input, choice):
    if choice == 0:
        return int(input)
    return input


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
        user_action = INPUTS[user_choice]["user_input"]
        parameter = input(user_action)
        function_parameter = check_parameter(parameter, user_choice)
        output = ACTIONS[user_choice]["action"](function_parameter)
        return print(output)
    else:
        output = ACTIONS[user_choice]["action"]()
        print(output)


if __name__ == "__main__":
    analyzer_menu()
