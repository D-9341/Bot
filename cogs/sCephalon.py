import asyncio
import sys
import json

import discord
from functions import translate, get_locale, set_locale
from typing import Literal
from main import uptime
from pathlib import Path
from discord import app_commands
from discord.ext import commands
from cogs.Constants import colors

CWD = Path(__file__).parents[0].parents[0]
CWD = str(CWD)

guilds = [693929822543675455, 735874149578440855, 818758712163827723]

class View(discord.ui.View):
    def __init__(self, timeout):
        super().__init__(timeout = 5)

    async def on_timeout(self, interaction: discord.Interaction):
        await interaction.response.edit_message('Время вышло', view = None)

class GrayButton(discord.ui.Button):
    def __init__(self, label):
        super().__init__(label = label, style = discord.ButtonStyle.gray)

class RedButton(discord.ui.Button):
    def __init__(self, label):
        super().__init__(label = label, style = discord.ButtonStyle.red)

class sCephalon(commands.Cog):
    def __init__(self, client):
        self.client: commands.Bot = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('/ - Команды Cephalon синхронизированы')

    @app_commands.command(description = 'Помощь по командам')
    @app_commands.describe(command = 'Выберите команду, по которой нужна помощь')
    async def help(self, interaction: discord.Interaction, command: Literal['help', 'content', 'edit', 'say', 'about', 'avatar', 'roll', 'roleinfo', 'rolemembers', 'vote', 'dotersbrain', 'ban', 'dm', 'deaf', 'kick', 'give', 'mute', 'take', 'timeout', 'undeaf', 'unmute'] = None):
        if command == None:
            emb = discord.Embed(description = 'Все доступные / команды.', color = colors.JDH)
            emb.set_author(name = self.client.user.name, url = 'https://discord.com/api/oauth2/authorize?client_id=694170281270312991&permissions=8&scope=bot%20applications.commands')
            emb.add_field(name = 'Cephalon', value = '`botver`, `devs`, `help`, `info`, `invite`, `locale`, `ping`, `uptime`', inline = False)
            emb.add_field(name = 'Embeds', value = '`content`, `edit`, `say`', inline = False)
            emb.add_field(name = 'Fun', value = '`aghanim`, `dotersbrain`', inline = False)
            emb.add_field(name = 'Mod', value = '`ban`, `dm`, `deaf`, `give`, `kick`, `mute`, `take`, `timeout`, `undeaf`, `unmute`', inline = False)
            emb.add_field(name = 'Misc', value = '`about`, `avatar`, `coinflip`, `guild`, `roll`, `roleinfo`, `rolemembers`', inline = False)
            emb.add_field(name = 'ᅠ', value = 'Указанные разрешения необходимы для исполнителя команды если не указано другого.', inline = False)
            emb.add_field(name = 'ᅠ', value = 'Не используйте `[] <> /` при написании команды.', inline = False)
            emb.add_field(name = 'ᅠ', value = '**Используйте** `/help [команда]` **для подробностей использования.**\n\n**[Ссылка-приглашение](https://discord.com/api/oauth2/authorize?client_id=694170281270312991&permissions=8&scope=bot%20applications.commands)**', inline = False)
            emb.set_footer(text = 'Cephalon Cy ©️ Sus&Co\n2020 - Present')
            return await interaction.response.send_message(embed = emb)
        locale = get_locale(interaction.user.id)
        return await interaction.response.send_message(embed = discord.Embed(description = (translate(locale, f'{command}_help')), color = colors.JDH))

    @app_commands.command(description = 'Время бота в сети')
    async def uptime(self, interaction: discord.Interaction):
        now = discord.utils.utcnow()
        up_time = now - uptime
        hours, remainder = divmod(up_time.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        await interaction.response.send_message(embed = discord.Embed(description = f'Я в сети уже `{hours} ч, {minutes} м, {seconds} с`', color = colors.JDH))

    @app_commands.command(description = 'Выберите локаль бота')
    async def locale(self, interaction: discord.Interaction):
        locale = get_locale(interaction.user.id)
        rbutton = GrayButton('RU')
        gbutton = RedButton('GNIDA')
        ebutton = GrayButton('EN')
        tbutton = GrayButton('TEST' if locale == 'en' else 'ТЕСТ')
        ibutton = GrayButton('INFO' if locale == 'en' else 'ИНФО')
        ybutton = RedButton('YES' if locale == 'en' else 'ДА')
        nbutton = GrayButton('NO' if locale == 'en' else 'НЕТ')
        confirm = discord.ui.View(timeout = 5)
        confirm.add_item(ybutton)
        confirm.add_item(nbutton)
        view = discord.ui.View(timeout = 5)
        view.add_item(rbutton)
        view.add_item(gbutton)
        if interaction.user.id in self.client.owner_ids:
            view.add_item(ebutton)
        view.add_item(tbutton)
        view.add_item(ibutton)
        async def rbutton_callback(interaction):
            set_locale(str(interaction.user.id), 'ru')
            await interaction.response.edit_message(embed = discord.Embed(description = 'Ваша локаль была установлена на `ru`', color = colors.JDH), view = None)
        async def gbutton_callback(interaction):
            await interaction.response.edit_message(embed = discord.Embed(description = 'Ты бля уверен?', color = colors.JDH), view = confirm)
        async def ybutton_callback(interaction):
            set_locale(str(interaction.user.id), 'gnida')
            await interaction.response.edit_message(embed = discord.Embed(description = 'Твоя ёбаная локаль была установлена на `gnida`!', color = colors.JDH), view = None)
        async def nbutton_callback(interaction):
            await interaction.response.edit_message(embed = discord.Embed(description = 'Ну ок', color = colors.JDH), view = None)
        async def ebutton_callback(interaction):
            set_locale(str(interaction.user.id), 'en')
            await interaction.response.edit_message(embed = discord.Embed(description = 'Your locale has been set to `en`', color = colors.JDH), view = None)
        async def test_callback(interaction):
            await interaction.response.edit_message(embed = discord.Embed(description = translate(locale, 'locale_test'), color = colors.JDH), view = None)
        async def info_callback(interaction):
            await interaction.response.edit_message(content = None, embed = discord.Embed(description = translate(locale, 'locale_info'), color = colors.LO), view = None)
        rbutton.callback = rbutton_callback
        gbutton.callback = gbutton_callback
        ebutton.callback = ebutton_callback
        tbutton.callback = test_callback
        ibutton.callback = info_callback
        ybutton.callback = ybutton_callback
        nbutton.callback = nbutton_callback
        if locale == 'ru':
            rbutton.disabled = True
        if locale == 'gnida':
            gbutton.disabled = True
        if locale == 'en':
            ebutton.disabled = True
        await interaction.response.send_message(embed = discord.Embed(description = translate(locale, 'locale_options'), color = colors.JDH), view = view)

    @app_commands.command(description = 'Информация о боте')
    async def info(self, interaction: discord.Interaction):
        emb = discord.Embed(title = 'Пару строк кода сюда, новые фишки туда', description = 'Создатели бота постоянно совершенствуют своё детище, поддерживая его в актуальном состоянии', color = colors.JDH)
        emb.set_author(name = self.client.user.name, url = 'https://warframe.fandom.com/wiki/Cephalon_Cy', icon_url = self.client.user.avatar.url)
        emb.add_field(name = 'Версия', value = '0.14.6.0')
        emb.add_field(name = 'Написан на', value = f'discord.py v{discord.__version__}\nPython v{sys.version[:7]}')
        emb.add_field(name = 'Разработчики 🇷🇺', value = '[сасиска](https://discord.com/users/338714886001524737)\n[Prokaznik](https://discord.com/users/417012231406878720)')
        emb.add_field(name = 'Обслуживаю', value = f'{len(self.client.users)} человек')
        emb.add_field(name = 'Существую на', value = f'{len(self.client.guilds)} серверах')
        emb.set_footer(text = 'Данное приложение вдохновлено игрой Warframe', icon_url = 'https://i.playground.ru/p/yVaOZNSTdgUTxmzy_qvzzQ.png')
        await interaction.response.send_message(embed = emb)

    @app_commands.command(description = 'Информация о разработчиках бота')
    async def devs(self, interaction: discord.Interaction):
        emb = discord.Embed(description = 'Разработчики бота, в частности члены команды Sus&Co', color = colors.JDH)
        emb.add_field(name = 'сасиска', value = 'Первичный владелец бота, по совместительству основатель Sus&Co', inline = False)
        emb.add_field(name = 'Проказник', value = 'Причастен к созданию локали gnida, помогает с идеями для основного бота. Хоть и считается разработчиком, не имеет доступа к коду', inline = False)
        await interaction.response.send_message(embed = emb)

    @app_commands.command(description = 'Пригласите бота на сервер!')
    async def invite(self, interaction: discord.Interaction):
        emb = discord.Embed(description = '[Ссылка](https://discord.com/oauth2/authorize?client_id=694170281270312991&permissions=8&scope=bot%20applications.commands) для приглашения Cy на сервера', color = colors.JDH)
        await interaction.response.send_message(embed = emb)

    @app_commands.command(description = 'Показывает задержку клиента бота')
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(embed = discord.Embed(description = '`Получаю..`', color = colors.JDH))
        await asyncio.sleep(self.client.latency)
        await interaction.edit_original_response(embed = discord.Embed(description = f'Pong!  `{round(self.client.latency * 1000)} ms`', color = colors.JDH))

    @app_commands.command(description = 'Узнайте, что было в предыдущих версиях бота')
    @app_commands.describe(version = 'Укажите конкретную версию')
    async def botver(self, interaction: discord.Interaction, version: Literal['0.12.9.10519', '0.12.9.10988', '0.12.9.11410', '0.12.10.1.11661', '0.12.10.2.12528', '0.12.11.2.13771', '0.12.12.0.0', '0.12.12.10.0', '0.12.12.10.16367', '0.12.12.30.0', '0.13.0.2.21680', '0.14.6.0', '1.0']):
        with open(CWD / 'versions.json', 'r', encoding = 'utf-8') as f:
            versions = json.load(f)
        version_data = versions[str(version)]
        await interaction.response.send_message(embed = discord.Embed(title = version, description = version_data, color = colors.DEFAULT))

async def setup(client):
    await client.add_cog(sCephalon(client))
