import json

def translate(locale: str, id: str) -> str:
    """
    Translates the string from a JSON file by `locale` and `id`

    Parameters
    -----------
    locale:
        The locale to parse into function
    id:
        The id of the string you want to retrieve
    """
    with open(f'locales/{locale}/locale.json', 'r', encoding = 'utf-8') as file:
        data = json.load(file)
        return data.get(id, "Локаль не найдена")

def get_locale(author_id: str) -> str:
    """
    Gets the locale by `author_id` provided by discord.py's `author.id`

    Parameters
    -----------
    author_id:
        The `id` that string should be searched by
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
        The `id` that locale should be searched by
    locale:
        The new locale to be set
    """
    with open('locales/users.json', 'r') as file:
        data = json.load(file)
    data[str(author_id)] = locale
    with open('locales/users.json', 'w') as file:
        json.dump(data, file, indent = 4)
