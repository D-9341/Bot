import discord
from discord.ext import commands
import random

class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('Дополнение Fun успешно загружено.')

    @commands.command()
    async def rp(self, ctx):
        await ctx.message.delete()
        emb = discord.Embed(description = '[Ныа](https://www.youtube.com/watch?v=idmTSW9mfYI)', colour = discord.Color.orange())
        await ctx.send(embed = emb)
        
    @commands.command(aliases = ['.rap'])
    async def rap(self, ctx):
        await ctx.message.delete()
        emb = discord.Embed(colour = ctx.author.color)
        emb.set_image(url = 'https://thumbs.gfycat.com/MessyCarefreeHousefly-size_restricted.gif')
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb)
        
    @commands.command()
    async def zatka(self, ctx):
        await ctx.message.delete()
        emb = discord.Embed(title = 'Форма заявки для Набор кадров', colour = ctx.author.color)
        emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
        emb.add_field(name = '(1). ZATKA в STEAM.  ZATKA_KING#8406 в Discord.', value = 'возраст 14+  часовой пояс IL +0.', inline = False)
        emb.add_field(name = '(2). Интересующая управление:', value = 'Discord', inline = False)
        emb.add_field(name = '(3). Опыт администрирования:', value = 'Есть.', inline = False)
        emb.add_field(name = 'творческие:', value = 'Есть.', inline = False)
        emb.add_field(name = 'технические навыки:', value = 'Нет.', inline = False)
        emb.add_field(name = '(4). Сколько часов готовы уделять работе', value = '[ 15+ в неделю ]', inline = False)
        emb.add_field(name = 'в какое время дня свободны', value = '16:00 до 22:00+', inline = False)
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb)

    @commands.command(aliases = ['Cu', 'CU'])
    async def cu(self, ctx):
        await ctx.message.delete()
        await ctx.send('Медь')
    
    @commands.command(aliases = ['c', 'C', 'coin', 'Coin', 'COIN', 'Coinflip', 'COINFLIP'])
    async def coinflip(self, ctx):
        await ctx.message.delete()
        choices = ['Орёл!', 'Решка!']
        rancoin = random.choice(choices)
        await ctx.send(rancoin)
        
def setup(client):
    client.add_cog(Fun(client))
