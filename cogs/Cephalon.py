import asyncio
import secrets
import sys
import json
from pathlib import Path
from datetime import timedelta

import discord
from functions import translate, get_locale, set_locale, get_plural_form, get_command_help
from main import uptime
from discord.ext import commands

CWD = Path(__file__).parents[0].parents[0]
CWD = str(CWD)

class GrayButton(discord.ui.Button):
    def __init__(self, label):
        super().__init__(label = label, style = discord.ButtonStyle.gray)

class RedButton(discord.ui.Button):
    def __init__(self, label):
        super().__init__(label = label, style = discord.ButtonStyle.red)

class Cephalon(commands.Cog):
    def __init__(self, client):
        self.client: commands.Bot = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Модуль Cephalon загружен')

    @commands.command()
    async def help(self, ctx: commands.Context, command = None):
        owner_commands = ['guilds', 'reset', 'status', 'generate', 'invite', 'disable', 'enable', 'reload', 'list', 'load', 'unload']
        if command is None:
            emb = discord.Embed(description = 'Все доступные команды', color = 0xff8000)
            emb.set_author(name = self.client.user.name, url = 'https://discord.com/api/oauth2/authorize?client_id=694170281270312991&permissions=8&scope=bot%20applications.commands')
            emb.add_field(name = 'Cephalon', value = '`botver`, `devs`, `help`, `info`, `invite`, `locale`, `ping`, `uptime`', inline = False)
            emb.add_field(name = 'Embeds', value = '`content`, `edit`, `say`', inline = False)
            emb.add_field(name = 'Fun', value = '`aghanim`, `dotersbrain`, `roulette`', inline = False)
            emb.add_field(name = 'Mod', value = '`ban`, `clear`, `dm`, `deaf`, `give`, `kick`, `mute`, `take`, `timeout`, `undeaf`, `unmute`', inline = False)
            emb.add_field(name = 'Misc', value = '`about`, `avatar`, `coinflip`, `roll`, `roleinfo`, `rolemembers`, `serverinfo`, `someone`', inline = False)
            # emb.add_field(name = 'Music', value = '`join`, `leave`, `play`, `pause`, `resume`, `stop`') # , `volume`
            emb.add_field(name = 'ᅠ', value = 'Указанные разрешения необходимы для исполнителя команды если не указано другого', inline = False)
            emb.add_field(name = 'ᅠ', value = 'Не используйте `[] <> /` при написании команды', inline = False)
            emb.add_field(name = 'ᅠ', value = '**Используйте** `cy/help [команда]` **для подробностей использования.**\n\n**[Ссылка-приглашение](https://discord.com/api/oauth2/authorize?client_id=694170281270312991&permissions=8&scope=bot%20applications.commands)**', inline = False)
            emb.set_footer(text = 'Cephalon Cy ©️ Sus&Co\n2020 - Present')
            return await ctx.send(embed = emb)
        if ctx.author.id in self.client.owner_ids and command in owner_commands:
            if command == 'list':
                return await ctx.send(embed = discord.Embed(description = f'```{', '.join(owner_commands)}```', color = 0xff8000))
            if command == 'guilds':
                return await ctx.send(embed = discord.Embed(description = '```py\ncy/guilds\n\nПоказывает список серверов, на которых находится бот```', color = 0xff8000))
            if command == 'reset':
                return await ctx.send(embed = discord.Embed(description = '```py\ncy/reset <команда>\n\nСбрасывает счётчик перезарядки команды```', color = 0xff8000))
            if command == 'status':
                return await ctx.send(embed = discord.Embed(description = '```py\ncy/status\n\nПоказывает состояние бота и его модулей. Если какой-либо модуль неисправен, будет выведено соответствующее сообщение```', color = 0xff8000))
            if command == 'generate':
                return await ctx.send(embed = discord.Embed(description = '```py\ncy/generate\n\nСоздаёт случайный код```', color = 0xff8000))
            if command == 'invite':
                return await ctx.send(embed = discord.Embed(description = '```py\ncy/invite [beta/pro]\n\nПоказывает ссылку для приглашения бота. beta - бета-версия, pro - про-версия```', color = 0xff8000))
            if command == 'disable':
                return await ctx.send(embed = discord.Embed(description = '```py\ncy/disable <команда>\n\nВыключает команду/модуль```', color = 0xff8000))
            if command == 'enable':
                return await ctx.send(embed = discord.Embed(description = '```py\ncy/enable <команда>\n\nВключает команду/модуль```', color = 0xff8000))
            if command == 'reload':
                return await ctx.send(embed = discord.Embed(description = '```py\ncy/reload\n\nИнструмент для перезагрузки всех модулей.\nОшибкой считается только то, что наследуется от commands.ExtensionFailed, в т.ч. и ошибки синтаксиса.\nТ.о., если какая-либо команда имеет незначительные ошибки синтаксиса, модуль всё равно будет перезагружен```|| эх вот бы проказник написал юнит-тесты для модулей ||', color = 0xff8000))
        locale = get_locale(ctx.author.id)
        return await ctx.send(embed = discord.Embed(description = (get_command_help(locale, command)), color = 0xff8000))

    @commands.command()
    async def status(self, ctx: commands.Context, target = 'list'):
        if ctx.author.id not in self.client.owner_ids:
            raise commands.NotOwner()
        cogs = ['Cephalon', 'Embeds', 'Fun', 'Mod', 'Misc', 'Music', 'sCephalon', 'sEmbeds', 'sFun', 'sMod', 'sMisc']
        if target == 'list':
            now = discord.utils.utcnow()
            up_time = now - uptime
            hours, remainder = divmod(up_time.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            emb = discord.Embed(title = 'Состояние бота', description = '`🟢` - модуль активен\n`🟡` - модуль активен, но какая-то команда отключена\n`🔴` - модуль отключён или выдаёт исключение', color = 0xff8000)
            emb.add_field(name = 'Задержка:', value = f'`{'🔴 ' if round(self.client.latency * 1000) >= 180 else '🟡 ' if round(self.client.latency * 1000) >= 150 else ''}{round(self.client.latency * 1000)} ms`')
            emb.add_field(name = 'Время запуска:', value = f'`{(uptime + timedelta(hours = 3)).strftime("%d.%m.%Y %H:%M:%S")}`')
            emb.add_field(name = 'Время в сети:', value = f'`{hours} ч, {minutes} м, {seconds} с`')
            emb.add_field(name = 'Количество серверов:', value = f'`{len(self.client.guilds)}`')
            emb.add_field(name = 'Количество пользователей:', value = f'`{len(self.client.users)}`')
            emb.add_field(name = 'Количество активных модулей:', value = f'`{len(self.client.cogs)}`')
            emb.add_field(name = '**Состояние модулей**:', value = '\n'.join([f'{"`🟢`" if module in self.client.cogs and module in cogs and all(command.enabled for command in self.client.get_cog(module).get_commands()) else '`🟡`' if module in self.client.cogs and any(command.enabled for command in self.client.get_cog(module).get_commands()) else '`🔴`'} `{module}`' for module in cogs]), inline = False)
            emb.set_footer(text = 'Cephalon Cy ©️ Sus&Co\n2020 - Present')
            return await ctx.send(embed = emb)
        else:
            if target not in cogs:
                if target not in self.client.all_commands:
                    return await ctx.send(embed = discord.Embed(description = f'Объект `{target}` не найден', color = 0xff8000))
                return await ctx.send(embed = discord.Embed(description = f'{'`🟢`' if self.client.get_command(target).enabled else '`🔴`'} `{target}`', color = 0xff8000))
            if not all(command.enabled for command in self.client.get_cog(target).get_commands()) and target in self.client.cogs:
                cmds = '\n'.join([f'{'`🟢`' if command.enabled else '`🔴`'} `{command.name}`' for command in self.client.get_cog(target).get_commands()])
                return await ctx.send(embed = discord.Embed(description = f'Состояние модуля `{target}`:\n {cmds}', color = 0xff8000))
            if target in cogs and target not in self.client.cogs:
                return await ctx.send(embed = discord.Embed(description = 'Модуль отключён', color = 0xff8000))
            if target in cogs and target in self.client.cogs:
                return await ctx.send(embed = discord.Embed(description = 'Модуль активен', color = 0xff8000))

    @commands.command()
    async def uptime(self, ctx: commands.Context):
        if ctx.author.id in self.client.owner_ids:
            return await self.status(ctx)
        now = discord.utils.utcnow()
        up_time = now - uptime
        hours, remainder = divmod(up_time.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        await ctx.send(embed = discord.Embed(description = f'Я в сети уже `{hours} ч, {minutes} м, {seconds} с`', color = 0xff8000))

    @commands.command()
    async def guilds(self, ctx: commands.Context):
        if ctx.author.id not in self.client.owner_ids:
            raise commands.NotOwner()
        client_guilds = self.client.guilds
        client_guilds = '\n'.join([guild.name for guild in self.client.guilds])
        await ctx.send(embed = discord.Embed(description = f'Существую на следующих серверах ({len(self.client.guilds)}):\n{client_guilds}', color = 0xff8000))

    @commands.command()
    async def reset(self, ctx: commands.Context, command):
        if ctx.author.id not in self.client.owner_ids:
            raise commands.NotOwner()
        command = self.client.get_command(command)
        if not command.is_on_cooldown(ctx):
            return await ctx.send(embed = discord.Embed(description = 'Команда не на перезарядке', color = 0xff8000))
        await ctx.send(embed = discord.Embed(description = f'Счётчик перезарядки для `{command.name}` сброшен. Счётчик перезарядки был равен `{round(command.get_cooldown_retry_after(ctx))}` {get_plural_form(round(command.get_cooldown_retry_after(ctx))), ['секунда', 'секунды', 'секунд']}', color = 0xff8000))
        await command.reset_cooldown(ctx)

    @commands.command() # ru, gnida, en
    async def locale(self, ctx: commands.Context):
        locale = get_locale(ctx.author.id)
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
        if ctx.author.id in self.client.owner_ids:
            view.add_item(ebutton)
        view.add_item(tbutton)
        view.add_item(ibutton)
        async def rbutton_callback(interaction: discord.Interaction):
            set_locale(str(ctx.author.id), 'ru')
            return await interaction.response.edit_message(embed = discord.Embed(description = 'Ваша локаль была установлена на `ru`', color = 0xff8000), view = None)
        async def gbutton_callback(interaction: discord.Interaction):
            await interaction.response.edit_message(embed = discord.Embed(description = 'Ты бля уверен?', color = 0xff8000), view = confirm)
        async def ybutton_callback(interaction: discord.Interaction):
            set_locale(str(ctx.author.id), 'gnida')
            return await interaction.response.edit_message(embed = discord.Embed(description = 'Твоя ёбаная локаль была установлена на `gnida`!', color = 0xff8000), view = None)
        async def nbutton_callback(interaction: discord.Interaction):
            return await interaction.response.edit_message(embed = discord.Embed(description = 'Ну ок', color = 0xff8000), view = None)
        async def ebutton_callback(interaction: discord.Interaction):
            set_locale(str(ctx.author.id), 'en')
            return await interaction.response.edit_message(embed = discord.Embed(description = 'Your locale has been set to `en`', color = 0xff8000), view = None)
        async def test_callback(interaction: discord.Interaction):
            return await interaction.response.edit_message(embed = discord.Embed(description = translate(locale, 'locale_test'), color = 0xff8000), view = None)
        async def info_callback(interaction: discord.Interaction):
            return await interaction.response.edit_message(content = None, embed = discord.Embed(description = translate(locale, 'locale_info'), color = 0xb00b69), view = None)
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
        try:
            msg = await ctx.send(embed = discord.Embed(description = translate(locale, 'locale_options'), color = 0xff8000), view = view)
            await self.client.wait_for('message_edit', check = lambda message: message.author.id == ctx.author.id and message.id == msg.id, timeout = 10)
        except asyncio.TimeoutError:
            await msg.edit(embed = discord.Embed(description = 'Время вышло', color = 0xff8000), view = None)

    @commands.command()
    async def generate(self, ctx: commands.Context):
        if ctx.author.id not in self.client.owner_ids:
            raise commands.NotOwner()
        token = '-'.join([''.join([secrets.choice('QWERTYUIOPASDFGHJKLZXCVBNM1234567890') for _ in range(5)]) for _ in range(3)])
        await ctx.send(f'```{token}```')

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def info(self, ctx: commands.Context):
        emb = discord.Embed(title = 'Пару строк кода сюда, новые фишки туда', description = 'Создатели бота постоянно совершенствуют своё детище, поддерживая его в актуальном состоянии', color = 0xff8000)
        emb.set_author(name = self.client.user.name, url = 'https://warframe.fandom.com/wiki/Cephalon_Cy', icon_url = self.client.user.avatar.url)
        emb.add_field(name = 'Версия', value = '0.14.6.0')
        emb.add_field(name = 'Написан на', value = f'discord.py v{discord.__version__}\nPython v{sys.version[:7]}')
        emb.add_field(name = 'Разработчики 🇷🇺', value = '[сасиска](https://discord.com/users/338714886001524737)\n[Prokaznik](https://discord.com/users/417012231406878720)')
        emb.add_field(name = 'Обслуживаю', value = f'{len(self.client.users)} человек')
        emb.add_field(name = 'Существую на', value = f'{len(self.client.guilds)} серверах')
        emb.set_footer(text = 'Данное приложение вдохновлено игрой Warframe', icon_url = 'https://i.playground.ru/p/yVaOZNSTdgUTxmzy_qvzzQ.png')
        await ctx.send(embed = emb)

    @commands.command()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def devs(self, ctx: commands.Context):
        emb = discord.Embed(description = 'Разработчики бота, в частности члены команды Sus&Co', color = 0xff8000)
        emb.add_field(name = 'сасиска', value = 'Первичный разработчик бота, по совместительству основатель Sus&Co. Делает основную работу', inline = False)
        emb.add_field(name = 'Проказник', value = 'Причастен к созданию локали gnida, помогает с идеями для основного бота. Хоть и считается разработчиком, не имеет доступа к коду', inline = False)
        await ctx.send(embed = emb)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def invite(self, ctx: commands.Context, arg = None):
        if arg is None:
            await ctx.send(embed = discord.Embed(description = '[Ссылка](https://discord.com/oauth2/authorize?client_id=694170281270312991&permissions=8&scope=bot%20applications.commands) для приглашения Cy на сервера', color = 0xff8000))
        if arg == 'beta':
            if ctx.author.id not in self.client.owner_ids:
                raise commands.NotOwner()
            await ctx.send(embed = discord.Embed(description = '[Ссылка](https://discord.com/oauth2/authorize?client_id=764882153812787250&permissions=8&scope=bot%20applications.commands) для приглашения Cy Beta на сервера', color = 0xff8000))
        if arg == 'pro':
            if ctx.author.id not in self.client.owner_ids:
                raise commands.NotOwner()
            await ctx.send(embed = discord.Embed(description = '[Ссылка](https://discord.com/oauth2/authorize?client_id=762015251264569352&permissions=8&scope=bot%20applications.commands) для приглашения Cy PRO на сервера', color = 0xff8000))

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ping(self, ctx: commands.Context):
        message = await ctx.send(embed = discord.Embed(description = '`Получаю..`', color = 0xff8000))
        await asyncio.sleep(self.client.latency)
        await message.edit(embed = discord.Embed(description = f'Pong! `{round(self.client.latency * 1000)} ms`', color = 0xff8000))

    @commands.command()
    async def botver(self, ctx: commands.Context, version: str = '0.14.6.0'):
        with open(CWD + '\\versions.json', 'r', encoding = 'utf-8') as f:
            versions = json.load(f)
        version_data = versions[str(version)]
        await ctx.send(embed = discord.Embed(title = version, description = version_data, color = 0x2f3136))

async def setup(client):
    await client.add_cog(Cephalon(client))
