import asyncio
import os
import sys

import discord
from typing import Literal
from discord import app_commands
from discord.ext import commands
from pymongo import MongoClient

PASS = os.environ.get('PASS')
cluster = MongoClient(f"mongodb+srv://cephalon:{PASS}@locale.ttokw.mongodb.net/Locale?retryWrites=true&w=majority")
collection = cluster.Locale.locale

friends = [351071668241956865, 417362845303439360]

guilds = [693929822543675455, 735874149578440855, 818758712163827723]

uptime = discord.utils.utcnow()

def reset_cooldown(command: commands.Command, message: discord.Message) -> None:
    if command._buckets.valid:
        bucket = command._buckets.get_bucket(message)
        bucket._tokens = min(bucket.rate, bucket._tokens + 1)

class View(discord.ui.View):
    def __init__(self, timeout):
        super().__init__(timeout = 5)

    async def on_timeout(self, interaction):
        await interaction.response.edit_message('Время вышло.', view = None)

class GrayButton(discord.ui.Button):
    def __init__(self, label):
        super().__init__(label = label, style = discord.ButtonStyle.gray)

class RedButton(discord.ui.Button):
    def __init__(self, label):
        super().__init__(label = label, style = discord.ButtonStyle.red)

class sCephalon(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('/ - Команды Cephalon синхронизированы')

    @app_commands.command(description = 'Помощь по командам')
    @app_commands.describe(command = 'Выберите команду, по которой нужна помощь')
    async def help(self, interaction: discord.Interaction, command: Literal['help', 'content', 'edit', 'say', 'about', 'avatar', 'roll', 'roleinfo', 'rolemembers', 'vote', 'dotersbrain', 'ban', 'dm', 'deaf', 'kick', 'give', 'mute', 'take', 'timeout', 'undeaf', 'unmute'] = None):
        if command == None:
            emb = discord.Embed(description = 'Все доступные / команды.', color = 0xff8000)
            emb.set_author(name = self.client.user.name, url = 'https://discord.com/api/oauth2/authorize?client_id=694170281270312991&permissions=8&scope=bot%20applications.commands')
            emb.add_field(name = 'Cephalon', value = '`botver`, `devs`, `help`, `info`, `invite`, `locale`, `ping`, `uptime`', inline = False)
            emb.add_field(name = 'Embeds', value = '`content`, `edit`, `say`', inline = False)
            emb.add_field(name = 'Fun', value = '`aghanim`, `dotersbrain`', inline = False)
            emb.add_field(name = 'Mod', value = '`ban`, `dm`, `deaf`, `give`, `kick`, `mute`, `take`, `timeout`, `undeaf`, `unmute`', inline = False)
            emb.add_field(name = 'Misc', value = '`about`, `avatar`, `coinflip`, `guild`, `roll`, `roleinfo`, `rolemembers`', inline = False)
            #emb.add_field(name = 'Music', value = '`join`, `leave`, `play`, `pause`, `resume`, `volume`', inline = False)
            emb.add_field(name = 'ᅠ', value = 'Указанные разрешения необходимы для исполнителя команды если не указано другого.', inline = False)
            emb.add_field(name = 'ᅠ', value = 'Не используйте `[] <> /` при написании команды.', inline = False)
            emb.add_field(name = 'ᅠ', value = '**Используйте** `/help [команда]` **для подробностей использования.**\n\n**[Ссылка-приглашение](https://discord.com/api/oauth2/authorize?client_id=694170281270312991&permissions=8&scope=bot%20applications.commands)**', inline = False)
            emb.set_footer(text = 'Cephalon Cy ©️ Sus&Co\n2020 - Present')
            await interaction.response.send_message(embed = emb)
        #elif command == 'play':
        #    await interaction.response.send_message('```python\n/play <ссылка на видео YouTube>\nСсылка должна быть только с YouTube\n\n<> - обязательно```')
        #elif command == 'volume':
        #    await interaction.response.send_message('```python\n/volume <громкость>\nГромкость должна быть в пределе от 0 до 100\n\n<> - обязательно```')
        elif command == 'dotersbrain':
            await interaction.response.send_message('```python\n/dotersbrain\n\nСлова и ответы к ним: чё - хуй через плечо, а - хуй на, да - пизда, нет - пидора ответ, ок - хуй намок```')
        elif command == 'timeout':
            await interaction.response.send_message('```python\n/timeout <@пинг/имя/ID> [причина]\n\n[] - опционально, <> - обязательно, / - или\nНеобходимы разрешения - управлять каналами```')
        elif command == 'deaf':
            await interaction.response.send_message('```python\n/deaf <@пинг/имя/ID> [причина]\nВ отличии от команды mute, бот будет заглушать людей в голосовом канале с ролью **Deafened**\n\n[] - опционально, <> - обязательно, / - или\nНеобходимы разрешения - управлять каналами```')
        elif command == 'undeaf':
            await interaction.response.send_message('```python\n/undeaf <@пинг/имя/ID> [причина]\n\n[] - опционально, <> - обязательно, / - или\nНеобходимы разрешения - управлять каналами```')
        elif command == 'roll':
            await interaction.response.send_message('```python\n/roll [от] [до]\nесли не указано [до], [от] станет [до].\n/roll 80 (0-80)\n/roll 26 90 (26-90)\n/roll (0-100)\n\n[] - опционально```')
        elif command == 'about':
            await interaction.response.send_message('```python\n/about [@пинг/имя/ID]\n\n[] - опционально, / - или```')
        elif command == 'avatar':
            await interaction.response.send_message('```python\n/avatar [@пинг/имя/ID]\n\n[] - опционально, / - или```')
        elif command == 'ban':
            await interaction.response.send_message('```python\n/ban <@пинг/имя/ID> [причина/--soft --reason]\n/ban 185476724627210241 --soft --reason лошара\n/ban @сасиска чмо\n/ban "Sgt White" --soft\n\nПри использовании --soft обязательно указывать --reason после него, однако можно не использовать --reason\n[] - опционально, <> - обязательно, / - или\nНеобходимы разрешения - банить участников```')
        elif command == 'content':
            await interaction.response.send_message('```python\ncy/content <ID> [канал, в котором находится сообщение] [--edit]\n\nЭта команда выведет полный контент сообщения, т.о. можно быстро скопировать запрошенное сообщение с сохранением всего форматирования\nЕсли применено к сообщению с эмбедом, вернётся контент некоторых полей, включая описание, заголовок, футер, ссылки на картинки и цвет\nВ случае с сообщениями бота возвращает контент в формате cy/say *то, что надо написать для повторения запрошенного сообщения*\nПолностью работает с эмбедами от лица бота, однако эмбеды из других источников будут неполными\nАргумент --edit вернёт сообщение в формате cy/edit *id сообщения* *то, что нужно написать для повторения запрошенного сообщения*\n\n[] - опционально, <> - обязательно```')
        elif command == 'dm':
            await interaction.response.send_message('```python\n/dm <@пинг/имя/ID> <текст>\n\n<> - обязательно, / - или\nНеобходимы разрешения - просматривать лог аудита```')
        elif command == 'say':
            await interaction.response.send_message('```python\n/say [обычный текст] [&t title текст] [&d description текст] [&th ссылка на картинку справа] [&img ссылка на картинку снизу] [&f footer текст] [&c цвет в HEX коде] [&msg сообщение над эмбедом]\n/say &t Заголовок &d Описание\n/say [текст]\n\nУчтите, что если вы захотите упомянуть роль с использованием какого либо аргумента текст не будет показан из-за способа упоминания ролей в Discord\nВсе аргументы являются необязательными, но если отправить пустую команду - ответ будет этим сообщением\n\n[] - опционально, но необходимо хоть что-то```')
        elif command == 'edit':
            await interaction.response.send_message('```python\n/edit <ID> [обычный текст] [&t title текст] [&d description текст] [&f footer текст] [&c цвет в HEX коде] [&th ссылка на картинку справа] [&img ссылка на картинку снизу]\n/edit <ID> [текст]\n/edit <ID> --clean\n/edit <ID> --noembed\n/edit <ID> --delete\n\n--clean удалит контент над эмбедом\n--noembed удалит эмбед\n--delete удалит сообщение\n\nИспользование --clean и --noembed одновременно невозможно.\nЕсли у сообщения есть эмбед и в команде нет агрументов, автоматически будет заменён &msg\nЗаголовок, описание и цвет будут взяты со старого эмбеда, если таковой имеется и эти аргументы не были указаны.\nДля очистки какого-либо поля укажите аргумент и оставьте его пустым:\n/edit <ID> &d\nЭто опустошит описание.\n\n[] - опционально, <> - обязательно\nНеобходимы разрешения - управлять сообщениями```')
        elif command == 'give':
            await interaction.response.send_message('```python\n/give <@пинг/имя/ID> <@роль/имя роли/ID роли>\n\n<> - обязательно, / - или\nНеобходимы разрешения - управлять каналами```')
        elif command == 'kick':
            await interaction.response.send_message('```python\n/kick <@пинг/имя/ID> [причина]\n\n[] - опционально, <> - обязательно, / - или\nНеобходимы разрешения - выгонять участников```')
        elif command == 'mute':
            await interaction.response.send_message('```python\n/mute <@пинг/имя/ID> [причина]\n\n[] - опционально, <> - обязательно, / - или\nНеобходимы разрешения - просматривать лог аудита```')
        elif command == 'roleinfo':
            await interaction.response.send_message('```python\n/roleinfo <@роль/имя роли/ID роли>\n\n<> - обязательно, / - или```')
        elif command == 'take':
            await interaction.response.send_message('```python\n/take <@пинг/имя/ID> <@роль/имя роли/ID роли>\n\n<> - обязательно, / - или\nНеобходимы разрешения - управлять каналами```')
        elif command == 'someone':
            await interaction.response.send_message('```python\n/someone <текст>\n\n<> - обязательно```')
        elif command == 'unmute':
            await interaction.response.send_message('```python\n/unmute <@пинг/имя/ID> [причина]\n\n[] - опционально, <> - обязательно, / - или\nНеобходимы разрешения - управлять каналами```')
        elif command == 'help':
            await interaction.response.send_message('```python\n/help [команда]\n\n[] - опционально```')
        else:
            emb = discord.Embed(description = f'Команда `{command}` не обнаружена или выполняется лишь её написанием.', color = 0xff8000)
            await interaction.response.send_message(embed = emb)

    @app_commands.command(description = 'Время бота в сети')
    async def uptime(self, interaction: discord.Interaction):
        now = discord.utils.utcnow()
        up_time = now - uptime
        hours, remainder = divmod(up_time.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        await interaction.response.send_message(embed = discord.Embed(description = f'Я в сети уже `{hours} ч, {minutes} м, {seconds} с`', color = 0xff8000))

    @app_commands.command(description = 'Выберите локаль бота')
    async def locale(self, interaction: discord.Interaction):
        locale = collection.find_one({"_id": interaction.user.id})["locale"]
        rbutton = GrayButton('RU')
        gbutton = RedButton('GNIDA')
        ebutton = GrayButton('EN')
        tbutton = GrayButton('TEST' if locale != 'ru' else 'ТЕСТ')
        ibutton = GrayButton('INFO' if locale != 'ru' else 'ИНФО')
        ybutton = RedButton('YES' if locale != 'ru' else 'ДА')
        nbutton = GrayButton('NO' if locale != 'ru' else 'НЕТ')
        confirm = View(timeout = 5)
        confirm.add_item(ybutton)
        confirm.add_item(nbutton)
        view = View(timeout = 5)
        view.add_item(rbutton)
        view.add_item(gbutton)
        #view.add_item(ebutton)
        view.add_item(tbutton)
        view.add_item(ibutton)
        async def rbutton_callback(interaction):
            collection.update_one({'_id': interaction.author.id}, {"$set": {'locale': 'ru'}})
            await interaction.response.edit_message(embed = discord.Embed(description = 'Ваша локаль была установлена на `ru`.', color = 0xff8000), view = None)
        async def gbutton_callback(interaction):
            await interaction.response.edit_message(embed = discord.Embed(description = 'Ты бля уверен?', color = 0xff8000), view = confirm)
        async def ybutton_callback(interaction):
            collection.update_one({'_id': interaction.author.id}, {"$set": {'locale': 'gnida'}})
            await interaction.response.edit_message(embed = discord.Embed(description = 'Твоя ёбаная локаль была установлена на `gnida`!', color = 0xff8000), view = None)
        async def nbutton_callback(interaction):
            await interaction.response.edit_message(embed = discord.Embed(description = 'Ну ок', color = 0xff8000), view = None)
        async def ebutton_callback(interaction):
            collection.update_one({'_id': interaction.author.id}, {"$set": {'locale': 'en'}})
            await interaction.response.edit_message(embed = discord.Embed(description = 'Your locale has been set to `en`.', color = 0xff8000), view = None)
        async def test_callback(interaction):
            if locale == 'ru':
                await interaction.response.edit_message(embed = discord.Embed(description = 'Ваша локаль установлена на `ru`', color = 0xff8000), view = None)
            if locale == 'gnida':
                await interaction.response.edit_message(embed = discord.Embed(description = 'Твоя ёбаная локаль установлена на `gnida`', color = 0xff8000), view = None)
            if locale == 'en':
                await interaction.response.edit_message(embed = discord.Embed(description = 'Your locale set to `en`', color = 0xff8000), view = None)
        async def info_callback(interaction):
            if locale == 'ru':
                await interaction.response.edit_message(content = None, embed = discord.Embed(description = 'Возможные локали:\nru\ngnida\nen\n\nУстановка локали на gnida производится на __ваш__ страх и риск. Создатели этого приложения не несут ответсвенности за **__любые__** происшествия, связанные с этой локалью.', color = 0xb00b69), view = None)
            if locale == 'gnida':
                await interaction.response.edit_message(content = None, embed = discord.Embed(description = 'Возможные локали:\nru\ngnida\nen\n\nТут короче предупреждение должно быть о том, создатели бота ответственности за локаль не несут.', color = 0xb00b69), view = None)
            if locale == 'en':
                await interaction.response.edit_message(content = None, embed = discord.Embed(description = 'Possible locales:\nru\ngnida\nen', color = 0xb00b69), view = None)
        rbutton.callback = rbutton_callback
        gbutton.callback = gbutton_callback
        ebutton.callback = ebutton_callback
        tbutton.callback = test_callback
        ibutton.callback = info_callback
        ybutton.callback = ybutton_callback
        nbutton.callback = nbutton_callback
        if locale == 'ru':
            rbutton.disabled = True
            await interaction.response.send_message('Выберите опцию:', view = view)
        if locale == 'gnida':
            gbutton.disabled = True
            await interaction.response.send_message('Чё надо', view = view)
        if locale == 'en':
            ebutton.disabled = True
            await interaction.response.send_message('Choose option:', view = view)

    @app_commands.command(description = 'Информация о боте')
    async def info(self, interaction: discord.Interaction):
        emb = discord.Embed(title = 'Пару строк кода сюда, новые фишки туда', description = 'Создатели бота постоянно совершенствуют своё детище, поддерживая его в актуальном состоянии.', color = 0xff8000)
        emb.set_author(name = self.client.user.name, url = 'https://warframe.fandom.com/wiki/Cephalon_Cy', icon_url = self.client.user.avatar.url)
        emb.add_field(name = 'Версия', value = '0.13.0.2.21680')
        emb.add_field(name = 'Написан на', value = f'discord.py v{discord.__version__}\nPython v{sys.version[:7]}')
        emb.add_field(name = 'Разработчики 🇷🇺', value = '[сасиска](https://discord.com/users/338714886001524737)\n[Prokaznik](https://discord.com/users/417012231406878720)\n[MegaVanya](https://discord.com/users/647853887583289354)')
        emb.add_field(name = 'Обслуживаю', value = f'{len(self.client.users)} человек')
        emb.add_field(name = 'Существую на', value = f'{len(self.client.guilds)} серверах')
        emb.set_footer(text = 'Данное приложение вдохновлено игрой Warframe', icon_url = 'https://i.playground.ru/p/yVaOZNSTdgUTxmzy_qvzzQ.png')
        await interaction.response.send_message(embed = emb)

    @app_commands.command(description = 'Информация о разработчиках бота')
    async def devs(self, interaction: discord.Interaction):
        emb = discord.Embed(description = 'Разработчики бота, в частности члены команды Sus&Co', color = 0xff8000)
        emb.add_field(name = 'сасиска', value = 'Первичный владелец бота, по совместительству основатель Sus&Co', inline = False)
        emb.add_field(name = 'Проказник', value = 'Причастен к созданию локали gnida, помогает с идеями для основного бота. Хоть и считается разработчиком, не имеет доступа к коду', inline = False)
        emb.add_field(name = 'Zoddof', value = 'Переработал категорию Fun, **имеет** доступ к коду версии Beta', inline = False)
        await interaction.response.send_message(embed = emb)

    @app_commands.command(description = 'Пригласите бота на сервер!')
    async def invite(self, interaction: discord.Interaction):
        emb = discord.Embed(description = '[Ссылка](https://discord.com/oauth2/authorize?client_id=694170281270312991&permissions=8&scope=bot%20applications.commands) для приглашения Cy на сервера.', color = 0xff8000)
        await interaction.response.send_message(embed = emb)

    @app_commands.command(description = 'Показывает задержку клиента бота')
    async def ping(self, interaction: discord.Interaction):
        emb = discord.Embed(description = '`Получаю..`', color = 0xff8000)
        emb1 = discord.Embed(description = f'Pong!  `{round(self.client.latency * 1000)} ms`', color = 0xff8000)
        await interaction.response.send_message(embed = emb)
        await asyncio.sleep(self.client.latency)
        await interaction.edit_original_response(embed = emb1)

    @app_commands.command(description = 'Узнайте, что было в предыдущих версиях бота')
    @app_commands.describe(version = 'Укажите конкретную версию')
    async def botver(self, interaction: discord.Interaction, version: Literal['0.12.9.10519', '0.12.9.10988', '0.12.9.11410', '0.12.10.1.11661', '0.12.10.2.12528', '0.12.11.2.13771', '0.12.12.0.0', '0.12.12.10.0', '0.12.12.10.16367', '0.12.12.30.0', '0.13.0.2.21680 - последняя']):
        if version == '0.12.9.10519':
            emb = discord.Embed(color = 0x2f3136)
            emb.add_field(name = '0.12.9.10519', value = 'Небольшие исправления, в целом никак не связанные с работой бота.')
            await interaction.response.send_message(embed = emb)
        if version == '0.12.9.10988':
            emb = discord.Embed(color = 0x2f3136)
            emb.add_field(name = '0.12.9.10988', value = 'Добавлены Slash-Команды! Теперь вы можете просто написать `/`, чтобы вам вывелся список всех команд. Для их работы нужна новая [ссылка-приглашение](https://discord.com/api/oauth2/authorize?client_id=694170281270312991&permissions=8&scope=bot%20applications.commands). Slash-Команды применены ко всем командам за исключением тех, что находятся в категории Fun, Embeds и некоторые в Cephalon или имеют конвертеры (mute, remind, someone) ***Всё ещё БЕТА!***', inline = False)
            await interaction.response.send_message(embed = emb)
        if version == '0.12.9.11410':
            emb = discord.Embed(color = 0x2f3136)
            emb.add_field(name = '0.12.9.11410', value = 'Некоторые исправления и добавление скрытых фич.')
            await interaction.response.send_message(embed = emb)
        if version == '0.12.10.1.11661':
            emb = discord.Embed(color = 0x2f3136)
            emb.add_field(name = '0.12.10.1.11661', value = 'Slash-Команды теперь применены ко всем командам, кроме тех, что используют конвертеры. Также, исправлены недоработки старых Slash-Команд и созданы новые (при написании некоторых команд будет ответ **Ошибка взаимодействия**, даже если команда была выполнена правильно).\n\n**Say**\n\nУбран аргумент `c&`, добавлен аргумент `f&` - текст в самом низу эмбеда.\n\n**Иное**\n\nТеперь команды пользователя не будут удаляться - это решение связано с рядом причин.')
            await interaction.response.send_message(embed = emb)
        if version == '0.12.10.2.11856':
            emb = discord.Embed(color = 0x2f3136)
            emb.add_field(name = '0.12.10.2.11856', value = 'Добавлена команда locale для изменения локали. Пока доступны только `ru` (по умолчанию) и `gnida`.\nSay/Edit\nУбран аргумент --everyone и запрещено упоминание @everyone каким-либо способом.')
            await interaction.response.send_message(embed = emb)
        if version == '0.12.10.2.12528':
            emb = discord.Embed(color = discord.Color.blurple())
            emb.add_field(name = '0.12.10.2.12528', value = 'Отдельные куски кода были рассортированы по разным файлам.')
            await interaction.response.send_message(embed = emb)
        if version == '0.12.11.2.13771':
            emb = discord.Embed(color = 0x2f3136)
            emb.add_field(name = '0.12.11.2.13771', value = 'Deaf/Undeaf:\nЗаглушает участника в голосовом канале, когда в его ролях есть Deafened\nHelp:\nТеперь указывает список команд, применимый для способа вызова Help. Таким образом, Slash-help будет показывать команды только без конвертеров, а обычная Help все команды.\nТакже, многочисленные исправления')
            await interaction.response.send_message(embed = emb)
        if version == '0.12.12.0.0':
            emb = discord.Embed(color = 0x2f3136)
            emb.add_field(name = '0.12.12.0.0', value = 'Переход на новую библиотеку, способствующий дальнейшему поддержанию бота в живых. Изменения:\nУбрана команда vote из меню Slash-команд, так как новая либра не даёт мне способов ставить реакции под сообщением, что отправил бот\nНовая команда - timeout\nПозволяет `отправить подумать над своим поведением` пользователя.')
            await interaction.response.send_message(embed = emb)
        if version == '0.12.12.10.0':
            emb = discord.Embed(color = 0x2f3136)
            emb.add_field(name = '0.12.12.10.0', value = 'Некоторое количество исправлений, возвращение команды vote через /\nИзменена логика команды mute - теперь нельзя установить время, на которое человек заглушается')
            await interaction.response.send_message(embed = emb)
        if version == '0.12.12.10.16367':
            emb = discord.Embed(color = 0x2f3136)
            emb.add_field(name = '0.12.12.10.16367', value = 'Изменение команд Embeds\n\nИзменено написание команд **say**, **edit** и переписана help под их изменение')
            await interaction.response.send_message(embed = emb)
        if version == '0.12.12.30.0':
            emb = discord.Embed(color = 0x2f3136)
            emb.add_field(name = '0.12.12.30.0', value = '**Библиотека**\nСовершён переезд на discord.py, позволяющий облегчить существование бота\n**someone**\nИсправлена ошибка, не позволяющяя писать более одного слова, в то время как остальные просто игнорировались\n**edit, say**\nБыли починены и улучшены, возвращён аргумент &c\n**Категория Fun**\nУдалена.\n**Locale**\nТеперь изменения локали применяются ко всем командам.\n\n***Slash-команды неактивны.***')
            await interaction.response.send_message(embed = emb)
        if version == '0.13.0.2.21680 - последняя':
            emb = discord.Embed(color = 0x2f3136)
            emb.add_field(name = '0.13.0.2.21680', value = '- Была добавлена категория Fun (4 новых команды)\n- Для большинства команд была добавлена слэш (/) версия\nОт себя хочется отметить, что в категории Fun появилась НЕВЕРОЯТНАЯ команда - dotersbrain\n\nВсё ёпта, такой вот патч вышел. Следующий ждите через год (~~Завтра~~)')
            emb.set_footer(text = 'Написано разработчиком Проказник#2785')
            await interaction.response.send_message(embed = emb)

async def setup(client):
    await client.add_cog(sCephalon(client))