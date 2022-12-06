# coding=utf-8
import asyncio
import datetime
import json
import os
import random
import re
import itertools

import discord
from pathlib import Path
from discord.ext import commands
from discord.utils import get
from pymongo import MongoClient
from discord.ext import tasks

client = commands.Bot(command_prefix = commands.when_mentioned_or('cy/'), intents = discord.Intents.all(), status = discord.Status.idle, owner_ids = [338714886001524737, 417012231406878720], case_insensitive = True, allowed_mentions = discord.AllowedMentions(everyone = False))
client.remove_command('help')
passw = os.environ['passw']
cluster = MongoClient(f"mongodb+srv://cephalon:{passw}@locale.ttokw.mongodb.net/Locale?retryWrites=true&w=majority")
collection = cluster.Locale.locale
cwd = Path(__file__).parents[0]
cwd = str(cwd)

def reset_cooldown(command: commands.Command, message: discord.Message) -> None:
    if command._buckets.valid:
        bucket = command._buckets.get_bucket(message)
        bucket._tokens = min(bucket.rate, bucket._tokens + 1)

@tasks.loop(seconds = 10)
async def change_status():
    await client.change_presence(status = discord.Status.idle, activity = discord.Activity(type = discord.ActivityType.watching, name = f'{round(client.latency * 1000)}ms'))

@client.event
async def on_ready():
    change_status.start()
    channel = client.get_channel(714175791033876490)
    emb = discord.Embed(description = 'В сети, поверхностная проверка не выявила ошибок.', color = 0x2f3136, timestamp = discord.utils.utcnow())
    emb.set_footer(text = 'Cephalon Cy © Sus&Co')
    await channel.send(embed = emb)

@client.event
async def on_guild_role_update(before, after):
    if before.name == 'Muted':
        role = before.guild.get_role(after.id)
        await role.edit(name = 'Muted', color = discord.Color(0x000001), reason = 'Нельзя изменять эту роль.')
 
@client.event
async def on_command_completion(ctx):
    lchannel = client.get_channel(714175791033876490)
    emb = discord.Embed(title = 'ВЫПОЛНЕНИЕ_КОМАНДЫ', color = 0xff8000)
    emb.add_field(name = 'НАЗВАНИЕ', value = f'```{ctx.command.name}```')
    emb.add_field(name = 'ИСПОЛНИТЕЛЬ', value = f'{ctx.author.mention} ({ctx.author})')
    emb.add_field(name = 'СЕРВЕР', value = ctx.guild.name, inline = False)
    emb.add_field(name = 'КАНАЛ', value = f'{ctx.channel.name} ({ctx.channel.mention})', inline = False)
    await lchannel.send(embed = emb)

@client.event
async def on_member_join(member):
    if member.bot == False:
        user = 'УЧАСТНИК'
    else:
        user = 'БОТ'
    lchannel = client.get_channel(714175791033876490)
    emb = discord.Embed(title = f'{user}\_ЗАШЁЛ\_НА_СЕРВЕР', color = 0xff8000, timestamp = discord.utils.utcnow())
    emb.add_field(name = f'{user}', value = member)
    emb.add_field(name = 'УПОМИНАНИЕ', value = member.mention)
    emb.add_field(name = 'СЕРВЕР', value = member.guild.name)
    emb.set_footer(text = f'ID: {member.id}')
    await lchannel.send(embed = emb)

@client.event
async def on_member_remove(member):
    if member.bot == False:
        user = 'УЧАСТНИК'
    else:
        user = 'БОТ'
    channel = client.get_channel(714175791033876490)
    emb = discord.Embed(title = f'{user}\_ВЫШЕЛ\_С_СЕРВЕРА', color = 0xff8000, timestamp = discord.utils.utcnow())
    emb.add_field(name = f'{user}', value = member)
    emb.add_field(name = 'УПОМИНАНИЕ', value = member.mention)
    emb.add_field(name = 'СЕРВЕР', value = member.guild.name)
    emb.set_footer(text = f'ID: {member.id}')
    await channel.send(embed = emb)

@client.event
async def on_guild_remove(guild):
    channel = client.get_channel(714175791033876490)
    emb = discord.Embed(title = 'ВЫХОД\_С_СЕРВЕРА', color = 0xff8000, timestamp = discord.utils.utcnow())
    emb.add_field(name = 'СЕРВЕР', value = guild.name)
    emb.set_footer(text = f'ID: {guild.id}')
    await channel.send(embed = emb)

