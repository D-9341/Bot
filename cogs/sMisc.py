import asyncio
import datetime
import os
import random
import re

import discord
import discord_slash
from discord.ext import commands
from discord_slash import cog_ext as slash
from pymongo import MongoClient

passw = os.environ.get('passw')
cluster = MongoClient(f"mongodb+srv://cephalon:{passw}@locale.ttokw.mongodb.net/Locale?retryWrites=true&w=majority")
collection = cluster.Locale.locale

time_regex = re.compile(r"(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {'h': 3600, 's': 1, 'm': 60, 'd': 86400}

friends = [351071668241956865, 417362845303439360]

guilds = [693929822543675455, 735874149578440855, 818758712163827723]

botversions = [764882153812787250, 694170281270312991, 762015251264569352]

class Slapper(commands.Converter):
    async def convert(self, ctx, argument):
        mention = random.choice(ctx.guild.members)
        emb = discord.Embed(description = f'{argument}', colour =  0x2f3136, timestamp = ctx.message.created_at)
        emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
        return await ctx.send(f'@someone ||{mention.mention}||', embed = emb)

class TimeConverter(commands.Converter):
    async def convert(self, ctx, argument):
        args = argument.lower()
        time = 0
        matches = re.findall(time_regex, args)
        for key, value in matches:
            try:
                time += time_dict[value] * float(key)
            except KeyError:
                await ctx.send(f'{value} не является правильным аргументом! Правильные: h|m|s|d')
            except ValueError:
                await ctx.send(f'{key} не число!')
        return time

class sMisc(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Группа Slash-команд Misc загружена')

    @slash.cog_slash(name = 'vote', description = 'Устраивает голосование за какое-либо событие', options = [{'name': 'text', 'description': 'Текст для голосования за. Пишите так, будто слова *голосуем за* уже написаны', 'required': True, 'type': 3}])
    async def _vote(self, ctx, *, text):
        emb = discord.Embed(description = 'ГОЛОСОВАНИЕ', colour = discord.Color.orange())
        emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
        emb.add_field(name = 'Голосуем за:', value = text)
        emb.set_footer(text = '🚫 - воздержусь')
        sent = await ctx.send(embed = emb)
        await sent.add_reaction('👍')
        await sent.add_reaction('👎')
        await sent.add_reaction('🚫')

    @slash.cog_slash(name = 'rolemembers', description = 'Показывает участников с определённой ролью', options = [{'name': 'role', 'description': 'Роль для поиска', 'required': True, 'type': 8}])
    async def _rolemembers(self, ctx, role: discord.Role, member: discord.Member = None):
        emb = discord.Embed(colour = discord.Color.orange())
        if len(role.members) != 0:
            emb.add_field(name = f'Участники с ролью {role} ({len(role.members)})', value = ', '.join([member.mention for member in role.members]))
            if ctx.guild.owner.id != self.client.owner_id and ctx.guild.owner.id not in friends:
                emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        else:
            if ctx.guild.owner.id != self.client.owner_id and ctx.guild.owner.id not in friends:
                emb.set_footer(text = 'Обнаружено 0 участников с этой ролью. Cephalon Cy by сасиска#2472')
            else:
                emb.set_footer(text = 'Обнаружено 0 участников с этой ролью.')
        await ctx.send(embed = emb)

    @slash.cog_slash(name = 'guild', description = 'Показывает информацию о сервере')
    async def _guild(self, ctx):
        guild = ctx.guild
        emb = discord.Embed(colour = discord.Color.orange(), timestamp = datetime.datetime.utcnow())
        emb.set_author(name = guild, icon_url = guild.icon_url)
        emb.add_field(name = 'ID сервера', value = guild.id)
        emb.add_field(name = 'Голосовой регион', value = guild.region)
        emb.add_field(name = 'Владелец', value = guild.owner.mention)
        emb.add_field(name = 'Участников', value = guild.member_count)
        emb.add_field(name = 'Из них ботов', value = len(list(filter(lambda m: m.bot, ctx.guild.members))))
        emb.add_field(name = 'Из них людей', value = len(list(filter(lambda m: not m.bot, ctx.guild.members))))
        emb.add_field(name = 'Каналов', value = f'Текстовых {len(guild.text_channels)} | Голосовых {len(guild.voice_channels)}')
        roles = ', '.join([role.name for role in guild.roles[1:]])
        emb.add_field(name = f'Роли ({len(guild.roles)-1})', value = roles, inline = False)
        now = datetime.datetime.today()
        then = guild.created_at
        delta = now - then
        d = guild.created_at.strftime('%d.%m.%Y %H:%M:%S UTC')
        emb.add_field(name = 'Дата создания сервера', value = f'{delta.days} дней назад. ({d})', inline = False)
        emb.set_thumbnail(url = guild.icon_url)
        await ctx.send(embed = emb)

    @slash.cog_slash(name = 'roleinfo', description = 'Информация о роли', options = [{'name': 'role', 'description': 'Роль', 'required': True, 'type': 8}])
    async def _roleinfo(self, ctx, *, role: discord.Role):
        if role.mentionable == False:
            role.mentionable = 'Нет' 
        elif role.mentionable == True:
            role.mentionable = 'Да'
        if role.managed == False:
            role.managed = 'Нет'
        elif role.managed == True:
            role.managed = 'Да'
        if role.hoist == False:
            role.hoist = 'Нет'
        elif role.hoist == True:
            role.hoist = 'Да'
        emb = discord.Embed(title = role.name, colour = role.colour)
        emb.add_field(name = 'ID', value = role.id)
        emb.add_field(name = 'Цвет', value = role.color)
        emb.add_field(name = 'Упоминается?', value = role.mentionable)
        emb.add_field(name = 'Управляется интеграцией?', value = role.managed)
        emb.add_field(name = 'Позиция в списке', value = role.position)
        now = datetime.datetime.today()
        then = role.created_at
        delta = now - then
        d = role.created_at.strftime('%d.%m.%Y %H:%M:%S GMT')
        emb.add_field(name = 'Создана', value = f'{delta.days} дня(ей) назад. ({d})', inline = False)
        emb.add_field(name = 'Показывает участников отдельно?', value = role.hoist)
        await ctx.send(embed = emb)

    @slash.cog_slash(name = 'avatar', description = 'Выводит аватар участника', options = [{'name': 'member', 'description': 'Пользователь', 'required': False, 'type': 6}])
    async def _avatar(self, ctx, member: discord.Member = None):
        if member == None:
            member = ctx.author
        av = 'png'
        av1 = 'webp'
        av2 = 'jpg'
        emb = discord.Embed(colour = member.color)
        if member.is_avatar_animated() == False:
            emb.add_field(name = '.png', value = f'[Ссылка]({member.avatar_url_as(format = av)})')
            emb.add_field(name = '.webp', value = f'[Ссылка]({member.avatar_url_as(format = av1)})')
            emb.add_field(name = '.jpg', value = f'[Ссылка]({member.avatar_url_as(format = av2)})')
        else:
            emb.set_footer(text = 'по причине того, что аватар анимирован - ссылок на статичные форматы нет!')
        emb.set_image(url = member.avatar_url)
        emb.set_author(name = member)
        await ctx.send(embed = emb)

    @slash.cog_slash(name = 'about', description = 'Показывает информацию о участнике', options = [{'name': 'member', 'description': 'Участник', 'required': False, 'type': 6}])
    async def _about(self, ctx, member: discord.Member = None):
        if member == None:
            member = ctx.author
        if member.nick == None:
            member.nick = 'Н/Д'
        if member.bot == False:
            bot = 'Неа'
        elif member.bot == True:
            bot = 'Ага'
        emb = discord.Embed(colour = member.color, timestamp = datetime.datetime.utcnow())
        emb.set_author(name = member)
        emb.add_field(name = 'ID', value = member.id)
        now = datetime.datetime.today()
        then = member.created_at
        delta = now - then
        d = member.created_at.strftime('%d.%m.%Y %H:%M:%S UTC')
        then1 = member.joined_at
        delta1 = now - then1
        d1 = member.joined_at.strftime('%d.%m.%Y %H:%M:%S UTC')
        emb.add_field(name = 'Создан', value = f'{delta.days} дня(ей) назад. ({d})', inline = False)
        emb.add_field(name = 'Вошёл', value = f'{delta1.days} дня(ей) назад. ({d1})', inline = False)
        emb.add_field(name = 'Упоминание', value = member.mention)
        emb.add_field(name = 'Raw имя', value = member.name)
        emb.add_field(name = 'Никнейм', value = member.nick)
        if member.status == discord.Status.online:
            status = 'В сети'
        elif member.status == discord.Status.dnd:
            status = 'Не беспокоить'
        elif member.status == discord.Status.idle:
            status = 'Не активен'
        elif member.status == discord.Status.offline:
            status = 'Не в сети'
        emb.add_field(name = 'Статус', value = status)
        roles = ', '.join([role.name for role in member.roles[1:]])
        emb.add_field(name = 'Бот?', value = bot)
        limit = len(member.roles)
        if limit > 1:
            emb.add_field(name = f'Роли ({len(member.roles)-1})', value = roles, inline = False)
            emb.add_field(name = 'Высшая Роль', value = member.top_role.mention, inline = False)
        emb.set_thumbnail(url = member.avatar_url)
        await ctx.send(embed = emb)

def setup(client):
    client.add_cog(sMisc(client))
