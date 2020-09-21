import discord
from discord.ext import commands

class Test(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def rp1(self, ctx):
        await ctx.message.delete()
        emb = discord.Embed(description = '[Ныа](https://www.youtube.com/watch?v=idmTSW9mfYI)', colour = discord.Color.orange())
        await ctx.send(embed = emb)

def setup(client):
    client.add_cog(Test(client))
