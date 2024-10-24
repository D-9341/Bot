# coding=utf-8
import asyncio
import os
import random
import json
import discord

from dotenv import load_dotenv
from functions import get_plural_form
from pathlib import Path
from discord.ext import commands

intents = discord.Intents.all()

client = commands.Bot(command_prefix = commands.when_mentioned_or('cy/'), intents = intents, status = discord.Status.idle, activity = discord.Activity(type = discord.ActivityType.watching, name = 'в никуда'), owner_ids = {338714886001524737, 417012231406878720}, case_insensitive = True, allowed_mentions = discord.AllowedMentions(everyone = False))
client.remove_command('help')
CWD = Path(__file__).parents[0]
CWD = str(CWD)
load_dotenv(CWD + '\\vars.env')

def rearm(command: commands.Command, message: discord.Message):
    if command._buckets.valid:
        bucket = command._buckets.get_bucket(message)
        bucket._tokens = min(bucket.rate, bucket._tokens + 1)

@client.event
async def on_ready():
    await client.tree.sync()
    channel = client.get_channel(714175791033876490)
    emb = discord.Embed(description = 'В сети, поверхностная проверка не выявила ошибок', color = 0x2f3136, timestamp = discord.utils.utcnow())
    emb.set_footer(text = 'Cephalon Cy © Sus&Co')
    await channel.send(embed = emb)

@client.event
async def on_guild_role_update(before, after):
    if before.name == 'Muted':
        role = before.guild.get_role(after.id)
        await role.edit(name = 'Muted', color = 0x000001, reason = 'Нельзя изменять эту роль')
    if before.name == 'Deafened':
        role = before.guild.get_role(after.id)
        await role.edit(name = 'Deafened', color = 0x000001, reason = 'Нельзя изменять эту роль')

@client.event
async def on_command_completion(ctx):
    channel = client.get_channel(714175791033876490)
    emb = discord.Embed(title = 'ВЫПОЛНЕНИЕ_КОМАНДЫ', color = 0xff8000)
    emb.add_field(name = 'НАЗВАНИЕ', value = f'```{ctx.command.name}```')
    emb.add_field(name = 'ИСПОЛНИТЕЛЬ', value = f'{ctx.author.mention} ({ctx.author})')
    emb.add_field(name = 'СЕРВЕР', value = ctx.guild.name if ctx.guild else "ЛС", inline = False)
    emb.add_field(name = 'КАНАЛ', value = f'{ctx.channel.name} ({ctx.channel.mention})' if ctx.guild else "Недоступно в ЛС", inline = False)
    await channel.send(embed = emb)

@client.event
async def on_member_update(before, after):
    if before.id == 417362845303439360:
        if before.nick == 'Марат Каскинов':
            await after.edit(nick = 'Марат Каскинов', reason = 'Против пиписькина')

@client.event
async def on_member_join(member):
    user = 'БОТ' if member.bot else 'УЧАСТНИК'
    channel = client.get_channel(714175791033876490)
    emb = discord.Embed(title = rf'{user}\_ЗАШЁЛ\_НА_СЕРВЕР', color = 0xff8000, timestamp = discord.utils.utcnow())
    emb.add_field(name = f'{user}', value = member)
    emb.add_field(name = 'УПОМИНАНИЕ', value = member.mention)
    emb.add_field(name = 'СЕРВЕР', value = member.guild.name)
    emb.set_footer(text = f'ID: {member.id}')
    await channel.send(embed = emb)

@client.event
async def on_member_remove(member):
    user = 'БОТ' if member.bot else 'УЧАСТНИК'
    channel = client.get_channel(714175791033876490)
    emb = discord.Embed(title = rf'{user}\_ВЫШЕЛ\_С_СЕРВЕРА', color = 0xff8000, timestamp = discord.utils.utcnow())
    emb.add_field(name = f'{user}', value = member)
    emb.add_field(name = 'УПОМИНАНИЕ', value = member.mention)
    emb.add_field(name = 'СЕРВЕР', value = member.guild.name)
    emb.set_footer(text = f'ID: {member.id}')
    await channel.send(embed = emb)

@client.event
async def on_guild_remove(guild):
    channel = client.get_channel(714175791033876490)
    emb = discord.Embed(title = r'ВЫХОД\_С_СЕРВЕРА', color = 0xff8000, timestamp = discord.utils.utcnow())
    emb.add_field(name = 'СЕРВЕР', value = guild.name)
    emb.set_footer(text = f'ID: {guild.id}')
    await channel.send(embed = emb)

