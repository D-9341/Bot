import discord
from discord.ext import commands

class Cephalon(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Дополнение Cephalon успешно загружено.')

    @commands.command(aliases = ['Info', 'INFO'])
    @commands.cooldown(1, 5, commands.BucketType.default)
    async def info(self, ctx):
        await ctx.message.delete()
        emb = discord.Embed(title = 'Welcome to the cum zone', colour = discord.Color.orange())
        emb.set_author(name = self.client.user.name, url = 'https://warframe.fandom.com/wiki/Cephalon_Cy', icon_url = self.client.user.avatar_url)
        emb.add_field(name = 'Версия', value = '0.12.7.9018')
        emb.add_field(name = 'Написан на', value = 'discord.py')
        emb.add_field(name = 'Разработчик', value = 'Написано в футере, ха!')
        emb.add_field(name = 'Веб-сайт', value = '```http://ru-unioncraft.ru/```')
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb)
    
    @commands.command(aliases = ['invite', 'invcy'])
    @commands.cooldown(1, 5, commands.BucketType.default)
    async def invite_cy(self, ctx):
        await ctx.message.delete()
        emb = discord.Embed(description = '[Ссылка](https://discordapp.com/oauth2/authorize?&client_id=694170281270312991&scope=bot&permissions=8) для приглашения Cy на сервера', colour = discord.Color.orange(), timestamp = ctx.message.created_at)
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb)
    
    @commands.command(aliases = ['Ping', 'PING'])
    @commands.cooldown(1, 5, commands.BucketType.default)
    async def ping(self, ctx):
        await ctx.message.delete()
        emb = discord.Embed(description = f'Pong! `{round(self.client.latency * 1000)} ms`', colour = discord.Color.orange(), timestamp = ctx.message.created_at)
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb)
    
    @commands.command(aliases = ['Join', 'JOIN'])
    async def join(self, ctx):
        await ctx.message.delete()
        if ctx.author.voice and ctx.author.voice.channel:
            channel = ctx.author.voice.channel
        else:
            emb = discord.Embed(description = 'Ты должен быть в канале, чтобы использовать это.', colour = discord.Color.orange())
            emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
            await ctx.send(embed = emb)
            return
        vc = await channel.connect()

    @commands.command(aliases = ['Leave', 'LEAVE'])
    async def leave(self, ctx):
        await ctx.message.delete()
        channel = ctx.author.voice.channel
        if channel.is_connected():
            await channel.disconnect()
        
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.message.delete()
            emb = discord.Embed(description = f'{ctx.author.mention}, команда в кд, потерпи чутка!', colour = discord.Color.orange())
            emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
            await ctx.send(embed = emb)

def setup(client):
    client.add_cog(Cephalon(client))
