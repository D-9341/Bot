import discord
from discord.ext import commands

class Misc(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def rp(self, ctx):
        await ctx.message.delete()
        emb = discord.Embed(description = '[Ныа](https://www.youtube.com/watch?v=idmTSW9mfYI)', colour = discord.Color.orange())
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
        
def setup(client):
    client.add_cog(Misc(client))
