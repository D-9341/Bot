import asyncio
import datetime
import os
import random

import discord
from discord.ext import commands
from pymongo import MongoClient

passw = os.environ.get('passw')
cluster = MongoClient(f"mongodb+srv://cephalon:{passw}@locale.ttokw.mongodb.net/Locale?retryWrites=true&w=majority")
collection = cluster.Locale.locale

friends = [351071668241956865, 417362845303439360]

guilds = [693929822543675455, 735874149578440855, 818758712163827723]

botversions = [764882153812787250, 694170281270312991, 762015251264569352]

class Slapper(commands.Converter):
    async def convert(self, ctx, argument):
        mention = random.choice(ctx.channel.members)
        emb = discord.Embed(description = f'{argument}', color =  0x2f3136, timestamp = discord.utils.utcnow())
        emb.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar.url)
        return await ctx.send(f'@someone ||{mention.mention}||', embed = emb)

class Misc(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Модуль Misc загружен')

    @commands.command()
    async def roll(self, ctx, first: int = None, second: int = None):
        if first <= 0 or second <= 0:
            return await ctx.send(embed = discord.Embed(description = f'{ctx.author.display_name} попытался выролять отрицательное число', color = 0xff8000))
        if not first and not second:
            rand = random.randint(0, 100)
            if rand == 69:
                await ctx.send(embed = discord.Embed(description = f'{ctx.author.display_name} получает случайное число (0-100)\n`100`', color = 0xff8000))
            else:
                rand1 = random.randint(0, 9)
                rand2 = random.randint(0, 9)
                await ctx.send(embed = discord.Embed(description = f'{ctx.author.display_name} получает случайное число (0-100)\n`0{rand1}{rand2}`', color = 0xff8000))
        if first and not second:
            rand = random.randint(0, first)
            if first < 10:
                await ctx.send(embed = discord.Embed(description = f'`{ctx.author.display_name} получает случайное число (0-{first})\n0{rand}`', color = 0xff8000))
            else:
                await ctx.send(embed = discord.Embed(description = f'`{ctx.author.display_name} получает случайное число (0-{first})\n{rand}`', color = 0xff8000))
        if first and second:
            if first > second:
                rand = random.randint(first, first)
                return await ctx.send(embed = discord.Embed(description = f'`{ctx.author.display_name} получает случайное число ({first}-{first})\n{rand}`', color = 0xff8000))
            rand = random.randint(first, second)
            await ctx.send(embed = discord.Embed(description = f'`{ctx.author.display_name} получает случайное число ({first}-{second})\n{rand}`', color = 0xff8000))

    @commands.command(aliases = ['c', 'coin'])
    async def coinflip(self, ctx):
        coin = random.choice(['ОРЁЛ', 'РЕШКА'])
        await ctx.send(embed = discord.Embed(description = f'{ctx.author.mention} подбрасывает монетку: {coin}', color = 0xff8000))

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def vote(self, ctx, *, text):
        emb = discord.Embed(description = 'ГОЛОСОВАНИЕ', color = 0xff8000)
        emb.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar.url)
        emb.add_field(name = 'Голосуем за:', value = text)
        emb.set_footer(text = '🚫 - воздержусь')
        sent = await ctx.send(embed = emb)
        await sent.add_reaction('👍')
        await sent.add_reaction('👎')
        await sent.add_reaction('🚫')

    @commands.command()
    async def someone(self, ctx, *, text: Slapper):
        await ctx.send(embed = text)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def rolemembers(self, ctx, role: discord.Role):
        emb = discord.Embed(color = 0xff8000)
        if len(role.members) != 0:
            emb.add_field(name = f'Участники с ролью {role} ({len(role.members)})', value = ', '.join([member.mention for member in role.members]))
        else:
            emb.description = f'Роли {role.name} нет ни у кого.'
        await ctx.send(embed = emb)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def guild(self, ctx):
        guild = ctx.guild
        emb = discord.Embed(color = 0x2f3136, timestamp = discord.utils.utcnow())
        emb.set_author(name = guild, icon_url = guild.icon.url if guild.icon else 'https://cdn.discordapp.com/attachments/685176670344183836/1076601210485866546/76923ec8de0a6ca5.png')
        emb.add_field(name = 'ID сервера', value = guild.id)
        emb.add_field(name = 'Владелец', value = guild.owner.mention)
        emb.add_field(name = 'Участников', value = f'{guild.member_count}\n**Из них ботов:** {len(list(filter(lambda m: m.bot, guild.members)))}\n**Из них людей:** {len(list(filter(lambda m: not m.bot, guild.members)))}')
        emb.add_field(name = 'Каналов', value = f'Текстовых {len(guild.text_channels)} | Голосовых {len(guild.voice_channels)}')
        roles = ', '.join([role.name for role in guild.roles[1:]])
        if len(roles) > 1:
            emb.add_field(name = f'Роли ({len(guild.roles)-1})', value = roles, inline = False)
        d = guild.created_at.strftime('%d.%m.%Y %H:%M:%S GMT')
        emb.add_field(name = 'Дата создания сервера', value = f'{d}', inline = False)
        emb.set_thumbnail(url = guild.icon.url if guild.icon else 'https://cdn.discordapp.com/attachments/685176670344183836/1076601210485866546/76923ec8de0a6ca5.png')
        await ctx.send(embed = emb)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def roleinfo(self, ctx, role: discord.Role):
        match role.mentionable:
            case False:
                role.mentionable = 'Нет'
            case True:
                role.mentionable = 'Да'
        match role.managed:
            case False:
                role.managed = 'Нет'
            case True:
                role.managed = 'Да'
        match role.hoist:
            case False:
                role.hoist = 'Нет'
            case True:
                role.hoist = 'Да'
        emb = discord.Embed(title = role.name, color = 0x2f3136)
        emb.add_field(name = 'ID', value = role.id)
        emb.add_field(name = 'Цвет', value = role.color)
        emb.add_field(name = 'Упоминается?', value = role.mentionable)
        emb.add_field(name = 'Управляется интеграцией?', value = role.managed)
        emb.add_field(name = 'Позиция в списке', value = role.position)
        d = role.created_at.strftime('%d.%m.%Y %H:%M:%S GMT')
        emb.add_field(name = 'Создана', value = f'{d}', inline = False)
        emb.add_field(name = 'Показывает участников отдельно?', value = role.hoist)
        await ctx.send(embed = emb)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def avatar(self, ctx, member: discord.User = None):
        if member == None:
            member = ctx.author
        emb = discord.Embed(color = 0x2f3136)
        if not member.avatar.is_animated():
            emb.set_image(url = member.avatar.with_format('png'))
        else:
            emb.set_image(url = member.avatar.url)
        emb.set_author(name = member.display_name)
        await ctx.send(embed = emb)

    @commands.command(aliases = ['me'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def about(self, ctx, member: discord.Member = None):
        if member == None:
            member = ctx.author
        match member.bot:
            case False:
                bot = 'Нет'
            case True:
                bot = 'Да'
        emb = discord.Embed(color = 0x2f3136, timestamp = discord.utils.utcnow())
        emb.set_author(name = member.display_name)
        emb.add_field(name = 'ID', value = member.id)
        if ctx.guild:
            d = member.created_at.strftime('%d.%m.%Y %H:%M:%S GMT')
            d1 = member.joined_at.strftime('%d.%m.%Y %H:%M:%S GMT')
            emb.add_field(name = 'Создан', value = f'{d}', inline = False)
            emb.add_field(name = 'Вошёл', value = f'{d1}', inline = False)
        emb.add_field(name = 'Упоминание', value = member.mention)
        emb.add_field(name = 'Глобальное имя', value = member.name)
        if member.nick:
            emb.add_field(name = 'Никнейм', value = member.nick)
        match member.status:
            case discord.Status.online:
                status = 'В сети'
            case discord.Status.dnd:
                status = 'Не беспокоить'
            case discord.Status.idle:
                status = 'Не активен'
            case discord.Status.offline:
                status = 'Не в сети'
        emb.add_field(name = 'Статус', value = status)
        if ctx.guild:
            roles = ', '.join([role.name for role in member.roles[1:]])
            emb.add_field(name = 'Бот?', value = bot)
        if limit > 1 and ctx.guild:
            limit = len(member.roles)
            emb.add_field(name = f'Роли ({len(member.roles)-1})', value = roles, inline = False)
            emb.add_field(name = 'Высшая Роль', value = member.top_role.mention, inline = False)
        emb.set_thumbnail(url = member.avatar.url)
        await ctx.send(embed = emb)

async def setup(client):
    await client.add_cog(Misc(client))
