from tech_news.scraper import get_tech_news
from tech_news.analyzer.search_engine import (
    search_by_title,
    search_by_date,
    search_by_category,
    search_by_source,
)
from tech_news.analyzer.ratings import top_5_categories, top_5_news
import sys

menu_options = [
    "Selecione uma das opções a seguir:",
    " 0 - Popular o banco com notícias;",
    " 1 - Buscar notícias por título;",
    " 2 - Buscar notícias por data;",
    " 3 - Buscar notícias por fonte;",
    " 4 - Buscar notícias por categoria;",
    " 5 - Listar top 5 notícias;",
    " 6 - Listar top 5 categorias;",
    " 7 - Sair.",
]

LINE_BREAK = "\n"

search_functions = {
    "title": search_by_title,
    "date": search_by_date,
    "category": search_by_category,
    "source": search_by_source,
}

top_functions = {"news": top_5_news, "category": top_5_categories}


def populate_database():
    number_of_news = int(input("Digite quantas notícias serão buscadas:"))
    get_tech_news(number_of_news)


# def get_trigger_by_searches(options):
#     def trigger_search():
#         value = input(options["command"])
#         search_function = search_functions[options["property"]]
#         matched_news = search_function(value)
#         print(matched_news)

#     return trigger_search

# WARNING: THERE IS REPETITIVE CODE BELOW
# THIS IS DUE TO POORLY IMPLEMENTED TESTS NOT CATCHING VALID FUNCTION CALLS


def search_title():
    title = input("Digite o título:")
    matched_news = search_by_title(title)
    print(matched_news)


def search_date():
    date = input("Digite a data no formato aaaa-mm-dd:")
    matched_news = search_by_date(date)
    print(matched_news)


def search_source():
    source = input("Digite a fonte:")
    matched_news = search_by_source(source)
    print(matched_news)


def search_category():
    category = input("Digite a categoria:")
    matched_news = search_by_category(category)
    print(matched_news)


# def get_top_triggers(top_wanted):
#     def top_printer():
#         top_func = top_functions[top_wanted]
#         news = top_func()
#         print(news)

#     return top_printer
def top_news():
    news = top_5_news()
    print(news)


def top_categories():
    news = top_5_categories()
    print(news)


def end_script():
    print("Encerrando script")


options_mapping = {
    "0": populate_database,
    # "1": get_trigger_by_searches(
    #     {"command": "Digite o título:", "property": "title"}
    # ),
    "1": search_title,
    "2": search_date,
    "3": search_source,
    "4": search_category,
    # "2": get_trigger_by_searches(
    #     {
    #         "command": 'Digite a data no formato aaaa-mm-dd:',
    #         "property": "date",
    #     }
    # ),
    # "3": get_trigger_by_searches(
    #     {"command": "Digite a fonte:", "property": "source"}
    # ),
    # "4": get_trigger_by_searches(
    #     {"command": "Digite a categoria:", "property": "category"}
    # ),
    # "5": get_top_triggers("news"),
    # "6": get_top_triggers("category"),
    "5": top_news,
    "6": top_categories,
    "7": end_script,
}


def invalid_option():
    print("Opção inválida", file=sys.stderr)


def print_menu_options():
    formatted = LINE_BREAK.join(menu_options)

    print(formatted)


# Requisito 12
def analyzer_menu():
    print_menu_options()

    option = input()

    if not (option in options_mapping):
        return invalid_option()

    wanted_function = options_mapping[option]

    wanted_function()


# analyzer_menu()
