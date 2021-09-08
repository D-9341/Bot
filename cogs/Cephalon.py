import asyncio
import datetime
import os

import discord
from discord.ext import commands
from pymongo import MongoClient

passw = os.environ.get('passw')
cluster = MongoClient(f"mongodb+srv://cephalon:{passw}@locale.ttokw.mongodb.net/Locale?retryWrites=true&w=majority")
collection = cluster.Locale.locale

friends = [351071668241956865, 417362845303439360]

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
        if locale == None:
            await ctx.send('Возможные локали:\nru\ngnida\n\nПри установке локали на `gnida` будут прикольные штуки!')

    @commands.command()
    async def locale_test(self, ctx):
        rlocale = collection.find_one({"_id": ctx.author.id})["locale"]
        if rlocale == None:
            post = {
                '_id': ctx.author.id,
                'locale': 'ru'
            }
            if collection.count_documents({'_id': ctx.author.id}) == 0:
                collection.insert_one(post)
        if rlocale == 'ru':
            await ctx.send('Ваша локаль равна `ru`')
        if rlocale == 'gnida':
            await ctx.send('Твоя ёбаная локаль равна `gnida`')

    @commands.command()
    async def setup(self, ctx):
        post = {
            '_id': ctx.author.id,
            'locale': 'ru'
        }
        if collection.count_documents({'_id': ctx.author.id}) == 0:
            collection.insert_one(post)
        role3 = discord.utils.get(ctx.guild.roles, name = '----------Предупреждения----------')
        role1 = discord.utils.get(ctx.guild.roles, name = '1')
        role2 = discord.utils.get(ctx.guild.roles, name = '2')
        role = discord.utils.get(ctx.guild.roles, name = 'Muted')
        if role and role1 and role2 and role3 != None:
            emb = discord.Embed(description = 'Все нужные роли уже присутсвуют на сервере.', color = discord.Color.orange())
            return await ctx.send(embed = emb)
        emb = discord.Embed(description = 'С написанием этой команды на сервер будут добавлены несколько ролей, если их нет. Они нужны для правильной работы авто и обычного мута. Не следует их удалять, так как они будут созданы снова, но уже автоматически.', color = discord.Color.orange())
        await ctx.send(embed = emb)
        if role == None:
            await ctx.guild.create_role(name = 'Muted', colour = discord.Colour(0x000001), reason = 'Создано командой setup.')
        if role3 == None:
            await ctx.guild.create_role(name = '----------Предупреждения----------', color = discord.Color(0x2f3136), reason = 'Создано командой setup.')
        if role1 == None:
            await ctx.guild.create_role(name = '1', color = discord.Color(0xff0000), reason = 'Создано командой setup.')
        if role2 == None:
            await ctx.guild.create_role(name = '2', color = discord.Color(0xff0000), reason = 'Создано командой setup.')

    @commands.command()
    async def generate(self, ctx):
        token = ''.join([secrets.choice('QWERTYUIOPASDFGHJKLZXCVBNM1234567890') for i in range(4)])
        token1 = ''.join([secrets.choice('QWERTYUIOPASDFGHJKLZXCVBNM1234567890') for i in range(4)])
        token2 = ''.join([secrets.choice('QWERTYUIOPASDFGHJKLZXCVBNM1234567890') for i in range(4)])
        await ctx.send(f'```{token}-{token1}-{token2}```')

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def info(self, ctx):
        emb = discord.Embed(colour = discord.Color.orange())
        emb.set_author(name = self.client.user.name, url = 'https://warframe.fandom.com/wiki/Cephalon_Cy', icon_url = self.client.user.avatar_url)
        emb.add_field(name = 'Версия', value = '0.12.11.2.13771')
        emb.add_field(name = 'Написан на', value = 'discord.py v1.7.3 при помощи\ndiscord-py-slash-command v2.0.0.')
        emb.add_field(name = 'Разработчик', value = '[сасиска#2472](https://discord.com/users/338714886001524737)')
        if ctx.guild.owner.id != self.client.owner_id and ctx.guild.owner.id not in friends:
            emb.add_field(name = 'Сервер', value = 'Данный сервер не принадлежит моему Создателю или его знакомым. Все эмбед выводы будут иметь футер с текстом `Cephalon Cy by сасиска#2472`')
        if ctx.guild.id == 693929822543675455:
            emb.add_field(name = 'Принадлежность', value = 'Это - мой основной сервер.')
        if ctx.guild.id == 735874149578440855:
            emb.add_field(name = 'Тестирование', value = 'Это - мой тестовый сервер.')
        emb.add_field(name = 'Обслуживаю', value = f'{len(self.client.users)} человек')
        emb.add_field(name = 'Существую на', value = f'{len(self.client.guilds)} серверах')
        if ctx.guild.owner.id != self.client.owner_id and ctx.guild.owner.id not in friends:
            emb.set_footer(text = 'Данное приложение не имеет никакого причастия к игре Warframe. Cephalon Cy by сасиска#2472', icon_url = 'https://i.playground.ru/p/yVaOZNSTdgUTxmzy_qvzzQ.png')
        else:
            emb.set_footer(text = 'Данное приложение не имеет никакого причастия к игре Warframe.', icon_url = 'https://i.playground.ru/p/yVaOZNSTdgUTxmzy_qvzzQ.png')
        await ctx.send(embed = emb)
    
    @commands.command(aliases = ['invcy'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def invite(self, ctx, arg = None):
        if arg == None:
            emb = discord.Embed(description = '[Ссылка](https://discord.com/api/oauth2/authorize?client_id=694170281270312991&permissions=8&scope=bot%20applications.commands) для приглашения Cy на сервера.', colour = discord.Color.orange())
            if ctx.guild.owner.id != self.client.owner_id and ctx.guild.owner.id not in friends:
                emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
            await ctx.send(embed = emb)
        if arg == 'beta':
            emb = discord.Embed(description = '[Ссылка](https://discord.com/oauth2/authorize?client_id=764882153812787250&scope=bot&permissions=8&scope=bot%20applications.commands) для приглашения Cy Beta на сервера.', color = discord.Color.orange())
            if ctx.guild.owner.id != self.client.owner_id and ctx.guild.owner.id not in friends:
                emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
            await ctx.send(embed = emb)
        if arg == 'pro':
            if ctx.guild.id not in guilds:
                emb = discord.Embed(description = f'Сервер `{ctx.guild}` не имеет активных подписок. Купить можно по [Ссылке](https://www.patreon.com/cephaloncy) Преимущества: пинг не более 25ms, больший аптайм, защита от несанкционированного добавления на сервера.', colour = discord.Color.orange())
                await ctx.send(embed = emb)
            else:
                emb = discord.Embed(description = '[Ссылка](https://discord.com/oauth2/authorize?client_id=762015251264569352&scope=bot&permissions=8&scope=bot%20applications.commands) для приглашения Cy PRO на сервера.', color = discord.Color.orange())
                await ctx.send(embed = emb)
    
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ping(self, ctx):
        emb = discord.Embed(description = f'`fetching..`', colour = discord.Color.orange())
        emb1 = discord.Embed(description = f'Pong!  `{round(self.client.latency * 1000)} ms`', colour = discord.Color.orange())
        message = await ctx.send(embed = emb)
        if ctx.guild.owner.id != self.client.owner_id and ctx.guild.owner.id not in friends:
            emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
            emb1.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await asyncio.sleep(self.client.latency)
        await message.edit(embed = emb1)
        
    @commands.command()
    async def botver(self, ctx):
        emb = discord.Embed(color = 0x2f3136)
        emb.add_field(name = '0.12.11.2.13771 (Текущая версия, нормальное обновление)', value = 'Deaf/Undeaf:\nЗаглушает участника в голосовом канале, когда в его ролях есть Deafened\nHelp:\nТеперь указывает список команд, применимый для способа вызова Help. Таким образом, Slash-help будет показывать команды только без конвертеров, а обычная Help все команды.\nТакже, многочисленные исправления', inline = False)
        emb.add_field(name = '0.12.10.2.12528 (Предыдущая версия, полная перепись кода)', value = 'Отдельные куски кода были рассортированы по разным файлам.', inline = False)
        await ctx.send(embed = emb)

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice and ctx.author.voice.channel:
            channel = ctx.author.voice.channel
        else:
            emb = discord.Embed(description = 'Ты должен быть в канале, чтобы использовать это.', colour = discord.Color.orange())
            if ctx.guild.owner.id != self.client.owner_id and ctx.guild.owner.id not in friends:
                emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
            await ctx.send(embed = emb)
        global vc
        vc = await channel.connect()

    @commands.command()
    async def leave(self, ctx):
        if ctx.author.voice and ctx.author.voice.channel:
            pass
        else:
            emb = discord.Embed(description = 'Ты должен быть в канале, чтобы использовать это.', colour = discord.Color.orange())
            if ctx.guild.owner.id != self.client.owner_id and ctx.guild.owner.id not in friends:
                emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
            await ctx.send(embed = emb)
        await vc.disconnect()

    @commands.command()
    async def help(self, ctx, arg = None):
        if arg == None:
            emb = discord.Embed(description = f'Доступные команды.', color = discord.Color.orange())
            emb.set_author(name = self.client.user.name, url = 'https://discord.com/api/oauth2/authorize?client_id=694170281270312991&permissions=8&scope=bot%20applications.commands')
            emb.add_field(name = 'Cephalon', value = '`botver`, `info`, `invite`, `join`, `leave`, `locale`, `ping`, `setup`', inline = False)
            emb.add_field(name = 'Embeds', value = '`content`, `edit`, `say`', inline = False)
            if not (ctx.guild.owner.id != self.client.owner_id and ctx.guild.owner.id not in friends):
                emb.add_field(name = 'Fun', value = '`aye_balbec`, `cu`, `coinflip`, `dotersbrain`, `niggers`, `rp`, `rap`, `roll`, `zatka`', inline = False)
            emb.add_field(name = 'Mod', value = '`ban`, `clear`, `dm`, `deaf`, `give`, `kick`, `mute`, `take`, `undeaf`, `unmute`', inline = False)
            emb.add_field(name = 'Misc', value = '`about`, `avatar`, `guild`, `remind`, `roleinfo`, `rolemembers`, `someone`, `vote`', inline = False)
            emb.add_field(name = 'ᅠ', value = 'Назовите войс `Создать канал`, чтобы бот автоматически создавал для вас временные каналы, которые будут удаляться после того, как все люди выйдут из него.', inline = False)
            emb.add_field(name = 'ᅠ', value = '**Используйте** `cy/help [команда/категория]` **для подробностей использования.**\n\n[Ссылка-приглашение](https://discord.com/api/oauth2/authorize?client_id=694170281270312991&permissions=8&scope=bot%20applications.commands)', inline = False)
            emb.set_footer(text = 'Cephalon Cy © сасиска#2472')
            return await ctx.send(embed = emb)
        elif arg == 'deaf':
            await ctx.send('```apache\ncy/deaf <@пинг/имя/ID> [причина]\nВ отличии от команды mute, бот будет заглушать людей в голосовом канале с ролью *Deafened*\n([] - опционально, <> - обязательно, / - или)```')
        elif arg == 'undeaf':
            await ctx.send('```apache\ncy/undeaf <@пинг/имя/ID> [причина]\n([] - опционально, <> - обязательно, / - или)```')
        elif arg == 'locale':
            await ctx.send('```apache\ncy/locale [ru/gnida]\n([] - опционально)```')
        elif arg == 'setup':
            await ctx.send('```apache\ncy/setup\nвыполнение команды создаст 4 роли, если их нет на сервере.\nбудет выполнено автоматически, если сработает авто-мут.```')
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
        elif arg == 'mute':
            await ctx.send('```apache\ncy/mute <@пинг/имя/ID> <время(s/m/h/d(15s, 5m, 1h, 5d))> [причина] ([] - опционально, <> - обязательно, / - или)\nperms = view_audit_log```')
        elif arg == 'remind':
            await ctx.send('```apache\ncy/remind <время(s/m/h/d(15s, 5m, 1h, 5d))> <текст> (<> - обязательно, / - или)```')
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
        elif arg == 'aye_balbec':
            await ctx.send('```cy/aye_balbec```')
        elif arg == 'cu':
            await ctx.send('```cy/cu```')
        elif arg == 'coinflip' or arg == 'coin' or arg == 'c':
            await ctx.send('```cy/c```')
        elif arg == 'dotersbrain':
            await ctx.send('```cy/dotersbrain, список слов и рифм: чё - хуй через плечо; а - хуй на; да - пизда; нет - пидора ответ; ок - хуй намок```')
        elif arg == 'niggers':
            await ctx.send('```cy/niggers```')
        elif arg == 'rp':
            await ctx.send('```cy/rp```')
        elif arg == 'rap':
            await ctx.send('```cy/rap```')
        elif arg == 'zatka':
            await ctx.send('```cy/zatka```')
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
            emb = discord.Embed(description = f'Команда `{arg}` не обнаружена.', color = discord.Color.orange())
            await ctx.send(embed = emb)
        
def setup(client):
    client.add_cog(Cephalon(client))