@client.event
async def on_guild_join(guild):
    channel = client.get_channel(714175791033876490)
    emb = discord.Embed(title = 'ДОБАВЛЕНИЕ\_НА_СЕРВЕР', color = 0xff8000, timestamp = discord.utils.utcnow())
    emb.add_field(name = 'СЕРВЕР', value = guild.name)
    emb.set_footer(text = f'ID: {guild.id}')
    await channel.send(embed = emb)

@client.event
async def on_voice_state_update(member, before, after):
    role = discord.utils.get(member.guild.roles, name = 'Deafened')
    try:
        if after.channel.name == 'Создать канал':
            await after.channel.edit(user_limit = 1)
            if member.bot == True:
                room = 'Чего бля'
            if member.id == client.owner_id:
                room = 'Комната моего Создателя'
            else:
                room = f'Комната {member}'
            channel = await member.guild.create_voice_channel(name = room, category = after.channel.category)
            await member.move_to(channel)
            await channel.set_permissions(member, mute_members = True, move_members = True, manage_channels = True)
            def check(a,b,c):
                return len(channel.members) == 0
            await client.wait_for('voice_state_update', check = check)
            await channel.delete()
        if role in member.roles:
            await member.edit(mute = True, reason = 'Заглушён командой deaf')
    except Exception:
        pass

@client.event
async def on_message(message):
    post = {
        '_id': message.author.id,
        'locale': 'ru'
    }
    if collection.count_documents({'_id': message.author.id}) == 0 and message.author.bot == False:
        collection.insert_one(post)
    if message.channel.id == 890673628822274128 and message.author.id == client.owner_id:
        await message.channel.send('<@!468079847017676801>, <@!417362845303439360>, похоже, еблан на сасиске скинул код!')
    if message.content.startswith(f'<@{client.user.id}>') and len(message.content) == len(f'<@{client.user.id}>'):
        await message.channel.send(f'чё звал {message.author.mention} ||`cy/`||')
        await client.process_commands(message)
    if ('сделать') in message.content.lower() or ('предлагаю') in message.content.lower() or ('предложение') in message.content.lower() and message.author.bot == False:
        await message.add_reaction('👍')
        await message.add_reaction('👎')
    if ('поздравляю') in message.content.lower() or ('поздравим') in message.content.lower() or ('поздравляем') in message.content.lower():
        await message.add_reaction('🥳')
    elif message.channel.id == 750372413102883028:
        if message.author.bot == True and message.author.id != 694170281270312991:
            role = discord.utils.get(message.guild.roles, id = 750368477671325728)
            sent = await message.channel.send(role.mention)
            await sent.delete()
            channel = client.get_channel(714175791033876490)
            emb = discord.Embed(title = 'ОПОВЕЩЕНИЕ\_ОБ_ОБНОВЛЕНИИ', color = 0xff8000, timestamp = discord.utils.utcnow())
            emb.add_field(name = 'ОПОВЕЩЕНЫ', value = role.mention)
            await channel.send(embed = emb)
    elif message.channel.id == 750368033578680361:
        if message.author.bot == True and message.author.id != 694170281270312991:
            role = discord.utils.get(message.guild.roles, id = 750366804689420319)
            sent = await message.channel.send(role.mention)
            await sent.delete()
            channel = client.get_channel(714175791033876490)
            emb = discord.Embed(title = 'ОПОВЕЩЕНИЕ\_ОБ_ОБНОВЛЕНИИ', color = 0xff8000, timestamp = discord.utils.utcnow())
            emb.add_field(name = 'ОПОВЕЩЕНЫ', value = role.mention)
            await channel.send(embed = emb)
    elif message.channel.id == 750363498290348123:
        if message.author.bot == True and message.author.id != 694170281270312991:
            role = discord.utils.get(message.guild.roles, id = 750363797226782802)
            sent = await message.channel.send(role.mention)
            await sent.delete()
            channel = client.get_channel(714175791033876490)
            emb = discord.Embed(title = 'ОПОВЕЩЕНИЕ\_ОБ_ОБНОВЛЕНИИ', color = 0xff8000, timestamp = discord.utils.utcnow())
            emb.add_field(name = 'ОПОВЕЩЕНЫ', value = role.mention)
            await channel.send(embed = emb)
    elif message.channel.id == 750373602460827730:
        if message.author.bot == True and message.author.id != 694170281270312991:
            role = discord.utils.get(message.guild.roles, id = 750373687479238787)
            sent = await message.channel.send(role.mention)
            await sent.delete()
            channel = client.get_channel(714175791033876490)
            emb = discord.Embed(title = 'ОПОВЕЩЕНИЕ\_ОБ_ОБНОВЛЕНИИ', color = 0xff8000, timestamp = discord.utils.utcnow())
            emb.add_field(name = 'ОПОВЕЩЕНЫ', value = role.mention)
            await channel.send(embed = emb)
    elif message.channel.id == 707498623981715557:
        await message.add_reaction('👍')
        await message.add_reaction('👎')
    channel = client.get_channel(714175791033876490)
    if channel is None:
        await client.process_commands(message)
        return
    if not message.author.bot:
        if message.channel.id != 714175791033876490:
            emb = discord.Embed(color = 0xff8000, timestamp = discord.utils.utcnow())
            emb.set_author(name = message.author, icon_url = message.author.avatar.url)
            if isinstance(message.channel, discord.channel.DMChannel):
                emb.add_field(name = 'НА_СЕРВЕРЕ', value = 'ЛС')
            else:
                emb.add_field(name = 'НА_СЕРВЕРЕ', value = message.guild)
                emb.add_field(name = 'В_КАНАЛЕ', value = f'{message.channel.mention} ({message.channel.name})')
            if len(message.content) >= 1924:
                content = f'{message.content.strip()[:len(message.content) - 1200].strip()}\n||Сообщение было слишком длинным, поэтому я обрезал его на 1200 символов (итого - {len(message.content) - 1200})||'
            elif len(message.content) >= 1724:
                content = f'{message.content.strip()[:len(message.content) - 1000].strip()}\n||Сообщение было слишком длинным, поэтому я обрезал его на 1000 символов (итого - {len(message.content) - 1000})||'
            elif len(message.content) >= 1524:
                content = f'{message.content.strip()[:len(message.content) - 800].strip()}\n||Сообщение было слишком длинным, поэтому я обрезал его на 800 символов (итого - {len(message.content) - 800})||'
            elif len(message.content) >= 1324:
                content = f'{message.content.strip()[:len(message.content) - 600].strip()}\n||Сообщение было слишком длинным, поэтому я обрезал его на 600 символов (итого - {len(message.content) - 600})||'
            elif len(message.content) >= 1124:
                content = f'{message.content.strip()[:len(message.content) - 400].strip()}\n||Сообщение было слишком длинным, поэтому я обрезал его на 400 символов (итого - {len(message.content) - 400})||'
            elif len(message.content) >= 924:
                content = f'{message.content.strip()[:len(message.content) - 200].strip()}\n||Сообщение было слишком длинным, поэтому я обрезал его на 200 символов (итого - {len(message.content) - 200})||'
            else:
                content = f'{message.content}\n\n||{len(message.content)} символов||'
            emb.add_field(name = 'НАПИСАНО', value = f'{content}', inline = False)
            await client.process_commands(message)
            try:
                await channel.send(embed = emb)
            except Exception:
                pass

