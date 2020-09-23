import discord
from discord.ext import get

class Misc(commands.Cog):
    def __init__(client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('Дополнение Misc успешно загружено.')
        
def setup(client):
    client.add_cog(Misc(client))
