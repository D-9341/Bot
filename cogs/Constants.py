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

class locales_paths:
    RU = './locales/ru/locale.json'
    GNIDA = './locales/gnida/locale.json'
    EN = './locales/en/locale.json'

async def setup(client):
    await client.add_cog(Constants(client))
