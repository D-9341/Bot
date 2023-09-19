import asyncio
import datetime
import os
import re

import discord
from discord import app_commands
from discord.ext import commands
from pymongo import MongoClient

passw = os.environ.get('passw')
cluster = MongoClient(f"mongodb+srv://cephalon:{passw}@locale.ttokw.mongodb.net/Locale?retryWrites=true&w=majority")
collection = cluster.Locale.locale

guilds = [693929822543675455, 735874149578440855, 818758712163827723]

class sMod(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('/ - Команды Mod синхронизированы')

    @app_commands.command(description = 'Пишет участнику в лс сообщение')
    @app_commands.describe(member = 'Участник', text = 'Текст сообщения')
    @app_commands.checks.has_permissions(view_audit_log = True)
    async def dm(self, interaction: discord.Interaction, member: discord.Member, * , text: str):
        emb = discord.Embed(description = f'{text}', color = 0x2f3136)
        emb.set_author(name = interaction.user, icon_url = interaction.user.avatar.url)
        await member.send(embed = emb)
        rlocale = collection.find_one({"_id": interaction.user.id})["locale"]
        if rlocale == 'ru':
            await interaction.response.send_message('Сообщение отправлено.')
        if rlocale == 'gnida':
            await interaction.response.send_message('Твоя хуйня отправлена')

    @app_commands.command(description = 'Выгоняет участника')
    @app_commands.describe(member = 'Участник', reason = 'Причина')
    @app_commands.checks.has_permissions(kick_members = True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, *, reason: str = None):
        rlocale = collection.find_one({"_id": interaction.user.id})["locale"]
        bot = discord.utils.get(interaction.guild.members, id = self.client.user.id)
        if member.id not in self.client.owner_ids:
            if reason == None:
                if rlocale == 'ru':
                    reason = 'Не указана.'
                if rlocale == 'gnida':
                    reason = 'хз'
            if member == interaction.user:
                if rlocale == 'ru':
                    emb = discord.Embed(description = 'Ты **не** можешь кикнуть себя.', color = discord.Color.blurple())
                    return await interaction.response.send_message(embed = emb)
                if rlocale == 'gnida':
                    emb = discord.Embed(description = 'Для дохуя умных доношу - **нельзя** кикать __себя__', color = discord.Color.blurple())
                    return await interaction.response.send_message(embed = emb)
            if interaction.user.top_role == member.top_role:
                if rlocale == 'ru':
                    emb = discord.Embed(description = f'{interaction.user.mention}, ваша высшая роль равна высшей роли {member.mention}. Кик отклонён.', color = 0xff8000)
                    await interaction.response.send_message(embed = emb)
                if rlocale == 'gnida':
                    emb = discord.Embed(description = f'Твоя высшая роль равна высшей роли {member.mention}. Пошёл нахуй.', color = 0xff8000)
                    await interaction.response.send_message(embed = emb)
            elif member.top_role > interaction.user.top_role:
                if rlocale == 'ru':
                    emb = discord.Embed(description = f'{interaction.user.mention}, ваша высшая роль ниже высшей роли {member.mention}. Кик отклонён.', color = 0xff8000)
                    await interaction.response.send_message(embed = emb)
                if rlocale == 'gnida':
                    emb = discord.Embed(description = f'Твоя высшая роль ниже высшей роли {member.mention}. Пошёл нахуй.', color = 0xff8000)
                    await interaction.response.send_message(embed = emb)
            elif member.top_role > bot.top_role:
                if rlocale == 'ru':
                    emb = discord.Embed(description = f'**Моя** высшая роль ниже высшей роли {member.mention}. Кик невозможен.', color = 0xff0000)
                    await interaction.response.send_message(embed = emb)
                if rlocale == 'gnida':
                    emb = discord.Embed(description = f'МОЯ высшая роль ниже высшей роли {member.mention}. Сука.', color = 0xff0000)
                    await interaction.response.send_message(embed = emb)
            elif member.top_role == bot.top_role:
                if rlocale == 'ru':
                    emb = discord.Embed(description = f'**Моя** высшая роль идентична высшей роли {member.mention}. Кик невозможен.', color = 0xff0000)
                    await interaction.response.send_message(embed = emb)
                if rlocale == 'gnida':
                    emb = discord.Embed(description = f'МОЯ высшая роль идентична высшей роли {member.mention}. Сука.', color = 0xff0000)
                    await interaction.response.send_message(embed = emb)
            else:
                emb = discord.Embed(color = 0xff8000)
                emb.set_author(name = interaction.user, icon_url = interaction.user.avatar.url)
                emb.add_field(name = 'Был кикнут', value = member.mention)
                emb.add_field(name = 'По причине', value = reason)
                await interaction.response.send_message(embed = emb)
                await member.kick(reason = reason)
        else:
            if rlocale == 'ru':
                emb = discord.Embed(description = f'Извините, {interaction.user.mention}, но вы не можете кикнуть моего создателя!', color = 0xff0000)
                await interaction.response.send_message(embed = emb)
            if rlocale == 'gnida':
                emb = discord.Embed(description = 'Ого! Пошёл нахуй!', color = 0xff0000)
                await interaction.response.send_message(embed = emb)

    @app_commands.command(description = 'Блокирует участника')
    @app_commands.describe(member = 'Участник', reason = 'Причина')
    @app_commands.checks.has_permissions(ban_members = True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, *, reason: str = None):
        rlocale = collection.find_one({"_id": interaction.user.id})["locale"]
        bot = discord.utils.get(interaction.guild.members, id = self.client.user.id)
        if member.id not in self.client.owner_ids:
            if reason == None:
                if rlocale == 'ru':
                    reason = 'Не указана.'
                if rlocale == 'gnida':
                    reason = 'хз'
            if member == interaction.user:
                if rlocale == 'ru':
                    emb = discord.Embed(description = 'Ты **не** можешь забанить себя.', color = discord.Color.blurple())
                    return await interaction.response.send_message(embed = emb)
                if rlocale == 'gnida':
                    emb = discord.Embed(description = 'Для дохуя умных доношу - **нельзя** банить __себя__', color = discord.Color.blurple())
                    return await interaction.response.send_message(embed = emb)
            if interaction.user.top_role == member.top_role:
                if rlocale == 'ru':
                    emb = discord.Embed(description = f'{interaction.user.mention}, ваша высшая роль равна высшей роли {member.mention}. Бан отклонён.', color = 0xff8000)
                    await interaction.response.send_message(embed = emb)
                if rlocale == 'gnida':
                    emb = discord.Embed(description = f'Твоя высшая роль равна высшей роли {member.mention}. Саси.', color = 0xff8000)
                    await interaction.response.send_message(embed = emb)
            elif member.top_role > interaction.user.top_role:
                if rlocale == 'ru':
                    emb = discord.Embed(description = f'{interaction.user.mention}, ваша высшая роль ниже высшей роли {member.mention}. Бан отклонён.', color = 0xff8000)
                    await interaction.response.send_message(embed = emb)
                if rlocale == 'gnida':
                    emb = discord.Embed(description = f'Твоя высшая роль ниже высшей роли {member.mention}. Саси.', color = 0xff8000)
                    await interaction.response.send_message(embed = emb)
            elif member.top_role > bot.top_role:
                if rlocale == 'ru':
                    emb = discord.Embed(description = f'**Моя** высшая роль ниже высшей роли {member.mention}. Бан невозможен.', color = 0xff0000)
                    await interaction.response.send_message(embed = emb)
                if rlocale == 'gnida':
                    emb = discord.Embed(description = f'МОЯ высшая роль ниже высшей роли {member.mention}. Блять.', color = 0xff0000)
                    await interaction.response.send_message(embed = emb)
            elif member.top_role == bot.top_role:
                if rlocale == 'ru':
                    emb = discord.Embed(description = f'**Моя** высшая роль идентична высшей роли {member.mention}. Бан невозможен.', color = 0xff0000)
                    await interaction.response.send_message(embed = emb)
                if rlocale == 'gnida':
                    emb = discord.Embed(description = f'МОЯ высшая роль идентична высшей роли {member.mention}. Блять.', color = 0xff0000)
                    await interaction.response.send_message(embed = emb)
            else:
                if '--soft' in reason:
                    emb = discord.Embed(color = 0xff8000)
                    emb.set_author(name = interaction.user, icon_url = interaction.user.avatar.url)
                    emb.add_field(name = 'Упрощённо забанен', value = f'{member.mention} ({member.name})')
                    if '--reason' in reason:
                        reason = reason.strip()[15:].strip()
                    emb.add_field(name = 'По причине', value = reason)
                    await interaction.response.send_message(embed = emb)
                    await member.ban(reason = reason)
                    await member.unban(reason = '--softban')
                else:
                    emb = discord.Embed(color = 0xff8000)
                    emb.set_author(name = interaction.user, icon_url = interaction.user.avatar.url)
                    emb.add_field(name = 'Был забанен', value = member.mention)
                    emb.add_field(name = 'По причине', value = reason)
                    await interaction.response.send_message(embed = emb)
                    await member.ban(reason = reason)
        else:
            if rlocale == 'ru':
                emb = discord.Embed(description = f'Извините, {interaction.user.mention}, но вы не можете забанить моего создателя!', color = 0xff0000)
                await interaction.response.send_message(embed = emb)
            if rlocale == 'gnida':
                emb = discord.Embed(description = 'иди нахуй', color = 0xff0000)
                await interaction.response.send_message(embed = emb)

    @app_commands.command(description = 'Выдаёт участнику роль')
    @app_commands.describe(member = 'Участник', role = 'Роль')
    @app_commands.checks.has_permissions(manage_channels = True)
    async def give(self, interaction: discord.Interaction, member: discord.Member, role: discord.Role):
        rlocale = collection.find_one({"_id": interaction.user.id})["locale"]
        bot = interaction.guild.get_member(self.client.user.id)
        if role != None:
            if role.name == 'Muted':
                if member.id not in self.client.owner_ids:
                    if member == interaction.user:
                        if rlocale == 'ru':
                            emb = discord.Embed(description = 'Ты **не** можешь заглушить себя.', color = discord.Color.blurple())
                            return await interaction.response.send_message(embed = emb)
                        if rlocale == 'gnida':
                            emb = discord.Embed(description = 'Для дохуя умных доношу - **нельзя** мутить __себя__', color = discord.Color.blurple())
                            return await interaction.response.send_message(embed = emb)
                    else:
                        await member.add_roles(role)
                        if rlocale == 'ru':
                            emb = discord.Embed(description = f'{member.mention} был заглушён {interaction.user.mention}', color = 0x2f3136)
                            return await interaction.response.send_message(embed = emb)
                        if rlocale == 'gnida':
                            emb = discord.Embed(description = f'{member.mention} получает мут в ебало от {interaction.user.mention}', color = 0x2f3136)
                            return await interaction.response.send_message(embed = emb)
                else:
                    if rlocale == 'ru':
                        emb = discord.Embed(description = 'Вы всё ещё не можете заглушить моего создателя.', color = 0xff0000)
                        return await interaction.response.send_message(embed = emb)
                    if rlocale == 'gnida':
                        emb = discord.Embed(description = 'Ты думал мой Создатель тебе по зубам? ОН!?', color = 0xff0000)
                        return await interaction.response.send_message(embed = emb)
            else:
                if role > interaction.user.top_role:
                    if rlocale == 'ru':
                        emb = discord.Embed(description = f'Вы не можете выдать {role.mention}, так как она имеет более высокий ранг, чем ваша высшая роль.', color = 0xff8000)
                        await interaction.response.send_message(embed = emb)
                    if rlocale == 'gnida':
                        emb = discord.Embed(description = f'Дебилам вроде тебя запрещено выдавать {role.mention}, так как эта роль выше твоей высшей роли.', color = 0xff8000)
                        await interaction.response.send_message(embed = emb)
                elif role == interaction.user.top_role:
                    if rlocale == 'ru':
                        emb = discord.Embed(description = f'Вы не можете выдать {role.mention} кому-либо, так как она равна вашей высшей роли.', color = 0xff8000)
                        await interaction.response.send_message(embed = emb)
                    if rlocale == 'gnida':
                        emb = discord.Embed(description = f'Дебилам вроде тебя запрещено выдавать {role.mention}, так как она равна твоей высшей роли.', color = 0xff8000)
                        await interaction.response.send_message(embed = emb)
                elif role.is_default():
                    if rlocale == 'ru':
                        emb = discord.Embed(description = 'Выдавать @everyone?', color = 0xff8000)
                        await interaction.response.send_message(embed = emb)
                    if rlocale == 'gnida':
                        emb = discord.Embed(description = 'Это @everyone, еблан', color = 0xff8000)
                        await interaction.response.send_message(embed = emb)
                elif member.top_role > bot.top_role:
                    if rlocale == 'ru':
                        emb = discord.Embed(description = f'**Моя** высшая роль ниже чем {role.mention}. Выдать роль невозможно.', color = 0xff0000)
                        await interaction.response.send_message(embed = emb)
                    if rlocale == 'gnida':
                        emb = discord.Embed(description = f'МОЯ высшая роль ниже {role.mention}. Блять.', color = 0xff0000)
                        await interaction.response.send_message(embed = emb)
                elif member.top_role == bot.top_role:
                    if rlocale == 'ru':
                        emb = discord.Embed(description = f'**Моя** высшая роль это {role.mention}. Выдать роль невозможно.', color = 0xff0000)
                        await interaction.response.send_message(embed = emb)
                    if rlocale == 'gnida':
                        emb = discord.Embed(description = f'МОЯ высшая роль и есть {role.mention}, блять.', color = 0xff0000)
                        await interaction.response.send_message(embed = emb)
                else:
                    await member.add_roles(role)
                    emb = discord.Embed(color = 0xff8000, timestamp = discord.utils.utcnow())
                    emb.add_field(name = 'ВЫДАНА_РОЛЬ', value = f'{role.mention} | {role.name} | ID {role.id}')
                    emb.add_field(name = 'ВЫДАНА:', value = member.mention, inline = False)
                    emb.set_author(name = interaction.user, icon_url = interaction.user.avatar.url)
                    await interaction.response.send_message(embed = emb)
        else:
            if rlocale == 'ru':
                emb = discord.Embed(description = f'{interaction.user.mention}, я не могу найти {role} в списке ролей.\n||Используйте @упоминание роли||', color = member.color, timestamp = discord.utils.utcnow())
                await interaction.response.send_message(embed = emb)
            if rlocale == 'gnida':
                emb = discord.Embed(description = 'Не вижу я твоего высера в списке ролей', color = member.color, timestamp = discord.utils.utcnow())
                await interaction.response.send_message(embed = emb)

    @app_commands.command(description = 'Забирает роль у участника')
    @app_commands.describe(member = 'Участник', role = 'Роль')
    @app_commands.checks.has_permissions(manage_channels = True)
    async def take(self, interaction: discord.Interaction, member: discord.Member, role: discord.Role):
        rlocale = collection.find_one({"_id": interaction.user.id})["locale"]
        bot = interaction.guild.get_member(self.client.user.id)
        if role != None:
            if role.name == 'Muted':
                await member.remove_roles(role)
                if rlocale == 'ru':
                    emb = discord.Embed(description = f'{member.mention} был разглушён {interaction.user.mention}', color = 0xff8000)
                    return await interaction.response.send_message(embed = emb)
                if rlocale == 'gnida':
                    emb = discord.Embed(description = f'{member.mention} размучен {interaction.user.mention}', color = 0xff8000)
                    return await interaction.response.send_message(embed = emb)
            if role > interaction.user.top_role:
                if rlocale == 'ru':
                    emb = discord.Embed(description = f'Вы не можете забрать {role.mention}, так как она имеет более высокий ранг, чем ваша высшая роль. Забирание роли отменено.', color = 0x2f3136)
                    await interaction.response.send_message(embed = emb)
                if rlocale == 'gnida':
                    emb = discord.Embed(description = f'Тебе, уёбку, не разрешено забирать {role.mention}, так как эта роль круче твоей, говноед', color = 0x2f3136)
                    await interaction.response.send_message(embed = emb)
            elif role == interaction.user.top_role:
                if rlocale == 'ru':
                    emb = discord.Embed(description = f'Вы не можете забрать {role.mention}, так как она равна вашей высшей роли. Забирание роли отменено.', color = 0x2f3136)
                    await interaction.response.send_message(embed = emb)
                if rlocale == 'gnida':
                    emb = discord.Embed(description = f'Тебе, хуесосу, не положено отбирать {role.mention}, так как эта роль равна твоей, говна кусок', color = 0x2f3136)
                    await interaction.response.send_message(embed = emb)
            elif member.top_role > bot.top_role:
                if rlocale == 'ru':
                    emb = discord.Embed(description = f'**Моя** высшая роль ниже высшей роли {member.mention}. Забрать роль невозможно.', color = 0xff0000)
                    await interaction.response.send_message(embed = emb)
                if rlocale == 'gnida':
                    emb = discord.Embed(description = f'МОЯ самая крутая роль ниже самой крутой роли {member.mention}, я не могу её спиздить', color = 0xff0000)
                    await interaction.response.send_message(embed = emb)
            elif member.top_role == bot.top_role:
                if rlocale == 'ru':
                    emb = discord.Embed(description = f'**Моя** высшая роль идентична высшей роли {member.mention}. Забрать роль невозможно.', color = 0xff0000)
                    await interaction.response.send_message(embed = emb)
                if rlocale == 'ginda':
                    emb = discord.Embed(description = f'МОЯ самая крутая роль совпадает с самой крутой ролью этого пидораса -> {member.mention}, не могу спиздить', color = 0xff0000)
                    await interaction.response.send_message(embed = emb)
            elif role.is_default():
                if rlocale == 'ru':
                    emb = discord.Embed(description = 'Забрать @everyone?', color = 0xffffff)
                    await interaction.response.send_message(embed = emb)
                if rlocale == 'gnida':
                    emb = discord.Embed(description = 'Ты уверен что я должен отжать @everyone?', color = 0xffffff)
                    await interaction.response.send_message(embed = emb)
            else:
                await member.remove_roles(role)
                emb = discord.Embed(color = 0xff8000, timestamp = discord.utils.utcnow())
                emb.add_field(name = 'ЗАБРАНА_РОЛЬ', value = f'{role.mention} | {role.name} | ID {role.id}')
                emb.add_field(name = 'ЗАБРАНА_У:', value = member.mention, inline = False)
                emb.set_author(name = interaction.user, icon_url = interaction.user.avatar.url)
                await interaction.response.send_message(embed = emb)
        else:
            if rlocale == 'ru':
                emb = discord.Embed(description = f'{interaction.user.mention}, я не могу найти {role.mention} в списке ролей.\n||Используйте @упоминание роли||', color = member.color, timestamp = discord.utils.utcnow())
                await interaction.response.send_message(embed = emb)
            if rlocale == 'gnida':
                emb = discord.Embed(description = 'Не вижу я твоего высера в списке ролей', color = member.color, timestamp = discord.utils.utcnow())
                await interaction.response.send_message(embed = emb)

    @app_commands.command(description = 'Заглушение участника')
    @app_commands.describe(member = 'Участник', reason = 'Причина')
    @app_commands.checks.has_permissions(view_audit_log = True)
    async def mute(self, interaction: discord.Interaction, member: discord.Member, *, reason: str = None):
        rlocale = collection.find_one({"_id": interaction.user.id})["locale"]
        if reason == None:
            if rlocale == 'ru':
                reason = 'Не указана.'
            if rlocale == 'gnida':
                reason = 'хз'
        role = discord.utils.get(interaction.guild.roles, name = 'Muted')
        if role in member.roles:
            if rlocale == 'ru':
                emb = discord.Embed(description = 'Роль Muted уже есть в списке ролей участника.', color = 0x2f3136)
                return await interaction.response.send_message(embed = emb)
            if rlocale == 'gnida':
                emb = discord.Embed(description = 'Этот уебан уже награждён ролью Muted, попробуй на ком-нибудь другом', color = 0x2f3136)
                return await interaction.response.send_message(embed = emb)
        if member == interaction.user:
            if rlocale == 'ru':
                emb = discord.Embed(description = 'Ты **не** можешь заглушить себя.', color = discord.Color.blurple())
                return await interaction.response.send_message(embed = emb)
            if rlocale == 'gnida':
                emb = discord.Embed(description = 'Для дохуя умных доношу - **нельзя** мутить __себя__', color = discord.Color.blurple())
                return await interaction.response.send_message(embed = emb)
        if member.id not in self.client.owner_ids:
            if interaction.user.top_role == member.top_role:
                if rlocale == 'ru':
                    emb = discord.Embed(description = f'{interaction.user.mention}, ваша высшая роль равна высшей роли {member.mention}. Заглушение отклонено.', color = 0xff8000)
                    await interaction.response.send_message(embed = emb)
                if rlocale == 'gnida':
                    emb = discord.Embed(description = f'{interaction.user.mention}, твоя самая крутая роль совпадает с самой крутой ролью {member.mention}, выбери кого послабее ', color = 0xff8000)
                    await interaction.response.send_message(embed = emb)
            elif interaction.user.top_role < member.top_role:
                if rlocale == 'ru':
                    emb = discord.Embed(description = f'{interaction.user.mention}, ваша высшая роль ниже высшей роли {member.mention}. Заглушение отклонено.', color = 0xff8000)
                    await interaction.response.send_message(embed = emb)
                if rlocale == 'gnida':
                    emb = discord.Embed(description = f'Вот это дела {interaction.user.mention}, ты конкретно обосрался! Твоя самая крутая роль даже ниже самой крутой роли {member.mention}, выбери кого послабее, лошара!', color = 0xff8000)
                    await interaction.response.send_message(embed = emb)
            else:
                if role != None:
                    await member.add_roles(role)
                    emb = discord.Embed(color = 0xff8000, timestamp = discord.utils.utcnow())
                    emb.add_field(name = 'Заглушён', value = f'{member.mention}')
                    emb.add_field(name = 'Причина', value = reason)
                    await interaction.response.send_message(embed = emb)
                else:
                    role = await interaction.guild.create_role(name = 'Muted', color = 0x000001, reason = 'Создано автоматически командой mute')
                    await member.add_roles(role)
                    emb = discord.Embed(color = 0xff8000, timestamp = discord.utils.utcnow())
                    emb.add_field(name = 'Заглушён', value = f'{member.mention}')
                    emb.add_field(name = 'Причина', value = reason)
                    await interaction.response.send_message(embed = emb)
        else:
            if rlocale == 'ru':
                emb = discord.Embed(description = f'Извините, {interaction.user.mention}, но вы не можете заглушить моего создателя!', color = 0xff0000)
                await interaction.response.send_message(embed = emb)
            if rlocale == 'gnida':
                emb = discord.Embed(description = 'иди нахуй', color = 0xff0000)
                await interaction.response.send_message(embed = emb)

    @app_commands.command(description = 'Отключает человеку микрофон в голосовых каналах')
    @app_commands.describe(member = 'Участник', reason = 'Причина')
    @app_commands.checks.has_permissions(manage_channels = True)
    async def deaf(self, interaction: discord.Interaction, member: discord.Member, *, reason: str = None):
        rlocale = collection.find_one({"_id": interaction.user.id})["locale"]
        role = discord.utils.get(interaction.guild.roles, name = 'Deafened')
        if reason == None:
            if rlocale == 'ru':
                reason = 'Не указана.'
            if rlocale == 'gnida':
                reason = 'хз'
        if role in member.roles:
            if rlocale == 'ru':
                emb = discord.Embed(description = 'Роль Deafened уже есть в списке ролей участника.', color = 0x2f3136)
                return await interaction.response.send_message(embed = emb)
            if rlocale == 'gnida':
                emb = discord.Embed(description = 'Ослеп совсем? У него уже есть роль Deafened.', color = 0x2f3136)
                return await interaction.response.send_message(embed = emb)
        if member.id not in self.client.owner_ids:
            if interaction.user.top_role == member.top_role:
                if rlocale == 'ru':
                    emb = discord.Embed(description = f'{interaction.user.mention}, ваша высшая роль равна высшей роли {member.mention}. Заглушение отклонено.', color = 0xff8000)
                    await interaction.response.send_message(embed = emb)
                if rlocale == 'gnida':
                    emb = discord.Embed(description = f'{interaction.user.mention}, твоя наикрутейшая роль равна самой крутой роли {member.mention}. Не могу заглушить.', color = 0xff8000)
                    await interaction.response.send_message(embed = emb)
            elif interaction.user.top_role < member.top_role:
                if rlocale == 'ru':
                    emb = discord.Embed(description = f'{interaction.user.mention}, ваша высшая роль ниже высшей роли {member.mention}. Заглушение отклонено.', color = 0xff8000)
                    await interaction.response.send_message(embed = emb)
                if rlocale == 'gnida':
                    emb = discord.Embed(description = f'{interaction.user.mention}, ты настолько опущен, что твоя высшая роль ниже даже чем у {member.mention}. Хуй тебе, а не мут.', color = 0xff8000)
                    await interaction.response.send_message(embed = emb)
            else:
                if role != None:
                    await member.add_roles(role)
                    emb = discord.Embed(color = 0x2f3136, timestamp = discord.utils.utcnow())
                    emb.add_field(name = 'Заглушён', value = member.mention)
                    emb.add_field(name = 'Причина', value = reason)
                    await interaction.response.send_message(embed = emb)
                else:
                    role = await interaction.guild.create_role(name = 'Deafened', color = 0x000001, reason = 'Создано автоматически командой deaf')
                    await member.add_roles(role)
                    emb = discord.Embed(color = 0x2f3136, timestamp = discord.utils.utcnow())
                    emb.add_field(name = 'Заглушён', value = member.mention)
                    emb.add_field(name = 'Причина', value = reason)
                    await interaction.response.send_message(embed = emb)
        else:
            if rlocale == 'ru':
                emb = discord.Embed(description = f'Извините, {interaction.user.mention}, но вы не можете заглушить моего создателя!', color = 0xff0000)
                await interaction.response.send_message(embed = emb)
            if rlocale == 'gnida':
                emb = discord.Embed(description = 'иди нахуй', color = 0xff0000)
                await interaction.response.send_message(embed = emb)

    @app_commands.command(description = 'Отправляет подумать участника о своём поведении')
    @app_commands.describe(member = 'Участник', reason = 'Причина')
    @app_commands.checks.has_permissions(manage_channels = True)
    async def timeout(self, interaction: discord.Interaction, member: discord.Member, *, reason: str = None):
        rlocale = collection.find_one({"_id": interaction.user.id})["locale"]
        if reason == None:
            if rlocale == 'ru':
                reason = 'Не указана.'
            if rlocale == 'gnida':
                reason = 'хз'
        if member.id not in self.client.owner_ids:
            if member == interaction.user:
                if rlocale == 'ru':
                    emb = discord.Embed(description = 'Ты **не** можешь заглушить себя.', color = discord.Color.blurple())
                    await interaction.response.send_message(embed = emb)
                if rlocale == 'gnida':
                    emb = discord.Embed(description = 'Для дохуя умных доношу - **нельзя** мутить __себя__', color = discord.Color.blurple())
                    await interaction.response.send_message(embed = emb)
            if interaction.user.top_role == member.top_role:
                if rlocale == 'ru':
                    emb = discord.Embed(description = f'{interaction.user.mention}, ваша высшая роль равна высшей роли {member.mention}. Тайм-аут отклонён.', color = 0xff8000)
                    await interaction.response.send_message(embed = emb)
                if rlocale == 'gnida':
                    emb = discord.Embed(description = f'{interaction.user.mention}, смотри сюда, твоя наивысшая роль равна его наивысшей роли, понял? Это значит что я не могу отстранить {member.mention}, от пиздежа ', color = 0xff8000)
                    await interaction.response.send_message(embed = emb)
            elif interaction.user.top_role < member.top_role:
                if rlocale == 'ru':
                    emb = discord.Embed(description = f'{interaction.user.mention}, ваша высшая роль ниже высшей роли {member.mention}. Тайм-аут отклонён.', color = 0xff8000)
                    await interaction.response.send_message(embed = emb)
                if rlocale == 'gnida':
                    emb = discord.Embed(description = f'{interaction.user.mention}, твоя самая крутая роль даже ниже самой крутой роли {member.mention}. Надеюсь мне не надо объяснять почему я не могу отстранить его от пиздежа?', color = 0xff8000)
                    await interaction.response.send_message(embed = emb)
            else:
                await member.timeout(datetime.timedelta(hours = 1), reason = reason)
                emb = discord.Embed(title = f'Тайм-аут участника {member}', color = 0xff8000, timestamp = discord.utils.utcnow())
                emb.add_field(name = 'Причина', value = reason)
                emb.add_field(name = 'Время тайм-аута', value = '1 час')
                await interaction.response.send_message(embed = emb)
        else:
            if rlocale == 'ru':
                emb = discord.Embed(description = f'Извините, {interaction.user.mention}, но вы не можете заглушить моего создателя!', color = 0xff0000)
                await interaction.response.send_message(embed = emb)
            if rlocale == 'gnida':
                emb = discord.Embed(description = 'иди нахуй', color = 0xff0000)
                await interaction.response.send_message(embed = emb)
    
    @app_commands.command(description = 'Отменяет отключение микрофона')
    @app_commands.describe(member = 'Участник', reason = 'Причина')
    @app_commands.checks.has_permissions(manage_channels = True)
    async def undeaf(self, interaction: discord.Interaction, member: discord.Member, *, reason: str = None):
        rlocale = collection.find_one({"_id": interaction.user.id})["locale"]
        role = discord.utils.get(interaction.guild.roles, name = 'Deafened')
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
                        emb.add_field(name = 'Снял заглушение', value = interaction.user.mention)
                        emb.add_field(name = 'Причина', value = reason)
                        await interaction.response.send_message(embed = emb)
                    if rlocale == 'gnida':
                        emb = discord.Embed(title = f'Принудительный анмут этого пидораса -> {member}', color = 0xff8000, timestamp = discord.utils.utcnow())
                        emb.add_field(name = 'Размутил', value = interaction.user.mention)
                        emb.add_field(name = 'Причина', value = reason)
                        await interaction.response.send_message(embed = emb)
                else:
                    if rlocale == 'ru':
                        emb = discord.Embed(description = 'Снятие заглушения не требуется. Роли Deafened не обнаружено в списке ролей участника.', color = 0xff8000)
                        await interaction.response.send_message(embed = emb)
                    if rlocale == 'gnida':
                        emb = discord.Embed(description = 'Размут не требуется. Он и так уже размучен, ты чё слепой нахуй?', color = 0xff8000)
                        await interaction.response.send_message(embed = emb)
            else:
                if rlocale == 'ru':
                    emb = discord.Embed(description = f'{interaction.user.mention}, Я не могу снять заглушение у {member.mention} из-за того, что роль Deafened была удалена', color = 0xff8000, timestamp = discord.utils.utcnow())
                    await interaction.response.send_message(embed = emb)
                if rlocale == 'gnida':
                    emb = discord.Embed(description = f'Вот дела, {interaction.user.mention}, кажется я не могу размутить {member.mention} из-за того, что какой-то уебан удалил роль Deafened', color = 0xff8000, timestamp = discord.utils.utcnow())
                    await interaction.response.send_message(embed = emb)

    @app_commands.command(description = 'Разглушает участника')
    @app_commands.describe(member = 'Участник', reason = 'Причина')
    @app_commands.checks.has_permissions(manage_channels = True)
    async def unmute(self, interaction: discord.Interaction, member: discord.Member, *, reason: str = None):
        rlocale = collection.find_one({"_id": interaction.user.id})["locale"]
        role = discord.utils.get(interaction.guild.roles, name = 'Muted')
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
                    emb.add_field(name = 'Снял заглушение', value = interaction.user.mention)
                    emb.add_field(name = 'По причине', value = reason)
                    await interaction.response.send_message(embed = emb)
                if rlocale == 'gnida':
                    emb = discord.Embed(title = f'Принудительный анмут этого программиста -> {member}', color = 0xff8000, timestamp = discord.utils.utcnow())
                    emb.add_field(name = 'Размутил', value = interaction.user.mention)
                    emb.add_field(name = 'По причине', value = reason)
                    await interaction.response.send_message(embed = emb)
            else:
                if rlocale == 'ru':
                    emb = discord.Embed(description = 'Снятие заглушения не требуется. Роли Muted не обнаружено в списке ролей участника.', color = 0xff8000)
                    await interaction.response.send_message(embed = emb)
                if rlocale == 'gnida':
                    emb = discord.Embed(description = 'Анмут не требуется. Кажется ты уёбок ослеп, смотри внимательно, В СПИСКЕ ЕГО РОЛЕЙ MUTED НЕ ОБНАРУЖЕНА!', color = 0xff8000)
                    await interaction.response.send_message(embed = emb)
        else:
            if rlocale == 'ru':
                emb = discord.Embed(description = f'{interaction.user.mention}, Я не могу снять заглушение у {member.mention} из-за того, что роль Muted была удалена', color = 0xff8000, timestamp = discord.utils.utcnow())
                await interaction.response.send_message(embed = emb)
            if rlocale == 'gnida':
                emb = discord.Embed(description = f'Слушай сюда {interaction.user.mention}, не могу я его размутить, ясно? Какой-то гандон удалил роль Muted, найди его по журналу аудита и стукни по башке', color = 0xff8000, timestamp = discord.utils.utcnow())
                await interaction.response.send_message(embed = emb)

async def setup(client):
    await client.add_cog(sMod(client))
