import os
import random

import discord
from discord import app_commands
from discord.ext import commands

class sMisc(commands.Cog):
    def __init__(self, client):
        self.client: commands.Bot = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('/ - Команды Misc синхронизированы')

    @app_commands.command(description = 'Получение случайного числа')
    @app_commands.describe(first = 'Первое число', second = 'Второе число')
    async def roll(self, interaction: discord.Interaction, first: int = None, second: int = None):
        if not first and not second:
            rand = random.randint(0, 100)
            if rand == 69:
                await interaction.response.send_message(embed = discord.Embed(description = f'`{interaction.user} получает случайное число (0-100)\n100`', color = 0xff8000))
            else:
                rand1 = random.randint(0, 9)
                rand2 = random.randint(0, 9)
                await interaction.response.send_message(embed = discord.Embed(description = f'`{interaction.user} получает случайное число (0-100)\n0{rand1}{rand2}`', color = 0xff8000))
        if first and not second:
            rand = random.randint(0, first)
            if first < 10:
                await interaction.response.send_message(embed = discord.Embed(description = f'`{interaction.user} получает случайное число (0-{first})\n0{rand}`', color = 0xff8000))
            else:
                await interaction.response.send_message(embed = discord.Embed(description = f'`{interaction.user} получает случайное число (0-{first})\n{rand}`', color = 0xff8000))
        if not first and second:
            rand = random.randint(0, second)
            if second < 10:
                await interaction.response.send_message(embed = discord.Embed(description = f'`{interaction.user} получает случайное число (0-{second})\n0{rand}`', color = 0xff8000))
            else:
                await interaction.response.send_message(embed = discord.Embed(description = f'`{interaction.user} получает случайное число (0-{second})\n{rand}`', color = 0xff8000))
        if first and second:
            if first > second:
                rand = random.randint(first, first)
                await interaction.response.send_message(embed = discord.Embed(description = f'`{interaction.user} получает случайное число ({first}-{first})\n{rand}`', color = 0xff8000))
            rand = random.randint(first, second)
            await interaction.response.send_message(embed = discord.Embed(description = f'`{interaction.user} получает случайное число ({first}-{second})\n{rand}`', color = 0xff8000))

    @app_commands.command(description = 'Подбрасывает монетку')
    async def coinflip(self, interaction: discord.Interaction):
        coin = random.choice(['ОРЁЛ', 'РЕШКА'])
        await interaction.response.send_message(embed = discord.Embed(description = f'{interaction.user.mention} подбрасывает монетку: {coin}', color = 0xff8000))

    @app_commands.command(description = 'Показывает участников с определённой ролью')
    @app_commands.describe(role = 'Роль')
    @app_commands.allowed_contexts(guilds = True, dms = False)
    async def rolemembers(self, interaction: discord.Interaction, role: discord.Role):
        emb = discord.Embed(color = 0xff8000)
        if len(role.members) != 0:
            emb.add_field(name = f'Участники с ролью {role} ({len(role.members)})', value = ', '.join([member.mention for member in role.members]))
        else:
            emb.description = 'Этой роли нет ни у кого.'
        await interaction.response.send_message(embed = emb)

    @app_commands.command(description = 'Информация о сервере')
    @app_commands.allowed_contexts(guilds = True, dms = False)
    async def guild(self, interaction: discord.Interaction):
        guild = interaction.guild
        emb = discord.Embed(color = 0x2f3136, timestamp = discord.utils.utcnow())
        emb.set_author(name = guild, icon_url = guild.icon.url if guild.icon else 'https://cdn.discordapp.com/attachments/685176670344183836/1076601210485866546/76923ec8de0a6ca5.png')
        emb.add_field(name = 'ID сервера', value = guild.id)
        emb.add_field(name = 'Владелец', value = guild.owner.mention)
        emb.add_field(name = 'Участников', value = f'{guild.member_count}\n**Из них ботов:** {len(list(filter(lambda m: m.bot, guild.members)))}\n**Из них людей:** {len(list(filter(lambda m: not m.bot, guild.members)))}')
        emb.add_field(name = 'Каналов', value = f'Текстовых {len(guild.text_channels)} | Голосовых {len(guild.voice_channels)}')
        roles = ', '.join([role.name for role in guild.roles[1:]])
        if len(roles) > 1:
            emb.add_field(name = f'Роли ({len(guild.roles)-1})', value = roles, inline = False)
        d = guild.created_at.strftime('%d.%m.%Y %H:%M:%S UTC')
        emb.add_field(name = 'Дата создания сервера', value = f'{d}', inline = False)
        emb.set_thumbnail(url = guild.icon.url if guild.icon else 'https://cdn.discordapp.com/attachments/685176670344183836/1076601210485866546/76923ec8de0a6ca5.png')
        await interaction.response.send_message(embed = emb)

    @app_commands.command(description = 'Информация о роли')
    @app_commands.describe(role = 'Роль')
    @app_commands.allowed_contexts(guilds = True, dms = False)
    async def roleinfo(self, interaction: discord.Interaction, role: discord.Role):
        is_mentionable = 'Да' if role.mentionable else 'Нет'
        is_managed = 'Да' if role.managed else 'Нет'
        is_hoisted = 'Да' if role.hoist else 'Нет'
        emb = discord.Embed(title = role.name, color = 0x2f3136)
        emb.add_field(name = 'ID', value = role.id)
        emb.add_field(name = 'Цвет', value = role.color)
        emb.add_field(name = 'Упоминается?', value = is_mentionable)
        emb.add_field(name = 'Управляется интеграцией?', value = is_managed)
        emb.add_field(name = 'Позиция в списке', value = role.position)
        d = role.created_at.strftime('%d.%m.%Y %H:%M:%S GMT')
        emb.add_field(name = 'Создана', value = f'{d}', inline = False)
        emb.add_field(name = 'Показывает участников отдельно?', value = is_hoisted)
        await interaction.response.send_message(embed = emb)

    @app_commands.command(description = 'Аватар пользователя')
    @app_commands.describe(member = 'Пользователь. Оставьте пустым, чтобы показать ваш аватар')
    async def avatar(self, interaction: discord.Interaction, member: discord.User = None):
        member = member if member else interaction.user
        emb = discord.Embed(color = 0x2f3136)
        if not member.avatar.is_animated():
            emb.set_image(url = member.avatar.with_format('png'))
        else:
            emb.set_image(url = member.avatar.url)
        emb.set_author(name = member.display_name)
        await interaction.response.send_message(embed = emb)

    @app_commands.command(description = 'Информация о пользователе')
    @app_commands.describe(member = 'Пользователь. Оставьте пустым, чтобы показать вашу информацию')
    @app_commands.allowed_contexts(guilds = True, dms = False)
    async def about(self, interaction: discord.Interaction, member: discord.Member = None):
        member = member if member else interaction.user
        bot = 'Да' if member.bot else 'Нет'
        emb = discord.Embed(color = 0x2f3136, timestamp = discord.utils.utcnow())
        emb.set_author(name = member.display_name)
        emb.add_field(name = 'ID', value = member.id)
        d = member.created_at.strftime('%d.%m.%Y %H:%M:%S UTC')
        d1 = member.joined_at.strftime('%d.%m.%Y %H:%M:%S UTC')
        emb.add_field(name = 'Создан', value = f'{d}', inline = False)
        emb.add_field(name = 'Вошёл', value = f'{d1}', inline = False)
        emb.add_field(name = 'Упоминание', value = member.mention)
        emb.add_field(name = 'Глобальное имя', value = member.name)
        if member.nick:
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
        amount = len(member.roles)
        if amount > 1:
            emb.add_field(name = f'Роли ({len(member.roles)-1})', value = roles, inline = False)
            emb.add_field(name = 'Высшая Роль', value = member.top_role.mention, inline = False)
        emb.set_thumbnail(url = member.avatar.url)
        await interaction.response.send_message(embed = emb)

async def setup(client):
    await client.add_cog(sMisc(client))
