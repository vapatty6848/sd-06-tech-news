import sys
from tech_news.scraper import get_tech_news
from tech_news.analyzer.search_engine import (
    search_by_title,
    search_by_category,
    search_by_date,
    search_by_source,
    )
from tech_news.analyzer.ratings import top_5_news, top_5_categories


def end_script():
    print('Encerrando script')


MENU = {
    0: {
        'menu': '0 - Popular o banco com notícias;\n',
        'input': 'Digite quantas notícias serão buscadas: ',
        'action': get_tech_news,
        },
    1: {
        'menu': '1 - Buscar notícias por título;\n',
        'input': 'Digite o título: ',
        'action': search_by_title,
        },
    2: {
        'menu': '2 - Buscar noticias por data;\n',
        'input': 'Digite a data no formato aaaa-mm-dd: ',
        'action': search_by_date,
        },
    3: {
        'menu': '3 - Buscar notícias por fonte;\n',
        'input': 'Digite a fonte: ',
        'action': search_by_source,
        },
    4: {
        'menu': '4 - Buscar notícias por categoria;\n',
        'input': 'Digite a categoria: ',
        'action': search_by_category,
        },
    5: {
        'menu': '5 - Listar top 5 notícias;\n',
        'action': top_5_news,
        },
    6: {
        'menu': '6 - Listar top 5 categorias;\n',
        'action': top_5_categories,
        },
    7: {
        'menu': '7 - Sair.',
        'action': end_script,
        },
}


def initiate_menu():
    user_menu = ''.join([f' {MENU[key]["menu"]}' for key in MENU])
    user_input = input(
        f'Selecione uma das opções a seguir:\n{user_menu}\n')
    return int(user_input)


def handle_parameter(input, choice):
    return int(input) if choice == 0 else input


def validate_option(choice):
    if choice not in range(8):
        raise ValueError("Opção inválida")


def analyzer_menu():
    try:
        user_choice = initiate_menu()
        validate_option(user_choice)
    except ValueError:
        return print('Opção inválida', file=sys.stderr)
    except KeyboardInterrupt:
        return end_script()

    if user_choice in (0, 1, 2, 3, 4):
        user_action = MENU[user_choice]['input']
        parameter = handle_parameter(input(user_action), user_choice)
        output = MENU[user_choice]["action"](parameter)
        return print(output)
    elif user_choice != 7:
        output = MENU[user_choice]["action"]()
        print(output)
    else:
        end_script()


if __name__ == "__main__":
    analyzer_menu()