@client.event
async def on_guild_join(guild):
    channel = client.get_channel(714175791033876490)
    emb = discord.Embed(title = r'ДОБАВЛЕНИЕ\_НА_СЕРВЕР', color = 0xff8000, timestamp = discord.utils.utcnow())
    emb.add_field(name = 'СЕРВЕР', value = guild.name)
    emb.set_footer(text = f'ID: {guild.id}')
    await channel.send(embed = emb)

@client.event
async def on_voice_state_update(member, before, after):
    role = discord.utils.get(member.guild.roles, name = 'Deafened')
    if after.channel.name == 'Создать канал':
        await after.channel.edit(user_limit = 1)
        room = 'чё' if member.bot is True else f'Канал {member.display_name}'
        bitrate_map = {
            0: 96000,
            1: 128000,
            2: 256000,
        }
        bitrate = bitrate_map.get(member.guild.premium_tier, 384000)
        channel = await member.guild.create_voice_channel(name = room, category = after.channel.category, bitrate = bitrate)
        await member.move_to(channel)
        await channel.set_permissions(member, mute_members = True, move_members = True, manage_channels = True)
        await channel.send(embed = discord.Embed(description = 'Этот канал удалится после того, как все люди выйдут из него. Исключение - перезапуск бота. В таком случае, что делать с каналом решать вам', color = 0xff8000))
        def check(a, b, c): return len(channel.members) == 0
        await client.wait_for('voice_state_update', check = check)
        await channel.delete()
    if role in member.roles:
        await member.edit(mute = True, reason = 'Заглушён командой deaf')

