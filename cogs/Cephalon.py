import asyncio
import secrets
import sys

import discord
from functions import translate, get_locale, set_locale, get_plural_form, get_command_help
from discord.ext import commands

uptime = discord.utils.utcnow()

class GrayButton(discord.ui.Button):
    def __init__(self, label):
        super().__init__(label = label, style = discord.ButtonStyle.gray)

class RedButton(discord.ui.Button):
    def __init__(self, label):
        super().__init__(label = label, style = discord.ButtonStyle.red)

class Cephalon(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Модуль Cephalon загружен')

    @commands.command()
    async def help(self, ctx, command = None):
        if command is None:
            emb = discord.Embed(description = 'Все доступные команды', color = 0xff8000)
            emb.set_author(name = self.client.user.name, url = 'https://discord.com/api/oauth2/authorize?client_id=694170281270312991&permissions=8&scope=bot%20applications.commands')
            emb.add_field(name = 'Cephalon', value = '`botver`, `devs`, `help`, `info`, `invite`, `locale`, `ping`, `uptime`', inline = False)
            emb.add_field(name = 'Embeds', value = '`content`, `edit`, `say`', inline = False)
            emb.add_field(name = 'Fun', value = '`aghanim`, `dotersbrain`, `roulette`', inline = False)
            emb.add_field(name = 'Mod', value = '`ban`, `clear`, `dm`, `deaf`, `give`, `kick`, `mute`, `take`, `timeout`, `undeaf`, `unmute`', inline = False)
            emb.add_field(name = 'Misc', value = '`about`, `avatar`, `coinflip`, `roll`, `roleinfo`, `rolemembers`, `serverinfo`, `someone`', inline = False)
            emb.add_field(name = 'Music', value = '`join`, `leave`, `play`, `pause`, `resume`, `stop`') # , `volume`
            emb.add_field(name = 'ᅠ', value = 'Указанные разрешения необходимы для исполнителя команды если не указано другого', inline = False)
            emb.add_field(name = 'ᅠ', value = 'Не используйте `[] <> /` при написании команды', inline = False)
            emb.add_field(name = 'ᅠ', value = '**Используйте** `cy/help [команда]` **для подробностей использования.**\n\n**[Ссылка-приглашение](https://discord.com/api/oauth2/authorize?client_id=694170281270312991&permissions=8&scope=bot%20applications.commands)**', inline = False)
            emb.set_footer(text = 'Cephalon Cy ©️ Sus&Co\n2020 - Present')
            return await ctx.send(embed = emb)
        locale = get_locale(ctx.author.id)
        return await ctx.send(embed = discord.Embed(description = (get_command_help(locale, command)), color = 0xff8000))

    @commands.command()
    async def uptime(self, ctx):
        now = discord.utils.utcnow()
        up_time = now - uptime
        hours, remainder = divmod(up_time.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        await ctx.send(embed = discord.Embed(description = f'Я в сети уже `{hours} ч, {minutes} м, {seconds} с`', color = 0xff8000))

    @commands.command()
    async def guilds(self, ctx):
        if ctx.author.id not in self.client.owner_ids:
            raise commands.NotOwner()
        client_guilds = self.client.guilds
        client_guilds = '\n'.join([guild.name for guild in self.client.guilds])
        await ctx.send(embed = discord.Embed(description = f'Существую на следующих серверах ({len(self.client.guilds)}):\n{client_guilds}', color = 0xff8000))

    @commands.command()
    async def reset(self, ctx, command):
        if ctx.author.id not in self.client.owner_ids:
            raise commands.NotOwner()
        command = self.client.get_command(command)
        if not command.is_on_cooldown(ctx):
            return await ctx.send(embed = discord.Embed(description = 'Команда не на перезарядке', color = 0xff8000))
        await ctx.send(embed = discord.Embed(description = f'Счётчик перезарядки для `{command.name}` сброшен. Счётчик перезарядки был равен `{round(command.get_cooldown_retry_after(ctx))}` {get_plural_form(round(command.get_cooldown_retry_after(ctx))), ['секунда', 'секунды', 'секунд']}', color = 0xff8000))
        await command.reset_cooldown(ctx)

    @commands.command() # ru, gnida, en
    async def locale(self, ctx):
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
        async def rbutton_callback(interaction):
            set_locale(str(ctx.author.id), 'ru')
            return await interaction.response.edit_message(embed = discord.Embed(description = 'Ваша локаль была установлена на `ru`', color = 0xff8000), view = None)
        async def gbutton_callback(interaction):
            await interaction.response.edit_message(embed = discord.Embed(description = 'Ты бля уверен?', color = 0xff8000), view = confirm)
        async def ybutton_callback(interaction):
            set_locale(str(ctx.author.id), 'gnida')
            return await interaction.response.edit_message(embed = discord.Embed(description = 'Твоя ёбаная локаль была установлена на `gnida`!', color = 0xff8000), view = None)
        async def nbutton_callback(interaction):
            return await interaction.response.edit_message(embed = discord.Embed(description = 'Ну ок', color = 0xff8000), view = None)
        async def ebutton_callback(interaction):
            set_locale(str(ctx.author.id), 'en')
            return await interaction.response.edit_message(embed = discord.Embed(description = 'Your locale has been set to `en`', color = 0xff8000), view = None)
        async def test_callback(interaction):
            return await interaction.response.edit_message(embed = discord.Embed(description = translate(locale, 'locale_test'), color = 0xff8000), view = None)
        async def info_callback(interaction):
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
    async def generate(self, ctx):
        if ctx.author.id not in self.client.owner_ids:
            raise commands.NotOwner()
        token = '-'.join([''.join([secrets.choice('QWERTYUIOPASDFGHJKLZXCVBNM1234567890') for _ in range(5)]) for _ in range(3)])
        await ctx.send(f'```{token}```')

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def info(self, ctx):
        emb = discord.Embed(title = 'Пару строк кода сюда, новые фишки туда', description = 'Создатели бота постоянно совершенствуют своё детище, поддерживая его в актуальном состоянии', color = 0xff8000)
        emb.set_author(name = self.client.user.name, url = 'https://warframe.fandom.com/wiki/Cephalon_Cy', icon_url = self.client.user.avatar.url)
        emb.add_field(name = 'Версия', value = '0.13.0.2.21680')
        emb.add_field(name = 'Написан на', value = f'discord.py v{discord.__version__}\nPython v{sys.version[:7]}')
        emb.add_field(name = 'Разработчики 🇷🇺', value = '[сасиска](https://discord.com/users/338714886001524737)\n[Prokaznik](https://discord.com/users/417012231406878720)')
        emb.add_field(name = 'Обслуживаю', value = f'{len(self.client.users)} человек')
        emb.add_field(name = 'Существую на', value = f'{len(self.client.guilds)} серверах')
        emb.set_footer(text = 'Данное приложение вдохновлено игрой Warframe', icon_url = 'https://i.playground.ru/p/yVaOZNSTdgUTxmzy_qvzzQ.png')
        await ctx.send(embed = emb)

    @commands.command()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def devs(self, ctx):
        emb = discord.Embed(description = 'Разработчики бота, в частности члены команды Sus&Co', color = 0xff8000)
        emb.add_field(name = 'сасиска', value = 'Первичный разработчик бота, по совместительству основатель Sus&Co. Делает основную работу', inline = False)
        emb.add_field(name = 'Проказник', value = 'Причастен к созданию локали gnida, помогает с идеями для основного бота. Хоть и считается разработчиком, не имеет доступа к коду', inline = False)
        await ctx.send(embed = emb)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def invite(self, ctx, arg = None):
        if arg is None:
            emb = discord.Embed(description = '[Ссылка](https://discord.com/oauth2/authorize?client_id=694170281270312991&permissions=8&scope=bot%20applications.commands) для приглашения Cy на сервера', color = 0xff8000)
            await ctx.send(embed = emb)
        if arg == 'beta':
            emb = discord.Embed(description = '[Ссылка](https://discord.com/oauth2/authorize?client_id=764882153812787250&permissions=8&scope=bot%20applications.commands) для приглашения Cy Beta на сервера', color = 0xff8000)
            await ctx.send(embed = emb)
        if arg == 'pro':
            if ctx.author.id not in self.client.owner_ids:
                raise commands.NotOwner()
            emb = discord.Embed(description = '[Ссылка](https://discord.com/oauth2/authorize?client_id=762015251264569352&permissions=8&scope=bot%20applications.commands) для приглашения Cy PRO на сервера', color = 0xff8000)
            await ctx.send(embed = emb)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ping(self, ctx):
        emb = discord.Embed(description = '`Получаю..`', color = 0xff8000)
        emb1 = discord.Embed(description = f'Pong!  `{round(self.client.latency * 1000)} ms`', color = 0xff8000)
        message = await ctx.send(embed = emb)
        await asyncio.sleep(self.client.latency)
        await message.edit(embed = emb1)

    @commands.command()
    async def botver(self, ctx):
        emb = discord.Embed(color = 0x2f3136)
        emb.add_field(name = '0.13.0.2.21680', value = '- Была добавлена категория Fun (4 новых команды)\n- Для большинства команд была добавлена слэш (/) версия\nОт себя хочется отметить, что в категории Fun появилась НЕВЕРОЯТНАЯ команда - dotersbrain\n\nВсё ёпта, такой вот патч вышел. Следующий ждите через год (~~Завтра~~)')
        emb.set_footer(text = 'Написано разработчиком Проказник#2785')
        await ctx.send(embed = emb)

async def setup(client):
    await client.add_cog(Cephalon(client))
