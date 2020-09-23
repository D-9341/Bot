import discord
from discord.ext import commands

class Misc(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('Дополнение Misc успешно загружено.')
        
def setup(client):
    client.add_cog(Misc(client))
