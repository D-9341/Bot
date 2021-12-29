import asyncio
import datetime
import os
import random
import re

import disnake
from disnake.ext import commands
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
        emb.set_author(name = ctx.author, icon_url = ctx.author.avatar.url)
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

    @commands.slash_command(name = "roll", description = 'Ролит случайное число')
    async def _roll(self, inter, first: int = None, second: int = None):
        '''
        Parameters
        ----------
        first: :class:`str`
            Первое число
        second: :class:`str`
            Второе число
        '''
        if first == None and second == None:
            rand = random.randint(0, 100)
            if rand == 69:
                await inter.response.send_message(f'`{inter.author} получает случайное число(0-100)\n100`')
            else:
                rand1 = random.randint(0, 9)
                rand2 = random.randint(0, 9)
                await inter.response.send_message(f'`{inter.author} получает случайное число(0-100)\n0{rand1}{rand2}`')
        if first != None and second == None:
            rand = random.randint(0, first)
            await inter.response.send_message(f'`{inter.author} получает случайное число(0-{first})\n{rand}`')
        if first != None and second != None:
            if first > second:
                await inter.response.send_message(f'`{inter.author} получает случайное число({first}-{first})\n{first}`')
            rand = random.randint(first, second)
            await inter.response.send_message(f'`{inter.author} получает случайное число({first}-{second})\n{rand}`')

    @commands.slash_command(name = 'coinflip', description = 'Подкидывает монетку')
    async def _coinflip(self, inter):
        emb = disnake.Embed(description = f'{inter.author.mention} подбрасывает монетку: ОРЁЛ', colour = 0x2f3136)
        emb1 = disnake.Embed(description = f'{inter.author.mention} подбрасывает монетку: РЕШКА', colour = 0x2f3136)
        choices = [emb, emb1]
        rancoin = random.choice(choices)
        await inter.response.send_message(embed = rancoin)

    @commands.slash_command(name = 'vote', description = 'Устраивает голосование за что-либо')
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def _vote(self, inter, *, text):
        '''
        Parameters
        ----------
        text: :class:`str`
            Текст для написания. Пишите его так, будто слова *голосуем за* уже написаны
        '''
        emb = disnake.Embed(description = 'ГОЛОСОВАНИЕ', colour = 0x2f3136)
        emb.set_author(name = inter.author, icon_url = inter.author.avatar.url)
        emb.add_field(name = 'Голосуем за:', value = text)
        emb.set_footer(text = '🚫 - воздержусь')
        await inter.response.send_message(embed = emb)
        sent = await inter.original_message()
        await sent.add_reaction('👍')
        await sent.add_reaction('👎')
        await sent.add_reaction('🚫')
        
    @commands.slash_command(name = 'rolemembers', description = 'Показывает участников с определённой ролью')
    async def _rolemembers(self, inter, role: disnake.Role, member: disnake.Member = None):
        '''
        Parameters
        ----------
        role: :class:`disnake.Role`
            Роль для поиска
        '''
        emb = disnake.Embed(colour = 0x2f3136)
        if len(role.members) != 0:
            emb.add_field(name = f'Участники с ролью {role} ({len(role.members)})', value = ', '.join([member.mention for member in role.members]))
        else:
            emb.set_footer(text = 'Обнаружено 0 участников с этой ролью.')
        await inter.response.send_message(embed = emb)

    @commands.slash_command(name = 'guild', description = 'Показывает информацию о сервере')
    async def _guild(self, inter):
        guild = inter.guild
        emb = disnake.Embed(colour = 0x2f3136, timestamp = disnake.utils.utcnow())
        emb.set_author(name = guild, icon_url = guild.icon.url)
        emb.add_field(name = 'ID сервера', value = guild.id)
        emb.add_field(name = 'Голосовой регион', value = guild.region)
        emb.add_field(name = 'Владелец', value = guild.owner.mention)
        emb.add_field(name = 'Участников', value = guild.member_count)
        emb.add_field(name = 'Из них ботов', value = len(list(filter(lambda m: m.bot, inter.guild.members))))
        emb.add_field(name = 'Из них людей', value = len(list(filter(lambda m: not m.bot, inter.guild.members))))
        emb.add_field(name = 'Каналов', value = f'Текстовых {len(guild.text_channels)} | Голосовых {len(guild.voice_channels)}')
        roles = ', '.join([role.name for role in guild.roles[1:]])
        if len(roles) > 1:
            emb.add_field(name = f'Роли ({len(guild.roles)-1})', value = roles, inline = False)
        d = guild.created_at.strftime('%d.%m.%Y %H:%M:%S UTC')
        emb.add_field(name = 'Дата создания сервера', value = f'{d}', inline = False)
        emb.set_thumbnail(url = guild.icon.url)
        await inter.response.send_message(embed = emb)

    @commands.slash_command(name = 'roleinfo', description = 'Информация о роли')
    async def _roleinfo(self, inter, *, role: disnake.Role):
        '''
        Parameters
        ----------
        role: :class:`disnake.Role`
            Роль
        '''
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
        emb = disnake.Embed(title = role.name, colour = 0x2f3136)
        emb.add_field(name = 'ID', value = role.id)
        emb.add_field(name = 'Цвет', value = role.color)
        emb.add_field(name = 'Упоминается?', value = role.mentionable)
        emb.add_field(name = 'Управляется интеграцией?', value = role.managed)
        emb.add_field(name = 'Позиция в списке', value = role.position)
        d = role.created_at.strftime('%d.%m.%Y %H:%M:%S GMT')
        emb.add_field(name = 'Создана', value = f'{d}', inline = False)
        emb.add_field(name = 'Показывает участников отдельно?', value = role.hoist)
        await inter.response.send_message(embed = emb)

    @commands.slash_command(name = 'avatar', description = 'Выводит аватар участника')
    async def _avatar(self, inter, member: disnake.Member = None):
        '''
        Parameters
        ----------
        member: :class:`disnake.Member`
            Пользователь
        '''
        if member == None:
            member = inter.author
        emb = disnake.Embed(colour = 0x2f3136)
        if not member.avatar.is_animated():
            emb.set_image(url = member.avatar.with_format('png'))
        else:
            emb.set_image(url = member.avatar.url)
        emb.set_author(name = member)
        await inter.response.send_message(embed = emb)

    @commands.slash_command(name = 'about', description = 'Показывает информацию о участнике')
    async def _about(self, inter, member: disnake.Member = None):
        '''
        Parameters
        ----------
        member: :class:`disnake.Member`
            Участник
        '''
        if member == None:
            member = inter.author
        if member.nick == None:
            member.nick = 'Н/Д'
        if member.bot == False:
            bot = 'Неа'
        elif member.bot == True:
            bot = 'Ага'
        emb = disnake.Embed(colour = 0x2f3136, timestamp = disnake.utils.utcnow())
        emb.set_author(name = member)
        emb.add_field(name = 'ID', value = member.id)
        d = member.created_at.strftime('%d.%m.%Y %H:%M:%S UTC')
        d1 = member.joined_at.strftime('%d.%m.%Y %H:%M:%S UTC')
        emb.add_field(name = 'Создан', value = f'{d}', inline = False)
        emb.add_field(name = 'Вошёл', value = f'{d1}', inline = False)
        emb.add_field(name = 'Упоминание', value = member.mention)
        emb.add_field(name = 'Необработанное имя', value = member.name)
        emb.add_field(name = 'Никнейм', value = member.nick)
        if member.status == disnake.Status.online:
            status = 'В сети'
        elif member.status == disnake.Status.dnd:
            status = 'Не беспокоить'
        elif member.status == disnake.Status.idle:
            status = 'Не активен'
        elif member.status == disnake.Status.offline:
            status = 'Не в сети'
        emb.add_field(name = 'Статус', value = status)
        roles = ', '.join([role.name for role in member.roles[1:]])
        emb.add_field(name = 'Бот?', value = bot)
        limit = len(member.roles)
        if limit > 1:
            emb.add_field(name = f'Роли ({len(member.roles)-1})', value = roles, inline = False)
            emb.add_field(name = 'Высшая Роль', value = member.top_role.mention, inline = False)
        emb.set_thumbnail(url = member.avatar.url)
        await inter.response.send_message(embed = emb)

def setup(client):
    client.add_cog(sMisc(client))
