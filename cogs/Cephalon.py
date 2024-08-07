import asyncio
import secrets
import sys

import discord
from functions import translate, get_locale, set_locale
from discord.ext import commands

guilds = [693929822543675455, 735874149578440855, 818758712163827723]

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
            emb.add_field(name = 'Misc', value = '`about`, `avatar`, `coinflip`, `guild`, `roll`, `roleinfo`, `rolemembers`, `someone`', inline = False)
            #emb.add_field(name = 'Music', value = '`join`, `leave`, `play`, `pause`, `resume`, `volume`')
            emb.add_field(name = 'ᅠ', value = 'Указанные разрешения необходимы для исполнителя команды если не указано другого', inline = False)
            emb.add_field(name = 'ᅠ', value = 'Не используйте `[] <> /` при написании команды', inline = False)
            emb.add_field(name = 'ᅠ', value = '**Используйте** `cy/help [команда]` **для подробностей использования.**\n\n**[Ссылка-приглашение](https://discord.com/api/oauth2/authorize?client_id=694170281270312991&permissions=8&scope=bot%20applications.commands)**', inline = False)
            emb.set_footer(text = 'Cephalon Cy ©️ Sus&Co\n2020 - Present')
            return await ctx.send(embed = emb)
        #elif command == 'play':
        #    await ctx.send('```python\ncy/play <ссылка на видео YouTube>\nСсылка должна быть только с YouTube\n\n<> - обязательно```')
        #elif command == 'volume':
        #    await ctx.send('```python\ncy/volume <громкость>\nГромкость должна быть в пределе от 0 до 100\n\n<> - обязательно```')
        elif command == 'dotersbrain':
            await ctx.send('```python\ncy/dotersbrain\n\nСлова и ответы к ним: чё - хуй через плечо, а - хуй на, да - пизда, нет - пидора ответ, ок - хуй намок\n\nБоту необходимы разрешения - управлять сообщениями```')
        elif command == 'roulette':
            await ctx.send('```python\ncy/roulette [@упоминание/имя/ID/leaderboard]\n\nСигарета - восстанавливает одно очко здоровья\nНожовка по металлу - следующий патрон нанесёт в 2 раза больше урона\nПиво - вы передёргиваете затвор\nЛупа - посмотреть, какой патрон сейчас в патроннике\nНаручники - надевший игрок пропускает следующий ход\nСтарый телефон - ответивший приоткроет завесу будущего\nПодозрительные таблетки - с 50% шансом вы можете получить 2 очка здоровья или потерять одно\nИнвертер - текущий патрон меняется на противоположный: боевой -> холостой, холостой -> боевой\nШприц адреналина - вы можете выбрать один предмет противника и сразу его использовать, кроме самого шприца\nПри начале игры вам будет предложено перейти в другой канал\n\n[] - опционально\nБоту необходимы разрешения - управление каналами```')
        elif command == 'timeout':
            await ctx.send('```python\ncy/timeout <@упоминание/имя/ID> [причина]\n\n[] - опционально, <> - обязательно, / - или\nНеобходимы разрешения - управлять каналами\nБоту необходимы разрешения - отправлять участников подумать над своим поведением```')
        elif command == 'deaf':
            await ctx.send('```python\ncy/deaf <@упоминание/имя/ID> [причина]\nВ отличии от команды mute, бот будет заглушать людей в голосовом канале с ролью **Deafened**\n\n[] - опционально, <> - обязательно, / - или\nНеобходимы разрешения - управлять каналами\nБоту необходимы разрешения - управлять ролями```')
        elif command == 'undeaf':
            await ctx.send('```python\ncy/undeaf <@упоминание/имя/ID> [причина]\n\n[] - опционально, <> - обязательно, / - или\nНеобходимы разрешения - управлять каналами\nБоту необходимы разрешения - управлять ролями```')
        elif command == 'roll':
            await ctx.send('```python\ncy/roll [от/1d20] [до]\ncy/roll 80 (0-80)\ncy/roll 26 90 (26-90)\ncy/roll (0-100)\ncy/roll 1d6\n\nЕсли не указано [до], [от] станет [до]\nВозможно бросание дайсов, формат - количество дайсов d количество граней дайсов: 1d20, 8d8, 4d4, 20d20\nМаксимальное количество граней и дайсов - 20\nКоличество граней не привязано к физическим вариантам дайсов\nПри броске дайсов не указывайте [до]!\n[] - опционально, / - или```')
        elif command == 'about':
            await ctx.send('```python\ncy/about [@упоминание/имя/ID]\n\n[] - опционально, / - или```')
        elif command == 'avatar':
            await ctx.send('```python\ncy/avatar [@упоминание/имя/ID]\n\n[] - опционально, / - или```')
        elif command == 'ban':
            await ctx.send('```python\ncy/ban <@упоминание/имя/ID> [причина/--soft --reason]\ncy/ban 185476724627210241 --soft --reason лошара\ncy/ban @сасиска чмо\ncy/ban "Sgt White" --soft\n\nПри использовании --soft обязательно указывать --reason после него, однако можно не использовать --reason\n[] - опционально, <> - обязательно, / - или\nНеобходимы разрешения боту и исполнителю - банить участников```')
        elif command == 'content' or command == 'ctx':
            await ctx.send('```python\ncy/content <ID> [канал, в котором находится сообщение] [--edit]\n\nЭта команда выведет полный контент сообщения, т.о. можно быстро скопировать запрошенное сообщение с сохранением всего форматирования\nЕсли применено к сообщению с эмбедом, вернётся контент некоторых полей, включая описание, заголовок, футер, ссылки на картинки и цвет\nВ случае с сообщениями бота возвращает контент в формате cy/say *то, что надо написать для повторения запрошенного сообщения*\nПолностью работает с эмбедами от лица бота, однако эмбеды из других источников будут неполными\nАргумент --edit вернёт сообщение в формате cy/edit *id сообщения* *то, что нужно написать для повторения запрошенного сообщения*\n\n[] - опционально, <> - обязательно```')
        elif command == 'clear':
            await ctx.send('```python\ncy/clear <количество> [диапазон] [фильтр]\ncy/clear 10\ncy/clear 50 --everyone хыха\ncy/clear 30 --bots\ncy/clear 15 --users\ncy/clear 5 --silent\ncy/clear 200 "--silent --everyone"\n\n--everyone удалит сообщения от всех\n--bots удалит сообщения только от ботов\n--users удалит сообщения только от людей\n--silent не покажет результаты удаления сообщений. Учтите, что если нужно будет подтверждение удаления - оно будет показано\nПри указании фильтра необходимо писать именно то, что написано в сообщении - команда чувствительна к регистру\n\nПри указании диапазона не будет удалено столько сообщений, сколько было указано, будет удалено столько, сколько будет найдено в пределах заданного количества сообщений\nДопустим cy/clear 10 --bots\nЕсли сообщения от ботов и людей чередуются, будет удалено лишь то кол-во сообщений от ботов, что было найдено в указанном пределе 10. Это сделано намеренно, но может быть изменено в будущем\n\nСообщения старше 2 недель будут удалены не сразу - лимит discord API\nПри удалении более 100 сообщений нужно подтверждение владельца сервера.\nТолько владелец сервера может удалять от 250 сообщений за раз.\nНе более 300 за раз!\n\n[] - опционально, <> - обязательно, / - или\nНеобходимы разрешения - права администратора\nБоту необходимы разрешения - управлять сообщениями```')
        elif command == 'dm':
            await ctx.send('```python\ncy/dm <@упоминание/имя/ID> <текст>\n\n<> - обязательно, / - или\nНеобходимы разрешения - просматривать лог аудита\nУчтите, что бот может не отправить сообщение, если у человека закрыты личные сообщения```')
        elif command == 'say':
            await ctx.send('```python\ncy/say [обычный текст] [&t title текст] [&d description текст] [&th ссылка на картинку справа] [&img ссылка на картинку снизу] [&f footer текст] [&c цвет в HEX коде] [&msg сообщение над эмбедом]\ncy/say &t Заголовок &d Описание\ncy/say [текст]\nУчтите, что если вы захотите упомянуть роль с использованием какого либо аргумента текст не будет показан из-за способа упоминания ролей в Discord\nВсе аргументы являются необязательными\n\n[] - опционально```')
        elif command == 'edit':
            await ctx.send('```python\ncy/edit <ID> [обычный текст] [&t title текст] [&d description текст] [&f footer текст] [&c цвет в HEX коде] [&th ссылка на картинку справа] [&img ссылка на картинку снизу]\ncy/edit <ID> [текст]\ncy/edit <ID> --clean\ncy/edit <ID> --noembed\ncy/edit <ID> --delete\n\n--clean удалит контент над эмбедом\n--noembed удалит эмбед\n--delete удалит сообщение\n\nИспользование --clean и --noembed одновременно невозможно\nЕсли у сообщения есть эмбед и в команде нет агрументов, автоматически будет заменён &msg\nЗаголовок, описание и цвет будут взяты со старого эмбеда, если таковой имеется и эти аргументы не были указаны\nДля очистки какого-либо поля укажите аргумент и оставьте его пустым:\ncy/edit <ID> &d\nЭто опустошит описание\n\n[] - опционально, <> - обязательно\nНеобходимы разрешения - управлять сообщениями```')
        elif command == 'give':
            await ctx.send('```python\ncy/give <@упоминание/имя/ID> <@роль/имя роли/ID роли>\n\n<> - обязательно, / - или\nНеобходимы разрешения - управлять каналами```')
        elif command == 'kick':
            await ctx.send('```python\ncy/kick <@упоминание/имя/ID> [причина]\n\n[] - опционально, <> - обязательно, / - или\nНеобходимы разрешения исполнителю и боту - выгонять участников```')
        elif command == 'mute':
            await ctx.send('```python\ncy/mute <@упоминание/имя/ID> [причина]\n\n[] - опционально, <> - обязательно, / - или\nНеобходимы разрешения - просматривать лог аудита\nБоту необходимы разрешения - управлять ролями```')
        elif command == 'roleinfo':
            await ctx.send('```python\ncy/roleinfo <@роль/имя роли/ID роли>\n\n<> - обязательно, / - или```')
        elif command == 'take':
            await ctx.send('```python\ncy/take <@упоминание/имя/ID> <@роль/имя роли/ID роли>\n\n<> - обязательно, / - или\nНеобходимы разрешения - управлять каналами\nБоту необходимы разрешения - управлять ролями```')
        elif command == 'someone':
            await ctx.send('```python\ncy/someone <текст>\n\n<> - обязательно```')
        elif command == 'unmute':
            await ctx.send('```python\ncy/unmute <@упоминание/имя/ID> [причина]\n\n[] - опционально, <> - обязательно, / - или\nНеобходимы разрешения - управлять каналами\nБоту необходимы разрешения - управлять ролями```')
        elif command == 'help':
            await ctx.send('```python\ncy/help [команда]\n\n[] - опционально```')
        else:
            emb = discord.Embed(description = f'Команда `{command}` не обнаружена или выполняется лишь её написанием.', color = 0xff8000)
            await ctx.send(embed = emb)

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
        else:
            guilds = self.client.guilds
            guilds = '\n'.join([guild.name for guild in self.client.guilds])
            await ctx.send(embed = discord.Embed(description = f'Существую на следующих серверах ({len(self.client.guilds)}):\n{guilds}', color = 0xff8000))

    @commands.command()
    async def reset(self, ctx, command):
        if ctx.author.id not in self.client.owner_ids:
            raise commands.NotOwner()
        else:
            command = self.client.get_command(command)
            if not command.is_on_cooldown(ctx):
                return await ctx.send(embed = discord.Embed(description = 'Команда не на перезарядке.', color = 0xff8000))
            await ctx.send(embed = discord.Embed(description = f'Счётчик перезарядки для `{command.name}` сброшен. Счётчик перезарядки был равен `{round(command.get_cooldown_retry_after(ctx))}` секунд.', color = 0xff8000))
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
            return await interaction.response.edit_message(embed = discord.Embed(description = 'Ваша локаль была установлена на `ru`.', color = 0xff8000), view = None)
        async def gbutton_callback(interaction):
            await interaction.response.edit_message(embed = discord.Embed(description = 'Ты бля уверен?', color = 0xff8000), view = confirm)
        async def ybutton_callback(interaction):
            set_locale(str(ctx.author.id), 'gnida')
            return await interaction.response.edit_message(embed = discord.Embed(description = 'Твоя ёбаная локаль была установлена на `gnida`!', color = 0xff8000), view = None)
        async def nbutton_callback(interaction):
            return await interaction.response.edit_message(embed = discord.Embed(description = 'Ну ок', color = 0xff8000), view = None)
        async def ebutton_callback(interaction):
            set_locale(str(ctx.author.id), 'en')
            return await interaction.response.edit_message(embed = discord.Embed(description = 'Your locale has been set to `en`.', color = 0xff8000), view = None)
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
        else:
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
            emb = discord.Embed(description = '[Ссылка](https://discord.com/oauth2/authorize?client_id=694170281270312991&permissions=8&scope=bot%20applications.commands) для приглашения Cy на сервера.', color = 0xff8000)
            await ctx.send(embed = emb)
        if arg == 'beta':
            emb = discord.Embed(description = '[Ссылка](https://discord.com/oauth2/authorize?client_id=764882153812787250&permissions=8&scope=bot%20applications.commands) для приглашения Cy Beta на сервера.', color = 0xff8000)
            await ctx.send(embed = emb)
        if arg == 'pro':
            if ctx.author.id not in self.client.owner_ids:
                raise commands.NotOwner()
            else:
                emb = discord.Embed(description = '[Ссылка](https://discord.com/oauth2/authorize?client_id=762015251264569352&permissions=8&scope=bot%20applications.commands) для приглашения Cy PRO на сервера.', color = 0xff8000)
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