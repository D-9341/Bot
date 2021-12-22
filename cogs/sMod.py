import datetime
import os
import re
import asyncio

import disnake
from disnake.ext import commands
from pymongo import MongoClient

passw = os.environ.get('passw')
cluster = MongoClient(f"mongodb+srv://cephalon:{passw}@locale.ttokw.mongodb.net/Locale?retryWrites=true&w=majority")
collection = cluster.Locale.locale

friends = [351071668241956865, 417362845303439360]

guilds = [693929822543675455, 735874149578440855, 818758712163827723]

class sMod(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Группа Slash-команд Mod загружена')

    @commands.slash_command(name = 'dm', description = 'Пишет в лс человеку от имени бота написанный вами текст')
    @commands.has_permissions(view_audit_log = True)
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def _dm(self, ctx, member: disnake.User, *, text):
        '''        
        Parameters
        ----------
        member: :class: `disnake.Member`
            Участник
        text: :class: `str`
            Текст для отправки
        '''
        emb = disnake.Embed(description = f'{text}', colour = 0x2f3136)
        emb.set_author(name = ctx.author, icon_url = ctx.author.avatar.url)
        await member.send(embed = emb)
        rlocale = collection.find_one({"_id": ctx.author.id})["locale"]
        if rlocale == 'ru':
            await ctx.send('Сообщение отправлено.')
        if rlocale == 'gnida':
            await ctx.send('Твоя хуйня отправлена')

    @commands.slash_command(name = 'kick', description = 'Выгоняет участника с сервера')
    @commands.has_permissions(kick_members = True)
    async def _kick(self, ctx, member: disnake.Member, *, reason = None):
        '''        
        Parameters
        ----------
        member: :class: `disnake.Member`
            Участник
        reason: :class: `str`
            Причина
        '''
        rlocale = collection.find_one({"_id": ctx.author.id})["locale"]
        bot = disnake.utils.get(ctx.guild.members, id = self.client.user.id)
        if member.id != 338714886001524737:
            if reason == None:
                if rlocale == 'ru':
                    reason = 'Не указана.'
                if rlocale == 'gnida':
                    reason = 'Я не ебу'
            if ctx.author.top_role == member.top_role:
                if rlocale == 'ru':
                    emb = disnake.Embed(description = f'{ctx.author.mention}, ваша высшая роль равна высшей роли {member.mention}. Кик отклонён.', colour = 0x2f3136)
                    await ctx.send(embed = emb)
                if rlocale == 'gnida':
                    emb = disnake.Embed(description = f'Твоя высшая роль равна высшей роли {member.mention}. Пошёл нахуй.', colour = 0x2f3136)
                    await ctx.send(embed = emb)
            elif member.top_role > ctx.author.top_role:
                if rlocale == 'ru':
                    emb = disnake.Embed(description = f'{ctx.author.mention}, ваша высшая роль ниже высшей роли {member.mention}. Кик отклонён.', colour = 0x2f3136)
                    await ctx.send(embed = emb)
                if rlocale == 'gnida':
                    emb = disnake.Embed(description = f'Твоя высшая роль ниже высшей роли {member.mention}. Пошёл нахуй.', colour = 0x2f3136)
                    await ctx.send(embed = emb)
            elif member.top_role > bot.top_role:
                if rlocale == 'ru':
                    emb = disnake.Embed(description = f'МОЯ высшая роль ниже высшей роли {member.mention}. Кик невозможен.', color = 0x2f3136)
                    await ctx.send(embed = emb)
                if rlocale == 'gnida':
                    emb = disnake.Embed(description = f'МОЯ высшая роль ниже высшей роли {member.mention}. Сука.', color = 0x2f3136)
                    await ctx.send(embed = emb)
            elif member.top_role == bot.top_role:
                if rlocale == 'ru':
                    emb = disnake.Embed(description = f'МОЯ высшая роль идентична высшей роли {member.mention}. Кик невозможен.', color = 0x2f3136)
                    await ctx.send(embed = emb)
                if rlocale == 'gnida':
                    emb = disnake.Embed(description = f'МОЯ высшая роль идентична высшей роли {member.mention}. Сука.', color = 0x2f3136)
                    await ctx.send(embed = emb)
            else:
                emb = disnake.Embed(colour = 0x2f3136)
                emb.set_author(name = ctx.author, icon_url = ctx.author.avatar.url)
                emb.add_field(name = 'Был кикнут', value = member.mention)
                emb.add_field(name = 'По причине', value = reason)
                await ctx.send(embed = emb)
                await member.kick(reason = reason)
        else:
            if rlocale == 'ru':
                emb = disnake.Embed(description = f'Извините, {ctx.author.mention}, но вы не можете кикнуть моего создателя!', colour = 0x2f3136)
                await ctx.send(embed = emb)
            if rlocale == 'gnida':
                emb = disnake.Embed(description = 'Ого! Пошёл нахуй!', colour = 0x2f3136)
                await ctx.send(embed = emb)

    @commands.slash_command(name = 'ban', description = 'Банит участника')
    async def _ban(self, ctx, member: disnake.Member, *, reason = None):
        '''        
        Parameters
        ----------
        member: :class: `disnake.Member`
            Участник
        reason: :class: `str`
            Причина и/или указание --soft --reason
        '''
        rlocale = collection.find_one({"_id": ctx.author.id})["locale"]
        bot = disnake.utils.get(ctx.guild.members, id = self.client.user.id)
        if member.id != 338714886001524737:
            if reason == None:
                if rlocale == 'ru':
                    reason = 'Не указана.'
                if rlocale == 'gnida':
                    reason = 'Я не ебу'
            if ctx.author.top_role == member.top_role:
                if rlocale == 'ru':
                    emb = disnake.Embed(description = f'{ctx.author.mention}, ваша высшая роль равна высшей роли {member.mention}. Бан отклонён.', colour = 0x2f3136)
                    await ctx.send(embed = emb)
                if rlocale == 'gnida':
                    emb = disnake.Embed(description = f'Твоя высшая роль равна высшей роли {member.mention}. Саси.', colour = 0x2f3136)
                    await ctx.send(embed = emb)
            elif member.top_role > ctx.author.top_role:
                if rlocale == 'ru':
                    emb = disnake.Embed(description = f'{ctx.author.mention}, ваша высшая роль ниже высшей роли {member.mention}. Бан отклонён.', colour = 0x2f3136)
                    await ctx.send(embed = emb)
                if rlocale == 'gnida':
                    emb = disnake.Embed(description = f'Твоя высшая роль ниже высшей роли {member.mention}. Саси.', colour = 0x2f3136)
                    await ctx.send(embed = emb)
            elif member.top_role > bot.top_role:
                if rlocale == 'ru':
                    emb = disnake.Embed(description = f'МОЯ высшая роль ниже высшей роли {member.mention}. Бан невозможен.', color = 0x2f3136)
                    await ctx.send(embed = emb)
                if rlocale == 'gnida':
                    emb = disnake.Embed(description = f'МОЯ высшая роль ниже высшей роли {member.mention}. Блять.', color = 0x2f3136)
                    await ctx.send(embed = emb)
            elif member.top_role == bot.top_role:
                if rlocale == 'ru':
                    emb = disnake.Embed(description = f'МОЯ высшая роль идентична высшей роли {member.mention}. Бан невозможен.', color = 0x2f3136)
                    await ctx.send(embed = emb)
                if rlocale == 'gnida':
                    emb = disnake.Embed(description = f'МОЯ высшая роль идентична высшей роли {member.mention}. Блять.', color = 0x2f3136)
                    await ctx.send(embed = emb)
            else:
                if '--soft' in reason:
                    emb = disnake.Embed(color = 0x2f3136)
                    emb.set_author(name = ctx.author, icon_url = ctx.author.avatar.url)
                    emb.add_field(name = 'Упрощённо забанен', value = f'{member.mention} ({member.name})')
                    if '--reason' in reason:
                        reason = reason.strip()[15:].strip()
                    else:
                        if rlocale == 'ru':
                            reason = 'Не указана.'
                        if rlocale == 'gnida':
                            reason == 'Я не ебу'
                    emb.add_field(name = 'По причине', value = reason)
                    await ctx.send(embed = emb)
                    await member.ban(reason = reason)
                    await member.unban(reason = '--softban')
                else:
                    emb = disnake.Embed(colour = 0x2f3136)
                    emb.set_author(name = ctx.author, icon_url = ctx.author.avatar.url)
                    emb.add_field(name = 'Был забанен', value = member.mention)
                    emb.add_field(name = 'По причине', value = reason)
                    await ctx.send(embed = emb)
                    await member.ban(reason = reason)
        else:
            if rlocale == 'ru':
                emb = disnake.Embed(description = f'Извините, {ctx.author.mention}, но вы не можете забанить моего создателя!', colour = 0x2f3136)
                await ctx.send(embed = emb)
            if rlocale == 'gnida':
                emb = disnake.Embed(description = 'А ты не прихуел даже ПЫТАТЬСЯ это сделать?!', colour = 0x2f3136)
                await ctx.send(embed = emb)

    @commands.slash_command(name = 'give', description = 'Выдаёт участнику роль')
    async def _give(self, ctx, member: disnake.Member, *, role: disnake.Role):
        '''        
        Parameters
        ----------
        member: :class: `disnake.Member`
            Участник
        role: :class: `disnake.Role`
            Роль
        '''
        rlocale = collection.find_one({"_id": ctx.author.id})["locale"]
        if role.name == 'Muted':
            if member.id != self.client.owner_id:
                await member.add_roles(role)
                if rlocale == 'ru':
                    emb = disnake.Embed(description = f'{member.mention} был перманентно заглушён {ctx.author.mention}', color = 0x2f3136)
                    return await ctx.send(embed = emb)
                if rlocale == 'gnida':
                    emb = disnake.Embed(description = f'{member.mention} получает мут в ебало от {ctx.author.mention}', color = 0x2f3136)
                    return await ctx.send(embed = emb)
            else:
                emb = disnake.Embed(description = 'Ты думал мой Создатель тебе по зубам? ОН!?', color = 0x2f3136)
                return await ctx.send(embed = emb)
        if role > ctx.author.top_role:
            if rlocale == 'ru':
                emb = disnake.Embed(description = f'Вы не можете выдать {role.mention}, так как она имеет более высокий ранг, чем ваша высшая роль.', color = 0x2f3136)
                await ctx.send(embed = emb)
            if rlocale == 'gnida':
                emb = disnake.Embed(description = f'Дебилам вроде тебя запрещено выдавать {role.mention}, так как эта роль выше твоей высшей роли.', color = 0x2f3136)
                await ctx.send(embed = emb)
        elif role == ctx.author.top_role:
            if rlocale == 'ru':
                emb = disnake.Embed(description = f'Вы не можете выдать {role.mention} кому-либо, так как она равна вашей высшей роли.', color = 0x2f3136)
                await ctx.send(embed = emb)
            if rlocale == 'gnida':
                emb = disnake.Embed(description = f'Дебилам вроде тебя запрещено выдавать {role.mention}, так как она равна твоей высшей роли.', color = 0x2f3136)
                await ctx.send(embed = emb)
        else:
            await member.add_roles(role)
            emb = disnake.Embed(colour = 0x2f3136, timestamp = disnake.utils.utcnow())
            emb.add_field(name = 'ВЫДАНА_РОЛЬ', value = f'{role.mention} | {role.name} | ID {role.id}')
            emb.add_field(name = 'ВЫДАНА:', value = member.mention, inline = False)
            emb.set_author(name = ctx.author, icon_url = ctx.author.avatar.url)
            await ctx.send(embed = emb)

    @commands.slash_command(name = 'take', description = 'Забирает роль у участника')
    @commands.has_permissions(manage_channels = True)
    async def _take(self, ctx, member: disnake.Member, *, role: disnake.Role):
        '''        
        Parameters
        ----------
        member: :class: `disnake.Member`
            Участник
        role: :class: `disnake.Role`
            Роль
        '''
        if role != None:
            bot = ctx.guild.get_member(self.client.user.id)
            if role > member.top_role:
                emb = disnake.Embed(description = f'Вы не можете забрать {role.mention}, так как она имеет более высокий ранг, чем ваша высшая роль. Забирание роли отменено.', color = 0x2f3136)
                await ctx.send(embed = emb)
            elif role == ctx.author.top_role:
                emb = disnake.Embed(description = f'Вы не можете забрать {role.mention}, так как она равна вашей высшей роли. Забирание роли отменено.', color = 0x2f3136)
                await ctx.send(embed = emb)
            elif member.top_role > bot.top_role:
                emb = disnake.Embed(description = f'МОЯ высшая роль ниже высшей роли {member.mention}. Забрать роль невозможно.', color = 0x2f3136)
                await ctx.send(embed = emb)
            elif member.top_role == bot.top_role:
                emb = disnake.Embed(description = f'МОЯ высшая роль идентична высшей роли {member.mention}. Забрать роль невозможно.', color = 0x2f3136)
                await ctx.send(embed = emb)
            elif role.is_default():
                emb = disnake.Embed(description = 'Забирать @everyone?', color = 0x2f3136)
                await ctx.send(embed = emb)
            else:
                await member.remove_roles(role)
                emb = disnake.Embed(colour = 0x2f3136, timestamp = disnake.utils.utcnow())
                emb.add_field(name = 'ЗАБРАНА_РОЛЬ', value = f'{role.mention} | {role.name} | ID {role.id}')
                emb.add_field(name = 'ЗАБРАНА_У:', value = member.mention, inline = False)
                emb.set_author(name = ctx.author, icon_url = ctx.author.avatar.url)
                await ctx.send(embed = emb)
        else:
            emb = disnake.Embed(description = f'{ctx.author.mention}, я не могу найти {role.mention} в списке ролей.', colour = 0x2f3136, timestamp = disnake.utils.utcnow())
            await ctx.send(embed = emb)

    @commands.slash_command(name = 'unmute', description = 'Отменяет заглушение участника')
    @commands.has_permissions(manage_channels = True)
    async def _unmute(self, ctx, member: disnake.Member, *, reason = None):
        '''        
        Parameters
        ----------
        member: :class: `disnake.Member`
            Участник
        reason: :class: `str`
            Причина
        '''
        role = disnake.utils.get(ctx.guild.roles, name = 'Muted')
        if role != None:
            if role in member.roles:
                await member.remove_roles(role)
                if reason == None:
                    reason = 'Не указана.'
                emb = disnake.Embed(title = f'Принудительное снятие заглушения у {member}', colour = 0x2f3136, timestamp = disnake.utils.utcnow())
                emb.add_field(name = 'Снял мут', value = ctx.author.mention)
                emb.add_field(name = 'По причине', value = reason)
                await ctx.send(embed = emb)
            else:
                emb = disnake.Embed(description = 'Снятие заглушения не требуется. Роли Muted не обнаружено в списке ролей участника.', colour = 0x2f3136)
                await ctx.send(embed = emb)
        else:
            emb = disnake.Embed(description = f'{ctx.author.mention}, Я не могу снять заглушение у {member.mention} из-за того, что роль Muted была удалена', colour = 0x2f3136, timestamp = disnake.utils.utcnow())
            await ctx.send(embed = emb)

    @commands.slash_command(name = 'clear', description = 'Очищает канал от указанного количества сообщений. Не работает, если в канале нет сообщений.')
    @commands.has_permissions(administrator = True)
    async def _clear(self, ctx, amount: int, members: str = commands.Param(choices = {"Удалить сообщения ото всех": "--everyone", "Удалить сообщения только от ботов": "--bots", "Удалить сообщения только от людей": "--users"}), *, filt = None):
        '''        
        Parameters
        ----------
        amount: :class: `int`
            Количество сообщений для удаления
        member: :class: `str`
            Указание диапазона удаления сообщений
        filt: :class: `str`
            Удаляет сообщение с заданным словом/словосочетанием
        '''
        authors = {}
        if not '--silent' in members:
            async for message in ctx.channel.history(limit = amount):
                if message.author not in authors:
                    authors[message.author] = 1
                else:
                    authors[message.author] += 1
        if amount == 2472:
            if ctx.author.id == self.client.owner_id:
                await ctx.channel.delete()
                emb = disnake.Embed(description = f'канал `{ctx.channel.name}` удалён.', color = 0x2f3136)
                await ctx.author.send(embed = emb)
            else:
                await ctx.author.send('Как ты узнал об этом?!')
        elif amount >= 300:
            emb = disnake.Embed(description = f'{ctx.author.mention}, при таком числе удаления сообщений ({amount}) возможно большое время ожидания ответа {self.client.user.mention}.', colour = 0x2f3136)
            await ctx.send(f'{ctx.guild.owner.mention}', embed = emb)
        elif amount >= 250:
            if ctx.author != ctx.guild.owner:
                emb = disnake.Embed(description = f'{ctx.author.mention}, операция с данным числом ({amount}) доступна только {ctx.guild.owner.mention}.', colour = 0x2f3136)
                await ctx.send(f'{ctx.guild.owner.mention}', embed = emb, delete_after = 5)
            else:
                emb = disnake.Embed(description = f'{ctx.author.mention}, обнаружено слишком большое число для удаления сообщений ({amount}). Возможны дальнейшие ошибки в работе {self.client.user.mention}. Продолжить? (y/n)\n||Отмена через 10 секунд.||', colour = 0x2f3136)
                sent = await ctx.send(embed = emb)
                try:
                    msg = await self.client.wait_for('message', timeout = 10, check = lambda message: message.channel == ctx.message.channel)
                    if msg.content.lower() == 'y' and msg.author.id == ctx.guild.owner.id:
                        await msg.delete()
                        await sent.delete()
                        if '--silent' not in members:
                            emb = disnake.Embed(description = 'Проверяем..', color = 0x2f3136)
                            sent = await ctx.send(embed = emb)
                            if members == '--bots':
                                if filt == None:
                                    cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == True, before = sent)
                                else:
                                    cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.author.bot == True, before = sent)
                                emb = disnake.Embed(title = 'Результаты удаления сообщений', color = 0x2f3136)
                                emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{len(cleared)}```')
                                if filt:
                                    emb.add_field(name = 'Применён фильтр:', value = f'```{filt}``` ({members})', inline = True)
                                emb.add_field(name = 'Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                                emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c".')
                                await sent.edit(embed = emb)
                            elif members == '--users':
                                if filt == None:
                                    cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False, before = sent)
                                else:
                                    cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False and m.content.lower() == filt.lower(), before = sent)
                                emb = disnake.Embed(title = 'Результаты удаления сообщений', color = 0x2f3136)
                                emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{len(cleared)}```')
                                if filt:
                                    emb.add_field(name = 'Применён фильтр:', value = f'```{filt}``` ({members})', inline = True)
                                emb.add_field(name = 'Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                                emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c".')
                                await sent.edit(embed = emb)
                            else:
                                if filt == None:
                                    cleared = await ctx.channel.purge(limit = amount, before = sent)
                                else:
                                    cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower(), before = sent)
                                emb = disnake.Embed(title = 'Результаты удаления сообщений', color = 0x2f3136)
                                emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{len(cleared)}```')
                                if filt:
                                    emb.add_field(name = 'Применён фильтр:', value = f'```{filt}``` ({members})', inline = True)
                                emb.add_field(name = 'Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                                emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c".')
                                await sent.edit(embed = emb)
                            try:
                                if '--silent' in members:
                                    return
                                msg = await self.client.wait_for('message', timeout = 10, check = lambda message: message.channel == ctx.message.channel and message.author == ctx.author and message.content.lower() == 'c')
                                emb = disnake.Embed(title = 'Результаты удаления сообщений', color = 0x2f3136)
                                emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{len(cleared)}```')
                                if filt:
                                    emb.add_field(name = 'Применён фильтр:', value = f'```{filt}``` ({members})', inline = True)
                                emb.add_field(name = 'Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                                await sent.edit(embed = emb)
                            except asyncio.TimeoutError:
                                await sent.delete()
                        else:
                            if '--bots' in members:
                                if filt == None:
                                    await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == True)
                                else:
                                    await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.author.bot == True)
                            elif '--users' in members:
                                if filt == None:
                                    await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False)
                                else:
                                    await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False and m.content.lower() == filt.lower())
                            elif '--everyone' in members:
                                if filt == None:
                                    await ctx.channel.purge(limit = amount)
                                else:
                                    await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower())
                            elif members == '--silent':
                                if filt == None:
                                    await ctx.channel.purge(limit = amount)
                                else:
                                    await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower())
                    elif msg.content.lower() == 'n' and msg.author.id == ctx.guild.owner.id:
                        await msg.delete()
                        await sent.delete()
                        emb = disnake.Embed(description = f'{ctx.guild.owner.mention} отменил запрос.', colour = 0x2f3136)
                        await ctx.send(embed = emb, delete_after = 3)
                    elif msg.content.lower() == 'n' or 'y' and msg.author.id != ctx.guild.owner.id:
                        await msg.delete()
                        await sent.delete()
                        emb = disnake.Embed(description = f'{ctx.author.mention}, ты не являешься владельцем сервера.', colour = 0x2f3136)
                        await ctx.send(embed = emb, delete_after = 3)
                    else:
                        await msg.delete()
                        await sent.delete()
                        emb = disnake.Embed(description = f'Обнаружен недопустимый ответ ({msg.content})', colour = 0x2f3136)
                        await ctx.send(embed = emb, delete_after = 3)
                except asyncio.TimeoutError:
                    await sent.delete()
                    emb = disnake.Embed(description = f'{ctx.author.mention}, Время вышло.', colour = 0x2f3136)
                    await ctx.send(f'{ctx.guild.owner.mention}', embed = emb, delete_after = 3)
        elif amount >= 100:
            if ctx.author != ctx.guild.owner:
                emb = disnake.Embed(description = f'{ctx.author.mention}, создан запрос на удаление {amount} сообщений. Мне нужен ответ создателя сервера на это действие. Продолжаем? (y/n)\n||Запрос будет отменён через 1 минуту.||', colour = 0x2f3136)
                sent = await ctx.send(f'{ctx.guild.owner.mention}', embed = emb)
                try:
                    msg = await self.client.wait_for('message', timeout = 10, check = lambda message: message.author == ctx.author and message.channel == ctx.message.channel)
                    if msg.content.lower() == 'y':
                        await msg.delete()
                        await sent.delete()
                        if '--silent' not in members:
                            emb = disnake.Embed(description = 'Проверяем..', color = 0x2f3136)
                            sent = await ctx.send(embed = emb)
                            if members == '--bots':
                                if filt == None:
                                    cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == True, before = sent)
                                else:
                                    cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.author.bot == True, before = sent)
                                emb = disnake.Embed(title = 'Результаты удаления сообщений', color = 0x2f3136)
                                emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{len(cleared)}```')
                                if filt:
                                    emb.add_field(name = 'Применён фильтр:', value = f'```{filt}``` ({members})', inline = True)
                                emb.add_field(name = 'Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                                emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c".')
                                await sent.edit(embed = emb)
                            elif members == '--users':
                                if filt == None:
                                    cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False, before = sent)
                                else:
                                    cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False and m.content.lower() == filt.lower(), before = sent)
                                emb = disnake.Embed(title = 'Результаты удаления сообщений', color = 0x2f3136)
                                emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{len(cleared)}```')
                                if filt:
                                    emb.add_field(name = 'Применён фильтр:', value = f'```{filt}``` ({members})', inline = True)
                                emb.add_field(name = 'Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                                emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c".')
                                await sent.edit(embed = emb)
                            else:
                                if filt == None:
                                    cleared = await ctx.channel.purge(limit = amount, before = sent)
                                else:
                                    cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower(), before = sent)
                                emb = disnake.Embed(title = 'Результаты удаления сообщений', color = 0x2f3136)
                                emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{len(cleared)}```')
                                if filt:
                                    emb.add_field(name = 'Применён фильтр:', value = f'```{filt}``` ({members})', inline = True)
                                emb.add_field(name = 'Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                                emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c".')
                                await sent.edit(embed = emb)
                            try:
                                if '--silent' in members:
                                    return
                                msg = await self.client.wait_for('message', timeout = 10, check = lambda message: message.channel == ctx.message.channel and message.author == ctx.author and message.content.lower() == 'c')
                                emb = disnake.Embed(title = 'Результаты удаления сообщений', color = 0x2f3136)
                                emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{len(cleared)}```')
                                if filt:
                                    emb.add_field(name = 'Применён фильтр:', value = f'```{filt}``` ({members})', inline = True)
                                emb.add_field(name = 'Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                                await sent.edit(embed = emb)
                            except asyncio.TimeoutError:
                                await sent.delete()
                        else:
                            if '--bots' in members:
                                if filt == None:
                                    await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == True)
                                else:
                                    await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.author.bot == True)
                            elif '--users' in members:
                                if filt == None:
                                    await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False)
                                else:
                                    await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False and m.content.lower() == filt.lower())
                            elif '--everyone' in members:
                                if filt == None:
                                    await ctx.channel.purge(limit = amount)
                                else:
                                    await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower())
                            elif members == '--silent':
                                if filt == None:
                                    await ctx.channel.purge(limit = amount)
                                else:
                                    await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower())
                    elif msg.content.lower() == 'n' and msg.author.id == ctx.guild.owner.id:
                        await msg.delete()
                        await sent.delete()
                        emb = disnake.Embed(description = f'{ctx.guild.owner} отменил запрос.', colour = 0x2f3136)
                        await ctx.send(embed = emb, delete_after = 3)
                    elif msg.content.lower() == 'n' or 'y' and msg.author.id != ctx.guild.owner.id:
                        await msg.delete()
                        await sent.delete()
                        emb = disnake.Embed(description = f'{ctx.author.mention}, ты не являешься владельцем сервера.', colour = 0x2f3136)
                        await ctx.send(embed = emb, delete_after = 3)
                    else:
                        await msg.delete()
                        await sent.delete()
                        emb = disnake.Embed(description = f'Обнаружен недопустимый ответ ({msg.content})', colour = 0x2f3136)
                        await ctx.send(embed = emb, delete_after = 3)
                except asyncio.TimeoutError:
                    await sent.delete()
                    emb = disnake.Embed(description = f'{ctx.author.mention}, Время вышло.', colour = 0x2f3136)
                    await ctx.send(f'{ctx.guild.owner.mention}', embed = emb, delete_after = 3)
            else:
                emb = disnake.Embed(description = f'{ctx.author.mention}, создан запрос на удаление {amount} сообщений. Продолжить? (y/n)\n||Запрос будет отменён через 10 секунд.||', colour = 0x2f3136)
                sent = await ctx.send(embed = emb)
                try:
                    msg = await self.client.wait_for('message', timeout = 10, check = lambda message: message.author == ctx.author and message.channel == ctx.message.channel)
                    if msg.content.lower() == 'y':
                        await msg.delete()
                        await sent.delete()
                        if '--silent' not in members:
                            emb = disnake.Embed(description = 'Проверяем..', color = 0x2f3136)
                            sent = await ctx.send(embed = emb)
                            if members == '--bots':
                                if filt == None:
                                    cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == True, before = sent)
                                else:
                                    cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.author.bot == True, before = sent)
                                emb = disnake.Embed(title = 'Результаты удаления сообщений', color = 0x2f3136)
                                emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{len(cleared)}```')
                                if filt:
                                    emb.add_field(name = 'Применён фильтр:', value = f'```{filt}``` ({members})', inline = True)
                                emb.add_field(name = 'Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                                emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c".')
                                await sent.edit(embed = emb)
                            elif members == '--users':
                                if filt == None:
                                    cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False, before = sent)
                                else:
                                    cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False and m.content.lower() == filt.lower(), before = sent)
                                emb = disnake.Embed(title = 'Результаты удаления сообщений', color = 0x2f3136)
                                emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{len(cleared)}```')
                                if filt:
                                    emb.add_field(name = 'Применён фильтр:', value = f'```{filt}``` ({members})', inline = True)
                                emb.add_field(name = 'Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                                emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c".')
                                await sent.edit(embed = emb)
                            else:
                                if filt == None:
                                    cleared = await ctx.channel.purge(limit = amount, before = sent)
                                else:
                                    cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower(), before = sent)
                                emb = disnake.Embed(title = 'Результаты удаления сообщений', color = 0x2f3136)
                                emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{len(cleared)}```')
                                if filt:
                                    emb.add_field(name = 'Применён фильтр:', value = f'```{filt}``` ({members})', inline = True)
                                emb.add_field(name = 'Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                                emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c".')
                                await sent.edit(embed = emb)
                            try:
                                if '--silent' in members:
                                    return
                                msg = await self.client.wait_for('message', timeout = 10, check = lambda message: message.channel == ctx.message.channel and message.author == ctx.author and message.content.lower() == 'c')
                                emb = disnake.Embed(title = 'Результаты удаления сообщений', color = 0x2f3136)
                                emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{len(cleared)}```')
                                if filt:
                                    emb.add_field(name = 'Применён фильтр:', value = f'```{filt}``` ({members})', inline = True)
                                emb.add_field(name = 'Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                                await sent.edit(embed = emb)
                            except asyncio.TimeoutError:
                                await sent.delete()
                        else:
                            if '--bots' in members:
                                if filt == None:
                                    await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == True)
                                else:
                                    await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.author.bot == True)
                            elif '--users' in members:
                                if filt == None:
                                    await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False)
                                else:
                                    await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False and m.content.lower() == filt.lower())
                            elif '--everyone' in members:
                                if filt == None:
                                    await ctx.channel.purge(limit = amount)
                                else:
                                    await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower())
                            elif members == '--silent':
                                if filt == None:
                                    await ctx.channel.purge(limit = amount)
                                else:
                                    await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower())
                    elif msg.content.lower() == 'n':
                        await msg.delete()
                        await sent.delete()
                        emb = disnake.Embed(description = 'Отменено.', colour = 0x2f3136)
                        await ctx.send(embed = emb, delete_after = 3)
                    else:
                        await msg.delete()
                        await sent.delete()
                        emb = disnake.Embed(description = f'Обнаружен недопустимый ответ ({msg.content})', colour = 0x2f3136)
                        await ctx.send(embed = emb, delete_after = 3)
                except asyncio.TimeoutError:
                    await sent.delete()
                    emb = disnake.Embed(description = f'{ctx.author.mention}, Время вышло.', colour = 0x2f3136)
                    await ctx.send(embed = emb, delete_after = 3)
        elif amount >= 10:
            emb = disnake.Embed(description = f'{ctx.author.mention}, создан запрос на удаление {amount} сообщений. Продолжить? (y/n)\n||Запрос будет отменён через 10 секунд.||', colour = 0x2f3136)
            sent = await ctx.send(embed = emb)
            try:
                msg = await self.client.wait_for('message', timeout = 10, check = lambda message: message.author == ctx.author and message.channel == ctx.message.channel)
                if msg.content.lower() == 'y':
                    await msg.delete()
                    await sent.delete()
                    if '--silent' not in members:
                        emb = disnake.Embed(description = 'Проверяем..', color = 0x2f3136)
                        sent = await ctx.send(embed = emb)
                        if members == '--bots':
                            if filt == None:
                                cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == True, before = sent)
                            else:
                                cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.author.bot == True, before = sent)
                            emb = disnake.Embed(title = 'Результаты удаления сообщений', color = 0x2f3136)
                            emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{len(cleared)}```')
                            if filt:
                                emb.add_field(name = 'Применён фильтр:', value = f'```{filt}``` ({members})', inline = True)
                            emb.add_field(name = 'Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                            emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c".')
                            await sent.edit(embed = emb)
                        elif members == '--users':
                            if filt == None:
                                cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False, before = sent)
                            else:
                                cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False and m.content.lower() == filt.lower(), before = sent)
                            emb = disnake.Embed(title = 'Результаты удаления сообщений', color = 0x2f3136)
                            emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{len(cleared)}```')
                            if filt:
                                emb.add_field(name = 'Применён фильтр:', value = f'```{filt}``` ({members})', inline = True)
                            emb.add_field(name = 'Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                            emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c".')
                            await sent.edit(embed = emb)
                        else:
                            if filt == None:
                                cleared = await ctx.channel.purge(limit = amount, before = sent)
                            else:
                                cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower(), before = sent)
                            emb = disnake.Embed(title = 'Результаты удаления сообщений', color = 0x2f3136)
                            emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{len(cleared)}```')
                            if filt:
                                emb.add_field(name = 'Применён фильтр:', value = f'```{filt}``` ({members})', inline = True)
                            emb.add_field(name = 'Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                            emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c".')
                            await sent.edit(embed = emb)
                        try:
                            if '--silent' in members:
                                return
                            msg = await self.client.wait_for('message', timeout = 10, check = lambda message: message.channel == ctx.message.channel and message.author == ctx.author and message.content.lower() == 'c')
                            emb = disnake.Embed(title = 'Результаты удаления сообщений', color = 0x2f3136)
                            emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{len(cleared)}```')
                            if filt:
                                emb.add_field(name = 'Применён фильтр:', value = f'```{filt}``` ({members})', inline = True)
                            emb.add_field(name = 'Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                            await sent.edit(embed = emb)
                        except asyncio.TimeoutError:
                            await sent.delete()
                    else:
                        if '--bots' in members:
                            if filt == None:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == True)
                            else:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.author.bot == True)
                        elif '--users' in members:
                            if filt == None:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False)
                            else:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False and m.content.lower() == filt.lower())
                        elif '--everyone' in members:
                            if filt == None:
                                await ctx.channel.purge(limit = amount)
                            else:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower())
                        elif members == '--silent':
                            if filt == None:
                                await ctx.channel.purge(limit = amount)
                            else:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower())
                elif msg.content.lower() == 'n':
                    await msg.delete()
                    await sent.delete()
                    emb = disnake.Embed(description = 'Отменено.', colour = 0x2f3136)
                    await ctx.send(embed = emb, delete_after = 3)
                else:
                    await msg.delete()
                    await sent.delete()
                    emb = disnake.Embed(description = f'Обнаружен недопустимый ответ ({msg.content})', colour = 0x2f3136)
                    await ctx.send(embed = emb, delete_after = 3)
            except asyncio.TimeoutError:
                await sent.delete()
                emb = disnake.Embed(description = f'{ctx.author.mention}, Время вышло.', colour = 0x2f3136)
                await ctx.send(embed = emb, delete_after = 3)
        elif amount == 0:
            emb = disnake.Embed(description = 'Удалять 0 сообщений? Ты еблан?', colour = 0x2f3136)
            await ctx.send(embed = emb, delete_after = 1)
        else:
            if '--silent' not in members:
                emb = disnake.Embed(description = 'Проверяем..', color = 0x2f3136)
                sent = await ctx.send(embed = emb)
                if '--bots' in members:
                    if filt == None:
                        cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == True, before = sent)
                    else:
                        cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.author.bot == True, before = sent)
                    emb = disnake.Embed(title = 'Результаты удаления сообщений', color = 0x2f3136)
                    emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{len(cleared)}```')
                    if filt:
                        emb.add_field(name = 'Применён фильтр:', value = f'```{filt}``` ({members})', inline = True)
                    emb.add_field(name = 'Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                    emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c".')
                    await sent.edit(embed = emb)
                elif '--users' in members:
                    if filt == None:
                        cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False, before = sent)
                    else:
                        cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False and m.content.lower() == filt.lower(), before = sent)
                    emb = disnake.Embed(title = 'Результаты удаления сообщений', color = 0x2f3136)
                    emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{len(cleared)}```')
                    if filt:
                        emb.add_field(name = 'Применён фильтр:', value = f'```{filt}``` ({members})', inline = True)
                    emb.add_field(name = 'Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                    emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c".')
                    await sent.edit(embed = emb)
                elif members == '--everyone':
                    if filt == None:
                        cleared = await ctx.channel.purge(limit = amount, before = sent)
                    else:
                        cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower(), before = sent)
                    emb = disnake.Embed(title = 'Результаты удаления сообщений', color = 0x2f3136)
                    emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{len(cleared)}```')
                    if filt:
                        emb.add_field(name = 'Применён фильтр:', value = f'```{filt}``` ({members})', inline = True)
                    emb.add_field(name = 'Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                    emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c".')
                    await sent.edit(embed = emb)
                try:
                    if '--silent' in members:
                        return
                    msg = await self.client.wait_for('message', timeout = 10, check = lambda message: message.channel == ctx.message.channel and message.author == ctx.author and message.content.lower() == 'c')
                    emb = disnake.Embed(title = 'Результаты удаления сообщений', color = 0x2f3136)
                    emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{len(cleared)}```')
                    if filt:
                        emb.add_field(name = 'Применён фильтр:', value = f'```{filt}``` ({members})', inline = True)
                    emb.add_field(name = 'Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                    await sent.edit(embed = emb)
                except asyncio.TimeoutError:
                    await sent.delete()
            else:
                if '--bots' in members:
                    if filt == None:
                        await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == True)
                    else:
                        await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.author.bot == True)
                elif '--users' in members:
                    if filt == None:
                        await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False)
                    else:
                        await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False and m.content.lower() == filt.lower())
                elif '--everyone' in members:
                    if filt == None:
                        await ctx.channel.purge(limit = amount)
                    else:
                        await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower())
                elif members == '--silent':
                    if filt == None:
                        await ctx.channel.purge(limit = amount)
                    else:
                        await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower())

def setup(client):
    client.add_cog(sMod(client))
