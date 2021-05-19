import sys
from datetime import datetime
from tech_news.scraper import get_tech_news
from tech_news.analyzer.search_engine import (
    search_by_title,
    search_by_date,
    search_by_source,
    search_by_category,
)
from tech_news.analyzer.ratings import top_5_news, top_5_categories


# Requisito 12
def populate_news_list():
    try:
        amount = int(input("Digite quantas notícias serão buscadas:"))
    except (ValueError, TypeError):
        print("A quantidade deve ser um número.")
        amount = int(input())
    else:
        get_tech_news(amount)
        print("Busca Finalizada")


def search_news_by_title():
    try:
        requested_title = input("Digite o título:")
    except Exception:
        print("Houve um erro. Tente novamente.")
        requested_title = input("Digite o título:")
    else:
        results = search_by_title(requested_title)
        print(results)
        print("Busca finalizada")


def search_news_by_date():
    date_pattern = "%Y-%m-%d"
    try:
        requested_date = input("Digite a data no formato aaaa-mm-dd:")
        datetime.strptime(requested_date, date_pattern)
    except (ValueError, TypeError):
        print("A data está incorreta.")
        requested_date = input("Digite a data no formato aaaa-mm-dd:")
    else:
        results = search_by_date(requested_date)
        print(results)
        print("Busca finalizada")


def search_news_by_source():
    try:
        requested_source = input("Digite a fonte:")
    except Exception:
        print("Houve um erro. Tente novamente.")
        requested_source = input("Digite o fonte:")
    else:
        results = search_by_source(requested_source)
        print(results)
        print("Busca finalizada")


def search_news_by_category():
    try:
        requested_category = input("Digite a categoria:")
    except Exception:
        print("Houve um erro. Tente novamente.")
        requested_category = input("Digite a categoria:")
    else:
        results = search_by_category(requested_category)
        print(results)
        print("Busca finalizada")


def search_top_5_news():
    results = top_5_news()
    print(results)


def search_top_5_categories():
    results = top_5_categories()
    print(results)


def quit():
    print("Encerrando script\n")


def default():
    sys.stderr.write("Opção inválida\n")


options = {
    0: populate_news_list,
    1: search_news_by_title,
    2: search_news_by_date,
    3: search_news_by_source,
    4: search_news_by_category,
    5: search_top_5_news,
    6: search_top_5_categories,
    7: quit,
}


def select_option(option):
    return options.get(option, default)()


def analyzer_menu():
    print("Selecione uma das opções a seguir:")
    print(" 0 - Popular o banco com notícias;")
    print(" 1 - Buscar notícias por título;")
    print(" 2 - Buscar notícias por data;")
    print(" 3 - Buscar notícias por fonte;")
    print(" 4 - Buscar notícias por categoria;")
    print(" 5 - Listar top 5 notícias;")
    print(" 6 - Listar top 5 categorias;")
    print(" 7 - Sair.")

    try:
        option = input()
        select_option(int(option))
    except ValueError:
        default()
