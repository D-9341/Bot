# coding=utf-8 
import asyncio
import datetime
import json
import os
import random
import re
import regex
import secrets

import discord
import discord_slash
from pathlib import Path
from pymongo import MongoClient
from discord.ext import commands
from discord.utils import get
from discord_slash import SlashCommand, SlashContext

client = commands.Bot(command_prefix = commands.when_mentioned_or('cy/'), intents = discord.Intents.all(), owner_id = 338714886001524737, status = discord.Status.idle, activity = discord.Activity(type = discord.ActivityType.watching, name = 'Slash Commands'), allowed_mentions = discord.AllowedMentions(everyone = False), case_insensitive = True)
client.remove_command('help')
slash = SlashCommand(client, sync_commands = True)
passw = os.environ.get('passw')
cluster = MongoClient(f"mongodb+srv://cephalon:{passw}@locale.ttokw.mongodb.net/Locale?retryWrites=true&w=majority")
collection = cluster.Locale.locale
cwd = Path(__file__).parents[0]
cwd = str(cwd)

@client.event
async def on_ready():
    channel = client.get_channel(714175791033876490)
    emb = discord.Embed(description = 'В сети, поверхностная проверка не выявила ошибок.', color = 0x2f3136, timestamp = datetime.datetime.utcnow())
    emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
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
    
def revert_cooldown(command: commands.Command, message: discord.Message) -> None:
    if command._buckets.valid:
        bucket = command._buckets.get_bucket(message)
        bucket._tokens = min(bucket.rate, bucket._tokens + 1)
    
@client.event
async def on_guild_role_update(before, after):
    if before.name == '1':
        role = before.guild.get_role(after.id)
        if after.name == '2' or after.name == 'Muted':
            await role.delete()
            g = await before.guild.create_role(name = '1', color = discord.Color(0xff0000), reason = 'Нет, нельзя менять название этой роли на Muted или 2') # it is not allowed to rename this role to Muted or 2
            await g.edit(position = 2)
        else:
            await role.edit(name = '1', color = discord.Color(0xff0000), reason = 'Нельзя изменять эту роль.') # it is not allowed to edit this role
    if before.name == '2':
        role = before.guild.get_role(after.id)
        if after.name == '1' or after.name == 'Muted':
            await role.delete()
            g = await before.guild.create_role(name = '2', color = discord.Color(0xff0000), reason = 'Нет, нельзя менять название этой роли на Muted или 1') # it is not allowed to rename this role to Muted or 1
            await g.edit(position = 1)
        else:
            await role.edit(name = '2', color = discord.Color(0xff0000), reason = 'Нельзя изменять эту роль.') # it is not allowed to edit this role
    if before.name == 'Muted':
        role = before.guild.get_role(after.id)
        if after.name == '2' or after.name == '1':
            await role.delete()
            g = await before.guild.create_role(name = 'Muted', color = discord.Color(0x000001), reason = 'Нет, нельзя менять название этой роли на 1 или 2') # it is not allowed to rename this role to 1 or 2
            await g.edit(position = 4)
        else:
            await role.edit(name = 'Muted', color = discord.Color(0x000001), reason = 'Нельзя изменять эту роль.') # it is not allowed to edit this role

@client.event
async def on_command_completion(ctx):
    lchannel = client.get_channel(714175791033876490)
    emb = discord.Embed(title = 'ВЫПОЛНЕНИЕ_КОМАНДЫ', color = discord.Color.orange()) # COMMAND_COMPLETION
    emb.add_field(name = 'НАЗВАНИЕ', value = f'```{ctx.command.name}```') # NAME
    emb.add_field(name = 'ИСПОЛНИТЕЛЬ', value = f'{ctx.author.mention} ({ctx.author})') # EXECUTED BY
    emb.add_field(name = 'СЕРВЕР', value = ctx.guild.name, inline = False) # SERVER
    emb.add_field(name = 'КАНАЛ', value = f'{ctx.channel.name} ({ctx.channel.mention})', inline = False) # CHANNEL
    await lchannel.send(embed = emb)

@client.event
async def on_member_update(before, after):
    channel = client.get_channel(714175791033876490)
    if before.bot == False:
        chmo = 'УЧАСТНИК' # MEMBER
    else:
        chmo = 'БОТ' # BOT
    if before.guild.id == 693929822543675455:
        if before.nick != after.nick:
            emb = discord.Embed(title = 'ИЗМЕНЕНИЕ_НИКНЕЙМА', color = discord.Colour.orange(), timestamp = datetime.datetime.utcnow()) # NICKNAME_CHANGED
            if before.nick == None:
                before.nick = 'НЕ\_БЫЛ_УКАЗАН' # WAS_NONE
            if after.nick == None:
                after.nick = 'НЕ_УКАЗАН' # NOW_NONE
            emb.add_field(name = f'{chmo}', value = before)
            emb.add_field(name = 'БЫЛ', value = before.nick) # WAS
            emb.add_field(name = 'СТАЛ', value = after.nick) # NOW
            emb.set_footer(text = f'ID: {before.id}')
            await channel.send(embed = emb)
        if before.roles != after.roles:
            a = set(before.roles)
            b = set(after.roles)
            async for event in before.guild.audit_logs(limit = 1, action = discord.AuditLogAction.member_role_update):
                if a > b:
                    emb = discord.Embed(title = 'РОЛЬ_ЗАБРАНА', description = ', '.join([getattr(r, "mention", r.id) for r in event.before.roles or event.after.roles]), colour = discord.Color.orange(), timestamp = datetime.datetime.utcnow()) # ROLE_REMOVED
                elif a < b:
                    emb = discord.Embed(title = 'РОЛЬ_ВЫДАНА', description = ', '.join([getattr(r, "mention", r.id) for r in event.before.roles or event.after.roles]), colour = discord.Color.orange(), timestamp = datetime.datetime.utcnow()) # ROLE_GIVEN
                emb.set_author(name = before, icon_url = before.avatar_url)
                emb.set_footer(text = f'ID: {before.id}')
            await channel.send(embed = emb)

@client.event
async def on_member_join(member):
    if member.bot == False:
        chmo = 'УЧАСТНИК' # MEMBER
    else:
        chmo = 'БОТ' # BOT
    lchannel = client.get_channel(714175791033876490)
    emb = discord.Embed(title = f'{chmo}\_ЗАШЁЛ\_НА_СЕРВЕР', colour = discord.Color.orange(), timestamp = datetime.datetime.utcnow()) # {chmo}_ENTERED_THE_SERVER
    emb.add_field(name = f'{chmo}', value = member)
    emb.add_field(name = 'УПОМИНАНИЕ', value = member.mention) # MENTION
    emb.add_field(name = 'СЕРВЕР', value = member.guild.name) # SERVER
    emb.set_footer(text = f'ID: {member.id}')
    await lchannel.send(embed = emb)
    if member.bot == False:
        role = discord.utils.get(member.guild.roles, id = 693933516294979704)
        if member.guild.id == 693929822543675455 and member.bot == False:
            channel = client.get_channel(693929823030214658)
            emb = discord.Embed(description = f'{member.mention} ({member.name}) пришёл к нам!', colour = discord.Color.orange(), timestamp = datetime.datetime.utcnow())
            await channel.send(embed = emb)
            if role != None:
                await member.add_roles(role)
        if member.guild.id == 818758712163827723:
            role = discord.utils.get(member.guild.roles, id = 818762863287074826)
            await member.add_roles(role)
            channel = client.get_channel(818776092013887508)
            emb = discord.Embed(description = f'{member.mention} ({member.name}) пришёл к нам!', color = discord.Color.orange(), timestamp = datetime.datetime.utcnow())
            await channel.send(embed = emb)
    else:
        role = discord.utils.get(member.guild.roles, id = 693933516831850527)
        role1 = discord.utils.get(member.guild.roles, id = 693933511412940800)
        await member.add_roles(role, role1)

@client.event
async def on_member_remove(member):
    if member.bot == False:
        chmo = 'УЧАСТНИК' # MEMBER
    else:
        chmo = 'БОТ' # BOT
    channel = client.get_channel(714175791033876490)
    emb = discord.Embed(title = f'{chmo}\_ВЫШЕЛ\_С_СЕРВЕРА', colour = discord.Color.orange(), timestamp = datetime.datetime.utcnow()) # {chmo}_LEFT_THE_SERVER
    emb.add_field(name = f'{chmo}', value = member)
    emb.add_field(name = 'УПОМИНАНИЕ', value = member.mention) # MENTION
    emb.add_field(name = 'СЕРВЕР', value = member.guild.name) # SERVER
    emb.set_footer(text = f'ID: {member.id}')
    await channel.send(embed = emb)
    if member.guild.id == 693929822543675455 and member.bot == False:
        channel = client.get_channel(693929823030214658)
        emb = discord.Embed(description = f'{member.mention} ({member.name}) покинул нас...', colour = discord.Color.orange(), timestamp = datetime.datetime.utcnow())
        await channel.send(embed = emb)
    if member.guild.id == 818758712163827723 and member.bot == False:
        channel = client.get_channel(818776092013887508)
        emb = discord.Embed(description = f'{member.mention} ({member.name}) покинул нас...', color = discord.Color.orange(), timestamp = datetime.datetime.utcnow())
        await channel.send(embed = emb)

@client.event
async def on_guild_remove(guild):
    channel = client.get_channel(714175791033876490)
    emb = discord.Embed(title = 'ВЫХОД\_С_СЕРВЕРА', colour = discord.Color.orange(), timestamp = datetime.datetime.utcnow()) # CLIENT_LEFT_SERVER
    emb.add_field(name = 'СЕРВЕР', value = guild.name) # SERVER
    emb.set_footer(text = f'ID: {guild.id}')
    await channel.send(embed = emb)

@client.event
async def on_guild_join(guild):
    channel = client.get_channel(714175791033876490)
    emb = discord.Embed(title = 'ДОБАВЛЕНИЕ\_НА_СЕРВЕР', colour = discord.Color.orange(), timestamp = datetime.datetime.utcnow()) # CLIENT_ADDED_TO_SERVER
    emb.add_field(name = 'СЕРВЕР', value = guild.name) # SERVER
    emb.set_footer(text = f'ID: {guild.id}')
    await channel.send(embed = emb)

@client.event
async def on_voice_state_update(member, before, after):
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
    except AttributeError:
        pass

