import argparse
import psycopg2
from psycopg2 import sql
from main import PASSWORD

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
        password = PASSWORD,
        port = 5432
    )
    cur = conn.cursor()
    cur.execute(sql.SQL("SELECT value FROM {} WHERE string_id = %s").format(sql.Identifier(locale)), (string_id,))
    result = cur.fetchone()
    conn.close()
    if '_help' in string_id:
        return result[0] if result else f'{translate(locale, 'command_not_found')}'.format(command = string_id[:-5])
    return result[0] if result else "Локаль не найдена"

def get_locale(user_id: int) -> str:
    """
    Gets the locale for an author

    Parameters
    ----------
    user_id: int
        The ID of the author to get the locale for

    Returns
    -------
    str
        The locale of the author
    """
    conn = psycopg2.connect(
        host = "localhost",
        database = "locales",
        user = "postgres",
        password = PASSWORD,
        port = 5432
    )
    cur = conn.cursor()
    cur.execute("SELECT locale FROM users WHERE user_id = %s", (user_id,))
    result = cur.fetchone()
    conn.close()
    return result[0] if result else "ru"

def set_locale(user_id: int, locale: str) -> None:
    """
    Sets the locale for an author

    Parameters
    ----------
    user_id: int
        The ID of the author to set the locale for
    locale: str
        The locale to set for the author
    """
    conn = psycopg2.connect(
        host = "localhost",
        database = "locales",
        user = "postgres",
        password = PASSWORD,
        port = 5432
    )
    cur = conn.cursor()
    cur.execute("INSERT INTO users (user_id, locale) VALUES (%s, %s) ON CONFLICT (user_id) DO UPDATE SET locale = %s", (user_id, locale, locale))
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

def parse_flags(flags_list: str) -> argparse.Namespace:
    """
    Parses a string of command-line-like flags into an argparse.Namespace object.

    Parameters
    ----------
    flags_list: str
        A string containing command-line-like flags that specify options for processing.

    Returns
    -------
    argparse.Namespace
        A Namespace object where each flag is an attribute with corresponding values.

    Notes
    -----
    - The function supports flags for including all members, users, or bot members.
    - If `--users` and `--bots` are both present, the `--everyone` flag is automatically set to True.
    - If neither `--users`, `--bots`, nor `--everyone` is explicitly set, `--everyone` defaults to True.
    - Additional flags include options for silent mode, exact string matching, substring containment, and content types like embeds, attachments, and stickers.
    """

    import shlex
    flags_list = shlex.split(flags_list)
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--everyone', type = bool, action = 'store_true', help = 'Include all members')
    parser.add_argument('-u', '--users', type = bool, action = 'store_true', help = 'Include user members')
    parser.add_argument('-b', '--bots', type = bool, action = 'store_true', help = 'Include bot members')
    parser.add_argument('-s', '--silent', type = bool, action = 'store_true', help = 'Silent mode for results')
    parser.add_argument('-x', '--exact', type = str, default = False, help = 'Exact string')
    parser.add_argument('-c', '--contains', type = str, default = False, help = 'Contains substring')
    parser.add_argument('-E', '--embeds', type = bool, action = 'store_true', help = 'Has embeds')
    parser.add_argument('-A', '--attachments', type = bool, action = 'store_true', help = 'Has attachments')
    parser.add_argument('-S', '--stickers', type = bool, action = 'store_true', help = 'Has stickers')
    flags, _ = parser.parse_known_args(flags_list)
    if flags.users and flags.bots:
        flags.everyone = True
    if not any([flags.bots, flags.users, flags.everyone]):
        flags.everyone = True
    return flags
