import json
from typing import Literal

def translate(locale: str, id: str) -> str:
    """
    Translates the string from a JSON file by `locale` and `id`

    Parameters
    -----------
    locale:
        The locale to pass into function
    id:
        The id of the string to be retrieved
    """
    with open(f'locales/{locale}/locale.json', 'r', encoding = 'utf-8') as file:
        data = json.load(file)
    return data.get(id, "Локаль не найдена")

def get_locale(author_id: str) -> str:
    """
    Gets the locale from `author_id` provided by discord.py's `author.id`

    Parameters
    -----------
    author_id:
        The `id` that locale should be searched for
    """
    with open('locales/users.json', 'r') as file:
        data = json.load(file)
    return data[str(author_id)]

def set_locale(author_id: str, locale: Literal['ru', 'en', 'gnida']) -> None:
    """
    Sets `author` locale to new `locale`

    Parameters
    -----------
    author_id:
        The `id` that locale should be searched for
    locale:
        The new locale to be set
    """
    with open('locales/users.json', 'r') as file:
        data = json.load(file)
    data[str(author_id)] = locale
    with open('locales/users.json', 'w') as file:
        json.dump(data, file, indent = 4)
    
def get_plural_form(number: int, words: list[str]) -> str:
    """
    Returns the plural form of a number for a russian language

    Parameters
    ----------
    number:
        The number to check
    words:
        The list of words

    Examples
    --------
    >>> get_plural_form(5, ["яблоко", "яблока", "яблок"])
    'яблок'
    >>> get_plural_form(2, ["победа", "победы", "побед"])
    'победы'
    """
    if number % 10 == 1 and number % 100 != 11: return words[0]
    elif number % 10 >= 2 and number % 10 <= 4 and (number % 100 < 10 or number % 100 >= 20): return words[1]
    else: return words[2]

def get_command_help(locale: str, command: str) -> str:
    """
    Returns the help message for the command
    """
    with open(f'locales/{locale}/help.json', 'r', encoding = 'utf-8') as file:
        data = json.load(file)
    return data.get(command, f'{translate(locale, 'command_not_found')}'.format(command = command))