@client.event
async def on_message(message):
    post = {
        '_id': message.author.id,
        'locale': 'ru'
    }
    if collection.count_documents({'_id': message.author.id}) == 0 and message.author.bot == False:
        collection.insert_one(post)
    if message.content.lower().startswith('cy|'):
        channel = client.get_channel(714175791033876490)
        emb = discord.Embed(title = 'ВОЗМОЖНОЕ\_ВЫПОЛНЕНИЕ_КОМАНДЫ', color = discord.Color.orange()) 
        emb.add_field(name = 'ВОЗМОЖНОЕ_НАЗВАНИЕ', value = message.content.strip()[3:].strip())
        emb.add_field(name = 'ВОЗМОЖНЫЙ_ИСПОЛНИТЕЛЬ', value = f'{message.author.mention} ({message.author.name})')
        emb.add_field(name = 'КАНАЛ', value = f'{message.channel.mention} ({message.channel.name})')
        emb.add_field(name = 'СЕРВЕР', value = message.guild.name, inline = False)
        await channel.send(embed = emb)
    if message.channel.id == 767848243291095090 and message.content.startswith('n!'):
        await message.delete()
    if message.content.startswith(f'<@!{client.user.id}>') and len(message.content) == len(f'<@!{client.user.id}>'):
        await message.channel.send(f'чё звал {message.author.mention} ||`cy/`||')
        await client.process_commands(message)
    def _check(m):
        return (m.author == message.author and len(m.mentions) and (datetime.datetime.utcnow() - m.created_at).seconds < 2)
    if len(list(filter(lambda m: _check(m), client.cached_messages))) >= 3:
        if not message.author.bot:
            role = discord.utils.get(message.guild.roles, name = 'Muted')
            role3 = discord.utils.get(message.guild.roles, name = '----------Предупреждения----------')
            role1 = discord.utils.get(message.guild.roles, name = '1')
            role2 = discord.utils.get(message.guild.roles, name = '2')
            if role != None and role1 != None and role2 != None and role3 != None:
                if role not in message.author.roles:
                    if role1 not in message.author.roles and role2 not in message.author.roles:
                        await message.channel.send(f'{message.author.mention} Был заглушён на 10 минут за спам упоминаниями. Больше так не делай!')
                        await message.author.add_roles(role, role1, role3)
                        channel = client.get_channel(714175791033876490)
                        emb = discord.Embed(title = 'СРАБОТАЛ\_АВТО_МУТ', color = discord.Color.orange(), timestamp = datetime.datetime.utcnow())
                        emb.add_field(name = 'СЕРВЕР', value = message.guild.name)
                        emb.add_field(name = 'ПРЕДУПРЕЖДЕНИЕ', value = 'ПЕРВОЕ')
                        emb.add_field(name = 'УЧАСТНИК', value = message.author)
                        await channel.send(embed = emb)
                        await asyncio.sleep(600)
                        if role != None:
                            if role in message.author.roles:
                                await message.author.remove_roles(role)
                                emb = discord.Embed(description = f'{message.author.mention} Был разглушён.', color = 0x2f3136)
                                await message.channel.send(embed = emb)
                            else:
                                emb = discord.Embed(description = f'Роли Muted не было обнаружено в списке ролей {message.author.mention}.', color = 0x2f3136)
                                await message.channel.send(embed = emb)
                        else:
                            emb = discord.Embed(description = f'Невозможно снять заглушение у {message.author.mention}, т.к. роль `Muted` была удалена.', color = 0x2f3136)
                            await message.channel.send(embed = emb)
                    if role1 in message.author.roles and role2 not in message.author.roles:
                        await message.channel.send(f'{message.author.mention} Был заглушён на 30 минут за спам упоминаниями. Последнее предупреждение.')
                        await message.author.remove_roles(role1)
                        await message.author.add_roles(role, role2, role3)
                        channel = client.get_channel(714175791033876490)
                        emb = discord.Embed(title = 'СРАБОТАЛ\_АВТО_МУТ', color = discord.Color.orange(), timestamp = datetime.datetime.utcnow())
                        emb.add_field(name = 'СЕРВЕР', value = message.guild.name)
                        emb.add_field(name = 'ПРЕДУПРЕЖДЕНИЕ', value = 'ПОСЛЕДНЕЕ')
                        emb.add_field(name = 'УЧАСТНИК', value = message.author)
                        await channel.send(embed = emb)
                        await asyncio.sleep(1800)
                        if role != None:
                            if role in message.author.roles:
                                await message.author.remove_roles(role)
                                emb = discord.Embed(description = f'{message.author.mention} Был разглушён.', color = 0x2f3136)
                                await message.channel.send(embed = emb)
                            else:
                                emb = discord.Embed(description = f'Роли Muted не было обнаружено в списке ролей {message.author.mention}.', color = 0x2f3136)
                                await message.channel.send(embed = emb)
                        else:
                            emb = discord.Embed(description = f'Невозможно снять заглушение у {message.author.mention}, т.к. роль `Muted` была удалена.', color = 0x2f3136)
                            await message.channel.send(embed = emb)
                    if role2 in message.author.roles:
                        await message.channel.send(f'{message.author.mention} Был заглушён навсегда за спам упоминаниями.')
                        await message.author.add_roles(role)
                        await message.author.remove_roles(role2, role3)
                        channel = client.get_channel(714175791033876490)
                        emb = discord.Embed(title = 'СРАБОТАЛ\_АВТО_МУТ', color = discord.Color.orange(), timestamp = datetime.datetime.utcnow())
                        emb.add_field(name = 'СЕРВЕР', value = message.guild.name)
                        emb.add_field(name = 'УЧАСТНИК', value = message.author)
                        await channel.send(embed = emb)
                else:
                    return
            elif role == None:
                r = await message.guild.create_role(name = 'Muted', colour = discord.Colour(0x000001), reason = 'Создано автоматически из-за недостатка ролей.')
                await r.edit(position = 4)
            elif role3 == None:
                r1 = await message.guild.create_role(name = '----------Предупреждения----------', colour = discord.Colour(0x2f3136), reason = 'Создано автоматически из-за недостатка ролей.')
                r1.edit(position = 3)
            elif role1 == None:
                r2 = await message.guild.create_role(name = '1', colour = discord.Colour(0xff0000), reason = 'Создано автоматически из-за недостатка ролей.')
                r2.edit(position = 2)
            elif role2 == None:
                r3 = await message.guild.create_role(name = '2', colour = discord.Colour(0xff0000), reason = 'Создано автоматически из-за недостатка ролей.')
                r3.edit(position = 1)
    if ('сделать') in message.content.lower() or ('предлагаю') in message.content.lower() or ('предложение') in message.content.lower() and message.author.bot == False:
        await message.add_reaction('👍')
        await message.add_reaction('👎')
    if ('поздравляю') in message.content.lower() or ('поздравим') in message.content.lower() or ('поздравляем') in message.content.lower():
        await message.add_reaction('🥳')
    elif message.channel.id == 750372413102883028: #EFT
        if message.author.bot == True and message.author.id != 694170281270312991:
            role = discord.utils.get(message.guild.roles, id = 750368477671325728)
            sent = await message.channel.send(role.mention)
            await sent.delete()
            channel = client.get_channel(714175791033876490)
            emb = discord.Embed(title = 'ОПОВЕЩЕНИЕ\_ОБ_ОБНОВЛЕНИИ', color = discord.Color.orange(), timestamp = datetime.datetime.utcnow())
            emb.add_field(name = 'ОПОВЕЩЕНЫ', value = role.mention)
            await channel.send(embed = emb)
    elif message.channel.id == 750368033578680361: #OV
        if message.author.bot == True and message.author.id != 694170281270312991:
            role = discord.utils.get(message.guild.roles, id = 750366804689420319)
            sent = await message.channel.send(role.mention)
            await sent.delete()
            channel = client.get_channel(714175791033876490)
            emb = discord.Embed(title = 'ОПОВЕЩЕНИЕ\_ОБ_ОБНОВЛЕНИИ', color = discord.Color.orange(), timestamp = datetime.datetime.utcnow())
            emb.add_field(name = 'ОПОВЕЩЕНЫ', value = role.mention)
            await channel.send(embed = emb)
    elif message.channel.id == 750363498290348123: #DOTA 2
        if message.author.bot == True and message.author.id != 694170281270312991:
            role = discord.utils.get(message.guild.roles, id = 750363797226782802)
            sent = await message.channel.send(role.mention)
            await sent.delete()
            channel = client.get_channel(714175791033876490)
            emb = discord.Embed(title = 'ОПОВЕЩЕНИЕ\_ОБ_ОБНОВЛЕНИИ', color = discord.Color.orange(), timestamp = datetime.datetime.utcnow())
            emb.add_field(name = 'ОПОВЕЩЕНЫ', value = role.mention)
            await channel.send(embed = emb)
    elif message.channel.id == 750373602460827730: #MC
        if message.author.bot == True and message.author.id != 694170281270312991:
            role = discord.utils.get(message.guild.roles, id = 750373687479238787)
            sent = await message.channel.send(role.mention)
            await sent.delete()
            channel = client.get_channel(714175791033876490)
            emb = discord.Embed(title = 'ОПОВЕЩЕНИЕ\_ОБ_ОБНОВЛЕНИИ', color = discord.Color.orange(), timestamp = datetime.datetime.utcnow())
            emb.add_field(name = 'ОПОВЕЩЕНЫ', value = role.mention)
            await channel.send(embed = emb)
    if message.channel.id == 693931411815661608:
        await message.add_reaction('👍')
        await message.add_reaction('👎')
    elif message.channel.id == 747838996729692160:
        await message.add_reaction('👍')
        await message.add_reaction('👎')
    elif message.channel.id == 707498623981715557:
        await message.add_reaction('👍')
        await message.add_reaction('👎')
    channel = client.get_channel(714175791033876490)
    if channel is None:
        await client.process_commands(message)
        return
    if not message.author.bot:
        if message.channel.id != 714175791033876490:
            emb = discord.Embed(colour = discord.Color.orange(), timestamp = datetime.datetime.utcnow())
            emb.set_author(name = message.author, icon_url = message.author.avatar_url)
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
            emb = discord.Embed(description = f'[ИЗМЕНЕНИЕ_СООБЩЕНИЯ]({before.jump_url})', colour = discord.Color.orange(), timestamp = datetime.datetime.utcnow())
            emb.set_author(name = before.author, icon_url = before.author.avatar_url)
            emb.add_field(name = 'НА_СЕРВЕРЕ', value = before.guild)
            emb.add_field(name = 'БЫЛО', value = f'```{before.content}```')
            emb.add_field(name = 'СТАЛО', value = f'```{after.content}```')
            await channel.send(embed = emb)
    
#Mod
@slash.slash(name = 'dm', description = 'Пишет в лс человеку от имени бота написанный текст', options = [{'name': 'member', 'description': 'Участник', 'required': True, 'type': 6}, {'name': 'text', 'description': 'Текст для написания', 'required': True, 'type': 3}])
async def _dm(ctx, member: discord.User, *, text):
    emb = discord.Embed(description = f'{text}', colour = 0x2f3136)
    emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
    await member.send(embed = emb)
    rlocale = collection.find_one({"_id": ctx.author.id})["locale"]
    if rlocale == 'ru':
        await ctx.send('Сообщение отправлено.')
    if rlocale == 'gnida':
        await ctx.send('Твоя хуйня отправлена')

@slash.slash(name = 'kick', description = 'Выгоняет участника с сервера', options = [{'name': 'member', 'description': 'Участник', 'required': True, 'type': 6}, {'name': 'reason', 'description': 'Причина', 'required': False, 'type': 3}])
async def _kick(ctx, member: discord.Member, *, reason = None):
    rlocale = collection.find_one({"_id": ctx.author.id})["locale"]
    bot = discord.utils.get(ctx.guild.members, id = client.user.id)
    if member.id != 338714886001524737:
        if reason == None:
            if rlocale == 'ru':
                reason = 'Не указана.'
            if rlocale == 'gnida':
                reason = 'Я не ебу'
        if ctx.author.top_role == member.top_role:
            if rlocale == 'ru':
                emb = discord.Embed(description = f'{ctx.author.mention}, ваша высшая роль равна высшей роли {member.mention}. Кик отклонён.', colour = discord.Color.orange())
                await ctx.send(embed = emb)
            if rlocale == 'gnida':
                emb = discord.Embed(description = f'Твоя высшая роль равна высшей роли {member.mention}. Пошёл нахуй.', colour = discord.Color.orange())
                await ctx.send(embed = emb)
        elif member.top_role > ctx.author.top_role:
            if rlocale == 'ru':
                emb = discord.Embed(description = f'{ctx.author.mention}, ваша высшая роль ниже высшей роли {member.mention}. Кик отклонён.', colour = discord.Color.orange())
                await ctx.send(embed = emb)
            if rlocale == 'gnida':
                emb = discord.Embed(description = f'Твоя высшая роль ниже высшей роли {member.mention}. Пошёл нахуй.', colour = discord.Color.orange())
                await ctx.send(embed = emb)
        elif member.top_role > bot.top_role:
            if rlocale == 'ru':
                emb = discord.Embed(description = f'МОЯ высшая роль ниже высшей роли {member.mention}. Кик невозможен.', color = 0xff0000)
                await ctx.send(embed = emb)
            if locale == 'gnida':
                emb = discord.Embed(description = f'МОЯ высшая роль ниже высшей роли {member.mention}. Сука.', color = 0xff0000)
                await ctx.send(embed = emb)
        elif member.top_role == bot.top_role:
            if rlocale == 'ru':
                emb = discord.Embed(description = f'МОЯ высшая роль идентична высшей роли {member.mention}. Кик невозможен.', color = 0xff0000)
                await ctx.send(embed = emb)
            if locale == 'gnida':
                emb = discord.Embed(description = f'МОЯ высшая роль идентична высшей роли {member.mention}. Сука.', color = 0xff0000)
                await ctx.send(embed = emb)
        else:
            emb = discord.Embed(colour = member.color)
            emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            emb.add_field(name = 'Был кикнут', value = member.mention)
            emb.add_field(name = 'По причине', value = reason)
            if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
            await ctx.send(embed = emb)
            await member.kick(reason = reason)
    else:
        if rlocale == 'ru':
            emb = discord.Embed(description = f'Извините, {ctx.author.mention}, но вы не можете кикнуть моего создателя!', colour = discord.Color.orange())
            await ctx.send(embed = emb)
        if rlocale == 'gnida':
            emb = discord.Embed(description = 'Ого! Пошёл нахуй!', colour = discord.Color.orange())
            await ctx.send(embed = emb)

