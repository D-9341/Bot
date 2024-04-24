import json

class memoize:
    """
    A `decorator` object that memoizes the results of recursive functions for multiple times faster execution, consuming more memory
    """
    def __init__(self, f):
        self.f = f
        self.memo = {}
    def __call__(self, *args):
        if not args in self.memo:
            self.memo[args] = self.f(*args)
        return self.memo[args]

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

def set_locale(author_id: str, locale: str) -> None:
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
