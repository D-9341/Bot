import argparse
import psycopg2
import os
from pathlib import Path
from dotenv import load_dotenv
from typing import Literal

load_dotenv(f'{Path(__file__).parents[0]}\\vars.env')

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
    conn = psycopg2.connect(
        host = "localhost",
        database = "locales",
        user = "postgres",
        password = os.getenv('DB_PASS'),
        port = 5432
    )
    cur = conn.cursor()
    if locale == 'ru':
        cur.execute("SELECT value FROM ru WHERE string_id = %s", (string_id))
    elif locale == 'en':
        cur.execute("SELECT value FROM en WHERE string_id = %s", (string_id))
    elif locale == 'gnida':
        cur.execute("SELECT value FROM gnida WHERE string_id = %s", (string_id))
    result = cur.fetchone()
    conn.close()
    if '_help' in string_id:
        return result[0] if result else f'{translate(locale, 'command_not_found')}'.format(command = string_id[:-5])
    return result[0] if result else "Локаль не найдена"

def get_locale(user_id: int) -> Literal['ru', 'en', 'gnida']:
    """
    Gets the locale for an author

    Parameters
    ----------
    user_id: int
        The ID of the author to get the locale for

    Returns
    -------
    Literal['ru', 'en', 'gnida']
        The locale of the author
    """
    conn = psycopg2.connect(
        host = "localhost",
        database = "locales",
        user = "postgres",
        password = os.getenv('DB_PASS'),
        port = 5432
    )
    cur = conn.cursor()
    cur.execute("SELECT locale FROM users WHERE user_id = %s", (user_id))
    result = cur.fetchone()
    conn.close()
    return result[0] if result else "ru"

def set_locale(user_id: int, locale: Literal['ru', 'en', 'gnida']) -> None:
    """
    Sets the locale for an author

    Parameters
    ----------
    user_id: int
        The ID of the author to set the locale for
    locale: Literal['ru', 'en', 'gnida']
        The locale to set for the author
    """
    conn = psycopg2.connect(
        host = "localhost",
        database = "locales",
        user = "postgres",
        password = os.getenv('DB_PASS'),
        port = 5432
    )
    cur = conn.cursor()
    cur.execute("INSERT INTO users (user_id, locale) VALUES (%s, %s) ON CONFLICT (user_id) DO NOTHING", (user_id, locale))
    conn.commit()
    conn.close()

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
    args, _ = parser.parse_known_args(args_list)
    if args.users and args.bots:
        args.everyone = True
    return args