@slash.slash(name = 'ban', description = 'Банит участника', options = [{'name': 'member', 'description': 'Участник', 'required': True, 'type': 6}, {'name': 'reason', 'description': 'Причина и/или указание --soft --reason', 'required': False, 'type': 3}])
async def _ban(ctx, member: discord.Member, *, reason = None):
    rlocale = collection.find_one({"_id": ctx.author.id})["locale"]
    bot = discord.utils.get(ctx.guild.members, id = client.user.id)
    if member.id != 338714886001524737:
        if reason == None:
            if rlocale == 'ru':
                reason = 'Не указана.'
            if rlocale == 'gnida':
                reason = 'Я не ебу'
        if ctx.author.top_role == member.top_role:
            if rlocale == 'ru':
                emb = discord.Embed(description = f'{ctx.author.mention}, ваша высшая роль равна высшей роли {member.mention}. Бан отклонён.', colour = discord.Color.orange())
                await ctx.send(embed = emb)
            if rlocale == 'gnida':
                emb = discord.Embed(description = f'Твоя высшая роль равна высшей роли {member.mention}. Саси.', colour = discord.Color.orange())
                await ctx.send(embed = emb)
        elif member.top_role > ctx.author.top_role:
            if rlocale == 'ru':
                emb = discord.Embed(description = f'{ctx.author.mention}, ваша высшая роль ниже высшей роли {member.mention}. Бан отклонён.', colour = discord.Color.orange())
                await ctx.send(embed = emb)
            if rlocale == 'gnida':
                emb = discord.Embed(description = f'Твоя высшая роль ниже высшей роли {member.mention}. Саси.', colour = discord.Color.orange())
                await ctx.send(embed = emb)
        elif member.top_role > bot.top_role:
            if rlocale == 'ru':
                emb = discord.Embed(description = f'МОЯ высшая роль ниже высшей роли {member.mention}. Бан невозможен.', color = 0xff0000)
                await ctx.send(embed = emb)
            if rlocale == 'gnida':
                emb = discord.Embed(description = f'МОЯ высшая роль ниже высшей роли {member.mention}. Блять.', color = 0xff0000)
                await ctx.send(embed = emb)
        elif member.top_role == bot.top_role:
            if rlocale == 'ru':
                emb = discord.Embed(description = f'МОЯ высшая роль идентична высшей роли {member.mention}. Бан невозможен.', color = 0xff0000)
                await ctx.send(embed = emb)
            if rlocale == 'gnida':
                emb = discord.Embed(description = f'МОЯ высшая роль идентична высшей роли {member.mention}. Блять.', color = 0xff0000)
                await ctx.send(embed = emb)
        else:
            if '--soft' in reason:
                emb = discord.Embed(color = 0x2f3136)
                emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                emb.add_field(name = 'Упрощённо забанен', value = f'{member.mention} ({member.name})')
                if '--reason' in reason:
                    reason = reason.strip()[15:].strip()
                else:
                    if rlocale == 'ru':
                        reason = 'Не указана.'
                    if rlocale == 'gnida':
                        reason == 'Я не ебу'
                emb.add_field(name = 'По причине', value = reason)
                await ctx.send(embed = emb)
                await member.ban(reason = reason)
                await member.unban(reason = '--softban')
            else:
                emb = discord.Embed(colour = 0x2f3136)
                emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                emb.add_field(name = 'Был забанен', value = member.mention)
                emb.add_field(name = 'По причине', value = reason)
                await ctx.send(embed = emb)
                await member.ban(reason = reason)
    else:
        if rlocale == 'ru':
            emb = discord.Embed(description = f'Извините, {ctx.author.mention}, но вы не можете забанить моего создателя!', colour = discord.Color.orange())
            await ctx.send(embed = emb)
        if rlocale == 'gnida':
            emb = discord.Embed(description = 'А ты не прихуел даже ПЫТАТЬСЯ это сделать?!', colour = discord.Color.orange())
            await ctx.send(embed = emb)

@slash.slash(name = 'give', description = 'Выдаёт участнику роль', options = [{'name': 'member', 'description': 'Участник', 'required': True, 'type': 6}, {'name': 'role', 'description': 'Роль', 'required': True, 'type': 8}])
async def _give(ctx, member: discord.Member, *, role: discord.Role):
    rlocale = collection.find_one({"_id": ctx.author.id})["locale"]
    if role.name == 'Muted':
        if member.id != client.owner_id:
            await member.add_roles(role)
            if rlocale == 'ru':
                emb = discord.Embed(description = f'{member.mention} был перманентно заглушён {ctx.author.mention}', color = 0x2f3136)
                if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                    emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
                return await ctx.send(embed = emb)
            if rlocale == 'gnida':
                emb = discord.Embed(description = f'{member.mention} получает мут в ебало от {ctx.author.mention}', color = 0x2f3136)
                if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                    emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
                return await ctx.send(embed = emb)
        else:
            emb = discord.Embed(description = 'Ты думал мой Создатель тебе по зубам? ОН!?', color = 0xff0000)
            if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
            return await ctx.send(embed = emb)
    if role > ctx.author.top_role:
        if rlocale == 'ru':
            emb = discord.Embed(description = f'Вы не можете выдать {role.mention}, так как она имеет более высокий ранг, чем ваша высшая роль.', color = discord.Color.orange())
            if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
            await ctx.send(embed = emb)
        if rlocale == 'gnida':
            emb = discord.Embed(description = f'Дебилам вроде тебя запрещено выдавать {role.mention}, так как эта роль выше твоей высшей роли.', color = discord.Color.orange())
            if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
            await ctx.send(embed = emb)
    elif role == ctx.author.top_role:
        if rlocale == 'ru':
            emb = discord.Embed(description = f'Вы не можете выдать {role.mention} кому-либо, так как она равна вашей высшей роли.', color = discord.Color.orange())
            if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
            await ctx.send(embed = emb)
        if rlocale == 'gnida':
            emb = discord.Embed(description = f'Дебилам вроде тебя запрещено выдавать {role.mention}, так как она равна твоей высшей роли.', color = discord.Color.orange())
            if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
            await ctx.send(embed = emb)
    else:
        await member.add_roles(role)
        emb = discord.Embed(colour = member.color, timestamp = datetime.datetime.utcnow())
        emb.add_field(name = 'ВЫДАНА_РОЛЬ', value = f'{role.mention} | {role.name} | ID {role.id}')
        emb.add_field(name = 'ВЫДАНА:', value = member.mention, inline = False)
        emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
        if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
            emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb)

@slash.slash(name = 'take', description = 'Забирает роль у участника', options = [{'name': 'member', 'description': 'Участник', 'required': True, 'type': 6}, {'name': 'role', 'description': 'Роль', 'required': True, 'type': 8}])
async def _take(ctx, member: discord.Member, *, role: discord.Role):
    bot = ctx.guild.get_member(client.user.id)
    if role.name == 'Muted':
        await member.remove_roles(role)
        emb = discord.Embed(description = f'{member.mention} был разглушён {ctx.author.mention}', color = 0x2f3136)
        if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
            emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        return await ctx.send(embed = emb)
    if role > ctx.author.top_role:
        emb = discord.Embed(description = f'Вы не можете забрать {role.mention}, так как она имеет более высокий ранг, чем ваша высшая роль. Забирание роли отменено.', color = 0x2f3136)
        if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
            emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb)
    elif role == ctx.author.top_role:
        emb = discord.Embed(description = f'Вы не можете забрать {role.mention}, так как она равна вашей высшей роли. Забирание роли отменено.', color = 0x2f3136)
        if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
            emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb)
    elif member.top_role > bot.top_role:
        emb = discord.Embed(description = f'МОЯ высшая роль ниже высшей роли {member.mention}. Забрать роль невозможно.', color = 0xff0000)
        if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
            emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb)
    elif member.top_role == bot.top_role:
        emb = discord.Embed(description = f'МОЯ высшая роль идентична высшей роли {member.mention}. Забрать роль невозможно.', color = 0xff0000)
        if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
            emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb)
    else:
        await member.remove_roles(role)
        emb = discord.Embed(colour = member.color, timestamp = datetime.datetime.utcnow())
        emb.add_field(name = 'ЗАБРАНА_РОЛЬ', value = f'{role.mention} | {role.name} | ID {role.id}')
        emb.add_field(name = 'ЗАБРАНА_У:', value = member.mention, inline = False)
        emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
        if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
            emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb)

@slash.slash(name = 'unmute', description = 'Отменяет заглушение участника', options = [{'name': 'member', 'description': 'Участник', 'required': True, 'type': 6}, {'name': 'reason', 'description': 'Причина', 'required': False, 'type': 3}])
async def _unmute(ctx, member: discord.Member, *, reason = None):
    role = discord.utils.get(ctx.guild.roles, name = 'Muted')
    if role != None:
        if role in member.roles:
            await member.remove_roles(role)
            if reason == None:
                reason = 'Не указана.'
            emb = discord.Embed(title = f'Принудительное снятие заглушения у {member}', colour = member.color, timestamp = datetime.datetime.utcnow())
            emb.add_field(name = 'Снял мут', value = ctx.author.mention)
            emb.add_field(name = 'По причине', value = reason)
            await ctx.send(embed = emb)
        else:
            emb = discord.Embed(description = 'Снятие заглушения не требуется. Роли Muted не обнаружено в списке ролей участника.', colour = discord.Color.orange())
            await ctx.send(embed = emb)
    else:
        emb = discord.Embed(description = f'{ctx.author.mention}, Я не могу снять заглушение у {member.mention} из-за того, что роль Muted была удалена/отредактирована!', colour = discord.Color.orange(), timestamp = datetime.datetime.now())
        await ctx.send(embed = emb)
        
