# coding=utf-8 
import asyncio
import datetime
import os
import re

import disnake
from pathlib import Path
from pymongo import MongoClient
from disnake.ext import commands
from disnake.utils import get

client = commands.Bot(command_prefix = commands.when_mentioned_or('cy/'), intents = disnake.Intents.all(), owner_id = 338714886001524737, status = disnake.Status.idle, activity = disnake.Activity(type = disnake.ActivityType.playing, name = 'disnake.py'), allowed_mentions = disnake.AllowedMentions(everyone = False), case_insensitive = True)
client.remove_command('help')
passw = os.environ.get('passw')
cluster = MongoClient(f"mongodb+srv://cephalon:{passw}@locale.ttokw.mongodb.net/Locale?retryWrites=true&w=majority")
collection = cluster.Locale.locale
cwd = Path(__file__).parents[0]
cwd = str(cwd)

@client.event
async def on_ready():
    channel = client.get_channel(714175791033876490)
    emb = disnake.Embed(description = 'В сети, поверхностная проверка не выявила ошибок.', color = 0x2f3136, timestamp = disnake.utils.utcnow())
    emb.set_footer(text = 'Cephalon Cy © сасиска#2472')
    await channel.send(embed = emb)

time_regex = re.compile(r"(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {'h': 3600, 's': 1, 'm': 60, 'd': 86400}

friends = [351071668241956865, 417362845303439360]

guilds = [693929822543675455, 735874149578440855]

botversions = [764882153812787250, 694170281270312991, 762015251264569352]

class TimeConverter(commands.Converter):
    async def convert(self, ctx, argument):
        args = argument.lower()
        time = 0
        matches = re.findall(time_regex, args)
        for key, value in matches:
            try:
                time += time_dict[value] * float(key)
            except KeyError:
                await ctx.send(f'{value} не является правильным аргументом! Правильные: h|m|s|d') #{value} is not valid argument! Use: h|m|s|d
            except ValueError:
                await ctx.send(f'{key} не число!') #{key} not a number!
        return time
    
def reset_cooldown(command: commands.Command, message: disnake.Message) -> None:
    if command._buckets.valid:
        bucket = command._buckets.get_bucket(message)
        bucket._tokens = min(bucket.rate, bucket._tokens + 1)
    
@client.event
async def on_guild_role_update(before, after):
    if before.name == '1':
        role = before.guild.get_role(after.id)
        if after.name == '2' or after.name == 'Muted':
            await role.delete()
            g = await before.guild.create_role(name = '1', color = disnake.Color(0xff0000), reason = 'Нет, нельзя менять название этой роли на Muted или 2') # it is not allowed to rename this role to Muted or 2
            await g.edit(position = 2)
        else:
            await role.edit(name = '1', color = disnake.Color(0xff0000), reason = 'Нельзя изменять эту роль.') # it is not allowed to edit this role
    if before.name == '2':
        role = before.guild.get_role(after.id)
        if after.name == '1' or after.name == 'Muted':
            await role.delete()
            g = await before.guild.create_role(name = '2', color = disnake.Color(0xff0000), reason = 'Нет, нельзя менять название этой роли на Muted или 1') # it is not allowed to rename this role to Muted or 1
            await g.edit(position = 1)
        else:
            await role.edit(name = '2', color = disnake.Color(0xff0000), reason = 'Нельзя изменять эту роль.') # it is not allowed to edit this role
    if before.name == 'Muted':
        role = before.guild.get_role(after.id)
        if after.name == '2' or after.name == '1':
            await role.delete()
            g = await before.guild.create_role(name = 'Muted', color = disnake.Color(0x000001), reason = 'Нет, нельзя менять название этой роли на 1 или 2') # it is not allowed to rename this role to 1 or 2
            await g.edit(position = 4)
        else:
            await role.edit(name = 'Muted', color = disnake.Color(0x000001), reason = 'Нельзя изменять эту роль.') # it is not allowed to edit this role

@client.event
async def on_command_completion(ctx):
    lchannel = client.get_channel(714175791033876490)
    emb = disnake.Embed(title = 'ВЫПОЛНЕНИЕ_КОМАНДЫ', color = disnake.Color.orange()) # COMMAND_COMPLETION
    emb.add_field(name = 'НАЗВАНИЕ', value = f'```{ctx.command.name}```') # NAME
    emb.add_field(name = 'ИСПОЛНИТЕЛЬ', value = f'{ctx.author.mention} ({ctx.author})') # EXECUTED BY
    emb.add_field(name = 'СЕРВЕР', value = ctx.guild.name, inline = False) # SERVER
    emb.add_field(name = 'КАНАЛ', value = f'{ctx.channel.name} ({ctx.channel.mention})', inline = False) # CHANNEL
    await lchannel.send(embed = emb)

@client.event
async def on_member_join(member):
    if member.bot == False:
        chmo = 'УЧАСТНИК' # MEMBER
    else:
        chmo = 'БОТ' # BOT
    lchannel = client.get_channel(714175791033876490)
    emb = disnake.Embed(title = f'{chmo}\_ЗАШЁЛ\_НА_СЕРВЕР', colour = disnake.Color.orange(), timestamp = disnake.utils.utcnow()) # {chmo}_ENTERED_THE_SERVER
    emb.add_field(name = f'{chmo}', value = member)
    emb.add_field(name = 'УПОМИНАНИЕ', value = member.mention) # MENTION
    emb.add_field(name = 'СЕРВЕР', value = member.guild.name) # SERVER
    emb.set_footer(text = f'ID: {member.id}')
    await lchannel.send(embed = emb)

@client.event
async def on_member_remove(member):
    if member.bot == False:
        chmo = 'УЧАСТНИК' # MEMBER
    else:
        chmo = 'БОТ' # BOT
    channel = client.get_channel(714175791033876490)
    emb = disnake.Embed(title = f'{chmo}\_ВЫШЕЛ\_С_СЕРВЕРА', colour = disnake.Color.orange(), timestamp = disnake.utils.utcnow()) # {chmo}_LEFT_THE_SERVER
    emb.add_field(name = f'{chmo}', value = member)
    emb.add_field(name = 'УПОМИНАНИЕ', value = member.mention) # MENTION
    emb.add_field(name = 'СЕРВЕР', value = member.guild.name) # SERVER
    emb.set_footer(text = f'ID: {member.id}')
    await channel.send(embed = emb)

@client.event
async def on_guild_remove(guild):
    channel = client.get_channel(714175791033876490)
    emb = disnake.Embed(title = 'ВЫХОД\_С_СЕРВЕРА', colour = disnake.Color.orange(), timestamp = disnake.utils.utcnow()) # CLIENT_LEFT_SERVER
    emb.add_field(name = 'СЕРВЕР', value = guild.name) # SERVER
    emb.set_footer(text = f'ID: {guild.id}')
    await channel.send(embed = emb)

@client.event
async def on_guild_join(guild):
    channel = client.get_channel(714175791033876490)
    emb = disnake.Embed(title = 'ДОБАВЛЕНИЕ\_НА_СЕРВЕР', colour = disnake.Color.orange(), timestamp = disnake.utils.utcnow()) # CLIENT_ADDED_TO_SERVER
    emb.add_field(name = 'СЕРВЕР', value = guild.name) # SERVER
    emb.set_footer(text = f'ID: {guild.id}')
    await channel.send(embed = emb)

@client.event
async def on_voice_state_update(member, before, after):
    role = disnake.utils.get(member.guild.roles, name = 'Deafened')
    try:
        if after.channel.name == 'Создать канал': # Create channel
            await after.channel.edit(user_limit = 1)
            if member.bot == True:
                room = 'Чего бля' # wtf
            if member.id == client.owner_id:
                room = 'Комната моего Создателя'
            else:
                room = f'Комната {member}' # {member}`s room
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
        await message.channel.send(f'<@!468079847017676801>, <@!417362845303439360>, похоже, еблан на сасиске скинул код!')
    if message.content.startswith(f'<@!{client.user.id}>') and len(message.content) == len(f'<@!{client.user.id}>'):
        await message.channel.send(f'чё звал {message.author.mention} ||`cy/`||')
        await client.process_commands(message)
    def _check(m):
        return (m.author == message.author and len(m.mentions) and (disnake.utils.utcnow() - m.created_at.utcnow()).seconds < 2)
    if len(list(filter(lambda m: _check(m), client.cached_messages))) >= 3:
        if not message.author.bot:
            role = disnake.utils.get(message.guild.roles, name = 'Muted')
            role3 = disnake.utils.get(message.guild.roles, name = '----------Предупреждения----------')
            role1 = disnake.utils.get(message.guild.roles, name = '1')
            role2 = disnake.utils.get(message.guild.roles, name = '2')
            if role != None and role1 != None and role2 != None and role3 != None:
                if role not in message.author.roles:
                    if role1 not in message.author.roles and role2 not in message.author.roles:
                        await message.channel.send(f'{message.author.mention} Был заглушён на 10 минут за спам упоминаниями. Больше так не делай!')
                        await message.author.add_roles(role, role1, role3)
                        channel = client.get_channel(714175791033876490)
                        emb = disnake.Embed(title = 'СРАБОТАЛ\_АВТО_МУТ', color = disnake.Color.orange(), timestamp = disnake.utils.utcnow())
                        emb.add_field(name = 'СЕРВЕР', value = message.guild.name)
                        emb.add_field(name = 'ПРЕДУПРЕЖДЕНИЕ', value = 'ПЕРВОЕ')
                        emb.add_field(name = 'УЧАСТНИК', value = message.author)
                        await channel.send(embed = emb)
                        await asyncio.sleep(600)
                        if role != None:
                            if role in message.author.roles:
                                await message.author.remove_roles(role)
                                emb = disnake.Embed(description = f'{message.author.mention} Был разглушён.', color = 0x2f3136)
                                await message.channel.send(embed = emb)
                            else:
                                emb = disnake.Embed(description = f'Роли Muted не было обнаружено в списке ролей {message.author.mention}.', color = 0x2f3136)
                                await message.channel.send(embed = emb)
                        else:
                            emb = disnake.Embed(description = f'Невозможно снять заглушение у {message.author.mention}, т.к. роль `Muted` была удалена.', color = 0x2f3136)
                            await message.channel.send(embed = emb)
                    if role1 in message.author.roles and role2 not in message.author.roles:
                        await message.channel.send(f'{message.author.mention} Был заглушён на 30 минут за спам упоминаниями. Последнее предупреждение.')
                        await message.author.remove_roles(role1)
                        await message.author.add_roles(role, role2, role3)
                        channel = client.get_channel(714175791033876490)
                        emb = disnake.Embed(title = 'СРАБОТАЛ\_АВТО_МУТ', color = disnake.Color.orange(), timestamp = datetime.datetime.utcnow())
                        emb.add_field(name = 'СЕРВЕР', value = message.guild.name)
                        emb.add_field(name = 'ПРЕДУПРЕЖДЕНИЕ', value = 'ПОСЛЕДНЕЕ')
                        emb.add_field(name = 'УЧАСТНИК', value = message.author)
                        await channel.send(embed = emb)
                        await asyncio.sleep(1800)
                        if role != None:
                            if role in message.author.roles:
                                await message.author.remove_roles(role)
                                emb = disnake.Embed(description = f'{message.author.mention} Был разглушён.', color = 0x2f3136)
                                await message.channel.send(embed = emb)
                            else:
                                emb = disnake.Embed(description = f'Роли Muted не было обнаружено в списке ролей {message.author.mention}.', color = 0x2f3136)
                                await message.channel.send(embed = emb)
                        else:
                            emb = disnake.Embed(description = f'Невозможно снять заглушение у {message.author.mention}, т.к. роль `Muted` была удалена.', color = 0x2f3136)
                            await message.channel.send(embed = emb)
                    if role2 in message.author.roles:
                        await message.channel.send(f'{message.author.mention} Был заглушён навсегда за спам упоминаниями.')
                        await message.author.add_roles(role)
                        await message.author.remove_roles(role2, role3)
                        channel = client.get_channel(714175791033876490)
                        emb = disnake.Embed(title = 'СРАБОТАЛ\_АВТО_МУТ', color = disnake.Color.orange(), timestamp = disnake.utils.utcnow())
                        emb.add_field(name = 'СЕРВЕР', value = message.guild.name)
                        emb.add_field(name = 'УЧАСТНИК', value = message.author)
                        await channel.send(embed = emb)
                else:
                    return
            elif role == None:
                r = await message.guild.create_role(name = 'Muted', colour = disnake.Colour(0x000001), reason = 'Создано автоматически из-за недостатка ролей.')
                await r.edit(position = 4)
            elif role3 == None:
                r1 = await message.guild.create_role(name = '----------Предупреждения----------', colour = disnake.Colour(0x2f3136), reason = 'Создано автоматически из-за недостатка ролей.')
                r1.edit(position = 3)
            elif role1 == None:
                r2 = await message.guild.create_role(name = '1', colour = disnake.Colour(0xff0000), reason = 'Создано автоматически из-за недостатка ролей.')
                r2.edit(position = 2)
            elif role2 == None:
                r3 = await message.guild.create_role(name = '2', colour = disnake.Colour(0xff0000), reason = 'Создано автоматически из-за недостатка ролей.')
                r3.edit(position = 1)
    if ('сделать') in message.content.lower() or ('предлагаю') in message.content.lower() or ('предложение') in message.content.lower() and message.author.bot == False:
        await message.add_reaction('👍')
        await message.add_reaction('👎')
    if ('поздравляю') in message.content.lower() or ('поздравим') in message.content.lower() or ('поздравляем') in message.content.lower():
        await message.add_reaction('🥳')
    elif message.channel.id == 750372413102883028: #EFT
        if message.author.bot == True and message.author.id != 694170281270312991:
            role = disnake.utils.get(message.guild.roles, id = 750368477671325728)
            sent = await message.channel.send(role.mention)
            await sent.delete()
            channel = client.get_channel(714175791033876490)
            emb = disnake.Embed(title = 'ОПОВЕЩЕНИЕ\_ОБ_ОБНОВЛЕНИИ', color = disnake.Color.orange(), timestamp = disnake.utils.utcnow())
            emb.add_field(name = 'ОПОВЕЩЕНЫ', value = role.mention)
            await channel.send(embed = emb)
    elif message.channel.id == 750368033578680361: #OV
        if message.author.bot == True and message.author.id != 694170281270312991:
            role = disnake.utils.get(message.guild.roles, id = 750366804689420319)
            sent = await message.channel.send(role.mention)
            await sent.delete()
            channel = client.get_channel(714175791033876490)
            emb = disnake.Embed(title = 'ОПОВЕЩЕНИЕ\_ОБ_ОБНОВЛЕНИИ', color = disnake.Color.orange(), timestamp = disnake.utils.utcnow())
            emb.add_field(name = 'ОПОВЕЩЕНЫ', value = role.mention)
            await channel.send(embed = emb)
    elif message.channel.id == 750363498290348123: #DOTA 2
        if message.author.bot == True and message.author.id != 694170281270312991:
            role = disnake.utils.get(message.guild.roles, id = 750363797226782802)
            sent = await message.channel.send(role.mention)
            await sent.delete()
            channel = client.get_channel(714175791033876490)
            emb = disnake.Embed(title = 'ОПОВЕЩЕНИЕ\_ОБ_ОБНОВЛЕНИИ', color = disnake.Color.orange(), timestamp = disnake.utils.utcnow())
            emb.add_field(name = 'ОПОВЕЩЕНЫ', value = role.mention)
            await channel.send(embed = emb)
    elif message.channel.id == 750373602460827730: #MC
        if message.author.bot == True and message.author.id != 694170281270312991:
            role = disnake.utils.get(message.guild.roles, id = 750373687479238787)
            sent = await message.channel.send(role.mention)
            await sent.delete()
            channel = client.get_channel(714175791033876490)
            emb = disnake.Embed(title = 'ОПОВЕЩЕНИЕ\_ОБ_ОБНОВЛЕНИИ', color = disnake.Color.orange(), timestamp = disnake.utils.utcnow())
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
            emb = disnake.Embed(colour = disnake.Color.orange(), timestamp = disnake.utils.utcnow())
            emb.set_author(name = message.author, icon_url = message.author.avatar.url)
            if isinstance(message.channel, disnake.channel.DMChannel):
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
            emb = disnake.Embed(description = f'[ИЗМЕНЕНИЕ_СООБЩЕНИЯ]({before.jump_url})', colour = disnake.Color.orange(), timestamp = disnake.utils.utcnow())
            emb.set_author(name = before.author, icon_url = before.author.avatar.url)
            emb.add_field(name = 'НА_СЕРВЕРЕ', value = before.guild)
            emb.add_field(name = 'БЫЛО', value = f'```{before.content}```')
            emb.add_field(name = 'СТАЛО', value = f'```{after.content}```')
            await channel.send(embed = emb)
    
@client.event
async def on_command_error(ctx, error):
    channel = client.get_channel(838506478108803112)
    if isinstance(error, commands.CommandNotFound):
        emb = disnake.Embed(description = f'{ctx.author.mention}, команда не обнаружена. Может, пропишите cy/help?', colour = disnake.Color.orange())
        await ctx.send(embed = emb)
        eemb = disnake.Embed(description = 'Поймана ошибка `CommandNotFound`', color = 0xff0000, timestamp = disnake.utils.utcnow())
        eemb.add_field(name = 'Сервер', value = ctx.guild.name)
        eemb.add_field(name = 'Вызвавший ошибку', value = f'{ctx.author.mention} ({ctx.author.name})', inline = False)
        eemb.add_field(name = 'Команда', value = ctx.command.name, inline = False)
        await channel.send(embed = eemb)
    elif isinstance(error, commands.MissingPermissions):
        emb = disnake.Embed(description = f'{ctx.author.mention}, у вас недостаточно прав на выполнение команды `{ctx.command.name}`', colour = disnake.Color.orange())
        await ctx.send(embed = emb)
        eemb = disnake.Embed(description = 'Поймана ошибка `MissingPermissions`', color = 0xff0000, timestamp = disnake.utils.utcnow())
        eemb.add_field(name = 'Сервер', value = ctx.guild.name)
        eemb.add_field(name = 'Вызвавший ошибку', value = f'{ctx.author.mention} ({ctx.author.name})', inline = False)
        eemb.add_field(name = 'Команда', value = ctx.command.name, inline = False)
        await channel.send(embed = eemb)
    elif isinstance(error, commands.CommandOnCooldown):
        s = error.retry_after
        choises = ['Its not time yet..', 'I am not ready..', 'Not yet..']
        choices1 = ['Its Not Time Yet.', 'I Am Not Ready.', 'Not Yet.']
        choices2 = ['ITS NOT TIME YET!', 'I AM NOT READY!', 'NOT YET!']
        rand = random.choice(choises)
        rand1 = random.choice(choices1)
        rand2 = random.choice(choices2)
        if round(s) >= 5:
            emb = disnake.Embed(description = f'{rand} Команда `{ctx.command.name}` будет доступна через {round(s)} секунд..', colour = disnake.Color.orange())
            await ctx.send(embed = emb)
        elif round(s) >= 2:
            emb = disnake.Embed(description = f'{rand1} Команда `{ctx.command.name}` будет доступна через {round(s)} секунды.', colour = disnake.Color.orange())
            await ctx.send(embed = emb)
        elif round(s) >= 1:
            emb = disnake.Embed(description = f'{rand2} Команда `{ctx.command.name}` будет доступна через {round(s)} секунду!', colour = disnake.Color.orange())
            await ctx.send(embed = emb)
        elif round(s) <= 0:
            emb = disnake.Embed(description = 'Ебать ты тайминг поймал конечно ||До перезарядки команды оставалось чуть больше, чем 0 секунд||', colour = disnake.Color.orange())
            await ctx.send(embed = emb)
        eemb = disnake.Embed(description = 'Поймана ошибка `CommandOnCooldown`', color = 0xff0000, timestamp = disnake.utils.utcnow())
        eemb.add_field(name = 'Сервер', value = ctx.guild.name)
        eemb.add_field(name = 'Вызвавший ошибку', value = f'{ctx.author.mention} ({ctx.author.name})', inline = False)
        eemb.add_field(name = 'Команда', value = ctx.command.name, inline = False)
        eemb.add_field(name = 'Оставалось времени', value = round(s), inline = False)
        await channel.send(embed = eemb)
    elif isinstance(error, commands.MissingRequiredArgument):
        reset_cooldown(ctx.command, ctx.message)
        if ctx.command.name == 'clear':
            await ctx.send('```apache\ncy/clear <количество> [автор] [фильтр]\ncy/clear 100\ncy/clear 10 @сасиска\ncy/clear 50 --everyone хыха\ncy/clear 30 --bots\ncy/clear 15 --users\ncy/clear 5 --silent\ncy/clear 200 "--silent --everyone" хыха\n\n--everyone удалит сообщения от всех\n--bots удалит сообщения только от ботов\n--users удалит сообщения только от участников\n--silent не оставит доказательств выполнения команды, исключение - количество >= 10\n\nПри указании автора не будет удалено столько сообщений, сколько было указано, будет удалено столько, сколько будет найдено в пределах этих сообщений.\nСообщения старше 2 недель будут удалены не сразу - лимит discord API\nПри удалении более 100 сообщений нужно подтверждение владельца сервера.\nТолько владелец может удалять от 250 сообщений за раз.\nНе более 300!\n([] - опционально, <> - обязательно, / - или)\nperms = adminstrator```')
        elif ctx.command.name == 'say':
            await ctx.send('```apache\ncy/say [обычный текст] [t& title текст] | [d& description текст] | [th& ссылка на картинку справа] | [img& ссылка на картинку снизу] [f& footer текст] [msg& сообщение над эмбедом]\ncy/say t& title | d& description\ncy/say --everyone | t& title | d& description\ncy/say [текст]\ncy/say --everyone [текст]\n(вам НЕ обязательно писать все аргументы в данном порядке, пишите только те, что вам нужны в любом порядке) ([] - опционально)```')
        elif ctx.command.name == 'edit':
            await ctx.send('```apache\ncy/edit <ID> [обычный текст] [t& title текст] | [d& description текст] | [th& ссылка на картинку справа] | [img& ссылка на картинку снизу]\ncy/edit <ID> [текст]\ncy/edit <ID> --clean | d& description\ncy/edit <ID> --clean\ncy/edit <ID> --noembed\ncy/edit <ID> --empty-embed\ncy/edit <ID> --delete\n--clean удалит контент над эмбедом, --noembed удалит эмбед, работает только если есть эмбед, --empty-embed опустошит эмбед, --delete удалит сообщение\nесли у сообщения есть эмбед и в команде нет агрументов, автоматически будет заменён msg&\n([] - опционально, <> - обязательно)\nperms = manage_channels```')
        elif ctx.command.name == 'ban':
            await ctx.send('```apache\ncy/ban <@пинг/имя/ID> [причина/--soft --reason]\ncy/ban 185476724627210241 --soft --reason лошара\ncy/ban @сасиска чмо\ncy/ban "Sgt White"\ncy/ban @крипочек --soft\n\nПри использовании --soft обязательно указывать --reason ПОСЛЕ --soft\n\n([] - опционально, <> - обязательно, / - или)\nperms = ban_members```')
        else:
            emb = disnake.Embed(description = f'{ctx.author.mention}, обнаружен недостаток аргументов для `{ctx.command.name}`. Попробуйте cy/help `{ctx.command.name}`', colour = disnake.Color.orange())
            emb.set_footer(text = 'Задержка команды сброшена, так как была вызвана ошибка при вводе пользователя')
            await ctx.send(embed = emb)
        eemb = disnake.Embed(description = 'Поймана ошибка `MissingRequiredArgument`', color = 0xff0000, timestamp = disnake.utils.utcnow())
        eemb.add_field(name = 'Сервер', value = ctx.guild.name)
        eemb.add_field(name = 'Вызвавший ошибку', value = f'{ctx.author.mention} ({ctx.author.name})', inline = False)
        eemb.add_field(name = 'Команда', value = ctx.command.name, inline = False)
        await channel.send(embed = eemb)
    elif isinstance(error, commands.MemberNotFound):
        reset_cooldown(ctx.command, ctx.message)
        emb = disnake.Embed(description = f'{ctx.author.mention}, участник не обнаружен.', color = disnake.Color.orange())
        emb.set_footer(text = 'Задержка команды сброшена, так как была вызвана ошибка при вводе пользователя')
        await ctx.send(embed = emb)
        eemb = disnake.Embed(description = 'Поймана ошибка `MemberNotFound`', color = 0xff0000, timestamp = disnake.utils.utcnow())
        eemb.add_field(name = 'Сервер', value = ctx.guild.name)
        eemb.add_field(name = 'Вызвавший ошибку', value = f'{ctx.author.mention} ({ctx.author.name})', inline = False)
        eemb.add_field(name = 'Команда', value = ctx.command.name, inline = False)
        await channel.send(embed = eemb)
    elif isinstance(error, commands.BadArgument):
        reset_cooldown(ctx.command, ctx.message)
        emb = disnake.Embed(description = f'{ctx.author.mention}, обнаружен неверный аргумент для `{ctx.command.name}`. Попробуйте cy/help `{ctx.command.name}`', colour = disnake.Color.orange())
        emb.set_footer(text = 'Задержка команды сброшена, так как была вызвана ошибка при вводе пользователя')
        await ctx.send(embed = emb)
        eemb = disnake.Embed(description = 'Поймана ошибка `BadArgument`', color = 0xff0000, timestamp = disnake.utils.utcnow())
        eemb.add_field(name = 'Сервер', value = ctx.guild.name)
        eemb.add_field(name = 'Вызвавший ошибку', value = f'{ctx.author.mention} ({ctx.author.name})', inline = False)
        eemb.add_field(name = 'Команда', value = ctx.command.name, inline = False)
        await channel.send(embed = eemb)

if __name__ == '__main__':
    for file in os.listdir(cwd+"/cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            client.load_extension(f"cogs.{file[:-3]}")
        
t = os.environ.get('t')
client.run(t)
