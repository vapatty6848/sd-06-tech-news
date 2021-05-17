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
    {"option": 0, "value": "0 - Popular banco"},
    {"option": 1, "value": "1 - Buscar notícias por título"},
    {"option": 2, "value": "2 - Buscar noticias por data"},
    {"option": 3, "value": "3 - Buscar notícias por fonte"},
    {"option": 4, "value": "4 - Buscar notícias por categoria"},
    {"option": 5, "value": "5 - Listar top 5 notícias"},
    {"option": 6, "value": "6 - Listar top 5 categorias"},
    {"option": 7, "value": "7 - Sair"},
]

INPUTS = [
    {"option": 0, "user_input": "Digite quantas notícias serão buscadas: "},
    {"option": 1, "user_input": "Digite o título: "},
    {"option": 2, "user_input": "Digite a data no formato aaaa-mm-dd: "},
    {"option": 3, "user_input": "Digite a fonte: "},
    {"option": 4, "user_input": "Digite a categoria: "},
]

ACTIONS = [
    {"option": 0, "action": get_tech_news},
    {"option": 1, "action": search_by_title},
    {"option": 2, "action": search_by_date},
    {"option": 3, "action": search_by_source},
    {"option": 4, "action": search_by_category},
    {"option": 5, "action": top_5_news},
    {"option": 6, "action": top_5_categories},
    {"option": 7, "action": end_script},
]


def menu_options():
    user_options = "".join([f"\n{option['value']}" for option in OPTIONS])
    user_input = input(f"Selecione uma das opções a seguir: {user_options}\n")
    return user_input


def check_parameter(input, choice):
    if choice == 0:
        return int(input)
    return input


def analyzer_menu():
    user_choice = int(menu_options())
    try:
        user_action = INPUTS[user_choice]["user_input"]
        if user_choice not in (5, 6):
            parameter = input(user_action)
            function_parameter = check_parameter(parameter, user_choice)
            output = ACTIONS[user_choice]["action"](function_parameter)
            return print(output)
        output = ACTIONS[user_choice]["action"]()
        print(output)
    except Exception:
        if user_choice > 7:
            return print("Opção inválida", file=sys.stderr)


if __name__ == "__main__":
    analyzer_menu()