@slash.slash(name = 'clear', description = 'Очищает канал от указанного количества сообщений. Не работает, если в канале нет сообщений.', options = [{'name': 'amount', 'description': 'Количество сообщений для удаления', 'required': True, 'type': 4}, {'name': 'members', 'description': 'Указание диапазона удаления сообщений', 'required': False, 'type': 3, 'choices': [{'name': 'Удалить сообщения ото всех', 'value': '--everyone'}, {'name': 'Удалить сообщения только от ботов', 'value': '--bots'}, {'name': 'Удалить сообщения только от людей', 'value': '--users'}, {'name': 'Не оставить доказательства исполнения команды, если количество сообщений для удаления меньше 10', 'value': '--silent'}]}, {'name': 'filt', 'description': 'Удаляет сообщение с заданным словом/словосочетанием', 'required': False, 'type': 3}])
async def _clear(ctx, amount: int, members = '--everyone', *, filt = None):
    authors = {}
    cleared = 0
    if not '--silent' in members:
        async for message in ctx.channel.history(limit = amount):
            if message.author not in authors:
                authors[message.author] = 1
            else:
                authors[message.author] += 1
            try:
                cleared += 1
            except Exception:
                pass
    if amount == 2472:
        if ctx.author.id == client.owner_id:
            await ctx.channel.delete()
            emb = discord.Embed(description = f'канал `{ctx.channel.name}` удалён.', color = discord.Color.orange())
            await ctx.author.send(embed = emb)
        else:
            await ctx.author.send('Как ты узнал об этом?!')
    elif amount >= 300:
        emb = discord.Embed(description = f'{ctx.author.mention}, при таком числе удаления сообщений ({amount}) неизбежны ошибки в работе {client.user.mention}.', colour = discord.Color.orange())
        await ctx.send(f'{ctx.guild.owner.mention}', embed = emb)
    elif amount >= 250:
        if ctx.author != ctx.guild.owner:
            emb = discord.Embed(description = f'{ctx.author.mention}, операция с данным числом ({amount}) доступна только {ctx.guild.owner.mention}. Отмена.', colour = discord.Color.orange())
            await ctx.send(f'{ctx.guild.owner.mention}', embed = emb, delete_after = 5)
        else:
            emb = discord.Embed(description = f'{ctx.author.mention}, обнаружено слишком большое число для удаления сообщений ({amount}). Возможны дальнейшие ошибки в работе {client.user.mention}. Продолжить? (y/n)\n||Отмена через 10 секунд.||', colour = discord.Color.orange())
            sent = await ctx.send(embed = emb)
            try:
                msg = await client.wait_for('message', timeout = 10, check = lambda message: message.channel == ctx.channel and message.author.id == ctx.guild.owner.id)
                if msg.content.lower() == 'y':
                    await msg.delete()
                    await sent.delete()
                    if '--silent' not in members:
                        emb = discord.Embed(description = 'Проверяем..', color = discord.Color.orange())
                        sent = await ctx.send(embed = emb)
                        if members == '--bots':
                            if filt == None:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == True, before = sent)
                            else:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.author.bot == True, before = sent)
                            emb = discord.Embed(title = 'Результаты удаления сообщений', color = discord.Color.orange())
                            emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{amount}```')
                            if filt:
                                emb.add_field(name = 'Применён фильтр:', value = f'{filt} ({members})', inline = True)
                            emb.add_field(name = 'Удалены/Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                            emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c".')
                            await sent.edit(embed = emb)
                        elif members == '--users':
                            if filt == None:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False, before = sent)
                            else:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False and m.content.lower() == filt.lower(), before = sent)
                            emb = discord.Embed(title = 'Результаты удаления сообщений', color = discord.Color.orange())
                            emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{cleared}```')
                            if filt:
                                emb.add_field(name = 'Применён фильтр:', value = f'{filt} ({members})', inline = True)
                            emb.add_field(name = 'Удалены/Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                            emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c".')
                            await sent.edit(embed = emb)
                        else:
                            if filt == None:
                                await ctx.channel.purge(limit = amount, before = sent)
                            else:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower(), before = sent)
                            emb = discord.Embed(title = 'Результаты удаления сообщений', color = discord.Color.orange())
                            emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{cleared}```')
                            if filt:
                                emb.add_field(name = 'Применён фильтр:', value = f'{filt} ({members})', inline = True)
                            emb.add_field(name = 'Удалены/Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                            emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c".')
                            await sent.edit(embed = emb)
                        try:
                            if '--silent' in members:
                                return
                            msg = await client.wait_for('message', timeout = 10, check = lambda message: message.channel == ctx.channel and message.author == ctx.author and message.content.lower() == 'c')
                            emb = discord.Embed(title = 'Результаты удаления сообщений', color = discord.Color.orange())
                            emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{cleared}```')
                            if filt:
                                emb.add_field(name = 'Применён фильтр:', value = f'{filt} ({members})', inline = True)
                            emb.add_field(name = 'Удалены/Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                            await sent.edit(embed = emb)
                        except asyncio.TimeoutError:
                            await sent.delete()
                    else:
                        if '--bots' in members:
                            if filt == None:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == True)
                            else:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.author.bot == True)
                        elif '--users' in members:
                            if filt == None:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False)
                            else:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False and m.content.lower() == filt.lower())
                        elif '--everyone' in members:
                            if filt == None:
                                await ctx.channel.purge(limit = amount)
                            else:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower())
                        elif members == '--silent':
                            if filt == None:
                                await ctx.channel.purge(limit = amount)
                            else:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower())
                elif msg.content.lower() == 'n' and msg.author.id == ctx.guild.owner.id:
                    await msg.delete()
                    await sent.delete()
                    emb = discord.Embed(description = f'{ctx.guild.owner.mention} отменил запрос.', colour = discord.Color.orange())
                    await ctx.send(embed = emb, delete_after = 3)
                elif msg.content.lower() == 'n' or 'y' and msg.author.id != ctx.guild.owner.id:
                    await msg.delete()
                    await sent.delete()
                    emb = discord.Embed(description = f'{ctx.author.mention}, ты не являешься владельцем сервера.', colour = discord.Color.orange())
                    await ctx.send(embed = emb, delete_after = 3)
                else:
                    await msg.delete()
                    await sent.delete()
                    emb = discord.Embed(description = f'Обнаружен недопустимый ответ ({msg.content})', colour = discord.Color.orange())
                    await ctx.send(embed = emb, delete_after = 3)
            except asyncio.TimeoutError:
                await sent.delete()
                emb = discord.Embed(description = f'{ctx.author.mention}, Время вышло.', colour = discord.Color.orange())
                await ctx.send(f'{ctx.guild.owner.mention}', embed = emb, delete_after = 3)
    elif amount >= 100:
        if ctx.author != ctx.guild.owner:
            emb = discord.Embed(description = f'{ctx.author.mention}, создан запрос на удаление {amount} сообщений. Мне нужен ответ создателя сервера на это действие. Продолжаем? (y/n)\n||Запрос будет отменён через 1 минуту.||', colour = discord.Color.orange())
            sent = await ctx.send(f'{ctx.guild.owner.mention}', embed = emb)
            try:
                msg = await client.wait_for('message', timeout = 10, check = lambda message: message.channel == ctx.channel and message.author.id == ctx.guild.owner.id)
                if msg.content.lower() == 'y':
                    await msg.delete()
                    await sent.delete()
                    if '--silent' not in members:
                        emb = discord.Embed(description = 'Проверяем..', color = discord.Color.orange())
                        sent = await ctx.send(embed = emb)
                        if members == '--bots':
                            if filt == None:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == True, before = sent)
                            else:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.author.bot == True, before = sent)
                            emb = discord.Embed(title = 'Результаты удаления сообщений', color = discord.Color.orange())
                            emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{cleared}```')
                            if filt:
                                emb.add_field(name = 'Применён фильтр:', value = f'{filt} ({members})', inline = True)
                            emb.add_field(name = 'Удалены/Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                            emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c".')
                            await sent.edit(embed = emb)
                        elif members == '--users':
                            if filt == None:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False, before = sent)
                            else:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False and m.content.lower() == filt.lower(), before = sent)
                            emb = discord.Embed(title = 'Результаты удаления сообщений', color = discord.Color.orange())
                            emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{cleared}```')
                            if filt:
                                emb.add_field(name = 'Применён фильтр:', value = f'{filt} ({members})', inline = True)
                            emb.add_field(name = 'Удалены/Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                            emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c".')
                            await sent.edit(embed = emb)
                        else:
                            if filt == None:
                                await ctx.channel.purge(limit = amount, before = sent)
                            else:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower(), before = sent)
                            emb = discord.Embed(title = 'Результаты удаления сообщений', color = discord.Color.orange())
                            emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{cleared}```')
                            if filt:
                                emb.add_field(name = 'Применён фильтр:', value = f'{filt} ({members})', inline = True)
                            emb.add_field(name = 'Удалены/Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                            emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c".')
                            await sent.edit(embed = emb)
                        try:
                            if '--silent' in members:
                                return
                            msg = await client.wait_for('message', timeout = 10, check = lambda message: message.channel == ctx.channel and message.author == ctx.author and message.content.lower() == 'c')
                            emb = discord.Embed(title = 'Результаты удаления сообщений', color = discord.Color.orange())
                            emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{cleared}```')
                            if filt:
                                emb.add_field(name = 'Применён фильтр:', value = f'{filt} ({members})', inline = True)
                            else:
                                emb.add_field(name = 'Удалены/Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                            await sent.edit(embed = emb)
                        except asyncio.TimeoutError:
                            await sent.delete()
                    else:
                        if '--bots' in members:
                            if filt == None:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == True)
                            else:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.author.bot == True)
                        elif '--users' in members:
                            if filt == None:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False)
                            else:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False and m.content.lower() == filt.lower())
                        elif '--everyone' in members:
                            if filt == None:
                                await ctx.channel.purge(limit = amount)
                            else:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower())
                        elif members == '--silent':
                            if filt == None:
                                await ctx.channel.purge(limit = amount)
                            else:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower())
                elif msg.content.lower() == 'n' and msg.author.id == ctx.guild.owner.id:
                    await msg.delete()
                    await sent.delete()
                    emb = discord.Embed(description = f'{ctx.guild.owner} отменил запрос.', colour = discord.Color.orange())
                    await ctx.send(embed = emb, delete_after = 3)
                elif msg.content.lower() == 'n' or 'y' and msg.author.id != ctx.guild.owner.id:
                    await msg.delete()
                    await sent.delete()
                    emb = discord.Embed(description = f'{ctx.author.mention}, ты не являешься владельцем сервера.', colour = discord.Color.orange())
                    await ctx.send(embed = emb, delete_after = 3)
                else:
                    await msg.delete()
                    await sent.delete()
                    emb = discord.Embed(description = f'Обнаружен недопустимый ответ ({msg.content})', colour = discord.Color.orange())
                    await ctx.send(embed = emb, delete_after = 3)
            except asyncio.TimeoutError:
                await sent.delete()
                emb = discord.Embed(description = f'{ctx.author.mention}, Время вышло.', colour = discord.Color.orange())
                await ctx.send(f'{ctx.guild.owner.mention}', embed = emb, delete_after = 3)
        else:
            emb = discord.Embed(description = f'{ctx.author.mention}, создан запрос на удаление {amount} сообщений. Продолжить? (y/n)\n||Запрос будет отменён через 10 секунд.||', colour = discord.Color.orange())
            sent = await ctx.send(embed = emb)
            try:
                msg = await client.wait_for('message', timeout = 10, check = lambda message: message.author == ctx.author and message.channel == ctx.channel)
                if msg.content.lower() == 'y':
                    await msg.delete()
                    await sent.delete()
                    if '--silent' not in members:
                        emb = discord.Embed(description = 'Проверяем..', color = discord.Color.orange())
                        sent = await ctx.send(embed = emb)
                        if members == '--bots':
                            if filt == None:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == True, before = sent)
                            else:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.author.bot == True, before = sent)
                            emb = discord.Embed(title = 'Результаты удаления сообщений', color = discord.Color.orange())
                            emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{cleared}```')
                            if filt:
                                emb.add_field(name = 'Применён фильтр:', value = f'{filt} ({members})', inline = True)
                            emb.add_field(name = 'Удалены/Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                            emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c".')
                            await sent.edit(embed = emb)
                        elif members == '--users':
                            if filt == None:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False, before = sent)
                            else:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False and m.content.lower() == filt.lower(), before = sent)
                            emb = discord.Embed(title = 'Результаты удаления сообщений', color = discord.Color.orange())
                            emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{cleared}```')
                            if filt:
                                emb.add_field(name = 'Применён фильтр:', value = f'{filt} ({members})', inline = True)
                            emb.add_field(name = 'Удалены/Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                            emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c".')
                            await sent.edit(embed = emb)
                        else:
                            if filt == None:
                                await ctx.channel.purge(limit = amount, before = sent)
                            else:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower(), before = sent)
                            emb = discord.Embed(title = 'Результаты удаления сообщений', color = discord.Color.orange())
                            emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{cleared}```')
                            if filt:
                                emb.add_field(name = 'Применён фильтр:', value = f'{filt} ({members})', inline = True)
                            emb.add_field(name = 'Удалены/Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                            emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c".')
                            await sent.edit(embed = emb)
                        try:
                            if '--silent' in members:
                                return
                            msg = await client.wait_for('message', timeout = 10, check = lambda message: message.channel == ctx.channel and message.author == ctx.author and message.content.lower() == 'c')
                            emb = discord.Embed(title = 'Результаты удаления сообщений', color = discord.Color.orange())
                            emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{cleared}```')
                            if filt:
                                emb.add_field(name = 'Применён фильтр:', value = f'{filt} ({members})', inline = True)
                            else:
                                emb.add_field(name = 'Удалены/Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                            await sent.edit(embed = emb)
                        except asyncio.TimeoutError:
                            await sent.delete()
                    else:
                        if '--bots' in members:
                            if filt == None:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == True)
                            else:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.author.bot == True)
                        elif '--users' in members:
                            if filt == None:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False)
                            else:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False and m.content.lower() == filt.lower())
                        elif '--everyone' in members:
                            if filt == None:
                                await ctx.channel.purge(limit = amount)
                            else:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower())
                        elif members == '--silent':
                            if filt == None:
                                await ctx.channel.purge(limit = amount)
                            else:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower())
                elif msg.content.lower() == 'n':
                    await msg.delete()
                    await sent.delete()
                    emb = discord.Embed(description = 'Отменено.', colour = discord.Color.orange())
                    await ctx.send(embed = emb, delete_after = 3)
                else:
                    await msg.delete()
                    await sent.delete()
                    emb = discord.Embed(description = f'Обнаружен недопустимый ответ ({msg.content})', colour = discord.Color.orange())
                    await ctx.send(embed = emb, delete_after = 3)
            except asyncio.TimeoutError:
                await sent.delete()
                emb = discord.Embed(description = f'{ctx.author.mention}, Время вышло.', colour = discord.Color.orange())
                await ctx.send(embed = emb, delete_after = 3)
    elif amount >= 10:
        emb = discord.Embed(description = f'{ctx.author.mention}, создан запрос на удаление {amount} сообщений. Продолжить? (y/n)\n||Запрос будет отменён через 10 секунд.||', colour = discord.Color.orange())
        sent = await ctx.send(embed = emb)
        try:
            msg = await client.wait_for('message', timeout = 10, check = lambda message: message.author == ctx.author and message.channel == ctx.channel)
            if msg.content.lower() == 'y':
                await msg.delete()
                await sent.delete()
                if '--silent' not in members:
                    emb = discord.Embed(description = 'Проверяем..', color = discord.Color.orange())
                    sent = await ctx.send(embed = emb)
                    if members == '--bots':
                        if filt == None:
                            await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == True, before = sent)
                        else:
                            await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.author.bot == True, before = sent)
                        emb = discord.Embed(title = 'Результаты удаления сообщений', color = discord.Color.orange())
                        emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{cleared}```')
                        if filt:
                            emb.add_field(name = 'Применён фильтр:', value = f'{filt} ({members})', inline = True)
                        emb.add_field(name = 'Удалены/Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                        emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c".')
                        await sent.edit(embed = emb)
                    elif members == '--users':
                        if filt == None:
                            await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False, before = sent)
                        else:
                            await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False and m.content.lower() == filt.lower(), before = sent)
                        emb = discord.Embed(title = 'Результаты удаления сообщений', color = discord.Color.orange())
                        emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{cleared}```')
                        if filt:
                            emb.add_field(name = 'Применён фильтр:', value = f'{filt} ({members})', inline = True)
                        emb.add_field(name = 'Удалены/Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                        emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c".')
                        await sent.edit(embed = emb)
                    else:
                        if filt == None:
                            await ctx.channel.purge(limit = amount, before = sent)
                        else:
                            await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower(), before = sent)
                        emb = discord.Embed(title = 'Результаты удаления сообщений', color = discord.Color.orange())
                        emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{cleared}```')
                        if filt:
                            emb.add_field(name = 'Применён фильтр:', value = f'{filt} ({members})', inline = True)
                        emb.add_field(name = 'Удалены/Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                        emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c".')
                        await sent.edit(embed = emb)
                    try:
                        if '--silent' in members:
                            return
                        msg = await client.wait_for('message', timeout = 10, check = lambda message: message.channel == ctx.channel and message.author == ctx.author and message.content.lower() == 'c')
                        emb = discord.Embed(title = 'Результаты удаления сообщений', color = discord.Color.orange())
                        emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{cleared}```')
                        if filt:
                            emb.add_field(name = 'Применён фильтр:', value = f'{filt} ({members})', inline = True)
                        else:
                            emb.add_field(name = 'Удалены/Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                        await sent.edit(embed = emb)
                    except asyncio.TimeoutError:
                        await sent.delete()
                else:
                    if '--bots' in members:
                        if filt == None:
                            await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == True)
                        else:
                            await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.author.bot == True)
                    elif '--users' in members:
                        if filt == None:
                            await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False)
                        else:
                            await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False and m.content.lower() == filt.lower())
                    elif '--everyone' in members:
                        if filt == None:
                            await ctx.channel.purge(limit = amount)
                        else:
                            await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower())
                    elif members == '--silent':
                        if filt == None:
                            await ctx.channel.purge(limit = amount)
                        else:
                            await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower())
            elif msg.content.lower() == 'n':
                await msg.delete()
                await sent.delete()
                emb = discord.Embed(description = 'Отменено.', colour = discord.Color.orange())
                await ctx.send(embed = emb, delete_after = 3)
            else:
                await msg.delete()
                await sent.delete()
                emb = discord.Embed(description = f'Обнаружен недопустимый ответ ({msg.content})', colour = discord.Color.orange())
                await ctx.send(embed = emb, delete_after = 3)
        except asyncio.TimeoutError:
            await sent.delete()
            emb = discord.Embed(description = f'{ctx.author.mention}, Время вышло.', colour = discord.Color.orange())
            await ctx.send(embed = emb, delete_after = 3)
    elif amount == 0:
        emb = discord.Embed(description = 'Удалять 0 сообщений? Ты еблан?', colour = discord.Color.orange())
        await ctx.send(embed = emb, delete_after = 1)
    else:
        if '--silent' not in members:
            emb = discord.Embed(description = 'Проверяем..', color = discord.Color.orange())
            sent = await ctx.send(embed = emb)
            if '--bots' in members:
                if filt == None:
                    await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == True, before = sent)
                else:
                    await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.author.bot == True, before = sent)
                emb = discord.Embed(title = 'Результаты удаления сообщений', color = discord.Color.orange())
                emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{cleared}```')
                if filt:
                    emb.add_field(name = 'Применён фильтр:', value = f'{filt} ({members})', inline = True)
                emb.add_field(name = 'Удалены/Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c".')
                await sent.edit(embed = emb)
            elif '--users' in members:
                if filt == None:
                    await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False, before = sent)
                else:
                    await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False and m.content.lower() == filt.lower(), before = sent)
                emb = discord.Embed(title = 'Результаты удаления сообщений', color = discord.Color.orange())
                emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{cleared}```')
                if filt:
                    emb.add_field(name = 'Применён фильтр:', value = f'{filt} ({members})', inline = True)
                emb.add_field(name = 'Удалены/Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c".')
                await sent.edit(embed = emb)
            elif members == '--everyone':
                if filt == None:
                    await ctx.channel.purge(limit = amount, before = sent)
                else:
                    await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower(), before = sent)
                emb = discord.Embed(title = 'Результаты удаления сообщений', color = discord.Color.orange())
                emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{cleared}```')
                if filt:
                    emb.add_field(name = 'Применён фильтр:', value = f'{filt} ({members})', inline = True)
                emb.add_field(name = 'Удалены/Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c".')
                await sent.edit(embed = emb)
            try:
                if '--silent' in members:
                    return
                msg = await client.wait_for('message', timeout = 10, check = lambda message: message.channel == ctx.channel and message.author == ctx.author and message.content.lower() == 'c')
                emb = discord.Embed(title = 'Результаты удаления сообщений', color = discord.Color.orange())
                emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{cleared}```')
                if filt:
                    emb.add_field(name = 'Применён фильтр:', value = f'{filt} ({members})', inline = True)
                else:
                    emb.add_field(name = 'Удалены/Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                await sent.edit(embed = emb)
            except asyncio.TimeoutError:
                await sent.delete()
        else:
            if '--bots' in members:
                if filt == None:
                    await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == True)
                else:
                    await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.author.bot == True)
            elif '--users' in members:
                if filt == None:
                    await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False)
                else:
                    await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False and m.content.lower() == filt.lower())
            elif '--everyone' in members:
                if filt == None:
                    await ctx.channel.purge(limit = amount)
                else:
                    await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower())
            elif members == '--silent':
                if filt == None:
                    await ctx.channel.purge(limit = amount)
                else:
                    await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower())