@client.event
async def on_message_edit(before, after):
    channel = client.get_channel(714175791033876490)
    if channel is None:
        return
    if not before.author.bot:
        if ('http') not in after.content.lower():
            emb = discord.Embed(description = f'[ИЗМЕНЕНИЕ_СООБЩЕНИЯ]({before.jump_url})', color = 0xff8000, timestamp = discord.utils.utcnow())
            emb.set_author(name = before.author, icon_url = before.author.avatar.url)
            emb.add_field(name = 'НА_СЕРВЕРЕ', value = before.guild)
            emb.add_field(name = 'БЫЛО', value = f'```{before.content}```')
            emb.add_field(name = 'СТАЛО', value = f'```{after.content}```')
            await channel.send(embed = emb)

@client.event
async def on_command_error(ctx, error):
    channel = client.get_channel(838506478108803112)
    if isinstance(error, commands.NotOwner):
        emb = discord.Embed(description = f'{ctx.author.mention}, вы не являетесь владельцем бота.', color = 0xff8000)
        emb.set_footer(text = 'Счётчик перезарядки сброшен')
        await ctx.send(embed = emb) 
    elif isinstance(error, commands.BotMissingPermissions):
        emb = discord.Embed(description = f'{ctx.author.mention}, у **меня** недостаточно прав на выполнение команды `{ctx.command.name}`\n||Выдача прав администратора решит эту проблему||', color = 0xff0000)
        await ctx.send(embed = emb)
        eemb = discord.Embed(description = 'Поймана ошибка `BotMissingPermissions`', color = 0xff0000, timestamp = discord.utils.utcnow())
        eemb.add_field(name = 'Сервер', value = ctx.guild.name)
        eemb.add_field(name = 'Чего не хватает', value = f'{error.missing_permissions}', inline = False)
        eemb.add_field(name = 'Команда', value = ctx.command.name, inline = False)
        await channel.send(embed = eemb)
    elif isinstance(error, commands.MissingPermissions):
        emb = discord.Embed(description = f'{ctx.author.mention}, у вас недостаточно прав на выполнение команды `{ctx.command.name}`', color = 0xff8000)
        await ctx.send(embed = emb)
        eemb = discord.Embed(description = 'Поймана ошибка `MissingPermissions`', color = 0xff0000, timestamp = discord.utils.utcnow())
        eemb.add_field(name = 'Сервер', value = ctx.guild.name)
        eemb.add_field(name = 'Вызвавший ошибку', value = f'{ctx.author.mention} ({ctx.author.name})', inline = False)
        eemb.add_field(name = 'Команда', value = ctx.command.name, inline = False)
        await channel.send(embed = eemb)
    elif isinstance(error, commands.CommandOnCooldown):
        s = error.retry_after
        choises = ['Ещё не время.', 'Я не готов.', 'Ещё нет.', 'Ещё. Не. Время.', 'Я. Не. Готов.', 'Ещё. Нет.', 'ЕЩЁ НЕ ВРЕМЯ!', 'Я НЕ ГОТОВ!', 'ЕЩЁ НЕТ!']
        rand = random.choice(choises)
        emb = discord.Embed(description = f'{rand} Команда `{ctx.command.name}` будет доступна через {round(s)} секунд!', color = 0xff0000)
        await ctx.send(embed = emb)
        eemb = discord.Embed(description = 'Поймана ошибка `CommandOnCooldown`', color = 0xff0000, timestamp = discord.utils.utcnow())
        eemb.add_field(name = 'Сервер', value = ctx.guild.name)
        eemb.add_field(name = 'Вызвавший ошибку', value = f'{ctx.author.mention} ({ctx.author.name})', inline = False)
        eemb.add_field(name = 'Команда', value = ctx.command.name, inline = False)
        eemb.add_field(name = 'Оставалось времени', value = round(s), inline = False)
        await channel.send(embed = eemb)
    elif isinstance(error, commands.MissingRequiredArgument):
        reset_cooldown(ctx.command, ctx.message)
        if ctx.command.name == 'clear':
            await ctx.send('```apache\ncy/clear <количество> [диапазон] [фильтр]\ncy/clear 10\ncy/clear 50 --everyone хыха\ncy/clear 30 --bots\ncy/clear 15 --users\ncy/clear 5 --silent\ncy/clear 200 "--silent --everyone"\n\n--everyone удалит сообщения от всех\n--bots удалит сообщения только от ботов\n--users удалит сообщения только от участников\n--silent не покажет результаты удаления сообщений. Учтите, что если нужно будет подтверждение удаления - оно будет показано\n\nПри указании диапазона не будет удалено столько сообщений, сколько было указано, будет удалено столько, сколько будет найдено в пределах заданного количества сообщений.\nДопустим cy/clear 10 --bots\nЕсли сообщения от ботов и людей чередуются, будет удалено лишь то кол-во сообщений от ботов, что было найдено в указанном пределе 10.\n\nСообщения старше 2 недель будут удалены не сразу - лимит discord API\nПри удалении более 100 сообщений нужно подтверждение владельца сервера.\nТолько владелец сервера может удалять от 250 сообщений за раз.\nНе более 300 за раз!\n\n([] - опционально, <> - обязательно, / - или)\nperms = administrator```')
        elif ctx.command.name == 'say':
            await ctx.send('```apache\ncy/say [обычный текст] [&t title текст] [&d description текст] [&th ссылка на картинку справа] [&img ссылка на картинку снизу] [&f footer текст] [&c цвет в HEX коде] [&msg сообщение над эмбедом]\ncy/say &t Заголовок &d Описание\ncy/say [текст]\nУчтите, что если вы захотите упомянуть роль с использованием какого либо аргумента текст не будет показан из-за способа упоминания ролей в Discord\nВсе аргументы являются необязательными, но если отправить пустую команду - ответ будет этим сообщением\n\n([] - опционально)```')
        elif ctx.command.name == 'edit':
            await ctx.send('```apache\ncy/edit <ID> [обычный текст] [&t title текст] [&d description текст] [&f footer текст] [&c цвет в HEX коде] [&th ссылка на картинку справа] [&img ссылка на картинку снизу]\ncy/edit <ID> [текст]\ncy/edit <ID> --clean &d description\ncy/edit <ID> --clean\ncy/edit <ID> --noembed\ncy/edit <ID> --delete\n\n--clean удалит контент над эмбедом\n--noembed удалит эмбед\n--delete удалит сообщение\nИспользование --clean и --noembed одновременно невозможно, так как сообщение должно будет стать пустым. При этом --clean выполниться первым.\nПри редактировании сообщения с эмбедом цвет этого эмбеда сбросится на стандартный, если не указывать &c с нужным цветом.\nЕсли у сообщения есть эмбед и в команде нет агрументов, автоматически будет заменён &msg\n\n([] - опционально, <> - обязательно)\nperms = manage_channels```')
        elif ctx.command.name == 'ban':
            await ctx.send('```apache\ncy/ban <@пинг/имя/ID> [причина/--soft --reason]\ncy/ban 185476724627210241 --soft --reason лошара\ncy/ban @сасиска чмо\ncy/ban @крипочек --soft\n\nПри использовании --soft обязательно указывать --reason __после__ него, однако можно не использовать --reason\ncy/ban adamant --soft --reason упырь\n\n([] - опционально, <> - обязательно, / - или)\nperms = ban_members```')
        else:
            emb = discord.Embed(description = f'{ctx.author.mention}, обнаружен недостаток аргументов для `{ctx.command.name}`. Попробуйте cy/help `{ctx.command.name}`', color = 0xff8000)
            emb.set_footer(text = 'Счётчик перезарядки сброшен')
            await ctx.send(embed = emb)
        eemb = discord.Embed(description = 'Поймана ошибка `MissingRequiredArgument`', color = 0xff0000, timestamp = discord.utils.utcnow())
        eemb.add_field(name = 'Сервер', value = ctx.guild.name)
        eemb.add_field(name = 'Вызвавший ошибку', value = f'{ctx.author.mention} ({ctx.author.name})', inline = False)
        eemb.add_field(name = 'Команда', value = ctx.command.name, inline = False)
        await channel.send(embed = eemb)
    elif isinstance(error, commands.MemberNotFound):
        reset_cooldown(ctx.command, ctx.message)
        emb = discord.Embed(description = f'{ctx.author.mention}, участник не обнаружен.', color = 0xff8000)
        emb.set_footer(text = 'Счётчик перезарядки сброшен')
        await ctx.send(embed = emb)
        eemb = discord.Embed(description = 'Поймана ошибка `MemberNotFound`', color = 0xff0000, timestamp = discord.utils.utcnow())
        eemb.add_field(name = 'Сервер', value = ctx.guild.name)
        eemb.add_field(name = 'Вызвавший ошибку', value = f'{ctx.author.mention} ({ctx.author.name})', inline = False)
        eemb.add_field(name = 'Команда', value = ctx.command.name, inline = False)
        await channel.send(embed = eemb)
    elif isinstance(error, commands.BadArgument):
        reset_cooldown(ctx.command, ctx.message)
        emb = discord.Embed(description = f'{ctx.author.mention}, обнаружен неверный аргумент для `{ctx.command.name}`. Попробуйте cy/help `{ctx.command.name}`', color = 0xff8000)
        emb.set_footer(text = 'Счётчик перезарядки сброшен')
        await ctx.send(embed = emb)
        eemb = discord.Embed(description = 'Поймана ошибка `BadArgument`', color = 0xff0000, timestamp = discord.utils.utcnow())
        eemb.add_field(name = 'Сервер', value = ctx.guild.name)
        eemb.add_field(name = 'Вызвавший ошибку', value = f'{ctx.author.mention} ({ctx.author.name})', inline = False)
        eemb.add_field(name = 'Команда', value = ctx.command.name, inline = False)
        await channel.send(embed = eemb)

async def load():
    for file in os.listdir(cwd+"/cogs"):
        if file.endswith(".py") and not file.startswith("_") and not file.startswith("s"):
            await client.load_extension(f"cogs.{file[:-3]}")

async def main():
    t = os.environ['TOKEN']
    await load()
    await client.start(t)
    
asyncio.run(main())
