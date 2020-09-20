import discord
from discord.ext import commands

class test(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def pong(self, ctx):
        await ctx.send('Ping!')

def setup(client):
    client.add_cog(test(client))
