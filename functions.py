import json
import argparse
from typing import Literal

def translate(locale: str, string_id: str) -> str:
    """
    Translates a string_id to a locale string from the locale file

    Parameters
    ----------
    locale: str
        The locale to translate to
    string_id: str
        The ID of the string to translate

    Returns
    -------
    str
        The translated string
    """
    with open(f'locales/{locale}/locale.json', 'r', encoding = 'utf-8') as file:
        user_data = json.load(file)
    return user_data.get(string_id, "Локаль не найдена")

def get_locale(author_id: str) -> Literal['ru', 'en', 'gnida']:
    """
    Gets the locale for an author

    Parameters
    ----------
    author_id: str
        The ID of the author to get the locale for

    Returns
    -------
    Literal['ru', 'en', 'gnida']
        The locale of the author
    """
    with open('locales/users.json', 'r', encoding = 'utf-8') as file:
        user_data = json.load(file)
    return user_data[str(author_id)]

def set_locale(author_id: str, locale: Literal['ru', 'en', 'gnida']) -> None:
    """
    Sets the locale for an author

    Parameters
    ----------
    author_id: str
        The ID of the author to set the locale for
    locale: Literal['ru', 'en', 'gnida']
        The locale to set for the author
    """
    with open('locales/users.json', 'r', encoding = 'utf-8') as file:
        user_data = json.load(file)
    user_data[str(author_id)] = locale
    with open('locales/users.json', 'w', encoding = 'utf-8') as file:
        json.dump(user_data, file, indent = 4)

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
    if number % 10 >= 2 and number % 10 <= 4 and (number % 100 < 10 or number % 100 >= 20): return words[1]
    return words[2]

def get_command_help(locale: str, command: str) -> str:
    """
    Returns the help message for the command
    """
    with open(f'locales/{locale}/help.json', 'r', encoding = 'utf-8') as file:
        command_data = json.load(file)
    return command_data.get(command, f'{translate(locale, 'command_not_found')}'.format(command = command))

def parse_members(args_list: list[str] | str) -> argparse.Namespace:
    """
    Parses a list of arguments or a string of arguments into a Namespace object.

    Parameters
    ----------
    args_list: list[str] | str
        A list of arguments or a string containing the arguments.

    Returns
    -------
    argparse.Namespace
        A Namespace object with parsed arguments as attributes.

    Notes
    -----
    - If both `--users` and `--bots` are specified, `--everyone` will be set to True.
    """
    if isinstance(args_list, str):
        args_list = args_list.split()
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--everyone', action = 'store_true', help = 'Include all members')
    parser.add_argument('-u', '--users', action = 'store_true', help = 'Include user members')
    parser.add_argument('-b', '--bots', action = 'store_true', help = 'Include bot members')
    parser.add_argument('-s', '--silent', action = 'store_true', help = 'Silent mode for results')
    args = parser.parse_args(args_list)
    if args.users and args.bots:
        args.everyone = True
    return args