#Mod

#Misc
@slash.slash(name = 'vote', description = 'Устраивает голосование за какое-либо событие', options = [{'name': 'text', 'description': 'Текст для голосования за. Пишите так, будто слова *голосуем за* уже написаны', 'required': True, 'type': 3}])
async def _vote(ctx, *, text):
    emb = discord.Embed(description = 'ГОЛОСОВАНИЕ', colour = discord.Color.orange())
    emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
    emb.add_field(name = 'Голосуем за:', value = text)
    emb.set_footer(text = '🚫 - воздержусь')
    sent = await ctx.send(embed = emb)
    await sent.add_reaction('👍')
    await sent.add_reaction('👎')
    await sent.add_reaction('🚫')

@slash.slash(name = 'rolemembers', description = 'Показывает участников с определённой ролью', options = [{'name': 'role', 'description': 'Роль для поиска', 'required': True, 'type': 8}])
async def _rolemembers(ctx, role: discord.Role, member: discord.Member = None):
    emb = discord.Embed(colour = discord.Color.orange())
    if len(role.members) != 0:
        emb.add_field(name = f'Участники с ролью {role} ({len(role.members)})', value = ', '.join([member.mention for member in role.members]))
    else:
        if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
            emb.set_footer(text = 'Обнаружено 0 участников с этой ролью. Cephalon Cy by сасиска#2472')
        else:
            emb.set_footer(text = 'Обнаружено 0 участников с этой ролью.')
    await ctx.send(embed = emb)

@slash.slash(name = 'guild', description = 'Показывает информацию о сервере')
async def _guild(ctx):
    guild = ctx.guild
    emb = discord.Embed(colour = discord.Color.orange(), timestamp = datetime.datetime.utcnow())
    emb.set_author(name = guild, icon_url = guild.icon_url)
    emb.add_field(name = 'ID сервера', value = guild.id)
    emb.add_field(name = 'Голосовой регион', value = guild.region)
    emb.add_field(name = 'Владелец', value = guild.owner.mention)
    emb.add_field(name = 'Участников', value = guild.member_count)
    emb.add_field(name = 'Из них ботов', value = len(list(filter(lambda m: m.bot, ctx.guild.members))))
    emb.add_field(name = 'Из них людей', value = len(list(filter(lambda m: not m.bot, ctx.guild.members))))
    emb.add_field(name = 'Каналов', value = f'Текстовых {len(guild.text_channels)} | Голосовых {len(guild.voice_channels)}')
    roles = ', '.join([role.name for role in guild.roles[1:]])
    emb.add_field(name = f'Роли ({len(guild.roles)-1})', value = roles, inline = False)
    now = datetime.datetime.today()
    then = guild.created_at
    delta = now - then
    d = guild.created_at.strftime('%d.%m.%Y %H:%M:%S GMT')
    emb.add_field(name = 'Дата создания сервера', value = f'{delta.days} дней назад. ({d})', inline = False)
    emb.set_thumbnail(url = guild.icon_url)
    await ctx.send(embed = emb)
    
@slash.slash(name = 'roleinfo', description = 'Информация о роли', options = [{'name': 'role', 'description': 'Роль', 'required': True, 'type': 8}])
async def roleinfo(ctx, *, role: discord.Role):
    if role.mentionable == False:
        role.mentionable = 'Нет'
    elif role.mentionable == True:
        role.mentionable = 'Да'
    if role.managed == False:
        role.managed = 'Нет'
    elif role.managed == True:
        role.managed = 'Да'
    if role.hoist == False:
        role.hoist = 'Нет'
    elif role.hoist == True:
        role.hoist = 'Да'
    emb = discord.Embed(title = role.name, colour = role.colour)
    emb.add_field(name = 'ID', value = role.id)
    emb.add_field(name = 'Цвет', value = role.color)
    emb.add_field(name = 'Упоминается?', value = role.mentionable)
    emb.add_field(name = 'Управляется интеграцией?', value = role.managed)
    emb.add_field(name = 'Позиция в списке', value = role.position)
    now = datetime.datetime.today()
    then = role.created_at
    delta = now - then
    d = role.created_at.strftime('%d.%m.%Y %H:%M:%S GMT')
    emb.add_field(name = 'Создана', value = f'{delta.days} дня(ей) назад. ({d})', inline = False)
    emb.add_field(name = 'Показывает участников отдельно?', value = role.hoist)
    await ctx.send(embed = emb)
    
@slash.slash(name = 'avatar', description = 'Выводит аватар участника', options = [{'name': 'member', 'description': 'Пользователь', 'required': False, 'type': 6}])
async def _avatar(ctx, member: discord.Member = None):
    if member == None:
        member = ctx.author
    av = 'png'
    av1 = 'webp'
    av2 = 'jpg'
    emb = discord.Embed(colour = member.color)
    if member.is_avatar_animated() == False:
        emb.add_field(name = '.png', value = f'[Ссылка]({member.avatar_url_as(format = av)})')
        emb.add_field(name = '.webp', value = f'[Ссылка]({member.avatar_url_as(format = av1)})')
        emb.add_field(name = '.jpg', value = f'[Ссылка]({member.avatar_url_as(format = av2)})')
    else:
        emb.set_footer(text = 'по причине того, что аватар анимирован - ссылок на статичные форматы нет.')
    emb.set_image(url = member.avatar_url)
    emb.set_author(name = member)
    await ctx.send(embed = emb)

