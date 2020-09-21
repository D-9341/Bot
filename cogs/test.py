import discord
from discord.ext import commands

class Test(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def unspecified(self, ctx):
        await ctx.send('чё')

def setup(client):
    client.add_cog(Test(client))
