import asyncio
import os
import secrets

import discord
from discord.ext import commands
from pymongo import MongoClient

passw = os.environ.get('passw')
cluster = MongoClient(f"mongodb+srv://cephalon:{passw}@locale.ttokw.mongodb.net/Locale?retryWrites=true&w=majority")
collection = cluster.Locale.locale

friends = [351071668241956865, 417362845303439360]

guilds = [693929822543675455, 735874149578440855, 818758712163827723]

uptime = discord.utils.utcnow()

def reset_cooldown(command: commands.Command, message: discord.Message) -> None:
    if command._buckets.valid:
        bucket = command._buckets.get_bucket(message)
        bucket._tokens = min(bucket.rate, bucket._tokens + 1)

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
    async def help(self, ctx, arg = None):
        if arg == None:
            emb = discord.Embed(description = 'Все доступные команды.', color = 0xff8000)
            emb.set_author(name = self.client.user.name, url = 'https://discord.com/api/oauth2/authorize?client_id=694170281270312991&permissions=8&scope=bot%20applications.commands')
            emb.add_field(name = 'Cephalon', value = '`botver`, `info`, `invite`, `locale`, `ping`, `setup`, `uptime`', inline = False)
            emb.add_field(name = 'Embeds', value = '`content`, `edit`, `say`', inline = False)
            emb.add_field(name = 'Mod', value = '`ban`, `clear`, `dm`, `deaf`, `give`, `kick`, `mute`, `take`, `timeout`, `undeaf`, `unmute`', inline = False)
            emb.add_field(name = 'Misc', value = '`about`, `avatar`, `coinflip`, `guild`, `roll`, `remind`, `roleinfo`, `rolemembers`, `someone`, `vote`', inline = False)
            #emb.add_field(name = 'Music', value = '`join`, `leave`, `play`, `pause`, `resume`, `volume`')
            emb.add_field(name = 'ᅠ', value = 'Назовите войс `Создать канал`, чтобы бот автоматически создавал для вас временные каналы, которые будут удаляться после того, как все люди выйдут из него.', inline = False)
            emb.add_field(name = 'ᅠ', value = 'Не используйте [], <>, / при написании команды.', inline = False)
            emb.add_field(name = 'ᅠ', value = '**Используйте** `cy/help [команда]` **для подробностей использования.**\n\n**[Ссылка-приглашение](https://discord.com/api/oauth2/authorize?client_id=694170281270312991&permissions=8&scope=bot%20applications.commands)**', inline = False)
            emb.set_footer(text = 'Cephalon Cy ©️ Sus&Co\n2020 - Present')
            return await ctx.send(embed = emb)
        #elif arg == 'play':
        #    await ctx.send('```apache\ncy/play <ссылка на видео YouTube>\nСсылка должна быть только с YouTube\n\n(<> - обязательно)```')
        #elif arg == 'volume':
        #    await ctx.send('```apache\ncy/volume <громкость>\nГромкость должна быть в пределе от 0 до 100\n\n(<> - обязательно)```')
        elif arg == 'timeout':
            await ctx.send('```apache\ncy/timeout <@пинг/имя/ID> <время(s/m/h/d(15s/5m/1h/5d))> [причина]\n\n([] - опционально, <> - обязательно, / - или)```')
        elif arg == 'deaf':
            await ctx.send('```apache\ncy/deaf <@пинг/имя/ID> [причина]\nВ отличии от команды mute, бот будет заглушать людей в голосовом канале с ролью **Deafened**\n\n([] - опционально, <> - обязательно, / - или)```')
        elif arg == 'undeaf':
            await ctx.send('```apache\ncy/undeaf <@пинг/имя/ID> [причина]\n\n([] - опционально, <> - обязательно, / - или)```')
        elif arg == 'setup':
            await ctx.send('```apache\ncy/setup\nвыполнение команды создаст 2 роли, если их нет на сервере.\nбудет выполнено автоматически, если будут вызваны команды mute или deaf.```')
        elif arg == 'roll':
            await ctx.send('```apache\ncy/roll [от] [до]\nесли не указано [до], [от] станет [до].\ncy/roll 80 (0-80)\ncy/roll 26 90 (26-90)\ncy/roll (0-100)\n\n([] - опционально)```')
        elif arg == 'about':
            await ctx.send('```apache\ncy/about [@пинг/имя/ID]\n\n([] - опционально, / - или)```')
        elif arg == 'avatar':
            await ctx.send('```apache\ncy/avatar [@пинг/имя/ID]\n\n([] - опционально, / - или)```')
        elif arg == 'ban':
            await ctx.send('```apache\ncy/ban <@пинг/имя/ID> [причина/--soft --reason]\ncy/ban 185476724627210241 --soft --reason лошара\ncy/ban @сасиска чмо\ncy/ban "Sgt White" --soft\n\nПри использовании --soft обязательно указывать --reason после него, однако можно не использовать --reason\n([] - опционально, <> - обязательно, / - или)\nperms = ban_members```')
        elif arg == 'content' or arg == 'ctx':
            await ctx.send('```apache\ncy/content <ID> [канал, в котором находится сообщение]\n\n([] - опционально, <> - обязательно)```')
        elif arg == 'clear':
            await ctx.send('```apache\ncy/clear <количество> [диапазон] [фильтр]\ncy/clear 100\ncy/clear 10\ncy/clear 50 --everyone хыха\ncy/clear 30 --bots\ncy/clear 15 --users\ncy/clear 5 --silent\ncy/clear 200 "--silent --everyone" хыха\n\n--everyone удалит сообщения от всех\n--bots удалит сообщения только от ботов\n--users удалит сообщения только от участников\n--silent не покажет результаты удаления сообщений\n\nПри указании диапазона не будет удалено столько сообщений, сколько было указано, будет удалено столько, сколько будет найдено в пределах заданного количества сообщений.\nДопустим cy/clear 10 --bots\nЕсли сообщения от ботов и людей чередуются, будет удалено лишь то кол-во сообщений от ботов, что было найдено в указанном пределе 10.\n\nСообщения старше 2 недель будут удалены не сразу - лимит discord API\nПри удалении более 100 сообщений нужно подтверждение владельца сервера.\nТолько владелец сервера может удалять от 250 сообщений за раз.\nНе более 300 за раз!\n\n([] - опционально, <> - обязательно, / - или)\nperms = administrator```')
        elif arg == 'dm':
            await ctx.send('```apache\ncy/dm <@пинг/имя/ID> <текст>\n\n(<> - обязательно, / - или)\nperms = view_audit_log```')
        elif arg == 'say':
            await ctx.send('```apache\ncy/say [обычный текст] [&t title текст] [&d description текст] [&th ссылка на картинку справа] [&img ссылка на картинку снизу] [&f footer текст] [&c цвет в HEX коде] [&msg сообщение над эмбедом]\ncy/say &t Заголовок &d Описание\ncy/say [текст]\nУчтите, что если вы захотите упомянуть роль с использованием какого либо аргумента текст не будет показан из-за способа упоминания ролей в Discord\nВсе аргументы являются необязательными, но если отправить пустую команду - ответ будет этим сообщением\n\n([] - опционально)```')
        elif arg == 'edit':
            await ctx.send('```apache\ncy/edit <ID> [обычный текст] [&t title текст] [&d description текст] [&f footer текст] [&c цвет в HEX коде] [&th ссылка на картинку справа] [&img ссылка на картинку снизу]\ncy/edit <ID> [текст]\ncy/edit <ID> --clean\ncy/edit <ID> --noembed\ncy/edit <ID> --delete\n\n--clean удалит контент над эмбедом\n--noembed удалит эмбед\n--delete удалит сообщение\nИспользование --clean и --noembed одновременно невозможно, так как сообщение должно будет стать пустым. При этом --clean выполниться первым.\nПри редактировании сообщения с эмбедом цвет этого эмбеда сбросится на стандартный, если не указывать &c с нужным цветом.\nЕсли у сообщения есть эмбед и в команде нет агрументов, автоматически будет заменён &msg\n\n([] - опционально, <> - обязательно)\nperms = manage_channels```')
        elif arg == 'give':
            await ctx.send('```apache\ncy/give <@пинг/имя/ID> <@роль/имя роли/ID роли>\n\n(<> - обязательно, / - или)\nperms = manage_channels```')
        elif arg == 'kick':
            await ctx.send('```apache\ncy/kick <@пинг/имя/ID> [причина]\n\n([] - опционально, <> - обязательно, / - или)\nperms = kick_members```')
        elif arg == 'mute':
            await ctx.send('```apache\ncy/mute <@пинг/имя/ID> [причина]\n\n([] - опционально, <> - обязательно, / - или)\nperms = view_audit_log```')
        elif arg == 'roleinfo':
            await ctx.send('```apache\ncy/roleinfo <@роль/имя роли/ID роли>\n\n(<> - обязательно, / - или)```')
        elif arg == 'take':
            await ctx.send('```apache\ncy/take <@пинг/имя/ID> <@роль/имя роли/ID роли>\n\n(<> - обязательно, / - или)\nperms = manage_channels```')
        elif arg == 'someone':
            await ctx.send('```apache\ncy/someone <текст>\n\n(<> - обязательно)```')
        elif arg == 'unmute':
            await ctx.send('```apache\ncy/unmute <@пинг/имя/ID> [причина]\n\n([] - опционально, <> - обязательно, / - или)\nperms = manage_channels```')
        elif arg == 'vote':
            await ctx.send('```apache\ncy/vote <текст>\n\n(<> - обязательно)```')
        elif arg == 'help':
            await ctx.send('```apache\ncy/help [команда]\n\n([] - опционально)```')
        else:
            emb = discord.Embed(description = f'Команда `{arg}` не обнаружена или выполняется лишь её написанием.', color = 0xff8000)
            await ctx.send(embed = emb)

    @commands.command()
    async def uptime(self, ctx):
        bot_time = discord.utils.utcnow() - uptime
        await ctx.send(embed = discord.Embed(description = f'Я в сети уже `{bot_time}`', color = 0x2f3136))

    @commands.command() #ru, gnida, en
    async def locale(self, ctx):
        rlocale = collection.find_one({"_id": ctx.author.id})["locale"]
        rbutton = GrayButton('RU')
        gbutton = RedButton('GNIDA')
        ebutton = GrayButton('EN')
        tbutton = GrayButton('TEST')
        ibutton = GrayButton('INFO')
        ybutton = RedButton('YES')
        nbutton = GrayButton('NO')
        confirm = discord.ui.View(timeout = 5)
        confirm.add_item(ybutton)
        confirm.add_item(nbutton)
        view = discord.ui.View(timeout = 5)
        view.add_item(rbutton)
        view.add_item(gbutton)
        view.add_item(ebutton)
        view.add_item(tbutton)
        view.add_item(ibutton)
        async def on_timeout(interaction):
            await interaction.response.edit_message('Время вышло', view = None)
        async def rbutton_callback(interaction):
            collection.update_one({'_id': ctx.author.id}, {"$set": {'locale': 'ru'}})
            await interaction.response.edit_message(content = 'Ваша локаль была установлена на `ru`.', view = None)
        async def gbutton_callback(interaction):
            await interaction.response.edit_message(content = 'Ты бля уверен?', view = confirm)
        async def ybutton_callback(interaction):
            collection.update_one({'_id': ctx.author.id}, {"$set": {'locale': 'gnida'}})
            await interaction.response.edit_message(content = 'Твоя ёбаная локаль была установлена на `gnida`!', view = None)
        async def nbutton_callback(interaction):
            await interaction.response.edit_message(content = 'Ну ок ||локаль осталась той же самой||', view = None)
        async def ebutton_callback(interaction):
            collection.update_one({'_id': ctx.author.id}, {"$set": {'locale': 'en'}})
            await interaction.response.edit_message(content = 'Your locale has been set to `en`.', view = None)
        async def test_callback(interaction):
            if rlocale == 'ru':
                await interaction.response.edit_message(content = 'Ваша локаль установлена на `ru`', view = None)
            if rlocale == 'gnida':
                await interaction.response.edit_message(content = 'Твоя ёбаная локаль установлена на `gnida`', view = None)
            if rlocale == 'en':
                await interaction.response.edit_message(content = 'Your locale set to `en`', view = None)
        async def info_callback(interaction):
            if rlocale == 'ru':
                await interaction.response.edit_message(content = None, embed = discord.Embed(description = 'Возможные локали:\nru\ngnida\nen\n\nУстановка локали на gnida производится на __ваш__ страх и риск. Автор этой локали, равно как и кода этого приложения не несут ответсвенности за **__любые__** происшествия, связанные с этой локалью.', color = 0xb00b69), view = None)
            if rlocale == 'gnida':
                await interaction.response.edit_message(content = None, embed = discord.Embed(description = 'Возможные локали:\nru\ngnida\nen\n\nТут короче предупреждение должно быть о том, создатель бота и/или локали ответственности за неё не несёт.', color = 0xb00b69), view = None)
            if rlocale == 'en':
                await interaction.response.edit_message(content = None, embed = discord.Embed(description = 'Possible locales:\nru\ngnida\nen\n\nlocale gnida is the Russian one, you don`t need that.', color = 0xb00b69), view = None)
        rbutton.callback = rbutton_callback
        gbutton.callback = gbutton_callback
        ebutton.callback = ebutton_callback
        tbutton.callback = test_callback
        ibutton.callback = info_callback
        ybutton.callback = ybutton_callback
        nbutton.callback = nbutton_callback
        if rlocale == 'ru':
            rbutton.disabled = True
            sent = await ctx.send('Выберите опцию:', view = view)
        if rlocale == 'gnida':
            gbutton.disabled = True
            sent = await ctx.send('Чё надо', view = view)
        if rlocale == 'en':
            ebutton.disabled = True
            sent = await ctx.send('Choose option:', view = view)
  
    @commands.command()
    async def setup(self, ctx):
        post = {
            '_id': ctx.author.id,
            'locale': 'ru'
        }
        if collection.count_documents({'_id': ctx.author.id}) == 0:
            collection.insert_one(post)
        role1 = discord.utils.get(ctx.guild.roles, name = 'Deafened')
        role = discord.utils.get(ctx.guild.roles, name = 'Muted')
        if role and role1 != None:
            emb = discord.Embed(description = 'Все нужные роли уже присутсвуют на сервере.', color = 0xff8000)
            return await ctx.send(embed = emb)
        emb = discord.Embed(description = 'С написанием этой команды на сервер добавлены роли, если их нет. Они будут созданы автоматически, если будут вызваны команды `mute` или `deaf`', color = 0xff8000)
        await ctx.send(embed = emb)
        if role == None:
            await ctx.guild.create_role(name = 'Muted', color = discord.Color(0x000001), reason = 'Создано командой setup.')
        if role1 == None:
            await ctx.guild.create_role(name = 'Deafened', color = discord.Color(0x000001), reason = 'Создано командой setup.')

    @commands.command()
    async def generate(self, ctx):
        if ctx.author.id not in self.client.owner_ids:
            raise commands.NotOwner()
        else:
            token = ''.join([secrets.choice('QWERTYUIOPASDFGHJKLZXCVBNM1234567890') for i in range(4)])
            token1 = ''.join([secrets.choice('QWERTYUIOPASDFGHJKLZXCVBNM1234567890') for i in range(4)])
            token2 = ''.join([secrets.choice('QWERTYUIOPASDFGHJKLZXCVBNM1234567890') for i in range(4)])
            await ctx.send(f'```{token}-{token1}-{token2}```')

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def info(self, ctx):
        emb = discord.Embed(color = 0xff8000)
        emb.set_author(name = self.client.user.name, url = 'https://warframe.fandom.com/wiki/Cephalon_Cy', icon_url = self.client.user.avatar.url)
        emb.add_field(name = 'Версия', value = '0.12.12.30.0')
        emb.add_field(name = 'Написан на', value = f'discord.py v{discord.__version__}')
        emb.add_field(name = 'Разработчики 🇷🇺', value = '[сасиска#2472](https://discord.com/users/338714886001524737)\n[Prokaznik#2785](https://discord.com/users/417012231406878720)')
        if ctx.guild.id == 693929822543675455:
            emb.add_field(name = 'Принадлежность', value = 'Это - мой основной сервер.')
        if ctx.guild.id == 735874149578440855:
            emb.add_field(name = 'Тестирование', value = 'Это - мой тестовый сервер.')
        emb.add_field(name = 'Обслуживаю', value = f'{len(self.client.users)} человек')
        emb.add_field(name = 'Существую на', value = f'{len(self.client.guilds)} серверах')
        emb.set_footer(text = 'Данное приложение не имеет никакого причастия к игре Warframe.', icon_url = 'https://i.playground.ru/p/yVaOZNSTdgUTxmzy_qvzzQ.png')
        await ctx.send(embed = emb)

    @commands.command()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def owners(self, ctx):
        emb = discord.Embed(description = 'Владельцы бота, в частности члены команды Sus&Co', color = 0xff8000)
        emb.add_field(name = 'сасиска', value = 'Первичный владелец бота, по совместительству основатель Sus&Co')
        emb.add_field(name = 'Проказник', value = 'Причастен к созданию локали gnida, помогает с идеями для основного бота.')
        await ctx.send(embed = emb)
    
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def invite(self, ctx, arg = None):
        if arg == None:
            emb = discord.Embed(description = '[Ссылка](https://discord.com/oauth2/authorize?client_id=694170281270312991&permissions=8&scope=bot%20applications.commands) для приглашения Cy на сервера.', color = 0xff8000)
            await ctx.send(embed = emb)
        if arg == 'beta':
            emb = discord.Embed(description = '[Ссылка](https://discord.com/oauth2/authorize?client_id=764882153812787250&scope=bot&permissions=8&scope=bot%20applications.commands) для приглашения Cy Beta на сервера.', color = 0xff8000)
            await ctx.send(embed = emb)
        if arg == 'pro':
            if ctx.author.id not in self.client.owner_ids:
                raise commands.NotOwner()
            else:
                emb = discord.Embed(description = '[Ссылка](https://discord.com/oauth2/authorize?client_id=762015251264569352&scope=bot&permissions=8&scope=bot%20applications.commands) для приглашения Cy PRO на сервера.', color = 0xff8000)
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
        emb.add_field(name = '0.12.12.30.0', value = '**Библиотека**\nСовершён переезд на discord.py, позволяющий облегчить существование бота\n**someone**\nИсправлена ошибка, не позволяющяя писать более одного слова, в то время как остальные просто игнорировались\n**edit, say**\nБыли починены и улучшены, возвращён аргумент &c\n**Категория Fun**\nУдалена.\n**Locale**\nТеперь изменения локали применяются ко всем командам.\n\n***Slash-команды неактивны.***')
        await ctx.send(embed = emb)

async def setup(client):
    await client.add_cog(Cephalon(client))