@client.event
async def on_message(message):
    await client.process_commands(message)
    if message.author.bot is False:
        with open('locales/users.json', 'r', encoding = 'utf-8') as users_file:
            file = json.load(users_file)
        if str(message.author.id) not in file:
            file[str(message.author.id)] = 'ru'
            with open('locales/users.json', 'w', encoding = 'utf-8') as users_file:
                json.dump(file, users_file, indent = 4)
    if message.content.startswith(f'<@{client.user.id}>') and len(message.content) == len(f'<@{client.user.id}>'):
        await message.channel.send(f'чё звал {message.author.mention} ||`cy/`||')
    if message.channel.id == 1041417879788208169:
        if message.author.bot is True and message.author.id != 694170281270312991:
            role = discord.utils.get(message.guild.roles, id = 1078051320088510644)
            sent = await message.channel.send(role.mention)
            await sent.delete()
            channel = client.get_channel(714175791033876490)
            emb = discord.Embed(title = r'ОПОВЕЩЕНИЕ\_ОБ_ОБНОВЛЕНИИ', color = 0xff8000, timestamp = discord.utils.utcnow())
            emb.add_field(name = 'ОПОВЕЩЕНЫ', value = 'РАЗРАБОТЧИКИ')
            await channel.send(embed = emb)
    elif message.channel.id == 750372413102883028:
        if message.author.bot is True and message.author.id != 694170281270312991:
            role = discord.utils.get(message.guild.roles, id = 750368477671325728)
            sent = await message.channel.send(role.mention)
            await sent.delete()
            channel = client.get_channel(714175791033876490)
            emb = discord.Embed(title = r'ОПОВЕЩЕНИЕ\_ОБ_ОБНОВЛЕНИИ', color = 0xff8000, timestamp = discord.utils.utcnow())
            emb.add_field(name = 'ОПОВЕЩЕНЫ', value = role.mention)
            await channel.send(embed = emb)
    elif message.channel.id == 750368033578680361:
        if message.author.bot is True and message.author.id != 694170281270312991:
            role = discord.utils.get(message.guild.roles, id = 750366804689420319)
            sent = await message.channel.send(role.mention)
            await sent.delete()
            channel = client.get_channel(714175791033876490)
            emb = discord.Embed(title = r'ОПОВЕЩЕНИЕ\_ОБ_ОБНОВЛЕНИИ', color = 0xff8000, timestamp = discord.utils.utcnow())
            emb.add_field(name = 'ОПОВЕЩЕНЫ', value = role.mention)
            await channel.send(embed = emb)
    elif message.channel.id == 750363498290348123:
        if message.author.bot is True and message.author.id != 694170281270312991:
            role = discord.utils.get(message.guild.roles, id = 750363797226782802)
            sent = await message.channel.send(role.mention)
            await sent.delete()
            channel = client.get_channel(714175791033876490)
            emb = discord.Embed(title = r'ОПОВЕЩЕНИЕ\_ОБ_ОБНОВЛЕНИИ', color = 0xff8000, timestamp = discord.utils.utcnow())
            emb.add_field(name = 'ОПОВЕЩЕНЫ', value = role.mention)
            await channel.send(embed = emb)
    elif message.channel.id == 750373602460827730:
        if message.author.bot is True and message.author.id != 694170281270312991:
            role = discord.utils.get(message.guild.roles, id = 750373687479238787)
            sent = await message.channel.send(role.mention)
            await sent.delete()
            channel = client.get_channel(714175791033876490)
            emb = discord.Embed(title = r'ОПОВЕЩЕНИЕ\_ОБ_ОБНОВЛЕНИИ', color = 0xff8000, timestamp = discord.utils.utcnow())
            emb.add_field(name = 'ОПОВЕЩЕНЫ', value = role.mention)
            await channel.send(embed = emb)
    elif message.channel.id == 1298756046604734594:
        if message.author.bot is True and message.author.id != 694170281270312991:
            sus = client.get_user(338714886001524737)
            await message.channel.send(sus.mention)
    elif message.channel.id == 707498623981715557:
        await message.add_reaction('👍')
        await message.add_reaction('👎')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.DisabledCommand):
        emb = discord.Embed(description = f'{ctx.author.mention}, команда `{ctx.command.name}` отключена', color = 0xff8000)
        await ctx.send(embed = emb)
    elif isinstance(error, commands.NotOwner):
        emb = discord.Embed(description = f'{ctx.author.mention}, это действие может совершить только один из создателей бота', color = 0xff8000)
        emb.set_footer(text = 'Счётчик перезарядки сброшен')
        await ctx.send(embed = emb)
    elif isinstance(error, commands.BotMissingPermissions):
        emb = discord.Embed(description = f'{ctx.author.mention}, у **меня** недостаточно прав на выполнение команды `{ctx.command.name}`, напишите cy/help `{ctx.command.name}` для просмотра необходимых прав\n||Выдача прав администратора решит эту проблему||', color = 0xff0000)
        await ctx.send(embed = emb)
    elif isinstance(error, commands.MissingPermissions):
        emb = discord.Embed(description = f'{ctx.author.mention}, у вас недостаточно прав на выполнение команды `{ctx.command.name}`. Напишите cy/help `{ctx.command.name}` для просмотра необходимых прав', color = 0xff8000)
        await ctx.send(embed = emb)
    elif isinstance(error, commands.CommandOnCooldown):
        s = error.retry_after
        choises = ['Ещё не время.', 'Я не готов.', 'Ещё нет.', 'Ещё. Не. Время.', 'Я. Не. Готов.', 'Ещё. Нет.', 'ЕЩЁ НЕ ВРЕМЯ!', 'Я НЕ ГОТОВ!', 'ЕЩЁ НЕТ!']
        rand = random.choice(choises)
        emb = discord.Embed(description = f'{rand} Команда `{ctx.command.name}` будет доступна через {round(s)} {get_plural_form(round(s), ["секунду", "секунды", "секунд"])}!', color = 0xff0000)
        await ctx.send(embed = emb)
    elif isinstance(error, commands.MissingRequiredArgument):
        rearm(ctx.command, ctx.message)
        if ctx.command.name == 'clear':
            await ctx.send('```apache\ncy/clear <количество> [диапазон] [фильтр]\ncy/clear 10\ncy/clear 50 --everyone хыха\ncy/clear 30 --bots\ncy/clear 15 --users\ncy/clear 5 --silent\ncy/clear 200 "--silent --everyone"\n\n--everyone удалит сообщения от всех\n--bots удалит сообщения только от ботов\n--users удалит сообщения только от людей\n--silent не покажет результаты удаления сообщений. Учтите, что если нужно будет подтверждение удаления - оно будет показано\nПри указании фильтра необходимо писать именно то, что написано в сообщении - команда чувствительна к регистру\n\nПри указании диапазона не будет удалено столько сообщений, сколько было указано, будет удалено столько, сколько будет найдено в пределах заданного количества сообщений\nДопустим cy/clear 10 --bots\nЕсли сообщения от ботов и людей чередуются, будет удалено лишь то кол-во сообщений от ботов, что было найдено в указанном пределе 10. Это сделано намеренно, но может быть изменено в будущем\n\nСообщения старше 2 недель будут удалены не сразу - лимит discord API\nПри удалении более 100 сообщений нужно подтверждение владельца сервера.\nТолько владелец сервера может удалять от 250 сообщений за раз.\nНе более 300 за раз!\n\n[] - опционально, <> - обязательно, / - или\nНеобходимы разрешения - права администратора\nБоту необходимы разрешения - управлять сообщениями```')
        elif ctx.command.name == 'say':
            await ctx.send('```apache\ncy/say [обычный текст] [&t title текст] [&d description текст] [&th ссылка на картинку справа] [&img ссылка на картинку снизу] [&f footer текст] [&c цвет в HEX коде] [&msg сообщение над эмбедом]\ncy/say &t Заголовок &d Описание\ncy/say [текст]\nУчтите, что если вы захотите упомянуть роль с использованием какого либо аргумента текст не будет показан из-за способа упоминания ролей в Discord\nВсе аргументы являются необязательными, но если отправить пустую команду - ответ будет этим сообщением\n\n[] - опционально```')
        elif ctx.command.name == 'edit':
            await ctx.send('```apache\ncy/edit <ID> [обычный текст] [&t title текст] [&d description текст] [&f footer текст] [&c цвет в HEX коде] [&th ссылка на картинку справа] [&img ссылка на картинку снизу]\ncy/edit <ID> [текст]\ncy/edit <ID> --clean\ncy/edit <ID> --noembed\ncy/edit <ID> --delete\n\n--clean удалит контент над эмбедом\n--noembed удалит эмбед\n--delete удалит сообщение\n\nИспользование --clean и --noembed одновременно невозможно\nЕсли у сообщения есть эмбед и в команде нет агрументов, автоматически будет заменён &msg\nЗаголовок, описание и цвет будут взяты со старого эмбеда, если таковой имеется и эти аргументы не были указаны\nДля очистки какого-либо поля укажите аргумент и оставьте его пустым:\ncy/edit <ID> &d\nЭто опустошит описание\n\n[] - опционально, <> - обязательно\nНеобходимы разрешения - управлять сообщениями```')
        elif ctx.command.name == 'ban':
            await ctx.send('```apache\ncy/ban <@пинг/имя/ID> [причина/--soft --reason]\ncy/ban 185476724627210241 --soft --reason лошара\ncy/ban @сасиска чмо\ncy/ban @крипочек --soft\n\nПри использовании --soft обязательно указывать --reason __после__ него, однако можно не использовать --reason\ncy/ban adamant --soft --reason упырь\n\n[] - опционально, <> - обязательно, / - или\nНеобходимы разрешения - банить участников```')
        else:
            emb = discord.Embed(description = f'{ctx.author.mention}, предоставлено недостаточно аргументов для `{ctx.command.name}`. Попробуйте cy/help `{ctx.command.name}`', color = 0xff8000)
            emb.set_footer(text = 'Счётчик перезарядки сброшен')
            await ctx.send(embed = emb)
    elif isinstance(error, commands.MemberNotFound):
        rearm(ctx.command, ctx.message)
        emb = discord.Embed(description = f'{ctx.author.mention}, участник не найден', color = 0xff8000)
        emb.set_footer(text = 'Счётчик перезарядки сброшен')
        await ctx.send(embed = emb)
    elif isinstance(error, commands.BadArgument):
        rearm(ctx.command, ctx.message)
        emb = discord.Embed(description = f'{ctx.author.mention}, предоставлен неверный аргумент для `{ctx.command.name}`. Попробуйте cy/help `{ctx.command.name}`', color = 0xff8000)
        emb.set_footer(text = 'Счётчик перезарядки сброшен')
        await ctx.send(embed = emb)

@client.command()
async def reload(ctx):
    for file in os.listdir(CWD+"/cogs"):
        if file.endswith(".py"):
            await client.unload_extension(f"cogs.{file[:-3]}")
            await client.load_extension(f"cogs.{file[:-3]}")
    await ctx.send(embed = discord.Embed(description = 'Модули перезагружены', color = 0xff8000))

async def load():
    for file in os.listdir(CWD+"/cogs"):
        if file.endswith(".py"):
            await client.load_extension(f"cogs.{file[:-3]}")

async def main():
    t = os.environ['TOKEN']
    await load()
    await client.start(t)

asyncio.run(main())
