import asyncio
import os
import random

import discord
from discord.ext import commands
from pymongo import MongoClient

passw = os.environ.get('passw')
cluster = MongoClient(f"mongodb+srv://cephalon:{passw}@locale.ttokw.mongodb.net/Locale?retryWrites=true&w=majority")
collection = cluster.Locale.locale

friends = [351071668241956865, 417362845303439360]

class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Модуль Fun загружен')

    @commands.command()
    async def roll(self, ctx, first: int = None, second: int = None):
        if first == None and second == None:
            rand = random.randint(0, 9)
            if rand == 9:
                await ctx.send(f'`{ctx.author} выпадает число(0-100)\n100`')
            else:
                rand1 = random.randint(0, 9)
                rand2 = random.randint(0, 9)
                await ctx.send(f'`{ctx.author} выпадает число(0-100)\n0{rand1}{rand2}`')
        if first != None and second == None:
            rand = random.randint(0, first)
            if first < 10:
                await ctx.send(f'`{ctx.author} выпадает число(0-{first})\n0{rand}`')
            else:
                await ctx.send(f'`{ctx.author} выпадает число(0-{first})\n{rand}`')
        if first != None and second != None:
            if first > second:
                rand = random.randint(first, first)
                await ctx.send(f'`{ctx.author} выпадает число({first}-{first})\n{rand}`')
            rand = random.randint(first, second)
            await ctx.send(f'`{ctx.author} выпадает число({first}-{second})\n{rand}`')

    @commands.command()
    async def dotersbrain(self, ctx):
        sent1 = await ctx.send(f'{ctx.author.mention}, через 5 секунд появится одно из слов (чё, а, да, нет, ок), на которое вам нужно будет правильно ответить. На размышление 4 секунды.')
        await asyncio.sleep(5)
        words = ['чё', 'а', 'да', 'нет', 'ок']
        rand = random.choice(words)
        sent = await ctx.send(rand)
        try:
            msg = await self.client.wait_for('message', timeout = 4, check = lambda message: message.author == ctx.author and message.channel == ctx.message.channel)
            if msg.content.lower() == 'хуй через плечо' and sent.content == 'чё':
                await ctx.send(f'Поздравляю, у вас 3 стадия рака!')
                await sent1.delete()
                await sent.delete()
            elif sent.content == 'а' and msg.content.lower() == 'хуй на':
                await ctx.send(f'Поздравляю, у вас 3 стадия рака!')
                await sent1.delete()
                await sent.delete()
            elif sent.content == 'да' and msg.content.lower() == 'пизда':
                await ctx.send(f'Поздравляю, у вас 3 стадия рака!')
                await sent1.delete()
                await sent.delete()
            elif sent.content == 'нет' and msg.content.lower() == 'пидора ответ':
                await ctx.send(f'Поздравляю, у вас 3 стадия рака!')
                await sent1.delete()
                await sent.delete()
            elif sent.content == 'ок' and msg.content.lower() == 'хуй намок':
                await ctx.send(f'Поздравляю, у вас 3 стадия рака!')
                await sent1.delete()
                await sent.delete()
            else:
                await ctx.send('Вы совершенно здоровый человек! ||попробуйте cy/help dotersbrain||')
                await sent1.delete()
                await sent.delete()
        except asyncio.TimeoutError:
            await ctx.send(f'{ctx.author.mention}, Слишком медленно.')
            await sent1.delete()
            await sent.delete()

    @commands.command()
    async def niggers(self, ctx):
        rlocale = rlocale = collection.find_one({"_id": ctx.author.id})["locale"]
        if rlocale == 'ru':
            emb = discord.Embed(description = '[осуждающее видео](https://www.youtube.com/watch?v=167apVK8Suw)', colour = discord.Color.orange())
            if ctx.guild.owner.id != self.client.owner_id and ctx.guild.owner.id not in friends:
                emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
            await ctx.send(embed = emb)
        if rlocale == 'gnida':
            emb = discord.Embed(description = '[негры пидарасы, и извинятся за это не буду!](https://www.youtube.com/watch?v=167apVK8Suw)', colour = discord.Color.orange())
            if ctx.guild.owner.id != self.client.owner_id and ctx.guild.owner.id not in friends:
                emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
            await ctx.send(embed = emb)

    @commands.command()
    async def aye_balbec(self, ctx):
        emb = discord.Embed(colour = ctx.author.color)
        emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
        emb.set_image(url = 'https://sun9-61.userapi.com/tja5cuQthduwgxq2yMigLiUxfYq_5fqiA6cJWg/sZOkbPajoSY.jpg')
        await ctx.send(embed = emb)

    @commands.command()
    async def rp(self, ctx):
        emb = discord.Embed(description = '[Ныа](https://www.youtube.com/watch?v=idmTSW9mfYI)', colour = discord.Color.orange())
        await ctx.send(embed = emb)

    @commands.command(aliases = ['.rap'])
    async def rap(self, ctx):
        emb = discord.Embed(colour = ctx.author.color)
        emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
        emb.set_image(url = 'https://thumbs.gfycat.com/MessyCarefreeHousefly-size_restricted.gif')
        await ctx.send(embed = emb)

    @commands.command()
    async def zatka(self, ctx):
        emb = discord.Embed(title = 'Форма заявки для Набор кадров', colour = ctx.author.color)
        emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
        emb.add_field(name = '(1). ZATKA в STEAM.  ZATKA_KING#8406 в Discord.', value = 'возраст 14+  часовой пояс IL +0.', inline = False)
        emb.add_field(name = '(2). Интересующая управление:', value = 'Discord', inline = False)
        emb.add_field(name = '(3). Опыт администрирования:', value = 'Есть.', inline = False)
        emb.add_field(name = 'творческие:', value = 'Есть.', inline = False)
        emb.add_field(name = 'технические навыки:', value = 'Нет.', inline = False)
        emb.add_field(name = '(4). Сколько часов готовы уделять работе', value = '[ 15+ в неделю ]', inline = False)
        emb.add_field(name = 'в какое время дня свободны', value = '16:00 до 22:00+', inline = False)
        await ctx.send(embed = emb)

    @commands.command(aliases = ['c', 'coin'])
    async def coinflip(self, ctx):
        emb = discord.Embed(description = 'Орёл!', colour = discord.Color.orange())
        emb.set_image(url = 'https://cdn.discordapp.com/attachments/524213591084105729/763835275930632252/-removebg-preview.png')
        emb1 = discord.Embed(description = 'Решка!', colour = discord.Color.orange())
        emb1.set_image(url = 'https://cdn.discordapp.com/attachments/524213591084105729/763837699240099890/-removebg-preview.png')
        choices = [emb, emb1]
        rancoin = random.choice(choices)
        await ctx.send(embed = rancoin)

def setup(client):
    client.add_cog(Fun(client))
