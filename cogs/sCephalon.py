import asyncio
import datetime
import os

import discord
import discord_slash
from discord.ext import commands
from discord_slash import cog_ext as slash
from pymongo import MongoClient

passw = os.environ.get('passw')
cluster = MongoClient(f"mongodb+srv://cephalon:{passw}@locale.ttokw.mongodb.net/Locale?retryWrites=true&w=majority")
collection = cluster.Locale.locale

friends = [351071668241956865, 417362845303439360]

guilds = [693929822543675455, 735874149578440855, 818758712163827723]

class sCephalon(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Группа Slash-команд Cephalon загружена')

    @slash.cog_slash(name = 'botver', description = 'Позволяет узнать текущую версию бота', options = [{'name': 'version', 'description': 'Версия', 'required': False, 'type': 3, 'choices': [
        {'name': '0.12.9.10519', 'value': '0.12.9.10519'}, 
        {'name': '0.12.9.10988', 'value': '0.12.9.10988'}, 
        {'name': '0.12.9.11410', 'value': '0.12.9.11410'},
        {'name': '0.12.10.1.11661', 'value': '0.12.10.1.11661'},
        {'name': '0.12.10.2.11856', 'value': '0.12.10.2.11856'},
        {'name': '0.12.10.2.12528', 'value': '0.12.10.2.12528'},
        {'name': '0.12.11.2.13771', 'value': '0.12.11.2.13771'}]}])
    async def _botver(self, ctx, version = None):
        if version == None:
            emb = discord.Embed(color = 0x2f3136) # будут маленькое, нормальное и крупное обновления
            emb.add_field(name = '0.12.10.2.12528 (Текущая версия, полная перепись кода)', value = 'Отдельные куски кода были рассортированы по разным файлам.', inline = False)
            emb.add_field(name = '0.12.10.2.11856 (Предыдущая версия, нормальное обновление)', value = 'Добавлена команда locale для изменения локали. Пока доступны только `ru` (по умолчанию) и `gnida`.\n\n**Say/Edit**\n\nУбран аргумент --everyone и запрещено упоминание @everyone каким-либо способом.', inline = False)
            await ctx.send(embed = emb)
        if version == '0.12.9.10519':
            emb = discord.Embed(color = 0x2f3136)
            emb.add_field(name = '0.12.9.10519', value = 'Небольшие исправления, в целом никак не связанные с работой бота.')
            await ctx.send(embed = emb)
        if version == '0.12.9.10988':
            emb = discord.Embed(color = 0x2f3136)
            emb.add_field(name = '0.12.9.10988', value = 'Добавлены Slash-Команды! Теперь вы можете просто написать `/`, чтобы вам вывелся список всех команд. Для их работы нужна новая [ссылка-приглашение](https://discord.com/api/oauth2/authorize?client_id=694170281270312991&permissions=8&scope=bot%20applications.commands). Slash-Команды применены ко всем командам за исключением тех, что находятся в категории Fun, Embeds и некоторые в Cephalon или имеют конвертеры (mute, remind, someone) ***Всё ещё БЕТА!***', inline = False)
            await ctx.send(embed = emb)
        if version == '0.12.9.11410':
            emb = discord.Embed(color = 0x2f3136)
            emb.add_field(name = '0.12.9.11410', value = 'Некоторые исправления и добавление скрытых фич.')
            await ctx.send(embed = emb)
        if version == '0.12.10.1.11661':
            emb = discord.Embed(color = 0x2f3136)
            emb.add_field(name = '0.12.10.1.11661', value = 'Slash-Команды теперь применены ко всем командам, кроме тех, что используют конвертеры. Также, исправлены недоработки старых Slash-Команд и созданы новые (при написании некоторых команд будет ответ **Ошибка взаимодействия**, даже если команда была выполнена правильно).\n\n**Say**\n\nУбран аргумент `c&`, добавлен аргумент `f&` - текст в самом низу эмбеда.\n\n**Иное**\n\nТеперь команды пользователя не будут удаляться - это решение связано с рядом причин.')
            await ctx.send(embed = emb)
        if version == '0.12.10.2.11856':
            emb = discord.Embed(color = 0x2f3136)
            emb.add_field(name = '0.12.10.2.11856', value = 'Добавлена команда locale для изменения локали. Пока доступны только `ru` (по умолчанию) и `gnida`.\nSay/Edit\nУбран аргумент --everyone и запрещено упоминание @everyone каким-либо способом.')
            await ctx.send(embed = emb)
        if version == '0.12.10.2.12528':
            emb = discord.Embed(color = discord.Color.blurple())
            emb.add_field(name = '0.12.10.2.12528', value = 'Отдельные куски кода были рассортированы по разным файлам.')
            await ctx.send(embed = emb)
        if version == '0.12.11.2.13771':
            emb = discord.Embed(color = 0x2f3136)
            emb.add_field(name = '', value = 'Deaf/Undeaf:\nЗаглушает участника в голосовом канале, когда в его ролях есть Deafened\nHelp:\nТеперь указывает список команд, применимый для способа вызова Help. Таким образом, Slash-help будет показывать команды только без конвертеров, а обычная Help все команды.\nТакже, многочисленные исправления')
            await ctx.send(embed = emb)
            
    @slash.cog_slash(name = 'ping', description = 'Отображение задержки клиента бота. Нормальная задержка в диапазоне от 90 до 130 миллисекунд.')
    async def _ping(self, ctx):
        emb = discord.Embed(description = f'`fetching..`', colour = discord.Color.orange())
        emb1 = discord.Embed(description = f'Pong!  `{round(self.client.latency * 1000)} ms`', colour = discord.Color.orange())
        message = await ctx.send(embed = emb)
        await asyncio.sleep(self.client.latency)
        await message.edit(embed = emb1)

    @slash.cog_slash(name = 'info', description = 'Информация о боте')
    async def _info(self, ctx):
        emb = discord.Embed(colour = discord.Color.orange())
        emb.set_author(name = self.client.user.name, url = 'https://warframe.fandom.com/wiki/Cephalon_Cy', icon_url = self.client.user.avatar_url)
        emb.add_field(name = 'Версия', value = '0.12.11.2.13771')
        emb.add_field(name = 'Написан на', value = 'discord.py v1.7.3 при помощи\ndiscord-py-slash-command v2.0.0')
        emb.add_field(name = 'Разработчик', value = '[сасиска#2472](https://discord.com/users/338714886001524737)')
        if ctx.guild.id == 693929822543675455:
            emb.add_field(name = 'Принадлежность', value = 'Это - мой основной сервер.')
        if ctx.guild.id == 735874149578440855:
            emb.add_field(name = 'Тестирование', value = 'Это - мой тестовый сервер.')
        emb.add_field(name = 'Обслуживаю', value = f'{len(self.client.users)} человек')
        emb.add_field(name = 'Существую на', value = f'{len(self.client.guilds)} серверах')
        emb.set_footer(text = 'Данное приложение не имеет никакого причастия к игре Warframe.', icon_url = 'https://i.playground.ru/p/yVaOZNSTdgUTxmzy_qvzzQ.png')
        await ctx.send(embed = emb)

    @slash.cog_slash(name = 'invite', description = 'Для приглашения бота на сервер')
    async def _invite(self, ctx):
        emb = discord.Embed(description = '[Ссылка](https://discord.com/api/oauth2/authorize?client_id=694170281270312991&permissions=8&scope=bot%20applications.commands) для приглашения Cy на сервера.', colour = discord.Color.orange())
        await ctx.send(embed = emb)

    @slash.cog_slash(name = 'help', description = 'Здесь можно получить полную помощь по всем командам', options = [{'name': 'arg', 'description': 'Выбор команды для помощи', 'required': False, 'type': 3, 'choices': [
        {'name': 'about', 'value': 'about'},
        {'name': 'avatar', 'value': 'avatar'},
        {'name': 'ban', 'value': 'ban'},
        {'name': 'content', 'value': 'content'},
        {'name': 'clear', 'value': 'clear'},
        {'name': 'dm', 'value': 'dm'},
        {'name': 'say', 'value': 'say'},
        {'name': 'edit', 'value': 'edit'},
        {'name': 'give', 'value': 'give'},
        {'name': 'kick', 'value': 'kick'},
        {'name': 'roleinfo', 'value': 'roleinfo'},
        {'name': 'take', 'value': 'take'},
        {'name': 'unmute', 'value': 'unmute'},
        {'name': 'vote', 'value': 'vote'},
        {'name': 'Embeds', 'value': 'embeds'},
        {'name': 'Cephalon', 'value': 'cephalon'},
        {'name': 'Mod', 'value': 'mod'},
        {'name': 'Misc', 'value': 'misc'},
        {'name': 'All', 'value': 'all'},
        {'name': 'roll', 'value': 'roll'}
        ]
        }])
    async def _help(self, ctx, arg = None):
            if arg == None:
                emb = discord.Embed(title = self.client.user.name, description = 'Доступные Slash-команды.', color = discord.Color.orange())
                emb.add_field(name = 'Cephalon', value = '`info`, `invite`, `join`, `leave`, `ping`', inline = False)
                emb.add_field(name = 'Embeds', value = '`content`, `edit`, `say`', inline = False)
                if not (ctx.guild.owner.id != self.client.owner_id and ctx.guild.owner.id not in friends):
                    emb.add_field(name = 'Fun', value = '`aye_balbec`, `cu`, `coinflip`, `dotersbrain`, `niggers`, `rp`, `rap`, `zatka`', inline = False)
                emb.add_field(name = 'Mod', value = '`ban`, `clear`, `dm`, `give`, `kick`, `take`, `unmute`', inline = False)
                emb.add_field(name = 'Misc', value = '`about`, `avatar`, `guild`, `role`, `rolemembers`, `vote`', inline = False)
                emb.add_field(name = 'ᅠ', value = 'Назовите комнату `Создать канал` (**регистр обязателен**), чтобы бот автоматически создавал для вас временные каналы, которые будут удаляться после того, как все люди выйдут из канала.')
                emb.add_field(name = 'ᅠ', value = '**Используйте** `cy/help [команда/категория]` **для подробностей использования.**\n\n**[Ссылка-приглашение](https://discord.com/api/oauth2/authorize?client_id=694170281270312991&permissions=8&scope=bot%20applications.commands)**', inline = False)
                emb.set_footer(text = 'Cephalon Cy © сасиска#2472')
                return await ctx.send(embed = emb)
            elif arg == 'roll':
                await ctx.send('```apache\ncy/roll [от] [до]\nесли не указано [до], [от] станет [до].\ncy/roll 80 (0-80)\ncy/roll 26 90 (26-90)\ncy/roll (0-100)\n([] - опционально)```')
            elif arg == 'about':
                await ctx.send('```apache\ncy/about [@пинг/имя/ID] ([] - опционально, / - или)```')
            elif arg == 'avatar':
                await ctx.send('```apache\ncy/avatar [@пинг/имя/ID] ([] - опционально, / - или)```')
            elif arg == 'ban':
                await ctx.send('```apache\ncy/ban <@пинг/имя/ID> [причина/--soft --reason]\ncy/ban 185476724627210241 --soft --reason лошара\ncy/ban @сасиска чмо\ncy/ban "Sgt.White"\n\nПри использовании --soft обязательно указывать --reason после него, однако можно не использовать --reason\n([] - опционально, <> - обязательно, / - или)\nperms = ban_members```')
            elif arg == 'content' or arg == 'ctx':
                await ctx.send('```apache\ncy/content <ID> [канал, в котором находится сообщение] ([] - опционально, <> - обязательно)```')
            elif arg == 'clear':
                await ctx.send('```apache\ncy/clear <количество> [автор] [фильтр]\ncy/clear 100\ncy/clear 10 @сасиска\ncy/clear 50 --everyone хыха\ncy/clear 30 --bots\ncy/clear 15 --users\ncy/clear 5 --silent\ncy/clear 200 "--silent --everyone" хыха\n\n--everyone удалит сообщения от всех\n--bots удалит сообщения только от ботов\n--users удалит сообщения только от участников\n--silent не оставит доказательств выполнения команды, исключение - количество >= 10\n\nПри указании автора не будет удалено столько сообщений, сколько было указано, будет удалено столько, сколько будет найдено в пределах этих сообщений.\nСообщения старше 2 недель будут удалены не сразу - лимит discord API\nПри использовании --silent нельзя сделать очистку по определённому участнику\nПри удалении более 100 сообщений нужно подтверждение владельца сервера.\nТолько владелец может удалять от 250 сообщений за раз.\nНе более 300!\n([] - опционально, <> - обязательно, / - или)\nperms = adminstrator```')
            elif arg == 'dm':
                await ctx.send('```apache\ncy/dm <@пинг/имя/ID> <текст> (<> - обязательно, / - или)\nperms = view_audit_log```')
            elif arg == 'say':
                    await ctx.send('```apache\ncy/say [обычный текст] [t& title текст] | [d& description текст] | [th& ссылка на картинку справа] | [img& ссылка на картинку снизу] [f& footer текст] [msg& сообщение над эмбедом]\ncy/say t& title | d& description\ncy/say [текст]\n(вам НЕ обязательно писать все аргументы в данном порядке, пишите только те, что вам нужны в любом порядке. Однако необходимо написать хоть что-то для выполнения команды) ([] - опционально)```')
            elif arg == 'edit':
                    await ctx.send('```apache\ncy/edit <ID> [обычный текст] [t& title текст] | [d& description текст] | [th& ссылка на картинку справа] | [img& ссылка на картинку снизу]\ncy/edit <ID> [текст]\ncy/edit <ID> --clean | d& description\ncy/edit <ID> --clean\ncy/edit <ID> --noembed\ncy/edit <ID> --empty-embed\ncy/edit <ID> --delete\n--clean удалит контент над эмбедом, --noembed удалит эмбед, работает только если есть эмбед, --empty-embed опустошит эмбед, --delete удалит сообщение\nесли у сообщения есть эмбед и в команде нет агрументов, автоматически будет заменён msg&\n([] - опционально, <> - обязательно)\nperms = manage_channels```')
            elif arg == 'give':
                await ctx.send('```apache\ncy/give <@пинг/имя/ID> <@роль/имя роли/ID роли> (<> - обязательно, / - или)\nperms = manage_channels```')
            elif arg == 'kick':
                await ctx.send('```apache\ncy/kick <@пинг/имя/ID> [причина] ([] - опционально, <> - обязательно, / - или)\nperms = kick_members```')
            elif arg == 'roleinfo':
                await ctx.send('```apache\ncy/roleinfo <@роль/имя роли/ID роли> (<> - обязательно, / - или)```')
            elif arg == 'take':
                await ctx.send('```apache\ncy/take <@пинг/имя/ID> <@роль/имя роли/ID роли> (<> - обязательно, / - или)\nperms = manage_channels```')
            elif arg == 'unmute':
                await ctx.send('```apache\ncy/unmute <@пинг/имя/ID> [причина] ([] - опционально, <> - обязательно, / - или)\nperms = manage_channels```')
            elif arg == 'vote':
                await ctx.send('```apache\ncy/vote <текст> (<> - обязательно)```')
            elif arg == 'help':
                await ctx.send('```apache\ncy/help [команда/категория] ([] - опционально, / - или)```')
            elif arg == 'Embeds' or arg == 'embeds':
                await ctx.send('```py\ncontent(ctx) - позволяет увидеть необработанный контент сообщения\nedit - редактирует сообщение, отправленное от лица бота. Иные сообщения редактировать нельзя.\nsay - используется для написания как текстов, так и эмбедов.```')
            elif arg == 'Cephalon' or arg == 'cephalon':
                await ctx.send('```py\ninfo - информация о боте\ninvite - ссылка-приглашения бота\njoin - бот зайдёт в ваш голосовой канал\nleave - бот из него выйдет\nping - проверяет задержку клиента бота.```')
            elif arg == 'Mod' or arg == 'mod':
                await ctx.send('```py\nban - бан участника\nclear - очистка чата, не более 300!\ndm - пишет в лс участнику написанный текст\ngive - выдаёт роль\nkick - кик участника\nmute - мут участника\ntake - забирает роль\nunmute - снятие мута участника.```')
            elif arg == 'Misc' or arg == 'misc':
                await ctx.send('```py\nabout - информация о человеке\navatar - аватар человека\nguild - информация о сервере\nremind - напоминание о событии\nroleinfo - информация о роли\nrolemembers - участники роли\nsomeone - упоминание someone\nvote - голосование за что-то.```')
            elif arg == 'All' or arg == 'all':
                await ctx.send('```py\ninfo - информация о боте\ninvite - ссылка-приглашения бота\njoin - бот зайдёт в ваш голосовой канал\nleave - бот из него выйдет\nping - проверяет задержку клиента бота.```')
                await ctx.send('```py\ncontent(ctx) - позволяет увидеть raw контент сообщения\nedit - редактирует сообщение, отправленное от лица бота. Иные сообщения редактировать нельзя.\nsay - используется для написания как текстов, так и эмбедов.```')
                await ctx.send('```py\naye_balbec - я не ангел и не бес, просто..\ncu - медь\ncoinflip(c, coin) - подкидывает монетку\ndotersbrain - проверка на мозг дотера\nniggers - осуждаем!\nrp - ультимативный гайд по рп отыгровке\nrap - .rap\nzatka - Форма заявки для набор кадров```')
                await ctx.send('```py\nban - бан участника\nclear - очистка чата, не более 300!\ndm - пишет в лс участнику написанный текст\ngive - выдаёт роль\nkick - кик участника\nmute - мут участника\ntake - забирает роль\nunmute - снятие мута участника.```')
                await ctx.send('```py\nabout - информация о человеке\navatar - аватар человека\nguild - информация о сервере\nremind - напоминание о событии\nroleinfo - информация о роли\nrolemembers - участники роли\nsomeone - упоминание someone\nvote - голосование за что-то.```')
            else:
                emb = discord.Embed(description = f'Команда `{arg}` не обнаружена.', color = discord.Color.orange())
                await ctx.send(embed = emb)

def setup(client):
    client.add_cog(sCephalon(client))
