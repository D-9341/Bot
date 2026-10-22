import argparse
import psycopg2
import atexit
import threading

from typing import Generator, Callable, overload
from psycopg2 import sql
from psycopg2.pool import ThreadedConnectionPool
from contextlib import closing
from main import PASSWORD

_pools = {}
_translate_cache: dict[tuple[str, str], str | None] = {}
_translate_lock = threading.Lock()

def _get_pool(db: str = 'locales') -> ThreadedConnectionPool:
    """
    Returns or creates a per-database connection pool
    """
    pool = _pools.get(db)
    if not pool:
        pool = ThreadedConnectionPool(2, 20, host = "localhost", database = db, user = "postgres", password = PASSWORD, port = 5432)
        _pools[db] = pool
    return pool

@atexit.register
def close_pools() -> None:
    """
    Safely closes all connection pools at program exit
    """
    for pool in _pools.values():
        pool.closeall()
    _pools.clear()

def clear_translate_cache() -> None:
    """
    Clears the translation cache
    """
    with _translate_lock:
        _translate_cache.clear()

class PooledConnection:
    __slots__ = ('_pool', '_conn')
    def __init__(self, pool: ThreadedConnectionPool, conn) -> None:
        self._pool = pool
        self._conn = conn

    def close(self) -> None:
        if self._conn is not None:
            self._pool.putconn(self._conn)
            self._conn = None

    def __getattr__(self, name):
        return getattr(self._conn, name)

def connect_db(db: str = 'locales') -> psycopg2.extensions.connection:
    """
    Borrows a connection to a PostgreSQL database from a per-database pool

    Parameters
    ----------
    db: str, optional
        The name of the database to connect to, defaults to 'locales'

    Returns
    -------
    PooledConnection
        A proxy over a pooled connection
    """
    pool = _get_pool(db)
    return PooledConnection(pool, pool.getconn())

def translate(locale: str, string_id: str, /, **format_kwargs) -> str:
    """
    Translates a string_id in a given locale, using format_kwargs if provided

    Parameters
    ----------
    locale: str
        The locale to translate in
    string_id: str
        The string_id to translate
    **format_kwargs
        Keyword arguments to pass to the translated string's format method

    Returns
    -------
    str
        The translated string
    """
    key = (locale, string_id)
    with _translate_lock:
        cached = _translate_cache.get(key, False)
    if cached is False:
        with closing(connect_db()) as conn, conn.cursor() as cur:
            cur.execute(sql.SQL("SELECT value FROM {} WHERE string_id = %s").format(sql.Identifier(locale)), (string_id,))
            result = cur.fetchone()
        value = result[0] if result else None
        with _translate_lock:
            _translate_cache[key] = value
    else:
        value = cached

    if '_help' in string_id:
        if value is not None:
            return value
        command_name = string_id[:-5]
        return translate(locale, 'command_not_found', command = command_name)
    if value is not None:
        return value.format(**format_kwargs) if format_kwargs else value
    return f"Строка `{string_id}` не найдена"

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
    with closing(connect_db()) as conn, conn.cursor() as cur:
        cur.execute("SELECT locale FROM users WHERE user_id = %s", (user_id,))
        result = cur.fetchone()
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
    with closing(connect_db()) as conn, conn.cursor() as cur:
        cur.execute("INSERT INTO users (user_id, locale) VALUES (%s, %s) ON CONFLICT (user_id) DO UPDATE SET locale = %s", (user_id, locale, locale))
        conn.commit()

def countdown(text: str, counter: int, plural_func: Callable[[int, list[str]], str], plurality_list: list) -> Generator[str, None, None]:
    """
    Generates a countdown sequence with proper plural forms

    Parameters
    ----------
    text:
        The text template containing placeholders for number and plural form
    counter:
        The starting number for countdown
    plural_func:
        The function that returns plural form for a given number
    plurality_list:
        The list of word forms for pluralization

    Yields
    ------
    str
        Formatted strings with number and its plural form

    Examples
    --------
    >>> plural_func = lambda n, words: words[0] if n == 1 else words[1]
    >>> list(countdown("{} {}", 3, plural_func, ["яблоко", "яблок"]))
    ['3 яблок', '2 яблок', '1 яблоко']
    
    >>> list(countdown("{} {}", 2, get_plural_form, ["победа", "победы", "побед"]))
    ['2 победы', '1 победа']
    """
    for string in range(counter, 0, -1):
        plural_form = plural_func(string, plurality_list)
        yield text.format(string, plural_form)

@overload
def get_plural_form(number: int, words: list[str], /) -> str: ...
@overload
def get_plural_form(number: int, words: tuple[str, str, str], /) -> str: ...
@overload
def get_plural_form(number: int, *words: str) -> str: ...

def get_plural_form(number: int, *args) -> str:
    """
    Returns the plural form of a number for a russian language

    Parameters
    ----------
    number:
        The number to check
    words:
        The words as a list, tuple, or separate arguments

    Examples
    --------
    >>> get_plural_form(5, ["яблоко", "яблока", "яблок"])
    'яблок'
    >>> get_plural_form(1, ("день", "дня", "дней"))
    'день'
    >>> get_plural_form(3, "час", "часа", "часов")
    'часа'
    """
    if len(args) == 1 and isinstance(args[0], (list, tuple)):
        words = args[0]
    else:
        words = args
    if len(words) != 3:
        raise ValueError("Expected exactly 3 word forms")

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
    - --before and --after flags are supported to specify a date range for processing messages.
    - Additional flags include options for silent mode, exact string matching, substring containment, and content types like embeds, attachments, and stickers.
    """

    import shlex
    flags_list = shlex.split(flags_list)
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--everyone', action = 'store_true', help = 'Include all members')
    parser.add_argument('-u', '--users', action = 'store_true', help = 'Include user members')
    parser.add_argument('-b', '--bots', action = 'store_true', help = 'Include bot members')
    parser.add_argument('-s', '--silent', action = 'store_true', help = 'Silent mode for results')
    parser.add_argument('-x', '--exact', type = str, default = False, help = 'Exact string')
    parser.add_argument('-c', '--contains', type = str, default = False, help = 'Contains substring')
    parser.add_argument('-E', '--embeds', action = 'store_true', help = 'Has embeds')
    parser.add_argument('-A', '--attachments', action = 'store_true', help = 'Has attachments')
    parser.add_argument('-S', '--stickers', action = 'store_true', help = 'Has stickers')
    # parser.add_argument('--before', action = 'store', help = 'Before timestamp')
    # parser.add_argument('--after', action = 'store', help = 'After timestamp')
    flags, _ = parser.parse_known_args(flags_list)
    if flags.users and flags.bots:
        flags.everyone = True
    if not any([flags.bots, flags.users, flags.everyone]):
        flags.everyone = True
    return flags
