import asyncio
import datetime
import os
import re

import discord
from discord.ext import commands
from pymongo import MongoClient

passw = os.environ.get('passw')
cluster = MongoClient(f"mongodb+srv://cephalon:{passw}@locale.ttokw.mongodb.net/Locale?retryWrites=true&w=majority")
collection = cluster.Locale.locale

guilds = [693929822543675455, 735874149578440855, 818758712163827723]

time_regex = re.compile(r"(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {'h': 3600, 's': 1, 'm': 60, 'd': 86400}

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

class Mod(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Модуль Mod загружен')

    @commands.command()
    @commands.has_permissions(view_audit_log = True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def dm(self, ctx, member: discord.Member, * , text):
        emb = discord.Embed(description = f'{text}', color = 0x2f3136)
        emb.set_author(name = ctx.author, icon_url = ctx.author.avatar.url)
        await member.send(embed = emb)
        rlocale = collection.find_one({"_id": ctx.author.id})["locale"]
        if rlocale == 'ru':
            await ctx.send('Сообщение отправлено.')
        if rlocale == 'gnida':
            await ctx.send('Твоя хуйня отправлена')

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, member: discord.Member, *, reason: str = None):
        rlocale = collection.find_one({"_id": ctx.author.id})["locale"]
        bot = discord.utils.get(ctx.guild.members, id = self.client.user.id)
        if member.id not in self.client.owner_ids:
            if reason == None:
                if rlocale == 'ru':
                    reason = 'Не указана.'
                if rlocale == 'gnida':
                    reason = 'хз'
            if member == ctx.author:
                if rlocale == 'ru':
                    emb = discord.Embed(description = 'Ты **не** можешь кикнуть себя.', color = discord.Color.blurple())
                    await ctx.send(embed = emb)
                if rlocale == 'gnida':
                    emb = discord.Embed(description = 'Для дохуя умных доношу - **нельзя** кикать __себя__', color = discord.Color.blurple())
                    await ctx.send(embed = emb)
            if ctx.author.top_role == member.top_role:
                if rlocale == 'ru':
                    emb = discord.Embed(description = f'{ctx.author.mention}, ваша высшая роль равна высшей роли {member.mention}. Кик отклонён.', color = 0xff8000)
                    await ctx.send(embed = emb)
                if rlocale == 'gnida':
                    emb = discord.Embed(description = f'Твоя высшая роль равна высшей роли {member.mention}. Пошёл нахуй.', color = 0xff8000)
                    await ctx.send(embed = emb)
            elif member.top_role > ctx.author.top_role:
                if rlocale == 'ru':
                    emb = discord.Embed(description = f'{ctx.author.mention}, ваша высшая роль ниже высшей роли {member.mention}. Кик отклонён.', color = 0xff8000)
                    await ctx.send(embed = emb)
                if rlocale == 'gnida':
                    emb = discord.Embed(description = f'Твоя высшая роль ниже высшей роли {member.mention}. Пошёл нахуй.', color = 0xff8000)
                    await ctx.send(embed = emb)
            elif member.top_role > bot.top_role:
                if rlocale == 'ru':
                    emb = discord.Embed(description = f'**Моя** высшая роль ниже высшей роли {member.mention}. Кик невозможен.', color = 0xff0000)
                    await ctx.send(embed = emb)
                if rlocale == 'gnida':
                    emb = discord.Embed(description = f'МОЯ высшая роль ниже высшей роли {member.mention}. Сука.', color = 0xff0000)
                    await ctx.send(embed = emb)
            elif member.top_role == bot.top_role:
                if rlocale == 'ru':
                    emb = discord.Embed(description = f'**Моя** высшая роль идентична высшей роли {member.mention}. Кик невозможен.', color = 0xff0000)
                    await ctx.send(embed = emb)
                if rlocale == 'gnida':
                    emb = discord.Embed(description = f'МОЯ высшая роль идентична высшей роли {member.mention}. Сука.', color = 0xff0000)
                    await ctx.send(embed = emb)
            else:
                emb = discord.Embed(color = 0xff8000)
                emb.set_author(name = ctx.author, icon_url = ctx.author.avatar.url)
                emb.add_field(name = 'Был кикнут', value = member.mention)
                emb.add_field(name = 'По причине', value = reason)
                await ctx.send(embed = emb)
                await member.kick(reason = reason)
        else:
            if rlocale == 'ru':
                emb = discord.Embed(description = f'Извините, {ctx.author.mention}, но вы не можете кикнуть моего создателя!', color = 0xff0000)
                await ctx.send(embed = emb)
            if rlocale == 'gnida':
                emb = discord.Embed(description = 'Ого! Пошёл нахуй!', color = 0xff0000)
                await ctx.send(embed = emb)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, member: discord.Member, *, reason: str = None):
        rlocale = collection.find_one({"_id": ctx.author.id})["locale"]
        bot = discord.utils.get(ctx.guild.members, id = self.client.user.id)
        if member.id not in self.client.owner_ids:
            if reason == None:
                if rlocale == 'ru':
                    reason = 'Не указана.'
                if rlocale == 'gnida':
                    reason = 'хз'
            if member == ctx.author:
                if rlocale == 'ru':
                    emb = discord.Embed(description = 'Ты **не** можешь забанить себя.', color = discord.Color.blurple())
                    await ctx.send(embed = emb)
                if rlocale == 'gnida':
                    emb = discord.Embed(description = 'Для дохуя умных доношу - **нельзя** банить __себя__', color = discord.Color.blurple())
                    await ctx.send(embed = emb)
            if ctx.author.top_role == member.top_role:
                if rlocale == 'ru':
                    emb = discord.Embed(description = f'{ctx.author.mention}, ваша высшая роль равна высшей роли {member.mention}. Бан отклонён.', color = 0xff8000)
                    await ctx.send(embed = emb)
                if rlocale == 'gnida':
                    emb = discord.Embed(description = f'Твоя высшая роль равна высшей роли {member.mention}. Саси.', color = 0xff8000)
                    await ctx.send(embed = emb)
            elif member.top_role > ctx.author.top_role:
                if rlocale == 'ru':
                    emb = discord.Embed(description = f'{ctx.author.mention}, ваша высшая роль ниже высшей роли {member.mention}. Бан отклонён.', color = 0xff8000)
                    await ctx.send(embed = emb)
                if rlocale == 'gnida':
                    emb = discord.Embed(description = f'Твоя высшая роль ниже высшей роли {member.mention}. Саси.', color = 0xff8000)
                    await ctx.send(embed = emb)
            elif member.top_role > bot.top_role:
                if rlocale == 'ru':
                    emb = discord.Embed(description = f'**Моя** высшая роль ниже высшей роли {member.mention}. Бан невозможен.', color = 0xff0000)
                    await ctx.send(embed = emb)
                if rlocale == 'gnida':
                    emb = discord.Embed(description = f'МОЯ высшая роль ниже высшей роли {member.mention}. Блять.', color = 0xff0000)
                    await ctx.send(embed = emb)
            elif member.top_role == bot.top_role:
                if rlocale == 'ru':
                    emb = discord.Embed(description = f'**Моя** высшая роль идентична высшей роли {member.mention}. Бан невозможен.', color = 0xff0000)
                    await ctx.send(embed = emb)
                if rlocale == 'gnida':
                    emb = discord.Embed(description = f'МОЯ высшая роль идентична высшей роли {member.mention}. Блять.', color = 0xff0000)
                    await ctx.send(embed = emb)
            else:
                if '--soft' in reason:
                    emb = discord.Embed(color = 0xff8000)
                    emb.set_author(name = ctx.author, icon_url = ctx.author.avatar.url)
                    emb.add_field(name = 'Упрощённо забанен', value = f'{member.mention} ({member.name})')
                    if '--reason' in reason:
                        reason = reason.strip()[15:].strip()
                    emb.add_field(name = 'По причине', value = reason)
                    await ctx.send(embed = emb)
                    await member.ban(reason = reason)
                    await member.unban(reason = '--softban')
                else:
                    emb = discord.Embed(color = 0xff8000)
                    emb.set_author(name = ctx.author, icon_url = ctx.author.avatar.url)
                    emb.add_field(name = 'Был забанен', value = member.mention)
                    emb.add_field(name = 'По причине', value = reason)
                    await ctx.send(embed = emb)
                    await member.ban(reason = reason)
        else:
            if rlocale == 'ru':
                emb = discord.Embed(description = f'Извините, {ctx.author.mention}, но вы не можете забанить моего создателя!', color = 0xff0000)
                await ctx.send(embed = emb)
            if rlocale == 'gnida':
                emb = discord.Embed(description = 'иди нахуй', color = 0xff0000)
                await ctx.send(embed = emb)

    @commands.command()
    @commands.has_permissions(manage_channels = True)
    async def give(self, ctx, member: discord.Member, role: discord.Role):
        rlocale = collection.find_one({"_id": ctx.author.id})["locale"]
        bot = ctx.guild.get_member(self.client.user.id)
        if role != None:
            if role.name == 'Muted':
                if member.id not in self.client.owner_ids:
                    if member == ctx.author:
                        if rlocale == 'ru':
                            emb = discord.Embed(description = 'Ты **не** можешь заглушить себя.', color = discord.Color.blurple())
                            return await ctx.send(embed = emb)
                        if rlocale == 'gnida':
                            emb = discord.Embed(description = 'Для дохуя умных доношу - **нельзя** мутить __себя__', color = discord.Color.blurple())
                            return await ctx.send(embed = emb)
                    else:
                        await member.add_roles(role)
                        if rlocale == 'ru':
                            emb = discord.Embed(description = f'{member.mention} был заглушён {ctx.author.mention}', color = 0x2f3136)
                            return await ctx.send(embed = emb)
                        if rlocale == 'gnida':
                            emb = discord.Embed(description = f'{member.mention} получает мут в ебало от {ctx.author.mention}', color = 0x2f3136)
                            return await ctx.send(embed = emb)
                else:
                    if rlocale == 'ru':
                        emb = discord.Embed(description = 'Вы всё ещё не можете заглушить моего создателя.', color = 0xff0000)
                        return await ctx.send(embed = emb)
                    if rlocale == 'gnida':
                        emb = discord.Embed(description = 'Ты думал мой Создатель тебе по зубам? ОН!?', color = 0xff0000)
                        return await ctx.send(embed = emb)
            else:
                if role > ctx.author.top_role:
                    if rlocale == 'ru':
                        emb = discord.Embed(description = f'Вы не можете выдать {role.mention}, так как она имеет более высокий ранг, чем ваша высшая роль.', color = 0xff8000)
                        await ctx.send(embed = emb)
                    if rlocale == 'gnida':
                        emb = discord.Embed(description = f'Дебилам вроде тебя запрещено выдавать {role.mention}, так как эта роль выше твоей высшей роли.', color = 0xff8000)
                        await ctx.send(embed = emb)
                elif role == ctx.author.top_role:
                    if rlocale == 'ru':
                        emb = discord.Embed(description = f'Вы не можете выдать {role.mention} кому-либо, так как она равна вашей высшей роли.', color = 0xff8000)
                        await ctx.send(embed = emb)
                    if rlocale == 'gnida':
                        emb = discord.Embed(description = f'Дебилам вроде тебя запрещено выдавать {role.mention}, так как она равна твоей высшей роли.', color = 0xff8000)
                        await ctx.send(embed = emb)
                elif role.is_default():
                    if rlocale == 'ru':
                        emb = discord.Embed(description = f'Выдавать @everyone?', color = 0xff8000)
                        await ctx.send(embed = emb)
                    if rlocale == 'gnida':
                        emb = discord.Embed(description = f'Это @everyone, еблан!', color = 0xff8000)
                        await ctx.send(embed = emb)
                elif member.top_role > bot.top_role:
                    if rlocale == 'ru':
                        emb = discord.Embed(description = f'**Моя** высшая роль ниже чем {role.mention}. Выдать роль невозможно.', color = 0xff0000)
                        await ctx.send(embed = emb)
                    if rlocale == 'gnida':
                        emb = discord.Embed(description = f'МОЯ высшая роль ниже {role.mention}. Блять.', color = 0xff0000)
                        await ctx.send(embed = emb)
                elif member.top_role == bot.top_role:
                    if rlocale == 'ru':
                        emb = discord.Embed(description = f'**Моя** высшая роль это {role.mention}. Выдать роль невозможно.', color = 0xff0000)
                        await ctx.send(embed = emb)
                    if rlocale == 'gnida':
                        emb = discord.Embed(description = f'МОЯ высшая роль и есть {role.mention}, блять.', color = 0xff0000)
                        await ctx.send(embed = emb)
                else:
                    await member.add_roles(role)
                    emb = discord.Embed(color = 0xff8000, timestamp = discord.utils.utcnow())
                    emb.add_field(name = 'ВЫДАНА_РОЛЬ', value = f'{role.mention} | {role.name} | ID {role.id}')
                    emb.add_field(name = 'ВЫДАНА:', value = member.mention, inline = False)
                    emb.set_author(name = ctx.author, icon_url = ctx.author.avatar.url)
                    await ctx.send(embed = emb)
        else:
            if rlocale == 'ru':
                emb = discord.Embed(description = f'{ctx.author.mention}, я не могу найти {role} в списке ролей.\n||Используйте @упоминание роли||', color = member.color, timestamp = discord.utils.utcnow())
                await ctx.send(embed = emb)
            if rlocale == 'gnida':
                emb = discord.Embed(description = f'Не вижу я твоего высера в списке ролей', color = member.color, timestamp = discord.utils.utcnow())
                await ctx.send(embed = emb)

    @commands.command()
    @commands.has_permissions(manage_channels = True)
    async def take(self, ctx, member: discord.Member, role: discord.Role):
        rlocale = collection.find_one({"_id": ctx.author.id})["locale"]
        bot = ctx.guild.get_member(self.client.user.id)
        if role != None:
            if role.name == 'Muted':
                await member.remove_roles(role)
                if rlocale == 'ru':
                    emb = discord.Embed(description = f'{member.mention} был разглушён {ctx.author.mention}', color = 0xff8000)
                    return await ctx.send(embed = emb)
                if rlocale == 'gnida':
                    emb = discord.Embed(description = f'{member.mention} размучен {ctx.author.mention}', color = 0xff8000)
                    return await ctx.send(embed = emb)
            if role > ctx.author.top_role:
                if rlocale == 'ru':
                    emb = discord.Embed(description = f'Вы не можете забрать {role.mention}, так как она имеет более высокий ранг, чем ваша высшая роль. Забирание роли отменено.', color = 0x2f3136)
                    await ctx.send(embed = emb)
                if rlocale == 'gnida':
                    emb = discord.Embed(description = f'Тебе, уёбку, не разрешено забирать {role.mention}, так как эта роль круче твоей, говноед', color = 0x2f3136)
                    await ctx.send(embed = emb)
            elif role == ctx.author.top_role:
                if rlocale == 'ru':
                    emb = discord.Embed(description = f'Вы не можете забрать {role.mention}, так как она равна вашей высшей роли. Забирание роли отменено.', color = 0x2f3136)
                    await ctx.send(embed = emb)
                if rlocale == 'gnida':
                    emb = discord.Embed(description = f'Тебе, хуесосу, не положено отбирать {role.mention}, так как эта роль равна твоей, говна кусок', color = 0x2f3136)
                    await ctx.send(embed = emb)
            elif member.top_role > bot.top_role:
                if rlocale == 'ru':
                    emb = discord.Embed(description = f'**Моя** высшая роль ниже высшей роли {member.mention}. Забрать роль невозможно.', color = 0xff0000)
                    await ctx.send(embed = emb)
                if rlocale == 'gnida':
                    emb = discord.Embed(description = f'МОЯ самая крутая роль ниже самой крутой роли {member.mention}, я не могу её спиздить', color = 0xff0000)
                    await ctx.send(embed = emb)
            elif member.top_role == bot.top_role:
                if rlocale == 'ru':
                    emb = discord.Embed(description = f'**Моя** высшая роль идентична высшей роли {member.mention}. Забрать роль невозможно.', color = 0xff0000)
                    await ctx.send(embed = emb)
                if rlocale == 'ginda':
                    emb = discord.Embed(description = f'МОЯ самая крутая роль совпадает с самой крутой ролью этого пидораса -> {member.mention}, не могу спиздить', color = 0xff0000)
                    await ctx.send(embed = emb)
            elif role.is_default():
                if rlocale == 'ru':
                    emb = discord.Embed(description = 'Забрать @everyone?', color = 0xffffff)
                    await ctx.send(embed = emb)
                if rlocale == 'gnida':
                    emb = discord.Embed(description = 'Ты уверен что я должен отжать @everyone?', color = 0xffffff)
                    await ctx.send(embed = emb)
            else:
                await member.remove_roles(role)
                emb = discord.Embed(color = 0xff8000, timestamp = discord.utils.utcnow())
                emb.add_field(name = 'ЗАБРАНА_РОЛЬ', value = f'{role.mention} | {role.name} | ID {role.id}')
                emb.add_field(name = 'ЗАБРАНА_У:', value = member.mention, inline = False)
                emb.set_author(name = ctx.author, icon_url = ctx.author.avatar.url)
                await ctx.send(embed = emb)
        else:
            if rlocale == 'ru':
                emb = discord.Embed(description = f'{ctx.author.mention}, я не могу найти {role.mention} в списке ролей.\n||Используйте @упоминание роли||', color = member.color, timestamp = discord.utils.utcnow())
                await ctx.send(embed = emb)
            if rlocale == 'gnida':
                emb = discord.Embed(description = f'Не вижу я твоего высера в списке ролей', color = member.color, timestamp = discord.utils.utcnow())
                await ctx.send(embed = emb)

    @commands.command()
    @commands.has_permissions(view_audit_log = True)
    async def mute(self, ctx, member: discord.Member, *, reason = None):
        rlocale = collection.find_one({"_id": ctx.author.id})["locale"]
        if reason == None:
            if rlocale == 'ru':
                reason = 'Не указана.'
            if rlocale == 'gnida':
                reason = 'хз'
        role = discord.utils.get(ctx.guild.roles, name = 'Muted')
        if role in member.roles:
            if rlocale == 'ru':
                emb = discord.Embed(description = 'Роль Muted уже есть в списке ролей участника.', color = 0x2f3136)
                return await ctx.send(embed = emb)
            if rlocale == 'gnida':
                emb = discord.Embed(description = 'Этот уебан уже награждён ролью Muted, попробуй на ком-нибудь другом', color = 0x2f3136)
                return await ctx.send(embed = emb)
        if member == ctx.author:
            if rlocale == 'ru':
                emb = discord.Embed(description = 'Ты **не** можешь заглушить себя.', color = discord.Color.blurple())
                return await ctx.send(embed = emb)
            if rlocale == 'gnida':
                emb = discord.Embed(description = 'Для дохуя умных доношу - **нельзя** мутить __себя__', color = discord.Color.blurple())
                return await ctx.send(embed = emb)
        if member.id not in self.client.owner_ids:
            if ctx.author.top_role == member.top_role:
                if rlocale == 'ru':
                    emb = discord.Embed(description = f'{ctx.author.mention}, ваша высшая роль равна высшей роли {member.mention}. Заглушение отклонено.', color = 0xff8000)
                    await ctx.send(embed = emb)
                if rlocale == 'gnida':
                    emb = discord.Embed(description = f'{ctx.author.mention}, твоя самая крутая роль совпадает с самой крутой ролью {member.mention}, выбери кого послабее ', color = 0xff8000)
                    await ctx.send(embed = emb)
            elif ctx.author.top_role < member.top_role:
                if rlocale == 'ru':
                    emb = discord.Embed(description = f'{ctx.author.mention}, ваша высшая роль ниже высшей роли {member.mention}. Заглушение отклонено.', color = 0xff8000)
                    await ctx.send(embed = emb)
                if rlocale == 'gnida':
                    emb = discord.Embed(description = f'Вот это дела {ctx.author.mention}, ты конкретно обосрался! Твоя самая крутая роль даже ниже самой крутой роли {member.mention}, выбери кого послабее, лошара!', color = 0xff8000)
                    await ctx.send(embed = emb)
            else:
                if role != None:
                    await member.add_roles(role)
                    emb = discord.Embed(color = 0xff8000, timestamp = discord.utils.utcnow())
                    emb.add_field(name = 'Заглушён', value = f'{member.mention}')
                    emb.add_field(name = 'Причина', value = reason)
                    await ctx.send(embed = emb)
                else:
                    role = await ctx.guild.create_role(name = 'Muted', color = 0x000001, reason = 'Создано автоматически командой mute')
                    await member.add_roles(role)
                    emb = discord.Embed(color = 0xff8000, timestamp = discord.utils.utcnow())
                    emb.add_field(name = 'Заглушён', value = f'{member.mention}')
                    emb.add_field(name = 'Причина', value = reason)
                    await ctx.send(embed = emb)
        else:
            if rlocale == 'ru':
                emb = discord.Embed(description = f'Извините, {ctx.author.mention}, но вы не можете заглушить моего создателя!', color = 0xff0000)
                await ctx.send(embed = emb)
            if rlocale == 'gnida':
                emb = discord.Embed(description = f'иди нахуй', color = 0xff0000)
                await ctx.send(embed = emb)

    @commands.command()
    @commands.has_permissions(manage_channels = True)
    async def timeout(self, ctx, member: discord.Member, duration: TimeConverter, *, reason = None):
        rlocale = collection.find_one({"_id": ctx.author.id})["locale"]
        if reason == None:
            if rlocale == 'ru':
                reason = 'Не указана.'
            if rlocale == 'gnida':
                reason = 'хз'
        if member.id not in self.client.owner_ids:
            if member == ctx.author:
                if rlocale == 'ru':
                    emb = discord.Embed(description = 'Ты **не** можешь заглушить себя.', color = discord.Color.blurple())
                    await ctx.send(embed = emb)
                if rlocale == 'gnida':
                    emb = discord.Embed(description = 'Для дохуя умных доношу - **нельзя** мутить __себя__', color = discord.Color.blurple())
                    await ctx.send(embed = emb)
            if ctx.author.top_role == member.top_role:
                if rlocale == 'ru':
                    emb = discord.Embed(description = f'{ctx.author.mention}, ваша высшая роль равна высшей роли {member.mention}. Тайм-аут отклонён.', color = 0xff8000)
                    await ctx.send(embed = emb)
                if rlocale == 'gnida':
                    emb = discord.Embed(description = f'{ctx.author.mention}, смотри сюда, твоя наивысшая роль равна его наивысшей роли, понял? Это значит что я не могу отстранить {member.mention}, от пиздежа ', color = 0xff8000)
                    await ctx.send(embed = emb)
            elif ctx.author.top_role < member.top_role:
                if rlocale == 'ru':
                    emb = discord.Embed(description = f'{ctx.author.mention}, ваша высшая роль ниже высшей роли {member.mention}. Тайм-аут отклонён.', color = 0xff8000)
                    await ctx.send(embed = emb)
                if rlocale == 'gnida':
                    emb = discord.Embed(description = f'{ctx.author.mention}, твоя самая крутая роль даже ниже самой крутой роли {member.mention}. Надеюсь мне не надо объяснять почему я не могу отстранить его от пиздежа?', color = 0xff8000)
                    await ctx.send(embed = emb)
            else:
                await member.timeout(reason = reason, duration = duration)
                emb = discord.Embed(title = f'Тайм-аут участника {member}', color = 0xff8000, timestamp = discord.utils.utcnow())
                emb.add_field(name = 'Причина', value = reason)
                emb.add_field(name = 'Время тайм-аута', value = f'{duration}s')
                await ctx.send(embed = emb)
        else:
            if rlocale == 'ru':
                emb = discord.Embed(description = f'Извините, {ctx.author.mention}, но вы не можете заглушить моего создателя!', color = 0xff0000)
                await ctx.send(embed = emb)
            if rlocale == 'gnida':
                emb = discord.Embed(description = f'иди нахуй', color = 0xff0000)
                await ctx.send(embed = emb)

    @commands.command()
    @commands.has_permissions(manage_channels = True)
    async def deaf(self, ctx, member: discord.Member, *, reason = None):
        rlocale = collection.find_one({"_id": ctx.author.id})["locale"]
        role = discord.utils.get(ctx.guild.roles, name = 'Deafened')
        if reason == None:
            if rlocale == 'ru':
                reason = 'Не указана.'
            if rlocale == 'gnida':
                reason = 'хз'
        if role in member.roles:
            if rlocale == 'ru':
                emb = discord.Embed(description = 'Роль Deafened уже есть в списке ролей участника.', color = 0x2f3136)
                return await ctx.send(embed = emb)
            if rlocale == 'gnida':
                emb = discord.Embed(description = 'Ослеп совсем? У него уже есть роль Deafened.', color = 0x2f3136)
                return await ctx.send(embed = emb)
        if member.id not in self.client.owner_ids:
            if ctx.author.top_role == member.top_role:
                if rlocale == 'ru':
                    emb = discord.Embed(description = f'{ctx.author.mention}, ваша высшая роль равна высшей роли {member.mention}. Заглушение отклонено.', color = 0xff8000)
                    await ctx.send(embed = emb)
                if rlocale == 'gnida':
                    emb = discord.Embed(description = f'{ctx.author.mention}, твоя наикрутейшая роль равна самой крутой роли {member.mention}. Не могу заглушить.', color = 0xff8000)
                    await ctx.send(embed = emb)
            elif ctx.author.top_role < member.top_role:
                if rlocale == 'ru':
                    emb = discord.Embed(description = f'{ctx.author.mention}, ваша высшая роль ниже высшей роли {member.mention}. Заглушение отклонено.', color = 0xff8000)
                    await ctx.send(embed = emb)
                if rlocale == 'gnida':
                    emb = discord.Embed(description = f'{ctx.author.mention}, ты настолько опущен, что твоя высшая роль ниже даже чем у {member.mention}. Хуй тебе, а не мут.', color = 0xff8000)
                    await ctx.send(embed = emb)
            else:
                if role != None:
                    await member.add_roles(role)
                    emb = discord.Embed(color = 0x2f3136, timestamp = discord.utils.utcnow())
                    emb.add_field(name = 'Заглушён', value = member.mention)
                    emb.add_field(name = 'Причина', value = reason)
                    await ctx.send(embed = emb)
                else:
                    role = await ctx.guild.create_role(name = 'Deafened', color = 0x000001, reason = 'Создано автоматически командой deaf')
                    await member.add_roles(role)
                    emb = discord.Embed(color = 0x2f3136, timestamp = discord.utils.utcnow())
                    emb.add_field(name = 'Заглушён', value = member.mention)
                    emb.add_field(name = 'Причина', value = reason)
                    await ctx.send(embed = emb)
        else:
            if rlocale == 'ru':
                emb = discord.Embed(description = f'Извините, {ctx.author.mention}, но вы не можете заглушить моего создателя!', color = 0xff0000)
                await ctx.send(embed = emb)
            if rlocale == 'gnida':
                emb = discord.Embed(description = f'иди нахуй', color = 0xff0000)
                await ctx.send(embed = emb)

    @commands.command()
    @commands.has_permissions(manage_channels = True)
    async def undeaf(self, ctx, member: discord.Member, *, reason = None):
        rlocale = collection.find_one({"_id": ctx.author.id})["locale"]
        role = discord.utils.get(ctx.guild.roles, name = 'Deafened')
        if reason == None:
            if rlocale == 'ru':
                reason = 'Не указана.'
            if rlocale == 'gnida':
                reason = 'хз'
        if member.id not in self.client.owner_ids:
            if role != None:
                if role in member.roles:
                    await member.remove_roles(role)
                    if rlocale == 'ru':
                        emb = discord.Embed(title = f'Принудительное снятие заглушения у {member}', color = 0xff8000, timestamp = discord.utils.utcnow())
                        emb.add_field(name = 'Снял заглушение', value = ctx.author.mention)
                        emb.add_field(name = 'Причина', value = reason)
                        await ctx.send(embed = emb)
                    if rlocale == 'gnida':
                        emb = discord.Embed(title = f'Принудительный анмут этого пидораса -> {member}', color = 0xff8000, timestamp = discord.utils.utcnow())
                        emb.add_field(name = 'Размутил', value = ctx.author.mention)
                        emb.add_field(name = 'Причина', value = reason)
                        await ctx.send(embed = emb)
                else:
                    if rlocale == 'ru':
                        emb = discord.Embed(description = 'Снятие заглушения не требуется. Роли Deafened не обнаружено в списке ролей участника.', color = 0xff8000)
                        await ctx.send(embed = emb)
                    if rlocale == 'gnida':
                        emb = discord.Embed(description = 'Размут не требуется. Он и так уже размучен, ты чё слепой нахуй?', color = 0xff8000)
                        await ctx.send(embed = emb)
            else:
                if rlocale == 'ru':
                    emb = discord.Embed(description = f'{ctx.author.mention}, Я не могу снять заглушение у {member.mention} из-за того, что роль Deafened была удалена', color = 0xff8000, timestamp = discord.utils.utcnow())
                    await ctx.send(embed = emb)
                if rlocale == 'gnida':
                    emb = discord.Embed(description = f'Вот дела, {ctx.author.mention}, кажется я не могу размутить {member.mention} из-за того, что какой-то уебан удалил роль Deafened', color = 0xff8000, timestamp = discord.utils.utcnow())
                    await ctx.send(embed = emb)

    @commands.command()
    @commands.has_permissions(manage_channels = True)
    async def unmute(self, ctx, member: discord.Member, *, reason = None):
        rlocale = collection.find_one({"_id": ctx.author.id})["locale"]
        role = discord.utils.get(ctx.guild.roles, name = 'Muted')
        if reason == None:
            if rlocale == 'ru':
                reason = 'Не указана.'
            if rlocale == 'gnida':
                reason = 'хз'
        if role != None:
            if role in member.roles:
                await member.remove_roles(role)
                if rlocale == 'ru':
                    emb = discord.Embed(title = f'Принудительное снятие заглушения у {member}', color = 0xff8000, timestamp = discord.utils.utcnow())
                    emb.add_field(name = 'Снял заглушение', value = ctx.author.mention)
                    emb.add_field(name = 'По причине', value = reason)
                    await ctx.send(embed = emb)
                if rlocale == 'gnida':
                    emb = discord.Embed(title = f'Принудительный анмут этого программиста -> {member}', color = 0xff8000, timestamp = discord.utils.utcnow())
                    emb.add_field(name = 'Размутил', value = ctx.author.mention)
                    emb.add_field(name = 'По причине', value = reason)
                    await ctx.send(embed = emb)
            else:
                if rlocale == 'ru':
                    emb = discord.Embed(description = 'Снятие заглушения не требуется. Роли Muted не обнаружено в списке ролей участника.', color = 0xff8000)
                    await ctx.send(embed = emb)
                if rlocale == 'gnida':
                    emb = discord.Embed(description = 'Анмут не требуется. Кажется ты уёбок ослеп, смотри внимательно, В СПИСКЕ ЕГО РОЛЕЙ MUTED НЕ ОБНАРУЖЕНА!', color = 0xff8000)
                    await ctx.send(embed = emb)
        else:
            if rlocale == 'ru':
                emb = discord.Embed(description = f'{ctx.author.mention}, Я не могу снять заглушение у {member.mention} из-за того, что роль Muted была удалена', color = 0xff8000, timestamp = discord.utils.utcnow())
                await ctx.send(embed = emb)
            if rlocale == 'gnida':
                emb = discord.Embed(description = f'Слушай сюда {ctx.author.mention}, не могу я его размутить, ясно? Какой-то гандон удалил роль Muted, найди его по журналу аудита и стукни по башке', color = 0xff8000, timestamp = discord.utils.utcnow())
                await ctx.send(embed = emb)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.bot_has_permissions(manage_messages = True)
    @commands.has_permissions(administrator = True)
    async def clear(self, ctx, amount: int, members = '--everyone', *, filt = None):
        await ctx.message.delete()
        authors = {}
        if not '--silent' in members:
            async for message in ctx.channel.history(limit = amount):
                if message.author not in authors:
                    authors[message.author] = 1
                else:
                    authors[message.author] += 1
        if amount == 2472:
            if ctx.author.id in self.client.owner_ids:
                await ctx.channel.delete()
                emb = discord.Embed(description = f'Канал `{ctx.channel.name}` удалён.', color = 0x2f3136)
                await ctx.author.send(embed = emb)
            else:
                await ctx.author.send('А я так не думаю.')
        elif amount >= 300:
            emb = discord.Embed(description = f'{ctx.author.mention}, при таком числе удаления сообщений ({amount}) последует большое время ожидания ответа {self.client.user.mention}.', color = 0x2f3136)
            await ctx.send(f'{ctx.guild.owner.mention}', embed = emb)
        elif amount >= 250:
            if ctx.author != ctx.guild.owner:
                emb = discord.Embed(description = f'{ctx.author.mention}, операция с данным числом ({amount}) доступна только {ctx.guild.owner.mention}.', color = 0x2f3136)
                await ctx.send(f'{ctx.guild.owner.mention}', embed = emb, delete_after = 5)
            else:
                emb = discord.Embed(description = f'{ctx.author.mention}, это слишком большое число для удаления сообщений ({amount}). Возможно большое время ожидания ответа {self.client.user.mention}, которое может усугубится разницей во времени между предыдущими сообщениями и сообщением содержащим команду **и повлияет не только на этот сервер!** Продолжить? (y/n)\n||Отмена через 20 секунд.||', color = 0x2f3136)
                sent = await ctx.send(embed = emb)
                try:
                    msg = await self.client.wait_for('message', timeout = 20, check = lambda message: message.channel == ctx.message.channel)
                    if msg.content.lower() == 'y' and msg.author.id == ctx.guild.owner.id:
                        await msg.delete()
                        await sent.delete()
                        if '--silent' not in members:
                            emb = discord.Embed(description = 'Проверяем..', color = 0x2f3136)
                            sent = await ctx.send(embed = emb)
                            if '--bots' in members:
                                if filt == None:
                                    cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == True and m.pinned == False, before = sent)
                                else:
                                    cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.author.bot == True and m.pinned == False, before = sent)
                            elif '--users' in members:
                                if filt == None:
                                    cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False and m.pinned == False, before = sent)
                                else:
                                    cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False and m.content.lower() == filt.lower() and m.pinned == False, before = sent)
                            elif '--users' in members and '--bots' in members:
                                if filt == None:
                                    cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.pinned == False, before = sent)
                                else:
                                    cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.pinned == False, before = sent)
                            else:
                                if filt == None:
                                    cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.pinned == False, before = sent)
                                else:
                                    cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.pinned == False, before = sent)
                            try:
                                emb = discord.Embed(title = 'Результаты удаления сообщений', color = 0x2f3136)
                                emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{len(cleared)} / {amount}```')
                                if filt:
                                    emb.add_field(name = 'Применён фильтр:', value = f'```{filt} ({members})```', inline = True)
                                emb.add_field(name = 'Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                                emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c".')
                                await sent.edit(embed = emb)
                                msg = await self.client.wait_for('message', timeout = 10, check = lambda message: message.channel == ctx.message.channel and message.author == ctx.author and message.content.lower() == 'c')
                                emb = discord.Embed(title = 'Результаты удаления сообщений', color = 0x2f3136)
                                emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{len(cleared)} / {amount}```')
                                if filt:
                                    emb.add_field(name = 'Применён фильтр:', value = f'```{filt} ({members})```', inline = True)
                                emb.add_field(name = 'Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                                await sent.edit(embed = emb)
                            except asyncio.TimeoutError:
                                await sent.delete()
                        else:
                            if '--bots' in members:
                                if filt == None:
                                    await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == True and m.pinned == False)
                                else:
                                    await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.author.bot == True and m.pinned == False)
                            elif '--users' in members:
                                if filt == None:
                                    await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False and m.pinned == False)
                                else:
                                    await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False and m.content.lower() == filt.lower() and m.pinned == False)
                            elif '--users' in members and '--bots' in members:
                                if filt == None:
                                    await ctx.channel.purge(limit = amount, check = lambda m: m.pinned == False)
                                else:
                                    await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.pinned == False)
                            elif '--everyone' in members:
                                if filt == None:
                                    await ctx.channel.purge(limit = amount, check = lambda m: m.pinned == False)
                                else:
                                    await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.pinned == False)
                            elif members == '--silent':
                                if filt == None:
                                    await ctx.channel.purge(limit = amount, check = lambda m: m.pinned == False)
                                else:
                                    await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.pinned == False)
                    elif msg.content.lower() == 'n' and msg.author.id == ctx.guild.owner.id:
                        await msg.delete()
                        await sent.delete()
                        emb = discord.Embed(description = f'{ctx.guild.owner.mention} отменил запрос.', color = 0x2f3136)
                        await ctx.send(embed = emb, delete_after = 3)
                    elif msg.content.lower() == 'n' or 'y' and msg.author.id != ctx.guild.owner.id:
                        await msg.delete()
                        await sent.delete()
                        emb = discord.Embed(description = f'{ctx.author.mention}, ты не являешься владельцем сервера.', color = 0x2f3136)
                        await ctx.send(embed = emb, delete_after = 3)
                    else:
                        await msg.delete()
                        await sent.delete()
                        emb = discord.Embed(description = f'Недопустимый ответ - {msg.content}', color = 0x2f3136)
                        await ctx.send(embed = emb, delete_after = 3)
                except asyncio.TimeoutError:
                    await sent.delete()
                    emb = discord.Embed(description = f'{ctx.author.mention}, Время вышло.', color = 0x2f3136)
                    await ctx.send(f'{ctx.guild.owner.mention}', embed = emb, delete_after = 3)
        elif amount >= 100:
            if ctx.author != ctx.guild.owner:
                emb = discord.Embed(description = f'{ctx.author.mention}, создан запрос на удаление {amount} сообщений. Мне нужен ответ создателя сервера на это действие. Продолжаем? (y/n)\n||Запрос будет отменён через 1 минуту.||', color = 0x2f3136)
                sent = await ctx.send(f'{ctx.guild.owner.mention}', embed = emb)
                try:
                    msg = await self.client.wait_for('message', timeout = 10, check = lambda message: message.author == ctx.author and message.channel == ctx.message.channel)
                    if msg.content.lower() == 'y':
                        await msg.delete()
                        await sent.delete()
                        if '--silent' not in members:
                            emb = discord.Embed(description = 'Проверяем..', color = 0x2f3136)
                            sent = await ctx.send(embed = emb)
                            if '--bots' in members:
                                if filt == None:
                                    cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == True and m.pinned == False, before = sent)
                                else:
                                    cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.author.bot == True and m.pinned == False, before = sent)
                            elif '--users' in members:
                                if filt == None:
                                    cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False and m.pinned == False, before = sent)
                                else:
                                    cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False and m.content.lower() == filt.lower() and m.pinned == False, before = sent)
                            elif '--users' in members and '--bots' in members:
                                if filt == None:
                                    cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.pinned == False, before = sent)
                                else:
                                    cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.pinned == False, before = sent)
                            else:
                                if filt == None:
                                    cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.pinned == False, before = sent)
                                else:
                                    cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.pinned == False, before = sent)
                            try:
                                emb = discord.Embed(title = 'Результаты удаления сообщений', color = 0x2f3136)
                                emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{len(cleared)} / {amount}```')
                                if filt:
                                    emb.add_field(name = 'Применён фильтр:', value = f'```{filt} ({members})```', inline = True)
                                emb.add_field(name = 'Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                                emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c".')
                                await sent.edit(embed = emb)
                                msg = await self.client.wait_for('message', timeout = 10, check = lambda message: message.channel == ctx.message.channel and message.author == ctx.author and message.content.lower() == 'c')
                                emb = discord.Embed(title = 'Результаты удаления сообщений', color = 0x2f3136)
                                emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{len(cleared)} / {amount}```')
                                if filt:
                                    emb.add_field(name = 'Применён фильтр:', value = f'```{filt} ({members})```', inline = True)
                                emb.add_field(name = 'Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                                await sent.edit(embed = emb)
                            except asyncio.TimeoutError:
                                await sent.delete()
                        else:
                            if '--bots' in members:
                                if filt == None:
                                    await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == True and m.pinned == False)
                                else:
                                    await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.author.bot == True and m.pinned == False)
                            elif '--users' in members:
                                if filt == None:
                                    await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False and m.pinned == False)
                                else:
                                    await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False and m.content.lower() == filt.lower() and m.pinned == False)
                            elif '--users' in members and '--bots' in members:
                                if filt == None:
                                    await ctx.channel.purge(limit = amount, check = lambda m: m.pinned == False)
                                else:
                                    await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.pinned == False)
                            elif '--everyone' in members:
                                if filt == None:
                                    await ctx.channel.purge(limit = amount, check = lambda m: m.pinned == False)
                                else:
                                    await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.pinned == False)
                            elif members == '--silent':
                                if filt == None:
                                    await ctx.channel.purge(limit = amount, check = lambda m: m.pinned == False)
                                else:
                                    await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.pinned == False)
                    elif msg.content.lower() == 'n' and msg.author.id == ctx.guild.owner.id:
                        await msg.delete()
                        await sent.delete()
                        emb = discord.Embed(description = f'{ctx.guild.owner} отменил запрос.', color = 0x2f3136)
                        await ctx.send(embed = emb, delete_after = 3)
                    elif msg.content.lower() == 'n' or msg.content.lower() == 'y' and msg.author.id != ctx.guild.owner.id:
                        await msg.delete()
                        await sent.delete()
                        emb = discord.Embed(description = f'{ctx.author.mention}, ты не являешься владельцем сервера.', color = 0x2f3136)
                        await ctx.send(embed = emb, delete_after = 3)
                    else:
                        await msg.delete()
                        await sent.delete()
                        emb = discord.Embed(description = f'Недопустимый ответ - {msg.content}', color = 0x2f3136)
                        await ctx.send(embed = emb, delete_after = 3)
                except asyncio.TimeoutError:
                    await sent.delete()
                    emb = discord.Embed(description = f'{ctx.author.mention}, Время вышло.', color = 0x2f3136)
                    await ctx.send(f'{ctx.guild.owner.mention}', embed = emb, delete_after = 3)
            else:
                emb = discord.Embed(description = f'{ctx.author.mention}, создан запрос на удаление {amount} сообщений. Продолжить? (y/n)\n||Запрос будет отменён через 10 секунд.||', color = 0x2f3136)
                sent = await ctx.send(embed = emb)
                try:
                    msg = await self.client.wait_for('message', timeout = 10, check = lambda message: message.author == ctx.author and message.channel == ctx.message.channel)
                    if msg.content.lower() == 'y':
                        await msg.delete()
                        await sent.delete()
                        if '--silent' not in members:
                            emb = discord.Embed(description = 'Проверяем..', color = 0x2f3136)
                            sent = await ctx.send(embed = emb)
                            if '--bots' in members:
                                if filt == None:
                                    cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == True and m.pinned == False, before = sent)
                                else:
                                    cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.author.bot == True and m.pinned == False, before = sent)
                            elif '--users' in members:
                                if filt == None:
                                    cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False and m.pinned == False, before = sent)
                                else:
                                    cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False and m.content.lower() == filt.lower() and m.pinned == False, before = sent)
                            elif '--users' in members and '--bots' in members:
                                if filt == None:
                                    cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.pinned == False, before = sent)
                                else:
                                    cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.pinned == False, before = sent)
                            else:
                                if filt == None:
                                    cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.pinned == False, before = sent)
                                else:
                                    cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.pinned == False, before = sent)
                            try:
                                emb = discord.Embed(title = 'Результаты удаления сообщений', color = 0x2f3136)
                                emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{len(cleared)} / {amount}```')
                                if filt:
                                    emb.add_field(name = 'Применён фильтр:', value = f'```{filt} ({members})```', inline = True)
                                emb.add_field(name = 'Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                                emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c".')
                                await sent.edit(embed = emb)
                                emb = discord.Embed(title = 'Результаты удаления сообщений', color = 0x2f3136)
                                emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{len(cleared)} / {amount}```')
                                if filt:
                                    emb.add_field(name = 'Применён фильтр:', value = f'```{filt} ({members})```', inline = True)
                                emb.add_field(name = 'Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                                emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c".')
                                await sent.edit(embed = emb)
                            except asyncio.TimeoutError:
                                await sent.delete()
                        else:
                            if '--bots' in members:
                                if filt == None:
                                    await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == True and m.pinned == False)
                                else:
                                    await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.author.bot == True and m.pinned == False)
                            elif '--users' in members:
                                if filt == None:
                                    await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False and m.pinned == False)
                                else:
                                    await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False and m.content.lower() == filt.lower() and m.pinned == False)
                            elif '--users' in members and '--bots' in members:
                                if filt == None:
                                    await ctx.channel.purge(limit = amount, check = lambda m: m.pinned == False)
                                else:
                                    await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.pinned == False)
                            elif '--everyone' in members:
                                if filt == None:
                                    await ctx.channel.purge(limit = amount, check = lambda m: m.pinned == False)
                                else:
                                    await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.pinned == False)
                            elif members == '--silent':
                                if filt == None:
                                    await ctx.channel.purge(limit = amount, check = lambda m: m.pinned == False)
                                else:
                                    await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.pinned == False)
                    elif msg.content.lower() == 'n':
                        await msg.delete()
                        await sent.delete()
                        emb = discord.Embed(description = 'Отменено.', color = 0x2f3136)
                        await ctx.send(embed = emb, delete_after = 3)
                    else:
                        await msg.delete()
                        await sent.delete()
                        emb = discord.Embed(description = f'Недопустимый ответ - {msg.content}', color = 0x2f3136)
                        await ctx.send(embed = emb, delete_after = 3)
                except asyncio.TimeoutError:
                    await sent.delete()
                    emb = discord.Embed(description = f'{ctx.author.mention}, Время вышло.', color = 0x2f3136)
                    await ctx.send(embed = emb, delete_after = 3)
        elif amount >= 10:
            emb = discord.Embed(description = f'{ctx.author.mention}, создан запрос на удаление {amount} сообщений. Продолжить? (y/n)\n||Запрос будет отменён через 10 секунд.||', color = 0x2f3136)
            sent = await ctx.send(embed = emb)
            try:
                msg = await self.client.wait_for('message', timeout = 10, check = lambda message: message.author == ctx.author and message.channel == ctx.message.channel)
                if msg.content.lower() == 'y':
                    await msg.delete()
                    await sent.delete()
                    if '--silent' not in members:
                        emb = discord.Embed(description = 'Проверяем..', color = 0x2f3136)
                        sent = await ctx.send(embed = emb)
                        if '--bots' in members:
                            if filt == None:
                                cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == True and m.pinned == False, before = sent)
                            else:
                                cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.author.bot == True and m.pinned == False, before = sent)
                        elif '--users' in members:
                            if filt == None:
                                cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False and m.pinned == False, before = sent)
                            else:
                                cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False and m.content.lower() == filt.lower() and m.pinned == False, before = sent)
                        elif '--users' in members and '--bots' in members:
                            if filt == None:
                                cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.pinned == False, before = sent)
                            else:
                                cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.pinned == False, before = sent)
                        else:
                            if filt == None:
                                cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.pinned == False, before = sent)
                            else:
                                cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.pinned == False, before = sent)
                        try:
                            emb = discord.Embed(title = 'Результаты удаления сообщений', color = 0x2f3136)
                            emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{len(cleared)} / {amount}```')
                            if filt:
                                emb.add_field(name = 'Применён фильтр:', value = f'```{filt} ({members})```', inline = True)
                            emb.add_field(name = 'Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                            emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c".')
                            await sent.edit(embed = emb)
                            msg = await self.client.wait_for('message', timeout = 10, check = lambda message: message.channel == ctx.message.channel and message.author == ctx.author and message.content.lower() == 'c')
                            emb = discord.Embed(title = 'Результаты удаления сообщений', color = 0x2f3136)
                            emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{len(cleared)} / {amount}```')
                            if filt:
                                emb.add_field(name = 'Применён фильтр:', value = f'```{filt} ({members})```', inline = True)
                            emb.add_field(name = 'Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                            await sent.edit(embed = emb)
                        except asyncio.TimeoutError:
                            await sent.delete()
                    else:
                        if '--bots' in members:
                            if filt == None:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == True and m.pinned == False)
                            else:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.author.bot == True and m.pinned == False)
                        elif '--users' in members:
                            if filt == None:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False and m.pinned == False)
                            else:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False and m.content.lower() == filt.lower() and m.pinned == False)
                        elif '--users' in members and '--bots' in members:
                            if filt == None:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.pinned == False)
                            else:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.pinned == False)
                        elif '--everyone' in members:
                            if filt == None:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.pinned == False)
                            else:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.pinned == False)
                        elif members == '--silent':
                            if filt == None:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.pinned == False)
                            else:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.pinned == False)
                elif msgtent.lower() == 'n':
                    await msg.delete()
                    await sent.delete()
                    emb = discord.Embed(description = 'Отменено.', color = 0x2f3136)
                    await ctx.send(embed = emb, delete_after = 3)
                else:
                    await msg.delete()
                    await sent.delete()
                    emb = discord.Embed(description = f'Недопустимый ответ - {msg.content}', color = 0x2f3136)
                    await ctx.send(embed = emb, delete_after = 3)
            except asyncio.TimeoutError:
                await sent.delete()
                emb = discord.Embed(description = f'{ctx.author.mention}, Время вышло.', color = 0x2f3136)
                await ctx.send(embed = emb, delete_after = 3)
        elif amount == 0:
            emb = discord.Embed(description = 'Удалять 0 сообщений? Ты еблан?', color = 0x2f3136)
            await ctx.send(embed = emb, delete_after = 1)
        else:
            if '--silent' not in members:
                emb = discord.Embed(description = 'Проверяем..', color = 0x2f3136)
                sent = await ctx.send(embed = emb)
                if '--bots' in members:
                    if filt == None:
                        cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == True and m.pinned == False, before = sent)
                    else:
                        cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.author.bot == True and m.pinned == False, before = sent)
                elif '--users' in members:
                    if filt == None:
                        cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False and m.pinned == False, before = sent)
                    else:
                        cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False and m.content.lower() == filt.lower() and m.pinned == False, before = sent)
                elif '--users' in members and '--bots' in members:
                    if filt == None:
                        cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.pinned == False, before = sent)
                    else:
                        cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.pinned == False, before = sent)
                else:
                    if filt == None:
                        cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.pinned == False, before = sent)
                    else:
                        cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.pinned == False, before = sent)
                try:
                    emb = discord.Embed(title = 'Результаты удаления сообщений', color = 0x2f3136)
                    emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{len(cleared)} / {amount}```')
                    if filt:
                        emb.add_field(name = 'Применён фильтр:', value = f'```{filt} ({members})```', inline = True)
                    emb.add_field(name = 'Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                    emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c".')
                    await sent.edit(embed = emb)
                    msg = await self.client.wait_for('message', timeout = 10, check = lambda message: message.channel == ctx.message.channel and message.author == ctx.author and message.content.lower() == 'c')
                    emb = discord.Embed(title = 'Результаты удаления сообщений', color = 0x2f3136)
                    emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{len(cleared)} / {amount}```')
                    if filt:
                        emb.add_field(name = 'Применён фильтр:', value = f'```{filt} ({members})```', inline = True)
                    emb.add_field(name = 'Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                    await sent.edit(embed = emb)
                except asyncio.TimeoutError:
                    await sent.delete()
            else:
                if '--bots' in members:
                    if filt == None:
                        await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == True and m.pinned == False)
                    else:
                        await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.author.bot == True and m.pinned == False)
                elif '--users' in members:
                    if filt == None:
                        await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False and m.pinned == False)
                    else:
                        await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False and m.content.lower() == filt.lower() and m.pinned == False)
                elif '--users' in members and '--bots' in members:
                    if filt == None:
                        await ctx.channel.purge(limit = amount, check = lambda m: m.pinned == False)
                    else:
                        await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.pinned == False)
                elif '--everyone' in members:
                    if filt == None:
                        await ctx.channel.purge(limit = amount, check = lambda m: m.pinned == False)
                    else:
                        await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.pinned == False)
                elif members == '--silent':
                    if filt == None:
                        await ctx.channel.purge(limit = amount, check = lambda m: m.pinned == False)
                    else:
                        await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.pinned == False)

async def setup(client):
    await client.add_cog(Mod(client))
