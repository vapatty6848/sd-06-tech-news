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
    return print('Encerrando script')


MENU = {
    0: {
        'menu': 'Popular o banco com notícias;',
        'input': 'Digite quantas notícias serão buscadas: ',
        'action': get_tech_news,
        'has_params': True,
        'params_to_int': True,
        },
    1: {
        'menu': 'Buscar notícias por título;',
        'input': 'Digite o título: ',
        'action': search_by_title,
        'has_params': True,
        },
    2: {
        'menu': 'Buscar notícias por data;',
        'input': 'Digite a data no formato aaaa-mm-dd: ',
        'action': search_by_date,
        'has_params': True,
        },
    3: {
        'menu': 'Buscar notícias por fonte;',
        'input': 'Digite a fonte: ',
        'action': search_by_source,
        'has_params': True,
        },
    4: {
        'menu': 'Buscar notícias por categoria;',
        'input': 'Digite a categoria: ',
        'action': search_by_category,
        'has_params': True,
        },
    5: {
        'menu': 'Listar top 5 notícias;',
        'action': top_5_news,
        'has_params': False,
        },
    6: {
        'menu': 'Listar top 5 categorias;',
        'action': top_5_categories,
        'has_params': False,
        },
    7: {
        'menu': 'Sair.',
        'action': end_script,
        'has_params': False,
        },
}


def initiate_menu():
    user_menu = '\n'.join([f' {key} - {MENU[key]["menu"]}' for key in MENU])
    user_input = input(f'Selecione uma das opções a seguir:\n{user_menu}')
    try:
        get_number_input = ''.join(
            char for char in user_input if char.isdigit())
        return int(get_number_input)
    except Exception:
        raise ValueError()


def handle_parameter(input, choice):
    if 'params_to_int' in choice:
        return ''.join(char for char in input if char.isdigit())
    return input


def validate_option(choice):
    if choice not in range(8):
        raise ValueError()


def analyzer_menu():
    try:
        user_choice = initiate_menu()
        validate_option(user_choice)

        if ('has_params' in MENU[user_choice] and
                MENU[user_choice]['has_params']):
            user_action = MENU[user_choice]['input']
            parameter = handle_parameter(input(user_action), MENU[user_choice])
            output = MENU[user_choice]['action'](parameter)
            return print(output)
        else:
            output = MENU[user_choice]['action']()
            print(output)

    except ValueError:
        return sys.stderr.write('Opção inválida\n')
    except (KeyboardInterrupt, Exception):
        return end_script()


if __name__ == '__main__':
    analyzer_menu()
