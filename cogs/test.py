import discord
from discord.ext import commands

class Test(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def purge(self, ctx):
        await ctx.message.delete()
        emb = discord.Embed(description = 'Мне нужно ваше подтверждение для продолжения.')
        emb.set_footer(text = 'Будет отменено через 5 секунд')
        sent = await ctx.send(embed = emb)
        try:
            msg = await self.client.wait_for('message', timeout = 5, check = lambda message: message.author == ctx.author and message.channel == ctx.channel)
            if msg:
                await sent.delete()
                await msg.delete()
                await ctx.channel.purge(limit = 5)
                await ctx.send('Удалено 5 сообщений')

        except asyncio.TimeoutError:
            await sent.delete()
            await ctx.send('Время вышло', delete_after = 3)

def setup(client):
    client.add_cog(Test(client))