@slash.slash(name = 'about', description = 'Показывает информацию о участнике', options = [{'name': 'member', 'description': 'Участник', 'required': False, 'type': 6}])
async def _about(ctx, member: discord.Member = None):
    if member == None:
        member = ctx.author
    if member.nick == None:
        member.nick = 'Н/Д'
    if member.bot == False:
        bot = 'Неа'
    elif member.bot == True:
        bot = 'Ага'
    emb = discord.Embed(colour = member.color, timestamp = datetime.datetime.utcnow())
    emb.set_author(name = member)
    emb.add_field(name = 'ID', value = member.id)
    now = datetime.datetime.today()
    then = member.created_at
    delta = now - then
    d = member.created_at.strftime('%d.%m.%Y %H:%M:%S GMT')
    then1 = member.joined_at
    delta1 = now - then1
    d1 = member.joined_at.strftime('%d.%m.%Y %H:%M:%S GMT')
    emb.add_field(name = 'Создан', value = f'{delta.days} дня(ей) назад. ({d})', inline = False)
    emb.add_field(name = 'Вошёл', value = f'{delta1.days} дня(ей) назад. ({d1})', inline = False)
    emb.add_field(name = 'Упоминание', value = member.mention)
    emb.add_field(name = 'Необработанное имя', value = member.name)
    emb.add_field(name = 'Никнейм', value = member.nick)
    if member.status == discord.Status.online:
        status = 'В сети'
    elif member.status == discord.Status.dnd:
        status = 'Не беспокоить'
    elif member.status == discord.Status.idle:
        status = 'Не активен'
    elif member.status == discord.Status.offline:
        status = 'Не в сети'
    emb.add_field(name = 'Статус', value = status)
    roles = ', '.join([role.name for role in member.roles[1:]])
    if member.id == 774273205745483797 or member.id == 764882153812787250 or member.id == 694170281270312991:
        bro = 'Даа'
    if member.id == client.owner_id:
        bro = 'Мой создатель a.k. чмырь'
    else:
        bro = 'Неа'
    emb.add_field(name = 'Бро?', value = bro, inline = False)
    emb.add_field(name = 'Бот?', value = bot)
    limit = len(member.roles)
    if limit != 1:
        emb.add_field(name = f'Роли ({len(member.roles)-1})', value = roles, inline = False)
        emb.add_field(name = 'Высшая Роль', value = member.top_role.mention, inline = False)
    emb.set_thumbnail(url = member.avatar_url)
    await ctx.send(embed = emb)
#Misc

#Fun
@slash.slash(name = "roll", description = 'Ролит случайное число', options = [{'name': 'first', 'description': 'Первое число', 'required': False, 'type': 4}, {'name': 'second', 'description': 'Второе число', 'required': False, 'type': 4}])
async def _roll(ctx, first: int = None, second: int = None):
    if first == None and second == None:
        rand = random.randint(0, 1)
        if rand == '1':
            await ctx.send(f'{ctx.author} выпадает число(0-100)\n`100`')
        else:
            rand1 = random.randint(0, 9)
            rand2 = random.randint(0, 9)
            await ctx.send(f'`{ctx.author} выпадает число(0-100)\n0{rand1}{rand2}`')
    if first != None and second == None:
        rand = random.randint(0, first)
        if first < 10:
            await ctx.send(f'`{ctx.author} выпадает число(0-{first})\n0{rand}`')
        else:
            await ctx.send(f'`{ctx.author} выпадает число(0-{first})\n{rand}`')
    if first != None and second != None:
        if first > second:
            rand = random.randint(first, first)
            await ctx.send(f'`{ctx.author} выпадает число({first}-{first})\n{rand}`')
        rand = random.randint(first, second)
        await ctx.send(f'`{ctx.author} выпадает число({first}-{second})\n{rand}`')

@slash.slash(name = 'dotersbrain', description = 'Полезно для проверки на мозг дотера')
async def dotersbrain(ctx):
    sent1 = await ctx.send(f'{ctx.author.mention}, через 5 секунд появится одно из слов (чё, а, да, нет, ок), на которое вам нужно будет правильно ответить. На размышление 4 секунды.')
    await asyncio.sleep(5)
    words = ['чё', 'а', 'да', 'нет', 'ок']
    rand = random.choice(words)
    sent = await ctx.send(rand)
    try:
        msg = await client.wait_for('message', timeout = 4, check = lambda message: message.author == ctx.author and message.channel == ctx.message.channel)
        if msg.content.lower() == 'хуй через плечо' and sent.content == 'чё':
            await ctx.send(f'Поздравляю, у вас 3 стадия рака!')
            await sent1.delete()
            await sent.delete()
        elif sent.content == 'а' and msg.content.lower() == 'хуй на':
            await ctx.send(f'Поздравляю, у вас 3 стадия рака!')
            await sent1.delete()
            await sent.delete()
        elif sent.content == 'да' and msg.content.lower() == 'пизда':
            await ctx.send(f'Поздравляю, у вас 3 стадия рака!')
            await sent1.delete()
            await sent.delete()
        elif sent.content == 'нет' and msg.content.lower() == 'пидора ответ':
            await ctx.send(f'Поздравляю, у вас 3 стадия рака!')
            await sent1.delete()
            await sent.delete()
        elif sent.content == 'ок' and msg.content.lower() == 'хуй намок':
            await ctx.send(f'Поздравляю, у вас 3 стадия рака!')
            await sent1.delete()
            await sent.delete()
        else:
            await ctx.send('Вы совершенно здоровый человек! ||попробуйте cy/help dotersbrain||')
            await sent1.delete()
            await sent.delete()
    except asyncio.TimeoutError:
        await ctx.send(f'{ctx.author.mention}, Слишком медленно.')
        await sent1.delete()
        await sent.delete()

@slash.slash(name = 'niggers', description = 'Осуждаем!')
async def _niggers(ctx):
    rlocale = collection.find_one({"_id": ctx.author.id})["locale"]
    if rlocale == 'ru':
        emb = discord.Embed(description = '[осуждающее видео](https://www.youtube.com/watch?v=167apVK8Suw)', colour = discord.Color.orange())
        if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
            emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb)
    if rlocale == 'gnida':
        emb = discord.Embed(description = '[негры пидарасы, и извинятся за это не буду!](https://www.youtube.com/watch?v=167apVK8Suw)', colour = discord.Color.orange())
        if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
            emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb)

@slash.slash(name = 'ayebalbec', description = 'Я не ангел и не бес, просто..')
async def balbec(ctx):
    emb = discord.Embed(colour = ctx.author.color)
    emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
    emb.set_image(url = 'https://sun9-61.userapi.com/tja5cuQthduwgxq2yMigLiUxfYq_5fqiA6cJWg/sZOkbPajoSY.jpg')
    await ctx.send(embed = emb)

@slash.slash(name = 'rp', description = 'Ультимативный гайд по рп отыгровке')
async def _rp(ctx):
    emb = discord.Embed(description = '[Ныа](https://www.youtube.com/watch?v=idmTSW9mfYI)', colour = discord.Color.orange())
    await ctx.send(embed = emb)

@slash.slash(name = 'rap', description = '.rap')
async def _rap(ctx):
    emb = discord.Embed(colour = ctx.author.color)
    emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
    emb.set_image(url = 'https://thumbs.gfycat.com/MessyCarefreeHousefly-size_restricted.gif')
    await ctx.send(embed = emb)

@slash.slash(name = 'zatka', description = 'Форма заявки для Набор кадров')
async def _zatka(ctx):
    emb = discord.Embed(title = 'Форма заявки для Набор кадров', colour = ctx.author.color)
    emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
    emb.add_field(name = '(1). ZATKA в STEAM.  ZATKA_KING#8406 в Discord.', value = 'возраст 14+  часовой пояс IL +0.', inline = False)
    emb.add_field(name = '(2). Интересующая управление:', value = 'Discord', inline = False)
    emb.add_field(name = '(3). Опыт администрирования:', value = 'Есть.', inline = False)
    emb.add_field(name = 'творческие:', value = 'Есть.', inline = False)
    emb.add_field(name = 'технические навыки:', value = 'Нет.', inline = False)
    emb.add_field(name = '(4). Сколько часов готовы уделять работе', value = '[ 15+ в неделю ]', inline = False)
    emb.add_field(name = 'в какое время дня свободны', value = '16:00 до 22:00+', inline = False)
    await ctx.send(embed = emb)

@slash.slash(name = 'cu', description = 'Медь')
async def _cu(ctx):
    await ctx.send('Медь')

@slash.slash(name = 'coinflip', description = 'Подкидывает монетку')
async def _coinflip(ctx):
    emb = discord.Embed(description = 'Орёл!', colour = discord.Color.orange())
    emb.set_image(url = 'https://cdn.discordapp.com/attachments/524213591084105729/763835275930632252/-removebg-preview.png')
    emb1 = discord.Embed(description = 'Решка!', colour = discord.Color.orange())
    emb1.set_image(url = 'https://cdn.discordapp.com/attachments/524213591084105729/763837699240099890/-removebg-preview.png')
    choices = [emb, emb1]
    rancoin = random.choice(choices)
    await ctx.send(embed = rancoin)
#Fun

#Embeds
@slash.slash(name = 'content', description = 'Позволяет получить необработанный контент сообщения, в том числе и эмбедов', options = [{'name': 'arg', 'description': 'ID сообщения', 'required': True, 'type': 3}, {'name': 'channel', 'description': 'Канал, из которого нужно достать сообщение', 'required': False, 'type': 7}])
async def _content(ctx, arg, channel: discord.TextChannel = None):
    if channel == None:
        channel = ctx.channel
    message = await channel.fetch_message(id = arg)
    for emb in message.embeds:
        if emb.color != emb.Empty:
            color = f' color {emb.color}'
        else:
            color = ''
        if emb.author.name != emb.Empty:
            author = f' author {emb.author.name}'
        else:
            author = ''
        if message.content == '':
            content = ''
        else:
            content = f'content {message.content}'
        if emb.image.url != emb.Empty:
            img = f' | img& {emb.image.url}'
            image = f' image {emb.image.url}'
        else:
            img = ''
            image = ''
        if emb.thumbnail.url != emb.Empty:
            th = f' | th& {emb.thumbnail.url}'
            thumb = f' thumbnail {emb.thumbnail.url}'
        else:
            th = ''
            thumb = ''
        if emb.description != emb.Empty:
            d = f' | d& {emb.description}'
            description = f' description {emb.description}'
        else:
            d = ''
            description = ''
        if emb.title != emb.Empty:
            t = f't& {emb.title}'
            title = f' title {emb.title}'
        else:
            t = ''
            title = ''
        if emb.footer.text != emb.Empty:
            f = f' | f& {emb.footer.text}'
            footer = f' footer {emb.footer.text}'
        else:
            f = ''
            footer = ''
    if message.author.id in botversions:
        if message.embeds == []:
            await ctx.send(f'```cy/say {message.content}```')
        else:
            await ctx.send(f'```cy/say {t}{d}{f}{th}{img}```')
    else:
        if message.embeds == []:
            if '```' in message.content:
                await ctx.send(f'@{message.author} {message.content}')
            else:
                await ctx.send(f'```@{message.author} {message.content}```')
        else:
            await ctx.send(f'```{content}{title}{description}{footer}{color}{author}{image}{thumb}```')

@slash.slash(name = 'say', description = 'Пишет от лица бота сообщение и/или эмбед. Используйте cy/help say для подробностей использования.', options = [{'name': 'msg', 'description': 'Аргументы/текст для написания', 'required': True, 'type': 3}])
async def _say(ctx, *, msg):
    title = ''
    description = ''
    image = thumbnail = message = footer = None
    embed_values = msg.split('|')
    for i in embed_values:
        if i.strip().lower().startswith('t&'):
            title = i.strip()[2:].strip()
        elif i.strip().lower().startswith('d&'):
            description = i.strip()[2:].strip()
        elif i.strip().lower().startswith('img&'):
            image = i.strip()[4:].strip()
        elif i.strip().lower().startswith('th&'):
            thumbnail = i.strip()[3:].strip()
        elif i.strip().lower().startswith('msg&'):
            message = i.strip()[4:].strip()
        elif i.strip().lower().startswith('f&'):
            footer = i.strip()[2:].strip()
    emb = discord.Embed(title = title, description = description, color = 0x2f3136)
    for i in embed_values:
        emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
        if image:
            emb.set_image(url = image)
        if thumbnail:
            emb.set_thumbnail(url = thumbnail)
        if footer:
            emb.set_footer(text = footer)
        if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
            emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        if 't&' not in msg and 'd&' not in msg and 'img&' not in msg and 'th&' not in msg and 'msg&' not in msg and 'f&' not in msg:
            return await ctx.send(msg)
        else:
            if message:
                return await ctx.send(f'{message}', embed = emb)
            else:
                return await ctx.send(embed = emb)

