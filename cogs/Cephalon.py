import asyncio
import datetime
import os

import discord
from discord.ext import commands
from pymongo import MongoClient

passw = os.environ.get('passw')
cluster = MongoClient(f"mongodb+srv://cephalon:{passw}@locale.ttokw.mongodb.net/Locale?retryWrites=true&w=majority")
collection = cluster.Locale.locale

friends = [351071668241956865, 417362845303439360]

guilds = [693929822543675455, 735874149578440855, 818758712163827723]

class Cephalon(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Модуль Cephalon загружен')

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def info(self, ctx):
        emb = discord.Embed(colour = discord.Color.orange())
        emb.set_author(name = self.client.user.name, url = 'https://warframe.fandom.com/wiki/Cephalon_Cy', icon_url = self.client.user.avatar_url)
        emb.add_field(name = 'Версия', value = '0.12.10.2.12528')
        emb.add_field(name = 'Написан на', value = 'discord.py v1.7.2 при помощи\ndiscord-py-slash-command v1.1.0')
        emb.add_field(name = 'Разработчик', value = '[сасиска#2472](https://discord.com/users/338714886001524737)')
        if ctx.guild.owner.id != self.client.owner_id and ctx.guild.owner.id not in friends:
            emb.add_field(name = 'Сервер', value = 'Данный сервер не принадлежит моему Создателю или его знакомым. Все эмбед выводы будут иметь футер с текстом `Cephalon Cy by сасиска#2472`')
        if ctx.guild.id == 693929822543675455:
            emb.add_field(name = 'Принадлежность', value = 'Это - мой основной сервер.')
        if ctx.guild.id == 735874149578440855:
            emb.add_field(name = 'Тестирование', value = 'Это - мой тестовый сервер.')
        emb.add_field(name = 'Раздражаю', value = f'{len(self.client.users)} человек')
        emb.add_field(name = 'Существую на', value = f'{len(self.client.guilds)} серверах')
        if ctx.guild.owner.id != self.client.owner_id and ctx.guild.owner.id not in friends:
            emb.set_footer(text = 'Данное приложение не имеет никакого причастия к игре Warframe. Cephalon Cy by сасиска#2472', icon_url = 'https://i.playground.ru/p/yVaOZNSTdgUTxmzy_qvzzQ.png')
        else:
            emb.set_footer(text = 'Данное приложение не имеет никакого причастия к игре Warframe.', icon_url = 'https://i.playground.ru/p/yVaOZNSTdgUTxmzy_qvzzQ.png')
        await ctx.send(embed = emb)
    
    @commands.command(aliases = ['invcy'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def invite(self, ctx, arg = None):
        if arg == None:
            emb = discord.Embed(description = '[Ссылка](https://discord.com/api/oauth2/authorize?client_id=694170281270312991&permissions=8&scope=bot%20applications.commands) для приглашения Cy на сервера.', colour = discord.Color.orange())
            if ctx.guild.owner.id != self.client.owner_id and ctx.guild.owner.id not in friends:
                emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
            await ctx.send(embed = emb)
        if arg == 'beta':
            emb = discord.Embed(description = '[Ссылка](https://discord.com/oauth2/authorize?client_id=764882153812787250&scope=bot&permissions=8&scope=bot%20applications.commands) для приглашения Cy Beta на сервера.', color = discord.Color.orange())
            if ctx.guild.owner.id != self.client.owner_id and ctx.guild.owner.id not in friends:
                emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
            await ctx.send(embed = emb)
        if arg == 'pro':
            if ctx.guild.id not in guilds:
                emb = discord.Embed(description = f'Сервер `{ctx.guild}` не имеет активных подписок. Купить можно по [Ссылке](https://www.patreon.com/cephaloncy) Преимущества: пинг не более 25ms, больший аптайм, защита от несанкционированного добавления на сервера.', colour = discord.Color.orange())
                await ctx.send(embed = emb)
            else:
                emb = discord.Embed(description = '[Ссылка](https://discord.com/oauth2/authorize?client_id=762015251264569352&scope=bot&permissions=8&scope=bot%20applications.commands) для приглашения Cy PRO на сервера.', color = discord.Color.orange())
                await ctx.send(embed = emb)
    
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ping(self, ctx):
        emb = discord.Embed(description = f'`fetching..`', colour = discord.Color.orange())
        emb1 = discord.Embed(description = f'Pong!  `{round(self.client.latency * 1000)} ms`', colour = discord.Color.orange())
        message = await ctx.send(embed = emb)
        if ctx.guild.owner.id != self.client.owner_id and ctx.guild.owner.id not in friends:
            emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
            emb1.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await asyncio.sleep(self.client.latency)
        await message.edit(embed = emb1)
        
    @commands.command()
    async def botver(self, ctx):
        emb = discord.Embed(color = 0x2f3136)
        emb.add_field(name = '0.12.10.2.12528 (Текущая версия, полная перепись кода)', value = 'Отдельные куски кода были рассортированы по разным файлам.', inline = False)
        emb.add_field(name = '0.12.10.2.11856 (Предыдущая версия, нормальное обновление)', value = 'Добавлена команда locale для изменения локали. Пока доступны только `ru` (по умолчанию) и `gnida`.\n\n**Say/Edit**\n\nУбран аргумент --everyone и запрещено упоминание @everyone каким-либо способом.', inline = False)
        await ctx.send(embed = emb)

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice and ctx.author.voice.channel:
            channel = ctx.author.voice.channel
        else:
            emb = discord.Embed(description = 'Ты должен быть в канале, чтобы использовать это.', colour = discord.Color.orange())
            if ctx.guild.owner.id != self.client.owner_id and ctx.guild.owner.id not in friends:
                emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
            await ctx.send(embed = emb)
        global vc
        vc = await channel.connect()

    @commands.command()
    async def leave(self, ctx):
        if ctx.author.voice and ctx.author.voice.channel:
            pass
        else:
            emb = discord.Embed(description = 'Ты должен быть в канале, чтобы использовать это.', colour = discord.Color.orange())
            if ctx.guild.owner.id != self.client.owner_id and ctx.guild.owner.id not in friends:
                emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
            await ctx.send(embed = emb)
        await vc.disconnect()

def setup(client):
    client.add_cog(Cephalon(client))
