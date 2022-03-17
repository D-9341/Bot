import asyncio
import datetime
import os

import disnake
from disnake.ext import commands
from pymongo import MongoClient

passw = os.environ.get('passw')
cluster = MongoClient(f"mongodb+srv://cephalon:{passw}@locale.ttokw.mongodb.net/Locale?retryWrites=true&w=majority")
collection = cluster.Locale.locale

friends = [351071668241956865, 417362845303439360]

guilds = [693929822543675455, 735874149578440855, 818758712163827723]

uptime = disnake.utils.utcnow()

class sCephalon(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Группа Slash-команд Cephalon загружена')

    @commands.slash_command(name = 'uptime', description = 'Позволяет узнать время бота в сети')
    async def _uptime(self, inter):
        bot_time = disnake.utils.utcnow() - uptime
        await inter.response.send_message(embed = disnake.Embed(description = f'Я в сети уже `{bot_time}`', color = 0x2f3136))

    @commands.slash_command(name = 'botver', description = 'Позволяет узнать текущую версию бота')
    async def _botver(self, inter, version: str = commands.Param(choices = {'0.12.9.10519': '0.12.9.10519', '0.12.9.10988': '0.12.9.10988', '0.12.9.11410': '0.12.9.11410', '0.12.10.1.11661': '0.12.10.1.11661', '0.12.10.2.11856': '0.12.10.2.11856', '0.12.10.2.12528': '0.12.10.2.12528', '0.12.11.2.13771': '0.12.11.2.13771', '0.12.12.0.0': '0.12.12.0.0', '0.12.12.10.0': '0.12.12.10.0', '0.12.12.10.16367': '0.12.12.10.16367'})):
        if version == '0.12.9.10519':
            emb = disnake.Embed(color = 0x2f3136)
            emb.add_field(name = '0.12.9.10519', value = 'Небольшие исправления, в целом никак не связанные с работой бота.')
            await inter.response.send_message(embed = emb)
        if version == '0.12.9.10988':
            emb = disnake.Embed(color = 0x2f3136)
            emb.add_field(name = '0.12.9.10988', value = 'Добавлены Slash-Команды! Теперь вы можете просто написать `/`, чтобы вам вывелся список всех команд. Для их работы нужна новая [ссылка-приглашение](https://discord.com/api/oauth2/authorize?client_id=694170281270312991&permissions=8&scope=bot%20applications.commands). Slash-Команды применены ко всем командам за исключением тех, что находятся в категории Fun, Embeds и некоторые в Cephalon или имеют конвертеры (mute, remind, someone) ***Всё ещё БЕТА!***', inline = False)
            await inter.response.send_message(embed = emb)
        if version == '0.12.9.11410':
            emb = disnake.Embed(color = 0x2f3136)
            emb.add_field(name = '0.12.9.11410', value = 'Некоторые исправления и добавление скрытых фич.')
            await inter.response.send_message(embed = emb)
        if version == '0.12.10.1.11661':
            emb = disnake.Embed(color = 0x2f3136)
            emb.add_field(name = '0.12.10.1.11661', value = 'Slash-Команды теперь применены ко всем командам, кроме тех, что используют конвертеры. Также, исправлены недоработки старых Slash-Команд и созданы новые (при написании некоторых команд будет ответ **Ошибка взаимодействия**, даже если команда была выполнена правильно).\n\n**Say**\n\nУбран аргумент `c&`, добавлен аргумент `f&` - текст в самом низу эмбеда.\n\n**Иное**\n\nТеперь команды пользователя не будут удаляться - это решение связано с рядом причин.')
            await inter.response.send_message(embed = emb)
        if version == '0.12.10.2.11856':
            emb = disnake.Embed(color = 0x2f3136)
            emb.add_field(name = '0.12.10.2.11856', value = 'Добавлена команда locale для изменения локали. Пока доступны только `ru` (по умолчанию) и `gnida`.\nSay/Edit\nУбран аргумент --everyone и запрещено упоминание @everyone каким-либо способом.')
            await inter.response.send_message(embed = emb)
        if version == '0.12.10.2.12528':
            emb = disnake.Embed(color = disnake.Color.blurple())
            emb.add_field(name = '0.12.10.2.12528', value = 'Отдельные куски кода были рассортированы по разным файлам.')
            await inter.response.send_message(embed = emb)
        if version == '0.12.11.2.13771':
            emb = disnake.Embed(color = 0x2f3136)
            emb.add_field(name = '0.12.11.2.13771', value = 'Deaf/Undeaf:\nЗаглушает участника в голосовом канале, когда в его ролях есть Deafened\nHelp:\nТеперь указывает список команд, применимый для способа вызова Help. Таким образом, Slash-help будет показывать команды только без конвертеров, а обычная Help все команды.\nТакже, многочисленные исправления')
            await inter.response.send_message(embed = emb)
        if version == '0.12.12.0.0':
            emb = disnake.Embed(color = 0x2f3136)
            emb.add_field(name = '0.12.12.0.0', value = 'Переход на новую библиотеку, способствующий дальнейшему поддержанию бота в живых. Изменения:\nУбрана команда vote из меню Slash-команд, так как новая либра не даёт мне способов ставить реакции под сообщением, что отправил бот\nНовая команда - timeout\nПозволяет `отправить подумать над своим поведением` пользователя.')
            await inter.response.send_message(embed = emb)
        if version == '0.12.12.10.0':
            emb = disnake.Embed(color = 0x2f3136)
            emb.add_field(name = '0.12.12.10.0', value = 'Некоторое количество исправлений, возвращение команды vote через /\nИзменена логика команды mute - теперь нельзя установить время, на которое человек заглушается')
            await inter.response.send_message(embed = emb)
        if version == '0.12.12.10.16367':
            emb = disnake.Embed(color = 0x2f3136)
            emb.add_field(name = '0.12.12.10.16367', value = 'Изменение команд Embeds\n\nИзменено написание команд **say**, **edit** и переписана help под их изменение')
            await inter.response.send_message(embed = emb)

    @commands.slash_command(name = 'ping', description = 'Отображение задержки клиента бота. Нормальная задержка в диапазоне от 90 до 130 миллисекунд.')
    async def _ping(self, inter):
        emb = disnake.Embed(description = f'`fetching..`', colour = disnake.Color.orange())
        emb1 = disnake.Embed(description = f'Pong!  `{round(self.client.latency * 1000)}ms`', colour = disnake.Color.orange())
        await inter.response.send_message(embed = emb)
        message = await inter.original_message()
        await asyncio.sleep(self.client.latency)
        await message.edit(embed = emb1)

    @commands.slash_command(name = 'info', description = 'Информация о боте')
    async def _info(self, inter):
        emb = disnake.Embed(colour = disnake.Color.orange())
        emb.set_author(name = self.client.user.name, url = 'https://warframe.fandom.com/wiki/Cephalon_Cy', icon_url = self.client.user.avatar.url)
        emb.add_field(name = 'Версия', value = '0.12.12.10.16367')
        emb.add_field(name = 'Написан на', value = 'disnake.py v2.3.0')
        emb.add_field(name = 'Разработчик', value = '[сасиска#2472](https://discord.com/users/338714886001524737)')
        if inter.guild.id == 693929822543675455:
            emb.add_field(name = 'Принадлежность', value = 'Это - мой основной сервер.')
        if inter.guild.id == 735874149578440855:
            emb.add_field(name = 'Тестирование', value = 'Это - мой тестовый сервер.')
        emb.add_field(name = 'Обслуживаю', value = f'{len(self.client.users)} человек')
        emb.add_field(name = 'Существую на', value = f'{len(self.client.guilds)} серверах')
        emb.set_footer(text = 'Данное приложение не имеет никакого причастия к игре Warframe.', icon_url = 'https://i.playground.ru/p/yVaOZNSTdgUTxmzy_qvzzQ.png')
        await inter.response.send_message(embed = emb)

    @commands.slash_command(name = 'invite', description = 'Для приглашения бота на сервер')
    async def _invite(self, inter):
        emb = disnake.Embed(description = '[Ссылка](https://discord.com/api/oauth2/authorize?client_id=694170281270312991&permissions=8&scope=bot%20applications.commands) для приглашения Cy на сервера.', colour = disnake.Color.orange())
        await inter.response.send_message(embed = emb)

    @commands.slash_command(name = 'help', description = 'Здесь можно получить полную помощь по всем командам')
    async def _help(self, inter, arg: str = commands.Param(default = None, choices = {'about': 'about', 'avatar': 'avatar', 'ban': 'ban', 'content': 'content', 'clear': 'clear', 'dm': 'dm', 'say': 'say', 'edit': 'edit', 'give': 'give', 'kick': 'kick', 'mute': 'mute', 'role': 'role', 'take': 'take', 'unmute': 'unmute', 'embeds': 'embeds', 'cephalon': 'cephalon', 'mod': 'mod', 'misc': 'misc', 'all': 'all', 'roll': 'roll'})):
        if arg == None:
            emb = disnake.Embed(title = self.client.user.name, description = 'Доступные Slash-команды', colour = disnake.Color.orange())
            emb.add_field(name = 'Cephalon', value = '`botver`, `info`, `invite`, `join`, `leave`, `ping`, `uptime`', inline = False)
            emb.add_field(name = 'Embeds', value = '`content`, `edit`, `say`', inline = False)
            emb.add_field(name = 'Fun', value = '`aye_balbec`, `dotersbrain`, `niggers`, `rp`, `rap`, `zatka`', inline = False)
            emb.add_field(name = 'Mod', value = '`ban`, `clear`, `dm`, `give`, `kick`, `mute`, `take`, `unmute`', inline = False)
            emb.add_field(name = 'Misc', value = '`about`, `avatar`, `coinflip`, `guild`, `remind`, `role`, `roll`, `rolemembers`, `vote`', inline = False)
            emb.add_field(name = 'ᅠ', value = 'Назовите комнату `Создать канал`, чтобы бот автоматически создавал для вас временные каналы, которые будут удаляться после того, как все люди выйдут из канала.')
            emb.add_field(name = 'ᅠ', value = 'Не используйте [], <>, / при написании команды.', inline = False)
            emb.add_field(name = 'ᅠ', value = '**Используйте** `/help [команда/категория]` **для подробностей использования.**\n\n**[Ссылка-приглашение](https://discord.com/api/oauth2/authorize?client_id=694170281270312991&permissions=8&scope=bot%20applications.commands)**', inline = False)
            emb.set_footer(text = 'Cephalon Cy ©️ сасиска#2472')
            await inter.response.send_message(embed = emb)
        if arg == 'setup':
            await inter.response.send_message('```apache\ncy/setup\nвыполнение команды создаст 4 роли, если их нет на сервере.\nбудет выполнено автоматически, если сработает авто-мут.```')
        elif arg == 'roll':
            await inter.response.send_message('```apache\ncy/roll [от] [до]\nесли не указано [до], [от] станет [до].\ncy/roll 80 (0-80)\ncy/roll 26 90 (26-90)\ncy/roll (0-100)\n([] - опционально)```')
        elif arg == 'about':
            await inter.response.send_message('```apache\ncy/about [@пинг/имя/ID] ([] - опционально, / - или)```')
        elif arg == 'avatar':
            await inter.response.send_message('```apache\ncy/avatar [@пинг/имя/ID] ([] - опционально, / - или)```')
        elif arg == 'ban':
            await inter.response.send_message('```apache\ncy/ban <@пинг/имя/ID> [причина/--soft --reason]\ncy/ban 185476724627210241 --soft --reason лошара\ncy/ban @сасиска чмо\ncy/ban "Sgt.White"\n\nПри использовании --soft обязательно указывать --reason после него, однако можно не использовать --reason\n([] - опционально, <> - обязательно, / - или)\nperms = ban_members```')
        elif arg == 'content' or arg == 'ctx':
            await inter.response.send_message('```apache\ncy/content <ID> [канал, в котором находится сообщение] ([] - опционально, <> - обязательно)```')
        elif arg == 'clear':
            await inter.response.send_message('```apache\ncy/clear <количество> [автор] [фильтр]\ncy/clear 100\ncy/clear 10 @сасиска\ncy/clear 50 --everyone хыха\ncy/clear 30 --bots\ncy/clear 15 --users\ncy/clear 5 --silent\ncy/clear 200 "--silent --everyone" хыха\n\n--everyone удалит сообщения от всех\n--bots удалит сообщения только от ботов\n--users удалит сообщения только от участников\n--silent не оставит доказательств выполнения команды, исключение - количество >= 10\n\nПри указании автора не будет удалено столько сообщений, сколько было указано, будет удалено столько, сколько будет найдено в пределах этих сообщений.\nСообщения старше 2 недель будут удалены не сразу - лимит discord API\nПри использовании --silent нельзя сделать очистку по определённому участнику\nПри удалении более 100 сообщений нужно подтверждение владельца сервера.\nТолько владелец может удалять от 250 сообщений за раз.\nНе более 300!\n([] - опционально, <> - обязательно, / - или)\nperms = adminstrator```')
        elif arg == 'dm':
            await inter.response.send_message('```apache\ncy/dm <@пинг/имя/ID> <текст> (<> - обязательно, / - или)\nperms = view_audit_log```')
        elif arg == 'say':
            await inter.response.send_message('```apache\ncy/say [обычный текст] [&t title текст] [&d description текст] [&th ссылка на картинку справа] [&img ссылка на картинку снизу] [&f footer текст] [&msg сообщение над эмбедом]\ncy/say &t Заголовок &d Описание\ncy/say [текст]\n(вам НЕ обязательно писать все аргументы в данном порядке, пишите только те, что вам нужны в любом порядке. Однако необходимо написать хоть что-то для выполнения команды) ([] - опционально)```')
        elif arg == 'edit':
            await inter.response.send_message('```apache\ncy/edit <ID> [обычный текст] [&t title текст] [&d description текст] [&th ссылка на картинку справа] [&img ссылка на картинку снизу]\ncy/edit <ID> [текст]\ncy/edit <ID> --clean &d description\ncy/edit <ID> --clean\ncy/edit <ID> --noembed\ncy/edit <ID> --empty-embed\ncy/edit <ID> --delete\n--clean удалит контент над эмбедом, --noembed удалит эмбед, работает только если есть эмбед, --empty-embed опустошит эмбед, --delete удалит сообщение\nесли у сообщения есть эмбед и в команде нет агрументов, автоматически будет заменён &msg\n([] - опционально, <> - обязательно)\nperms = manage_channels```')
        elif arg == 'give':
            await inter.response.send_message('```apache\ncy/give <@пинг/имя/ID> <@роль/имя роли/ID роли> (<> - обязательно, / - или)\nperms = manage_channels```')
        elif arg == 'kick':
            await inter.response.send_message('```apache\ncy/kick <@пинг/имя/ID> [причина] ([] - опционально, <> - обязательно, / - или)\nperms = kick_members```')
        elif arg == 'mute':
            await inter.response.send_message('```apache\ncy/mute <@пинг/имя/ID> [причина] ([] - опционально, <> - обязательно, / - или)\nperms = view_audit_log```')
        elif arg == 'roleinfo':
            await inter.response.send_message('```apache\ncy/roleinfo <@роль/имя роли/ID роли> (<> - обязательно, / - или)```')
        elif arg == 'take':
            await inter.response.send_message('```apache\ncy/take <@пинг/имя/ID> <@роль/имя роли/ID роли> (<> - обязательно, / - или)\nperms = manage_channels```')
        elif arg == 'unmute':
            await inter.response.send_message('```apache\ncy/unmute <@пинг/имя/ID> [причина] ([] - опционально, <> - обязательно, / - или)\nperms = manage_channels```')
        elif arg == 'help':
            await inter.response.send_message('```apache\ncy/help [команда/категория] ([] - опционально, / - или)```')
        elif arg == 'Embeds' or arg == 'embeds':
            await inter.response.send_message('```py\ncontent(ctx) - позволяет увидеть необработанный контент сообщения\nedit - редактирует сообщение, отправленное от лица бота. Иные сообщения редактировать нельзя.\nsay - используется для написания как текстов, так и эмбедов.```')
        elif arg == 'Cephalon' or arg == 'cephalon':
            await inter.response.send_message('```py\ninfo - информация о боте\ninvite - ссылка-приглашения бота\njoin - бот зайдёт в ваш голосовой канал\nleave - бот из него выйдет\nping - проверяет задержку клиента бота.```')
        elif arg == 'Mod' or arg == 'mod':
            await inter.response.send_message('```py\nban - бан участника\nclear - очистка чата, не более 300!\ndm - пишет в лс участнику написанный текст\ngive - выдаёт роль\nkick - кик участника\nmute - мут участника\ntake - забирает роль\nunmute - снятие мута участника.```')
        elif arg == 'Misc' or arg == 'misc':
            await inter.response.send_message('```py\nabout - информация о человеке\navatar - аватар человека\nguild - информация о сервере\nremind - напоминание о событии\nroleinfo - информация о роли\nrolemembers - участники роли\nsomeone - упоминание someone\nvote - голосование за что-то.```')
        elif arg == 'All' or arg == 'all':
            await inter.response.send_message('```py\ninfo - информация о боте\ninvite - ссылка-приглашения бота\njoin - бот зайдёт в ваш голосовой канал\nleave - бот из него выйдет\nping - проверяет задержку клиента бота.```')
            await inter.send('```py\ncontent(ctx) - позволяет увидеть raw контент сообщения\nedit - редактирует сообщение, отправленное от лица бота. Иные сообщения редактировать нельзя.\nsay - используется для написания как текстов, так и эмбедов.```')
            await inter.send('```py\naye_balbec - я не ангел и не бес, просто..\ncu - медь\ncoinflip(c, coin) - подкидывает монетку\ndotersbrain - проверка на мозг дотера\nniggers - осуждаем!\nrp - ультимативный гайд по рп отыгровке\nrap - .rap\nzatka - Форма заявки для набор кадров```')
            await inter.send('```py\nban - бан участника\nclear - очистка чата, не более 300!\ndm - пишет в лс участнику написанный текст\ngive - выдаёт роль\nkick - кик участника\nmute - мут участника\ntake - забирает роль\nunmute - снятие мута участника.```')
            await inter.send('```py\nabout - информация о человеке\navatar - аватар человека\nguild - информация о сервере\nremind - напоминание о событии\nroleinfo - информация о роли\nrolemembers - участники роли\nsomeone - упоминание someone\nvote - голосование за что-то.```')

def setup(client):
    client.add_cog(sCephalon(client))
