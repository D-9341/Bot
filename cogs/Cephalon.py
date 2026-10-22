import asyncio
import json
import secrets
import sys
from typing import cast

import discord
from discord.ext import commands

from cogs.Constants import LocalesManager, colors
from functions import get_locale, get_plural_form, set_locale, translate
from main import cogs, owner_commands, uptime, CWD

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

    @commands.command(aliases = ['?', 'негр'])
    async def help(self, ctx: commands.Context, command: str = None, locale: str = None):
        if locale is not None and locale not in LocalesManager.get_all_locales():
            return await ctx.send(embed = discord.Embed(description = 'Заданная локаль не существует', color = colors.ERROR))
        if command is None:
            emb = discord.Embed(description = 'Все доступные команды', color = colors.JDH)
            emb.set_author(name = self.client.user.name, url = 'https://discord.com/api/oauth2/authorize?client_id=694170281270312991&permissions=8&scope=bot%20applications.commands')
            emb.add_field(name = 'Cephalon', value = '`botver`, `devs`, `help`, `info`, `invite`, `locale`, `ping`, `uptime`', inline = False)
            emb.add_field(name = 'Embeds', value = '`content`, `edit`, `say`', inline = False)
            emb.add_field(name = 'Fun', value = '`aghanim`, `dotersbrain`, `leaderboard`, `roulette`, `settings`', inline = False)
            emb.add_field(name = 'Mod', value = '`ban`, `clear`, `dm`, `deaf`, `give`, `kick`, `mute`, `take`, `timeout`, `undeaf`, `unmute`', inline = False)
            emb.add_field(name = 'Misc', value = '`about`, `avatar`, `coinflip`, `roll`, `roleinfo`, `rolemembers`, `serverinfo`', inline = False)
            # emb.add_field(name = 'Music', value = '`join`, `leave`, `play`, `pause`, `resume`, `stop`') # , `volume`
            emb.add_field(name = 'ᅠ', value = 'Указанные разрешения необходимы для исполнителя команды если не указано другого', inline = False)
            emb.add_field(name = 'ᅠ', value = 'Не используйте `[] <> /` при написании команды', inline = False)
            emb.add_field(name = 'ᅠ', value = '**Используйте** `cy/help [команда]` **для подробностей использования.**\n\n**[Ссылка-приглашение](https://discord.com/api/oauth2/authorize?client_id=694170281270312991&permissions=8&scope=bot%20applications.commands) | [Веб-документация](https://d-9341.github.io/)**', inline = False)
            emb.set_footer(text = 'Cephalon Cy ©️ Sus&Co\n2020 - Present')
            return await ctx.send(embed = emb)
        if ctx.author.id in self.client.owner_ids and command in owner_commands:
            if command == 'list':
                return await ctx.send(embed = discord.Embed(description = f'```{', '.join(owner_commands)}```', color = colors.JDH))
            if command == 'guilds':
                return await ctx.send(embed = discord.Embed(description = '```py\ncy/guilds\n\nПоказывает список серверов, на которых находится бот```', color = colors.JDH))
            if command == 'reset':
                return await ctx.send(embed = discord.Embed(description = '```py\ncy/reset <команда>\n\nСбрасывает счётчик перезарядки команды для исполнителя```', color = colors.JDH))
            if command == 'status':
                return await ctx.send(embed = discord.Embed(description = '```py\ncy/status\n\nПоказывает состояние бота и его модулей. Если какой-либо модуль неисправен, будет выведено соответствующее сообщение```', color = colors.JDH))
            if command == 'generate':
                return await ctx.send(embed = discord.Embed(description = '```py\ncy/generate\n\nСоздаёт случайный код```', color = colors.JDH))
            if command == 'invite':
                return await ctx.send(embed = discord.Embed(description = '```py\ncy/invite [beta/pro]\n\nПоказывает ссылку для приглашения бота. beta - бета-версия, pro - про-версия```', color = colors.JDH))
            if command == 'tts':
                return await ctx.send(embed = discord.Embed(description = '```py\ncy/tts <текст>\n\nПроизношение текста с помощью АПИ гугла```', color = colors.JDH))
        locale = get_locale(ctx.author.id) if not locale else locale
        return await ctx.send(embed = discord.Embed(description = translate(locale, f'{command}_help'), color = colors.JDH))

    @commands.command()
    async def status(self, ctx: commands.Context, target = 'list'):
        if ctx.author.id not in self.client.owner_ids:
            raise commands.NotOwner()
        if target == 'list':
            now = discord.utils.utcnow()
            up_time = now - uptime
            days, remainder = divmod(up_time.days, 365)
            hours, remainder = divmod(remainder, 24)
            minutes, seconds = divmod(remainder, 60)
            emb = discord.Embed(title = 'Состояние бота', description = '`🟢` - модуль активен\n`🟡` - модуль активен с отключёнными командами\n`🔴` - модуль отключён или выдаёт исключение', color = colors.JDH)
            emb.add_field(name = 'Задержка:', value = f'`{'🔴 ' if round(self.client.latency * 1000) >= 180 else '🟡 ' if round(self.client.latency * 1000) >= 150 else ''}{round(self.client.latency * 1000)} ms`')
            emb.add_field(name = 'Время запуска:', value = f'<t:{int((uptime).timestamp())}:S>')
            emb.add_field(name = 'Время в сети:', value = f'`{days} д, {hours} ч, {minutes} м, {seconds} с`')
            emb.add_field(name = 'Количество серверов:', value = f'`{len(self.client.guilds)}`')
            emb.add_field(name = 'Количество пользователей:', value = f'`{len(self.client.users)}`')
            emb.add_field(name = 'Количество активных модулей:', value = f'`{len(self.client.cogs)}`')
            emb.add_field(name = '**Состояние модулей**:', value = '\n'.join([f'{"`🟢`" if module in self.client.cogs and module in cogs and all(command.enabled for command in self.client.get_cog(module).get_commands()) else '`🟡`' if module in self.client.cogs and any(command.enabled for command in self.client.get_cog(module).get_commands()) else '`🔴`'} `{module}`' for module in cogs]), inline = False)
            emb.set_footer(text = 'Cephalon Cy ©️ Sus&Co\n2020 - Present')
            return await ctx.send(embed = emb)
        else:
            if target not in cogs:
                if target not in self.client.all_commands:
                    return await ctx.send(embed = discord.Embed(description = f'Объект `{target}` не найден', color = colors.JDH))
                return await ctx.send(embed = discord.Embed(description = f'{'`🟢`' if self.client.get_command(target).enabled else '`🔴`'} `{target}`', color = colors.JDH))
            if not all(command.enabled for command in self.client.get_cog(target).get_commands()) and target in self.client.cogs:
                cmds = '\n'.join([f'{'`🟢`' if command.enabled else '`🔴`'} `{command.name}`' for command in self.client.get_cog(target).get_commands()])
                return await ctx.send(embed = discord.Embed(description = f'Состояние модуля `{target}`:\n {cmds}', color = colors.JDH))
            if target in cogs and target not in self.client.cogs:
                return await ctx.send(embed = discord.Embed(description = 'Модуль полностью отключён', color = colors.JDH))
            if target in cogs and target in self.client.cogs:
                return await ctx.send(embed = discord.Embed(description = 'Модуль полностью активен', color = colors.JDH))

    @commands.command()
    async def uptime(self, ctx: commands.Context):
        if ctx.author.id in self.client.owner_ids:
            return await self.status(ctx)
        now = discord.utils.utcnow()
        up_time = now - uptime
        hours, remainder = divmod(up_time.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        await ctx.send(embed = discord.Embed(description = f'Я в сети уже `{hours} ч, {minutes} м, {seconds} с`', color = colors.JDH))

    @commands.command()
    async def guilds(self, ctx: commands.Context):
        if ctx.author.id not in self.client.owner_ids:
            raise commands.NotOwner()
        client_guilds = self.client.guilds
        client_guilds = '\n'.join([guild.name for guild in self.client.guilds])
        await ctx.send(embed = discord.Embed(description = f'Существую на следующих серверах ({len(self.client.guilds)}):\n{client_guilds}', color = colors.JDH))

    @commands.command()
    async def reset(self, ctx: commands.Context, command: str):
        if ctx.author.id not in self.client.owner_ids:
            raise commands.NotOwner()
        cmd = self.client.get_command(command)
        if not cmd:
            return await ctx.send(embed = discord.Embed(description = 'Команда не найдена', color = colors.JDH))
        if not cmd.is_on_cooldown(ctx):
            return await ctx.send(embed = discord.Embed(description = 'Команда не на перезарядке', color = colors.JDH))
        retry_after = round(cmd.get_cooldown_retry_after(ctx))
        await ctx.send(embed = discord.Embed(description = f'Счётчик перезарядки для `{cmd.name}` сброшен на `{retry_after}` {get_plural_form(retry_after, ["секунде", "секундах", "секунде"])}', color = colors.JDH))
        cmd.reset_cooldown(ctx)

    @commands.command()
    async def locale(self, ctx: commands.Context):
        locale = get_locale(ctx.author.id)
        available_locales = LocalesManager.get_all_locales()
        LOCALES_CONFIG = {}
        for loc in available_locales:
            config = {
                'button_label': loc.upper(),
                'confirm_message': translate(loc, 'locale_test'),
                'style': discord.ButtonStyle.gray
            }
            if loc == 'gnida':
                config.update({
                    'style': discord.ButtonStyle.red,
                    'confirmation_required': True,
                    'confirmation_message': 'Ты бля уверен?' if locale != 'en' else 'Are you fucking sure?'
                })
            elif loc == 'gnida_lite':
                config.update({
                    'confirmation_required': True,
                    'confirmation_message': 'Ты реально уверен?' if locale != 'en' else 'Are you really sure?'
                })
            elif loc == 'en':
                config.update({
                    'owner_only': True
                })
            LOCALES_CONFIG[loc] = config
        SPECIAL_BUTTONS = {
            'test': {
                'label': lambda loc: 'TEST' if loc == 'en' else 'ТЕСТ',
                'style': discord.ButtonStyle.gray
            },
            'info': {
                'label': lambda loc: 'INFO' if loc == 'en' else 'ИНФО', 
                'style': discord.ButtonStyle.gray
            }
        }
        locale_buttons = {}
        view = discord.ui.View(timeout = 30)
        for locale_code, config in LOCALES_CONFIG.items():
            config = cast(dict, config)
            if config.get('owner_only', False) and ctx.author.id not in self.client.owner_ids:
                continue
            button = discord.ui.Button(label = config['button_label'], style = config['style'], disabled = (locale == locale_code))
            view.add_item(button)
            locale_buttons[locale_code] = (button, config)

        special_buttons = {}
        for button_id, config in SPECIAL_BUTTONS.items():
            button = discord.ui.Button(label = config['label'](locale), style = config['style'])
            view.add_item(button)
            special_buttons[button_id] = button

        async def test_callback(interaction: discord.Interaction):
            if interaction.user.id != ctx.author.id:
                return await interaction.response.send_message("Эта кнопка не для тебя!", ephemeral = True)
            current_locale = get_locale(ctx.author.id)
            await interaction.response.edit_message(embed = discord.Embed(description = translate(current_locale, 'locale_test'), color = colors.JDH), view = None)

        async def info_callback(interaction: discord.Interaction):
            if interaction.user.id != ctx.author.id:
                return await interaction.response.send_message("Эта кнопка не для тебя!", ephemeral = True)
            current_locale = get_locale(ctx.author.id)
            await interaction.response.edit_message(content = None, embed = discord.Embed(description = translate(current_locale, 'locale_info'), color = colors.LO), view = None)

        async def create_locale_callback(locale_code, config):
            confirm_view = discord.ui.View(timeout = 30)
            yes_label = translate(locale, 'roulette_yes')
            no_label = translate(locale, 'roulette_no')
            yes_button = discord.ui.Button(label=yes_label, style=discord.ButtonStyle.red)
            no_button = discord.ui.Button(label=no_label, style=discord.ButtonStyle.gray)
            confirm_view.add_item(yes_button)
            confirm_view.add_item(no_button)
            
            async def yes_callback(interaction: discord.Interaction):
                if interaction.user.id != ctx.author.id:
                    return await interaction.response.send_message("Эта кнопка не для тебя!", ephemeral = True)
                set_locale(ctx.author.id, locale_code)
                await interaction.response.edit_message(embed = discord.Embed(description = config['confirm_message'], color = colors.JDH), view = None)

            async def no_callback(interaction: discord.Interaction):
                if interaction.user.id != ctx.author.id:
                    return await interaction.response.send_message("Эта кнопка не для тебя!", ephemeral=True)
                current_locale = get_locale(ctx.author.id)
                no_message = translate(current_locale, 'roulette_play_cancel')
                await interaction.response.edit_message(embed = discord.Embed(description = no_message, color = colors.JDH), view = None)

            yes_button.callback = yes_callback
            no_button.callback = no_callback

            async def locale_callback(interaction: discord.Interaction):
                if interaction.user.id != ctx.author.id:
                    return await interaction.response.send_message("Эта кнопка не для тебя!", ephemeral = True)
                    
                if config.get('confirmation_required', False):
                    await interaction.response.edit_message(embed = discord.Embed(description = config['confirmation_message'], color = colors.JDH), view = confirm_view)
                else:
                    set_locale(ctx.author.id, locale_code)
                    await interaction.response.edit_message(embed = discord.Embed(description = config['confirm_message'], color = colors.JDH), view = None)
            return locale_callback

        for locale_code, (button, config) in locale_buttons.items():
            button = cast(discord.ui.Button, button)
            callback_func = await create_locale_callback(locale_code, config)
            button.callback = callback_func

        special_buttons['test'] = cast(discord.ui.Button, special_buttons['test'])
        special_buttons['info'] = cast(discord.ui.Button, special_buttons['info'])
        special_buttons['test'].callback = test_callback
        special_buttons['info'].callback = info_callback

        try:
            msg = await ctx.send(embed = discord.Embed(description = translate(locale, 'locale_options'), color = colors.JDH), view = view)
            await self.client.wait_for('interaction', check = lambda i: i.user.id == ctx.author.id, timeout = 30)

        except asyncio.TimeoutError:
            current_locale = get_locale(ctx.author.id)
            timeout_msg = translate(current_locale, 'roulette_invite_timeout')
            try:
                await msg.edit(embed = discord.Embed(description = timeout_msg, color = colors.JDH), view = None)
            except:
                pass

    @commands.command()
    async def generate(self, ctx: commands.Context):
        if ctx.author.id not in self.client.owner_ids:
            raise commands.NotOwner()
        token = '-'.join([''.join([secrets.choice('QWERTYUIOPASDFGHJKLZXCVBNM1234567890') for _ in range(5)]) for _ in range(3)])
        await ctx.send(f'```{token}```')

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def info(self, ctx: commands.Context):
        emb = discord.Embed(title = 'Пару строк кода сюда, новые фишки туда', description = 'Создатели бота постоянно совершенствуют своё детище, поддерживая его в актуальном состоянии', color = colors.JDH)
        emb.set_author(name = self.client.user.name, url = 'https://warframe.fandom.com/wiki/Cephalon_Cy', icon_url = self.client.user.avatar.url)
        emb.add_field(name = 'Версия', value = '1.0')
        emb.add_field(name = 'Написан на', value = f'discord.py v{discord.__version__}\nPython v{sys.version[:7]}')
        emb.add_field(name = 'Разработчики 🇷🇺', value = '[сасиска](https://discord.com/users/338714886001524737)\n[Prokaznik](https://discord.com/users/417012231406878720)')
        emb.add_field(name = 'Обслуживаю', value = f'{len(self.client.users)} человек')
        emb.add_field(name = 'Существую на', value = f'{len(self.client.guilds)} серверах')
        emb.set_footer(text = 'Данное приложение вдохновлено игрой Warframe', icon_url = 'https://i.playground.ru/p/yVaOZNSTdgUTxmzy_qvzzQ.png')
        await ctx.send(embed = emb)

    @commands.command()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def devs(self, ctx: commands.Context):
        emb = discord.Embed(description = 'Разработчики бота, в частности члены команды Sus&Co', color = colors.JDH)
        emb.add_field(name = 'сасиска', value = 'Первичный разработчик бота, по совместительству основатель Sus&Co. Делает основную работу', inline = False)
        emb.add_field(name = 'Проказник', value = 'Причастен к созданию локали gnida, помогает с идеями для основного бота. Хоть и считается разработчиком, не имеет доступа к коду', inline = False)
        await ctx.send(embed = emb)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def invite(self, ctx: commands.Context, arg = None):
        if arg is None:
            await ctx.send(embed = discord.Embed(description = '[Ссылка](https://discord.com/oauth2/authorize?client_id=694170281270312991&permissions=8&scope=bot%20applications.commands) для приглашения Cy на сервера', color = colors.JDH))
        if arg == 'beta':
            if ctx.author.id not in self.client.owner_ids:
                raise commands.NotOwner()
            await ctx.send(embed = discord.Embed(description = '[Ссылка](https://discord.com/oauth2/authorize?client_id=764882153812787250&permissions=8&scope=bot%20applications.commands) для приглашения Cy Beta на сервера', color = colors.JDH))
        if arg == 'pro':
            if ctx.author.id not in self.client.owner_ids:
                raise commands.NotOwner()
            await ctx.send(embed = discord.Embed(description = '[Ссылка](https://discord.com/oauth2/authorize?client_id=762015251264569352&permissions=8&scope=bot%20applications.commands) для приглашения Cy PRO на сервера', color = colors.JDH))

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ping(self, ctx: commands.Context):
        if ctx.author.id in self.client.owner_ids:
            return await self.status(ctx)
        message = await ctx.send(embed = discord.Embed(description = '`Получаю..`', color = colors.JDH))
        await asyncio.sleep(self.client.latency)
        await message.edit(embed = discord.Embed(description = f'Pong! `{round(self.client.latency * 1000)} ms`', color = colors.JDH))

    @commands.command()
    async def botver(self, ctx: commands.Context, version: str = '1.0'):
        with open(CWD / 'versions.json', 'r', encoding = 'utf-8') as f:
            versions = json.load(f)
        version_data = versions[str(version)]
        await ctx.send(embed = discord.Embed(title = version, description = version_data, color = colors.DEFAULT))

async def setup(client):
    await client.add_cog(Cephalon(client))
