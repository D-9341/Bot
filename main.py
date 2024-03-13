# coding=utf-8
import asyncio
import os
import random
import json
import warnings
warnings.filterwarnings("ignore")

import discord
from pathlib import Path
from discord.ext import commands

client = commands.Bot(command_prefix = commands.when_mentioned_or('cy/'), intents = discord.Intents.all(), status = discord.Status.idle, activity = discord.Activity(type = discord.ActivityType.watching, name = 'в никуда'), owner_ids = {338714886001524737, 417012231406878720}, case_insensitive = True, allowed_mentions = discord.AllowedMentions(everyone = False))
client.remove_command('help')
cwd = Path(__file__).parents[0]
cwd = str(cwd)

def rearm(command: commands.Command, message: discord.Message):
    if command._buckets.valid:
        bucket = command._buckets.get_bucket(message)
        bucket._tokens = min(bucket.rate, bucket._tokens + 1)

@client.event
async def on_ready():
    await client.tree.sync()
    channel = client.get_channel(714175791033876490)
    emb = discord.Embed(description = 'В сети, поверхностная проверка не выявила ошибок.', color = 0x2f3136, timestamp = discord.utils.utcnow())
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
async def on_member_join(member):
    user = 'БОТ' if member.bot else 'УЧАСТНИК'
    channel = client.get_channel(714175791033876490)
    emb = discord.Embed(title = f'{user}\_ЗАШЁЛ\_НА_СЕРВЕР', color = 0xff8000, timestamp = discord.utils.utcnow())
    emb.add_field(name = f'{user}', value = member)
    emb.add_field(name = 'УПОМИНАНИЕ', value = member.mention)
    emb.add_field(name = 'СЕРВЕР', value = member.guild.name)
    emb.set_footer(text = f'ID: {member.id}')
    await channel.send(embed = emb)

@client.event
async def on_member_remove(member):
    user = 'БОТ' if member.bot else 'УЧАСТНИК'
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
    if after.channel.name == 'Создать канал':
        await after.channel.edit(user_limit = 1)
        if member.bot == True:
            room = 'Чего бля'
        if member.id in client.owner_ids:
            room = f'Канал моего Создателя - {member.display_name}'
        else:
            room = f'Канал {member.display_name}'
        channel = await member.guild.create_voice_channel(name = room, category = after.channel.category)
        await member.move_to(channel)
        await channel.set_permissions(member, mute_members = True, move_members = True, manage_channels = True)
        await channel.send(embed = discord.Embed(description = 'Этот канал удалится после того, как все люди выйдут из него. Исключение - перезапуск бота. В таком случае, что делать с каналом решать вам.', color = 0xff8000))
        def check(a,b,c):
            return len(channel.members) == 0
        await client.wait_for('voice_state_update', check = check)
        await channel.delete()
    if role in member.roles:
        await member.edit(mute = True, reason = 'Заглушён командой deaf')

@client.event
async def on_message(message):
    await client.process_commands(message)
    if message.author.bot == False:
        with open('locales/users.json', 'r') as users_file:
            data = json.load(users_file)
        if str(message.author.id) not in data:
            data[str(message.author.id)] = 'ru'
            with open('locales/users.json', 'w') as users_file:
                json.dump(data, users_file, indent = 4)
    if message.content.startswith(f'<@{client.user.id}>') and len(message.content) == len(f'<@{client.user.id}>'):
        await message.channel.send(f'чё звал {message.author.mention} ||`cy/`||')
    if message.channel.id == 1041417879788208169:
        if message.author.bot == True and message.author.id != 694170281270312991:
            role = discord.utils.get(message.guild.roles, id = 1078051320088510644)
            sent = await message.channel.send(role.mention)
            await sent.delete()
            channel = client.get_channel(714175791033876490)
            emb = discord.Embed(title = 'ОПОВЕЩЕНИЕ\_ОБ_ОБНОВЛЕНИИ', color = 0xff8000, timestamp = discord.utils.utcnow())
            emb.add_field(name = 'ОПОВЕЩЕНЫ', value = 'РАЗРАБОТЧИКИ')
            await channel.send(embed = emb)
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
            await channel.send(embed = emb)

@client.event
async def on_message_edit(before, after):
    channel = client.get_channel(714175791033876490)
    if channel is None: return
    if not before.author.bot:
        if ('http') not in after.content.lower():
            emb = discord.Embed(description = f'ИЗМЕНЕНИЕ_[СООБЩЕНИЯ]({before.jump_url})', color = 0xff8000, timestamp = discord.utils.utcnow())
            emb.set_author(name = before.author, icon_url = before.author.avatar.url)
            emb.add_field(name = 'НА_СЕРВЕРЕ', value = before.guild if before.guild else 'ЛС')
            emb.add_field(name = 'БЫЛО', value = f'```{before.content}```')
            emb.add_field(name = 'СТАЛО', value = f'```{after.content}```')
            await channel.send(embed = emb)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.NotOwner):
        emb = discord.Embed(description = f'{ctx.author.mention}, это действие может совершить только один из создателей бота', color = 0xff8000)
        emb.set_footer(text = 'Счётчик перезарядки сброшен')
        await ctx.send(embed = emb) 
    elif isinstance(error, commands.BotMissingPermissions):
        emb = discord.Embed(description = f'{ctx.author.mention}, у **меня** недостаточно прав на выполнение команды `{ctx.command.name}`\n||Выдача прав администратора решит эту проблему||', color = 0xff0000)
        await ctx.send(embed = emb)
    elif isinstance(error, commands.MissingPermissions):
        emb = discord.Embed(description = f'{ctx.author.mention}, у вас недостаточно прав на выполнение команды `{ctx.command.name}`. Напишите cy/help `{ctx.command.name}` для просмотра необходимых прав', color = 0xff8000)
        await ctx.send(embed = emb)
    elif isinstance(error, commands.CommandOnCooldown):
        s = error.retry_after
        choises = ['Ещё не время.', 'Я не готов.', 'Ещё нет.', 'Ещё. Не. Время.', 'Я. Не. Готов.', 'Ещё. Нет.', 'ЕЩЁ НЕ ВРЕМЯ!', 'Я НЕ ГОТОВ!', 'ЕЩЁ НЕТ!']
        rand = random.choice(choises)
        emb = discord.Embed(description = f'{rand} Команда `{ctx.command.name}` будет доступна через {round(s)} секунд!', color = 0xff0000)
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

async def load():
    for file in os.listdir(cwd+"/cogs"):
        if file.endswith(".py") and not file.startswith("s"):
            await client.load_extension(f"cogs.{file[:-3]}")

async def main():
    t = 'Njk0MTcwMjgxMjcwMzEyOTkx.GupfdU.wPFXo0oocmWcs3esT7QelBMfIT_9kzy3iJIHj4'
    await load()
    await client.start(t)

asyncio.run(main())