@slash.slash(name = 'edit', description = 'Изменяет сообщение, отправленое ботом.', options = [{'name': 'arg', 'description': 'ID сообщения', 'required': True, 'type': 3}, {'name': 'msg', 'description': 'аргументы или текст, на который нужно заменить исходный', 'required': True, 'type': 3}])
@commands.has_permissions(manage_channels = True)
async def _edit(ctx, arg, *, msg):
    message = await ctx.fetch_message(id = arg)
    if message != None:
        old_embed = message.embeds[0]
        title = old_embed.title
        description = old_embed.description
        image = thumbnail = footer = None
        embed_values = msg.split('|')
        for i in embed_values:
            if i.strip().lower().startswith('t&'):
                title = i.strip()[2:].strip()
            elif i.strip().lower().startswith('d&'):
                description = i.strip()[2:].strip()
            elif i.strip().lower().startswith('img&'):
                image = i.strip()[4:].strip()
            elif i.strip().lower().startswith('th&'):
                thumbnail = i.strip()[3:].strip()
            elif i.strip().lower().startswith('f&'):
                footer = i.strip()[2:].strip()
        emb = discord.Embed(title = title, description = description, color = 0x2f3136, timestamp = ctx.message.created_at)
        for i in embed_values:
            emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            if image:
                emb.set_image(url = image)
            if thumbnail:
                emb.set_thumbnail(url = thumbnail)
            if footer:
                emb.set_footer(text = footer)
            if 't&' not in msg and 'd&' not in msg and 'img&' not in msg and 'th&' not in msg and 'f&' not in msg:
                if message.author == client.user:
                    if '--clean' in msg:
                        return await message.edit(content = None)
                    if '--delete' in msg:
                        return await message.delete()
                    if '--noembed' in msg:
                        if message.embeds != []:
                            return await message.edit(embed = None)
                        else:
                            return await ctx.send(f'{ctx.author.mention}, нечего удалять. Возможно, вы имели ввиду cy/edit {message.id} --delete ?')
                    if '--empty-embed' in msg:
                        if message.embeds != []:
                            emb = discord.Embed(title = None, description = None, color = 0x2f3136)
                            emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                            return await message.edit(embed = emb)
                        else:
                            return await ctx.send(f'{ctx.author.mention}, нечего очищать. Возможно, вы имели ввиду cy/edit {message.id} --delete ?')
                    else:
                        return await message.edit(content = msg)
                else:
                    return await ctx.send(f'{message.id} не является сообщением от {client.user}')
            else:
                if message.author == client.user:
                    if '--clean' in msg:
                        return await message.edit(content = None, embed = emb)
                    if '--noembed' in msg:
                        if message.embeds != []:
                            return await message.edit(embed = None)
                        else:
                            return await ctx.send(f'{ctx.author.mention}, нечего удалять. Возможно, вы имели ввиду cy/edit {message.id} --delete ?')
                    else:
                        return await message.edit(embed = emb)
                else:
                    return await ctx.send(f'{message.id} не является сообщением от {client.user}')
    else:
        return await ctx.send(f'сообщение {message.id} не обнаружено.')
#Embeds

#Cephalon
@client.command() #ru, gnida
async def locale(ctx, locale = None):
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
        
@client.command()
async def locale_test(ctx):
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
        
@client.command()
async def setup(ctx):
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

@client.command()
async def generate(ctx):
    token = ''.join([secrets.choice('QWERTYUIOPASDFGHJKLZXCVBNM1234567890') for i in range(4)])
    token1 = ''.join([secrets.choice('QWERTYUIOPASDFGHJKLZXCVBNM1234567890') for i in range(4)])
    token2 = ''.join([secrets.choice('QWERTYUIOPASDFGHJKLZXCVBNM1234567890') for i in range(4)])
    await ctx.send(f'```{token}-{token1}-{token2}```')

@slash.slash(name = 'ping', description = 'Отображение задержки клиента бота. Нормальная задержка в диапазоне от 90 до 130 миллисекунд.')
async def _ping(ctx):
    emb = discord.Embed(description = f'`fetching..`', colour = discord.Color.orange())
    emb1 = discord.Embed(description = f'Pong!  `{round(client.latency * 1000)} ms`', colour = discord.Color.orange())
    if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
        emb1.set_footer(text = 'Cephalon Cy by сасиска#2472')
    message = await ctx.send(embed = emb)
    await asyncio.sleep(client.latency)
    await message.edit(embed = emb1)

@slash.slash(name = 'invite', description = 'Для приглашения бота на сервер')
async def _invite(ctx):
    emb = discord.Embed(description = '[Ссылка](https://discord.com/api/oauth2/authorize?client_id=694170281270312991&permissions=8&scope=bot%20applications.commands) для приглашения Cy на сервера.', colour = discord.Color.orange())
    if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
    await ctx.send(embed = emb)

@slash.slash(name = 'info', description = 'Информация о боте')
async def _info(ctx):
    emb = discord.Embed(colour = discord.Color.orange())
    emb.set_author(name = client.user.name, url = 'https://warframe.fandom.com/wiki/Cephalon_Cy', icon_url = client.user.avatar_url)
    emb.add_field(name = 'Версия', value = '0.12.10.2.11856')
    emb.add_field(name = 'Написан на', value = 'discord.py v1.7.2 при помощи\ndiscord-py-slash-command v1.1.0')
    emb.add_field(name = 'Разработчик', value = '[сасиска#2472](https://discord.com/users/338714886001524737)')
    if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
        emb.add_field(name = 'Сервер', value = 'Данный сервер не принадлежит моему Создателю или его знакомым. Все эмбед выводы будут иметь футер с текстом `Cephalon Cy by сасиска#2472`')
    if ctx.guild.id == 693929822543675455:
        emb.add_field(name = 'Принадлежность', value = 'Это - мой основной сервер.')
    if ctx.guild.id == 735874149578440855:
        emb.add_field(name = 'Тестирование', value = 'Это - мой тестовый сервер.')
    emb.add_field(name = 'Раздражаю', value = f'{len(client.users)} человек')
    emb.add_field(name = 'Существую на', value = f'{len(client.guilds)} серверах')
    if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
        emb.set_footer(text = 'Данное приложение не имеет никакого причастия к игре Warframe. Cephalon Cy by сасиска#2472', icon_url = 'https://i.playground.ru/p/yVaOZNSTdgUTxmzy_qvzzQ.png')
    else:
        emb.set_footer(text = 'Данное приложение не имеет никакого причастия к игре Warframe.', icon_url = 'https://i.playground.ru/p/yVaOZNSTdgUTxmzy_qvzzQ.png')
    await ctx.send(embed = emb)

@slash.slash(name = 'botver', description = 'Позволяет узнать текущую версию бота', options = [{'name': 'version', 'description': 'Версия', 'required': False, 'type': 3, 'choices': [
    {'name': '0.12.9.10519', 'value': '0.12.9.10519'}, 
    {'name': '0.12.9.10988', 'value': '0.12.9.10988'}, 
    {'name': '0.12.9.11410', 'value': '0.12.9.11410'},
    {'name': '0.12.10.1.11661', 'value': '0.12.10.1.11661'},
    {'name': '0.12.10.2.11856', 'value': '0.12.10.2.11856'},
    {'name': '0.12.10.2.12528', 'value': '0.12.10.2.12528'}]}])
async def _botver(ctx, version = None):
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
    
@slash.slash(name = 'help', description = 'Здесь можно получить полную помощь по всем командам', options = [{'name': 'arg', 'description': 'Выберите команду для подробной помощи', 'required': False, 'type': 3, 'choices': [
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
    {'name': 'mute', 'value': 'mute'},
    {'name': 'remind', 'value': 'remind'},
    {'name': 'roleinfo', 'value': 'roleinfo'},
    {'name': 'take', 'value': 'take'},
    {'name': 'unmute', 'value': 'unmute'},
    {'name': 'vote', 'value': 'vote'},
    {'name': 'help', 'value': 'help'},
    {'name': 'Embeds', 'value': 'embeds'},
    {'name': 'Cephalon', 'value': 'cephalon'},
    {'name': 'Mod', 'value': 'mod'},
    {'name': 'Misc', 'value': 'misc'},
    {'name': 'All', 'value': 'all'},
    {'name': 'roll', 'value': 'roll'}
    ]
    }])
async def _help(ctx, arg = None):
    if arg == None:
        emb = discord.Embed(description = f'Вот команды, что я могу исполнить.', colour = discord.Color.orange())
        emb.set_author(name = client.user.name, url = 'https://discord.com/api/oauth2/authorize?client_id=694170281270312991&permissions=8&scope=bot%20applications.commands')
        emb.add_field(name = 'Cephalon', value = '`botver`, `info`, `invite`, `join`, `leave`, `ping`', inline = False)
        emb.add_field(name = 'Embeds', value = '`content`, `edit`, `say`', inline = False)
        if not (ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends):
            emb.add_field(name = 'Fun', value = '`aye_balbec`, `cu`, `coinflip`, `dotersbrain`, `rp`, `rap`, `zatka`', inline = False)
        emb.add_field(name = 'Mod', value = '`ban`, `clear`, `dm`, `give`, `kick`, `mute`, `take`, `unmute`', inline = False)
        emb.add_field(name = 'Misc', value = '`about`, `avatar`, `guild`, `remind`, `roleinfo`, `rolemembers`, `someone`, `vote`', inline = False)
        emb.add_field(name = 'ᅠ', value = 'Назовите войс `Создать канал`, чтобы бот автоматически создавал для вас временные каналы, которые будут удаляться после того, как все люди выйдут из него.')
        emb.add_field(name = 'ᅠ', value = '**Используйте** `cy/help [команда/категория]` **для подробностей использования.**\n\n[Ссылка-приглашение](https://discord.com/api/oauth2/authorize?client_id=694170281270312991&permissions=8&scope=bot%20applications.commands)', inline = False)
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb)
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
        await ctx.send('```apache\ncy/ban <@пинг/имя/ID> [причина/--soft --reason]\ncy/ban 185476724627210241 --soft --reason лошара\ncy/ban @сасиска чмо\ncy/ban "Sgt.White"\n\nПри использовании --soft обязательно указывать --reason после него, однако можно не использовать --reason\n\n([] - опционально, <> - обязательно, / - или)\nperms = ban_members```')
    elif arg == 'content':
        await ctx.send('```apache\ncy/content <ID> (<> - обязательно)```')
    elif arg == 'clear':
        await ctx.send('```apache\ncy/clear <количество> [автор] [фильтр]\ncy/clear 100\ncy/clear 10 @сасиска\ncy/clear 50 --everyone хыха\ncy/clear 30 --bots\ncy/clear 15 --users\n\n--everyone удалит сообщения от всех\n--bots удалит сообщения только от ботов\n--users удалит сообщения только от участников\n\nПри указании автора не будет удалено столько сообщений, сколько было указано, будет удалено столько, сколько будет найдено в пределах этих сообщений.\nСообщения старше 2 недель будут удалены не сразу - лимит discord API\nПри удалении более 100 сообщений нужно подтверждение владельца сервера.\nТолько владелец может удалять от 250 сообщений за раз.\nНе более 300!\n([] - опционально, <> - обязательно, / - или)\nperms = adminstrator```')
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
        await ctx.send('```apache\ncy/mute <@пинг/имя/ID> <время(s/m/h/d(15s, 5m, 1h, 5d))> [причина] ([] - опционально, <> - обязательно, / - или)\nperms = manage_channels```')
    elif arg == 'remind':
        await ctx.send('```apache\ncy/remind <время(s/m/h/d(15s, 5m, 1h, 5d))> <текст> (<> - обязательно, / - или)```')
    elif arg == 'roleinfo':
        await ctx.send('```apache\ncy/roleinfo <@роль/имя роли/ID роли> (<> - обязательно, / - или)```')
    elif arg == 'take':
        await ctx.send('```apache\ncy/take <@пинг/имя/ID> <@роль/имя роли/ID роли> (<> - обязательно, / - или)\nperms = view_audit_log```')
    elif arg == 'someone':
        await ctx.send('```apache\ncy/someone <текст> (<> - обязательно)```')
    elif arg == 'unmute':
        await ctx.send('```apache\ncy/unmute <@пинг/имя/ID> [причина] ([] - опционально, <> - обязательно, / - или)\nperms = manage_channels```')
    elif arg == 'vote':
        await ctx.send('```apache\ncy/vote <текст> (<> - обязательно)```')
    elif arg == 'help':
        await ctx.send('```apache\ncy/help [команда] ([] - опционально)```')
    elif arg == 'Embeds' or arg == 'embeds':
        await ctx.send('```ARM\ncontent(ctx) - позволяет увидеть необработанный контент сообщения\nedit - редактирует сообщение, отправленное от лица бота. Иные сообщения редактировать нельзя.\nsay - используется для написания как текстов, так и эмбедов.```')
    elif arg == 'Cephalon' or arg == 'cephalon':
        await ctx.send('```ARM\ninfo - информация о боте\ninvite - ссылка-приглашения бота\njoin - бот зайдёт в ваш голосовой канал\nleave - бот из него выйдет\nping - проверяет задержку клиента бота.```')
    elif arg == 'Fun' or arg == 'fun':
        await ctx.send('```ARM\naye_balbec - я не ангел и не бес, просто..\ncu - медь\ncoinflip(c, coin) - подкидывает монетку\ndotersbrain - проверка на мозг дотера\nniggers - осуждаем!\nrp - ультимативный гайд по рп отыгровке\nrap - .rap\nzatka - Форма заявки для набор кадров```')
    elif arg == 'Mod' or arg == 'mod':
        await ctx.send('```ARM\nban - бан участника\nclear - очистка чата, не более 300!\ndm - пишет в лс участнику написанный текст\ngive - выдаёт роль\nkick - кик участника\nmute - заглушение участника\ntake - забирает роль\nunmute - снятие заглушения участника.```')
    elif arg == 'Misc' or arg == 'misc':
        await ctx.send('```ARM\nabout - информация о человеке\navatar - аватар человека\nguild - информация о сервере\nremind - напоминание о событии\nroleinfo - информация о роли\nrolemembers - участники роли\nsomeone - упоминание someone\nvote - голосование за что-то.```')
    elif arg == 'All' or arg == 'all':
        await ctx.send('```ARM\ninfo - информация о боте\ninvite - ссылка-приглашения бота\njoin - бот зайдёт в ваш голосовой канал\nleave - бот из него выйдет\nping - проверяет задержку клиента бота.```')
        await ctx.send('```ARM\ncontent(ctx) - позволяет увидеть необработанный контент сообщения\nedit - редактирует сообщение, отправленное от лица бота. Иные сообщения редактировать нельзя.\nsay - используется для написания как текстов, так и эмбедов.```')
        await ctx.send('```ARM\naye_balbec - я не ангел и не бес, просто..\ncu - медь\ncoinflip(c, coin) - подкидывает монетку\ndotersbrain - проверка на мозг дотера\nniggers - осуждаем!\nrp - ультимативный гайд по рп отыгровке\nrap - .rap\nzatka - Форма заявки для набор кадров```')
        await ctx.send('```ARM\nban - бан участника\nclear - очистка чата, не более 300!\ndm - пишет в лс участнику написанный текст\ngive - выдаёт роль\nkick - кик участника\nmute - заглушение участника\ntake - забирает роль\nunmute - снятие заглушения участника.```')
        await ctx.send('```ARM\nabout - информация о человеке\navatar - аватар человека\nguild - информация о сервере\nremind - напоминание о событии\nroleinfo - информация о роли\nrolemembers - участники роли\nsomeone - упоминание someone\nvote - голосование за что-то.```')
    
