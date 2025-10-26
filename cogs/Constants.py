from discord.ext import commands

class Constants(commands.Cog):
    def __init__(self, client):
        self.client: commands.Bot = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Константы загружены')

class colors:
    DEFAULT = 0x2F3136
    ERROR = 0xFF0000
    SUCCESS = 0x00FF00
    BLACK = 0x000001
    WHITE = 0xFFFFFF
    JDH = 0xFF8000
    LO = 0x0080FF

class LocalesManager:
    PATHS = {
        'ru': './locales/ru.json',
        'en': './locales/en.json', 
        'gnida': './locales/gnida.json',
        'gnida_lite': './locales/gnida_lite.json'
    }

    @classmethod
    def get_path(cls, locale: str) -> str:
        """Вернуть путь к локали, при отсутствии возвращает ru"""
        return cls.PATHS.get(locale, cls.PATHS['ru'])

    @classmethod
    def get_all_locales(cls) -> list[str]:
        """Вернуть список всех доступных локалей"""
        return list(cls.PATHS.keys())

class botversions:
    botversions = [764882153812787250, 694170281270312991, 762015251264569352]

async def setup(client):
    await client.add_cog(Constants(client))
