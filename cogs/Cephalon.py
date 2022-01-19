import asyncio
import os
import secrets

import disnake
from disnake.ext import commands
from pymongo import MongoClient

passw = os.environ.get('passw')
cluster = MongoClient(f"mongodb+srv://cephalon:{passw}@locale.ttokw.mongodb.net/Locale?retryWrites=true&w=majority")
collection = cluster.Locale.locale

guilds = [693929822543675455, 735874149578440855, 818758712163827723]

class Cephalon(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Модуль Cephalon загружен')

    @commands.command() #ru, gnida
    async def locale(self, ctx, locale = None):
        if locale == 'gnida':
            rlocale = collection.find_one({"_id": ctx.author.id})["locale"]
            collection.update_one({"locale": 'ru', '_id': ctx.author.id}, {"$set": {'locale': 'gnida'}})
            await ctx.send('Твоя ёбаная локаль была установлена на `gnida`!')
        if locale == 'ru':
            glocale = collection.find_one({"_id": ctx.author.id})["locale"]
            collection.update_one({"locale": 'gnida', '_id': ctx.author.id}, {"$set": {'locale': 'ru'}})
            await ctx.send('Ваша локаль была установлена на `ru`.')
        if locale == 'test':
            rlocale = collection.find_one({"_id": ctx.author.id})["locale"]
            if rlocale == 'ru':
                await ctx.send('Ваша локаль равна `ru`')
            if rlocale == 'gnida':
                await ctx.send('Твоя ёбаная локаль равна `gnida`')
        if locale == None:
            await ctx.send(embed = disnake.Embed(description = 'Возможные локали:\nru\ngnida\n\nУстановка локали на gnida может подходить не всем серверам.', color = 0x2f3136))

    @commands.command()
    async def setup(self, ctx):
        post = {
            '_id': ctx.author.id,
            'locale': 'ru'
        }
        if collection.count_documents({'_id': ctx.author.id}) == 0:
            collection.insert_one(post)
        role1 = disnake.utils.get(ctx.guild.roles, name = 'Deafened')
        role = disnake.utils.get(ctx.guild.roles, name = 'Muted')
        if role and role1 != None:
            emb = disnake.Embed(description = 'Все нужные роли уже присутсвуют на сервере.', color = disnake.Color.orange())
            return await ctx.send(embed = emb)
        emb = disnake.Embed(description = 'С написанием этой команды на сервер добавлены роли, если их нет. Они будут созданы автоматически, если будут вызваны команды `mute` или `deaf`', color = disnake.Color.orange())
        await ctx.send(embed = emb)
        if role == None:
            await ctx.guild.create_role(name = 'Muted', colour = disnake.Colour(0x000001), reason = 'Создано командой setup.')
        if role1 == None:
            await ctx.guild.create_role(name = 'Deafened', color = disnake.Color(0x000001), reason = 'Создано командой setup.')

    @commands.command()
    async def generate(self, ctx):
        token = ''.join([secrets.choice('QWERTYUIOPASDFGHJKLZXCVBNM1234567890') for i in range(4)])
        token1 = ''.join([secrets.choice('QWERTYUIOPASDFGHJKLZXCVBNM1234567890') for i in range(4)])
        token2 = ''.join([secrets.choice('QWERTYUIOPASDFGHJKLZXCVBNM1234567890') for i in range(4)])
        await ctx.send(f'```{token}-{token1}-{token2}```')

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def info(self, ctx):
        emb = disnake.Embed(colour = disnake.Color.orange())
        emb.set_author(name = self.client.user.name, url = 'https://warframe.fandom.com/wiki/Cephalon_Cy', icon_url = self.client.user.avatar.url)
        emb.add_field(name = 'Версия', value = '0.12.12.10.16367')
        emb.add_field(name = 'Написан на', value = 'disnake.py v2.3.0')
        emb.add_field(name = 'Разработчик', value = '[сасиска#2472](https://discord.com/users/338714886001524737)')
        if ctx.guild.id == 693929822543675455:
            emb.add_field(name = 'Принадлежность', value = 'Это - мой основной сервер.')
        if ctx.guild.id == 735874149578440855:
            emb.add_field(name = 'Тестирование', value = 'Это - мой тестовый сервер.')
        emb.add_field(name = 'Обслуживаю', value = f'{len(self.client.users)} человек')
        emb.add_field(name = 'Существую на', value = f'{len(self.client.guilds)} серверах')
        emb.set_footer(text = 'Данное приложение не имеет никакого причастия к игре Warframe.', icon_url = 'https://i.playground.ru/p/yVaOZNSTdgUTxmzy_qvzzQ.png')
        await ctx.send(embed = emb)
    
    @commands.command(aliases = ['invcy'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def invite(self, ctx, arg = None):
        if arg == None:
            emb = disnake.Embed(description = '[Ссылка](https://discord.com/api/oauth2/authorize?client_id=694170281270312991&permissions=8&scope=bot%20applications.commands) для приглашения Cy на сервера.', colour = disnake.Color.orange())
            await ctx.send(embed = emb)
        if arg == 'beta':
            emb = disnake.Embed(description = '[Ссылка](https://discord.com/oauth2/authorize?client_id=764882153812787250&scope=bot&permissions=8&scope=bot%20applications.commands) для приглашения Cy Beta на сервера.', color = disnake.Color.orange())
            await ctx.send(embed = emb)
        if arg == 'pro':
            emb = disnake.Embed(description = '[Ссылка](https://discord.com/oauth2/authorize?client_id=762015251264569352&scope=bot&permissions=8&scope=bot%20applications.commands) для приглашения Cy PRO на сервера. ~~||ты бля ваще как об этом узнал ебанутый||~~', color = disnake.Color.orange())
            await ctx.send(embed = emb)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ping(self, ctx):
        emb = disnake.Embed(description = f'`fetching..`', colour = disnake.Color.orange())
        emb1 = disnake.Embed(description = f'Pong!  `{round(self.client.latency * 1000)} ms`', colour = disnake.Color.orange())
        message = await ctx.send(embed = emb)
        await asyncio.sleep(self.client.latency)
        await message.edit(embed = emb1)

    @commands.command()
    async def botver(self, ctx):
        emb = disnake.Embed(color = 0x2f3136)
        emb.add_field(name = '0.12.12.10.16367', value = 'Изменение команд Embeds\n\nИзменено написание команд **say**, **edit** и переписана help под их изменение')
        await ctx.send(embed = emb)

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice and ctx.author.voice.channel:
            channel = ctx.author.voice.channel
        else:
            emb = disnake.Embed(description = 'Ты должен быть в канале, чтобы использовать это.', colour = disnake.Color.orange())
            await ctx.send(embed = emb)
        global vc
        vc = await channel.connect()

    @commands.command()
    async def leave(self, ctx):
        if ctx.author.voice and ctx.author.voice.channel:
            pass
        else:
            emb = disnake.Embed(description = 'Ты должен быть в канале, чтобы использовать это.', colour = disnake.Color.orange())
            await ctx.send(embed = emb)
        await vc.disconnect()

    @commands.command()
    async def help(self, ctx, arg = None):
        if arg == None:
            emb = disnake.Embed(description = f'Все доступные команды.', color = disnake.Color.orange())
            emb.set_author(name = self.client.user.name, url = 'https://discord.com/api/oauth2/authorize?client_id=694170281270312991&permissions=8&scope=bot%20applications.commands')
            emb.add_field(name = 'Cephalon', value = '`botver`, `info`, `invite`, `join`, `leave`, `locale`, `ping`, `setup`', inline = False)
            emb.add_field(name = 'Embeds', value = '`content`, `edit`, `say`', inline = False)
            emb.add_field(name = 'Fun', value = '`aye_balbec`, `dotersbrain`, `niggers`, `rp`, `rap`, `zatka`', inline = False)
            emb.add_field(name = 'Mod', value = '`ban`, `clear`, `dm`, `deaf`, `give`, `kick`, `mute`, `take`, `timeout`, `undeaf`, `unmute`', inline = False)
            emb.add_field(name = 'Misc', value = '`about`, `avatar`, `coinflip`, `guild`, `roll`, `remind`, `roleinfo`, `rolemembers`, `someone`, `vote`', inline = False)
            emb.add_field(name = 'ᅠ', value = 'Назовите войс `Создать канал`, чтобы бот автоматически создавал для вас временные каналы, которые будут удаляться после того, как все люди выйдут из него.', inline = False)
            emb.add_field(name = 'ᅠ', value = 'Не используйте [], <>, / при написании команды.', inline = False)
            emb.add_field(name = 'ᅠ', value = '**Используйте** `cy/help [команда/категория]` **для подробностей использования.**\n\n**[Ссылка-приглашение](https://discord.com/api/oauth2/authorize?client_id=694170281270312991&permissions=8&scope=bot%20applications.commands)**', inline = False)
            emb.set_footer(text = 'Cephalon Cy © сасиска#2472')
            return await ctx.send(embed = emb)
        elif arg == 'dotersbrain':
            await ctx.send('```cy/dotersbrain, список слов и рифм: чё - хуй через плечо; а - хуй на; да - пизда; нет - пидора ответ; ок - хуй намок```')
        elif arg == 'timeout':
            await ctx.send('```apache\ncy/timeout <@пинг/имя/ID> <время(s/m/h/d(15s/5m/1h/5d))> [причина] ([] - опционально, <> - обязательно, / - или)```')
        elif arg == 'deaf':
            await ctx.send('```apache\ncy/deaf <@пинг/имя/ID> [причина]\nВ отличии от команды mute, бот будет заглушать людей в голосовом канале с ролью **Deafened**\n([] - опционально, <> - обязательно, / - или)```')
        elif arg == 'undeaf':
            await ctx.send('```apache\ncy/undeaf <@пинг/имя/ID> [причина]\n([] - опционально, <> - обязательно, / - или)```')
        elif arg == 'locale':
            await ctx.send('```apache\ncy/locale [ru/gnida/test]\n([] - опционально, / - или)```')
        elif arg == 'setup':
            await ctx.send('```apache\ncy/setup\nвыполнение команды создаст 4 роли, если их нет на сервере.\nбудет выполнено автоматически, если сработает авто-мут.```')
        elif arg == 'roll':
            await ctx.send('```apache\ncy/roll [от] [до]\nесли не указано [до], [от] станет [до].\ncy/roll 80 (0-80)\ncy/roll 26 90 (26-90)\ncy/roll (0-100)\n([] - опционально)```')
        elif arg == 'about':
            await ctx.send('```apache\ncy/about [@пинг/имя/ID] ([] - опционально, / - или)```')
        elif arg == 'avatar':
            await ctx.send('```apache\ncy/avatar [@пинг/имя/ID] ([] - опционально, / - или)```')
        elif arg == 'ban':
            await ctx.send('```apache\ncy/ban <@пинг/имя/ID> [причина/--soft --reason]\ncy/ban 185476724627210241 --soft --reason лошара\ncy/ban @сасиска чмо\ncy/ban "Sgt White" --soft\n\nПри использовании --soft обязательно указывать --reason после него, однако можно не использовать --reason\n([] - опционально, <> - обязательно, / - или)\nperms = ban_members```')
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
        elif arg == 'mute':
            await ctx.send('```apache\ncy/mute <@пинг/имя/ID> [причина] ([] - опционально, <> - обязательно, / - или)\nperms = view_audit_log```')
        elif arg == 'remind':
            await ctx.send('```apache\ncy/remind <время(s/m/h/d(15s/5m/1h/5d))> <текст> (<> - обязательно, / - или)```')
        elif arg == 'roleinfo':
            await ctx.send('```apache\ncy/roleinfo <@роль/имя роли/ID роли> (<> - обязательно, / - или)```')
        elif arg == 'take':
            await ctx.send('```apache\ncy/take <@пинг/имя/ID> <@роль/имя роли/ID роли> (<> - обязательно, / - или)\nperms = manage_channels```')
        elif arg == 'someone':
            await ctx.send('```apache\ncy/someone <текст> (<> - обязательно)```')
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
        elif arg == 'Fun' or arg == 'fun':
            await ctx.send('```py\naye_balbec - я не ангел и не бес, просто..\ncu - медь\ncoinflip(c, coin) - подкидывает монетку\ndotersbrain - проверка на мозг дотера\nniggers - осуждаем!\nrp - ультимативный гайд по рп отыгровке\nrap - .rap\nzatka - Форма заявки для набор кадров```')
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
            emb = disnake.Embed(description = f'Команда `{arg}` не обнаружена или у неё нет опций, требующие помощи', color = disnake.Color.orange())
            await ctx.send(embed = emb)
        
def setup(client):
    client.add_cog(Cephalon(client))