@client.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def help(ctx, arg = None):
    if arg == None:
        emb = discord.Embed(description = f'Вот команды, что я могу исполнить.', colour = discord.Color.orange())
        emb.set_author(name = client.user.name, url = 'https://discord.com/api/oauth2/authorize?client_id=694170281270312991&permissions=8&scope=bot%20applications.commands')
        emb.add_field(name = 'Cephalon', value = '`botver`, `info`, `invite`, `join`, `leave`, `ping`, `setup`', inline = False)
        emb.add_field(name = 'Embeds', value = '`content`, `edit`, `say`', inline = False)
        emb.add_field(name = 'Fun', value = '`aye_balbec`, `cu`, `coinflip`, `dotersbrain`, `rp`, `rap`, `roll`, `zatka`', inline = False)
        emb.add_field(name = 'Mod', value = '`ban`, `clear`, `dm`, `give`, `kick`, `mute`, `take`, `unmute`', inline = False)
        emb.add_field(name = 'Misc', value = '`about`, `avatar`, `guild`, `remind`, `roleinfo`, `rolemembers`, `someone`, `vote`', inline = False)
        emb.add_field(name = 'ᅠ', value = 'Назовите войс `Создать канал`, чтобы бот автоматически создавал для вас временные каналы, которые будут удаляться после того, как все люди выйдут из него.', inline = False)
        emb.add_field(name = 'ᅠ', value = '**Используйте** `cy/help [команда/категория]` **для подробностей использования.**\n\n[Ссылка-приглашение](https://discord.com/api/oauth2/authorize?client_id=694170281270312991&permissions=8&scope=bot%20applications.commands)', inline = False)
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb)
    elif arg == 'locale':
        await ctx.send('```apache\nlocale [ru/gnida]\n([] - опционально)```')
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

@client.event
async def on_command_error(ctx, error):
    channel = client.get_channel(838506478108803112)
    if isinstance(error, commands.CommandNotFound):
        emb = discord.Embed(description = f'{ctx.author.mention}, команда не обнаружена. Может, пропишите cy/help?', colour = discord.Color.orange())
        await ctx.send(embed = emb)
        eemb = discord.Embed(description = 'Поймана ошибка `CommandNotFound`', color = 0xff0000, timestamp = ctx.message.created_at)
        eemb.add_field(name = 'Сервер', value = ctx.guild.name)
        eemb.add_field(name = 'Вызвавший ошибку', value = f'{ctx.author.mention} ({ctx.author.name})', inline = False)
        eemb.add_field(name = 'Команда', value = ctx.command.name, inline = False)
        await channel.send(embed = eemb)
    elif isinstance(error, commands.MissingPermissions):
        emb = discord.Embed(description = f'{ctx.author.mention}, у вас недостаточно прав на выполнение команды `{ctx.command.name}`', colour = discord.Color.orange())
        await ctx.send(embed = emb)
        eemb = discord.Embed(description = 'Поймана ошибка `MissingPermissions`', color = 0xff0000, timestamp = ctx.message.created_at)
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
            emb = discord.Embed(description = f'{rand} Команда `{ctx.command.name}` будет доступна через {round(s)} секунд..', colour = discord.Color.orange())
            await ctx.send(embed = emb)
        elif round(s) >= 2:
            emb = discord.Embed(description = f'{rand1} Команда `{ctx.command.name}` будет доступна через {round(s)} секунды.', colour = discord.Color.orange())
            await ctx.send(embed = emb)
        elif round(s) >= 1:
            emb = discord.Embed(description = f'{rand2} Команда `{ctx.command.name}` будет доступна через {round(s)} секунду!', colour = discord.Color.orange())
            await ctx.send(embed = emb)
        elif round(s) <= 0:
            emb = discord.Embed(description = 'Ебать ты тайминг поймал конечно ||До перезарядки команды оставалось чуть больше, чем 0 секунд||', colour = discord.Color.orange())
            await ctx.send(embed = emb)
        eemb = discord.Embed(description = 'Поймана ошибка `CommandOnCooldown`', color = 0xff0000, timestamp = ctx.message.created_at)
        eemb.add_field(name = 'Сервер', value = ctx.guild.name)
        eemb.add_field(name = 'Вызвавший ошибку', value = f'{ctx.author.mention} ({ctx.author.name})', inline = False)
        eemb.add_field(name = 'Команда', value = ctx.command.name, inline = False)
        eemb.add_field(name = 'Оставалось времени', value = round(s), inline = False)
        await channel.send(embed = eemb)
    elif isinstance(error, commands.MissingRequiredArgument):
        revert_cooldown(ctx.command, ctx.message)
        if ctx.command.name == 'clear':
            await ctx.send('```apache\ncy/clear <количество> [автор] [фильтр]\ncy/clear 100\ncy/clear 10 @сасиска\ncy/clear 50 --everyone хыха\ncy/clear 30 --bots\ncy/clear 15 --users\ncy/clear 5 --silent\ncy/clear 200 "--silent --everyone" хыха\n\n--everyone удалит сообщения от всех\n--bots удалит сообщения только от ботов\n--users удалит сообщения только от участников\n--silent не оставит доказательств выполнения команды, исключение - количество >= 10\n\nПри указании автора не будет удалено столько сообщений, сколько было указано, будет удалено столько, сколько будет найдено в пределах этих сообщений.\nСообщения старше 2 недель будут удалены не сразу - лимит discord API\nПри удалении более 100 сообщений нужно подтверждение владельца сервера.\nТолько владелец может удалять от 250 сообщений за раз.\nНе более 300!\n([] - опционально, <> - обязательно, / - или)\nperms = adminstrator```')
        elif ctx.command.name == 'say':
            await ctx.send('```apache\ncy/say [обычный текст] [t& title текст] | [d& description текст] | [th& ссылка на картинку справа] | [img& ссылка на картинку снизу] [f& footer текст] [msg& сообщение над эмбедом]\ncy/say t& title | d& description\ncy/say --everyone | t& title | d& description\ncy/say [текст]\ncy/say --everyone [текст]\n(вам НЕ обязательно писать все аргументы в данном порядке, пишите только те, что вам нужны в любом порядке) ([] - опционально)```')
        elif ctx.command.name == 'edit':
            await ctx.send('```apache\ncy/edit <ID> [обычный текст] [t& title текст] | [d& description текст] | [th& ссылка на картинку справа] | [img& ссылка на картинку снизу]\ncy/edit <ID> [текст]\ncy/edit <ID> --clean | d& description\ncy/edit <ID> --clean\ncy/edit <ID> --noembed\ncy/edit <ID> --empty-embed\ncy/edit <ID> --delete\n--clean удалит контент над эмбедом, --noembed удалит эмбед, работает только если есть эмбед, --empty-embed опустошит эмбед, --delete удалит сообщение\nесли у сообщения есть эмбед и в команде нет агрументов, автоматически будет заменён msg&\n([] - опционально, <> - обязательно)\nperms = manage_channels```')
        elif ctx.command.name == 'ban':
            await ctx.send('```apache\ncy/ban <@пинг/имя/ID> [причина/--soft --reason]\ncy/ban 185476724627210241 --soft --reason лошара\ncy/ban @сасиска чмо\ncy/ban "Sgt White"\ncy/ban @крипочек --soft\n\nПри использовании --soft обязательно указывать --reason ПОСЛЕ --soft\n\n([] - опционально, <> - обязательно, / - или)\nperms = ban_members```')
        else:
            emb = discord.Embed(description = f'{ctx.author.mention}, обнаружен недостаток аргументов для `{ctx.command.name}`. Попробуйте cy/help `{ctx.command.name}`', colour = discord.Color.orange())
            emb.set_footer(text = 'Задержка команды сброшена, так как была вызвана ошибка при вводе пользователя')
            await ctx.send(embed = emb)
        eemb = discord.Embed(description = 'Поймана ошибка `MissingRequiredArgument`', color = 0xff0000, timestamp = ctx.message.created_at)
        eemb.add_field(name = 'Сервер', value = ctx.guild.name)
        eemb.add_field(name = 'Вызвавший ошибку', value = f'{ctx.author.mention} ({ctx.author.name})', inline = False)
        eemb.add_field(name = 'Команда', value = ctx.command.name, inline = False)
        await channel.send(embed = eemb)
    elif isinstance(error, commands.MemberNotFound):
        revert_cooldown(ctx.command, ctx.message)
        emb = discord.Embed(description = f'{ctx.author.mention}, участник не обнаружен.', color = discord.Color.orange())
        emb.set_footer(text = 'Задержка команды сброшена, так как была вызвана ошибка при вводе пользователя')
        await ctx.send(embed = emb)
        eemb = discord.Embed(description = 'Поймана ошибка `MemberNotFound`', color = 0xff0000, timestamp = ctx.message.created_at)
        eemb.add_field(name = 'Сервер', value = ctx.guild.name)
        eemb.add_field(name = 'Вызвавший ошибку', value = f'{ctx.author.mention} ({ctx.author.name})', inline = False)
        eemb.add_field(name = 'Команда', value = ctx.command.name, inline = False)
        await channel.send(embed = eemb)
    elif isinstance(error, commands.BadArgument):
        revert_cooldown(ctx.command, ctx.message)
        emb = discord.Embed(description = f'{ctx.author.mention}, обнаружен неверный аргумент для `{ctx.command.name}`. Попробуйте cy/help `{ctx.command.name}`', colour = discord.Color.orange())
        emb.set_footer(text = 'Задержка команды сброшена, так как была вызвана ошибка при вводе пользователя')
        await ctx.send(embed = emb)
        eemb = discord.Embed(description = 'Поймана ошибка `BadArgument`', color = 0xff0000, timestamp = ctx.message.created_at)
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
