# coding=utf-8
import asyncio
import datetime
import json
import os
import random
import re
import secrets

import discord
import discord_slash
from discord.ext import commands
from discord.utils import get
from discord_slash import SlashCommand, SlashContext

client = commands.Bot(command_prefix = commands.when_mentioned_or('cy/'), intents = discord.Intents.all(), owner_id = 338714886001524737)
client.remove_command('help')

@client.event
async def on_ready():
    await client.change_presence(status = discord.Status.idle, activity = discord.Activity(type = discord.ActivityType.watching, name = 'Slash Commands'))

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

class Slapper(commands.Converter):
    async def convert(self, ctx, argument):
        mention = random.choice(ctx.guild.members)
        emb = discord.Embed(description = f'{argument}', colour =  ctx.author.colour, timestamp = ctx.message.created_at)
        emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
        if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
            emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        return await ctx.send(f'@someone ||{mention.mention}||', embed = emb)

#Events
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
async def on_guild_channel_delete(channel):
    if channel.guild.id == 693929822543675455:
        lchannel = client.get_channel(714175791033876490)
        emb = discord.Embed(title = 'УДАЛЕНИЕ_КАНАЛА', color = discord.Color.orange(), timestamp = datetime.datetime.utcnow()) # CHANNEL_DELETED
        emb.add_field(name = 'НАЗВАНИЕ', value = channel.name) # NAME
        if channel.type == discord.ChannelType.voice:
            typ = 'ГОЛОСОВОЙ' # VOICE
        if channel.type == discord.ChannelType.text:
            typ = 'ТЕКСТОВЫЙ' # TEXT
        emb.add_field(name = 'ТИП', value = typ) # TYPE
        emb.set_footer(text = f'ID: {channel.id}')
        await lchannel.send(embed = emb)

@client.event
async def on_guild_channel_create(channel):
    if channel.guild.id == 693929822543675455:
        lchannel = client.get_channel(714175791033876490)
        emb = discord.Embed(title = 'СОЗДАНИЕ_КАНАЛА', color = discord.Color.orange(), timestamp = datetime.datetime.utcnow()) # CHANNEL_CREATED
        emb.add_field(name = 'НАЗВАНИЕ', value = channel.name) # NAME
        if channel.type == discord.ChannelType.voice:
            typ = 'ГОЛОСОВОЙ' # VOICE
        if channel.type == discord.ChannelType.text:
            typ = 'ТЕКСТОВЫЙ' # TEXT
        emb.add_field(name = 'ТИП', value = typ) # TYPE
        emb.set_footer(text = f'ID: {channel.id}')
        await lchannel.send(embed = emb)

@client.event
async def on_guild_channel_update(before, after):
    channel = client.get_channel(714175791033876490)
    if before.guild.id == 693929822543675455:
        if before.type == discord.ChannelType.voice:
            emb = discord.Embed(title = r'ИЗМЕНЕНИЕ\_ГОЛОСОВОГО_КАНАЛА', color = discord.Color.orange(), timestamp = datetime.datetime.utcnow()) # VOICE_CHANNEL_EDITED
            if before.name != after.name:
                emb.add_field(name = 'НАЗВАНИЕ_ДО', value = before.name) # NAME_BEFORE
                emb.add_field(name = 'НАЗВАНИЕ_ПОСЛЕ', value = after.name) # NAME_AFTER
                emb.set_footer(text = f'ID: {before.id}')
                await channel.send(embed = emb)
            if before.position != after.position:
                emb.add_field(name = 'НАЗВАНИЕ', value = before.name, inline = False) # NAME
                emb.add_field(name = 'ПОЗИЦИЯ_ДО', value = before.position) # POSITION_BEFORE
                emb.add_field(name = 'ПОЗИЦИЯ_ПОСЛЕ', value = after.position) # POSITION_AFTER
                emb.set_footer(text = f'ID: {before.id}')
                await channel.send(embed = emb)
        elif before.type == discord.ChannelType.text:
            emb = discord.Embed(title = r'ИЗМЕНЕНИЕ\_ТЕКСТОВОГО_КАНАЛА', color = discord.Color.orange(), timestamp = datetime.datetime.utcnow()) # TEXT_CHANNEL_EDITED
            if before.name != after.name:
                emb.add_field(name = 'НАЗВАНИЕ_ДО', value = before.name) # NAME_BEFORE
                emb.add_field(name = 'НАЗВАНИЕ_ПОСЛЕ', value = after.name) # NAME_AFTER
                emb.set_footer(text = f'ID: {before.id}')
                await channel.send(embed = emb)
            if before.position != after.position:
                emb.add_field(name = 'НАЗВАНИЕ', value = before.name, inline = False) # NAME
                emb.add_field(name = 'ПОЗИЦИЯ_ДО', value = before.position) # POSITION_BEFORE
                emb.add_field(name = 'ПОЗИЦИЯ_ПОСЛЕ', value = after.position) # POSITION_AFTER
                emb.set_footer(text = f'ID: {before.id}')
                await channel.send(embed = emb)

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
        role1 = discord.utils.get(member.guild.roles, id = 775265053162209300)
        role2 = discord.utils.get(member.guild.roles, id = 693933511412940800)
        if member.guild.id == 693929822543675455 and member.bot == False:
            channel = client.get_channel(693929823030214658)
            emb = discord.Embed(description = f'{member.mention} ({member.name}) пришёл к нам!', colour = discord.Color.orange(), timestamp = datetime.datetime.utcnow())
            await channel.send(embed = emb)
            if role != None:
                await member.add_roles(role, role1, role2)
                emb1 = discord.Embed(title = 'ВЫДАЧА\_РОЛЕЙ\_ЧЕРЕЗ\_АВТО_РОЛЬ', colour = discord.Color.orange(), timestamp = datetime.datetime.utcnow()) # AUTO_ROLES_ADDED
                emb1.add_field(name = 'УЧАСТНИК', value = member) # MEMBER
                emb1.add_field(name = 'УПОМИНАНИЕ', value = member.mention) # MENTION
                emb1.add_field(name = 'РОЛИ', value = f'{role.mention}, {role1.mention}, {role2.mention}') # ROLES
                emb1.set_footer(text = f'ID: {member.id}')
                await lchannel.send(embed = emb1)
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
        return (m.author == message.author and len(m.mentions) and (datetime.datetime.utcnow() - m.created_at).seconds < 1)
    if len(list(filter(lambda m: _check(m), client.cached_messages))) >= 2 and message.author.id != client.owner_id:
        role = discord.utils.get(message.guild.roles, name = 'Muted')
        role3 = discord.utils.get(message.guild.roles, name = '----------Предупреждения----------')
        role1 = discord.utils.get(message.guild.roles, name = '1')
        role2 = discord.utils.get(message.guild.roles, name = '2')
        if role != None and role1 != None and role2 != None and role3 != None:
            if role not in message.author.roles:
                if role1 not in message.author.roles and role2 not in message.author.roles:
                    await message.channel.send(f'{message.author.mention} Был замучен на 10 минут за спам упоминаниями. Больше так не делай!')
                    await message.author.add_roles(role, role1, role3)
                    channel = client.get_channel(714175791033876490)
                    emb = discord.Embed(title = 'СРАБОТАЛ\_АВТО_МУТ', color = discord.Color.orange(), timestamp = datetime.datetime.utcnow())
                    emb.add_field(name = 'СЕРВЕР', value = message.guild.name)
                    emb.add_field(name = 'УЧАСТНИК', value = message.author)
                    await channel.send(embed = emb)
                    await asyncio.sleep(600)
                    if role != None:
                        if role in message.author.roles:
                            await message.author.remove_roles(role)
                            await message.channel.send(f'{message.author.mention} Был размучен.')
                        else:
                            await message.channel.send(f'Роли Muted не было обнаружено в списке ролей {message.author.mention}.')
                    else:
                        await message.channel.send(f'Невозможно снять мут у {message.author.mention}, т.к. роль `Muted` была удалена.')
                if role1 in message.author.roles and role2 not in message.author.roles:
                    await message.channel.send(f'{message.author.mention} Был замучен на 30 минут за спам упоминаниями. Последнее предупреждение.')
                    await message.author.remove_roles(role1)
                    await message.author.add_roles(role, role2, role3)
                    channel = client.get_channel(714175791033876490)
                    emb = discord.Embed(title = 'СРАБОТАЛ\_АВТО_МУТ', color = discord.Color.orange(), timestamp = datetime.datetime.utcnow())
                    emb.add_field(name = 'СЕРВЕР', value = message.guild.name)
                    emb.add_field(name = 'УЧАСТНИК', value = message.author)
                    await channel.send(embed = emb)
                    await asyncio.sleep(1800)
                    if role != None:
                        if role in message.author.roles:
                            await message.author.remove_roles(role)
                            await message.channel.send(f'{message.author.mention} Был размучен.')
                        else:
                            await message.channel.send(f'Роли Muted не было обнаружено в списке ролей {message.author.mention}.')
                    else:
                        await message.channel.send(f'Невозможно снять мут у {message.author.mention}, т.к. роль `Muted` была удалена.')
                if role2 in message.author.roles:
                    await message.channel.send(f'{message.author.mention} Был замучен навсегда за спам упоминаниями.')
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
    elif message.channel.id == 750372413102883028: #EFT
        if message.author.bot == True and message.author.id != 694170281270312991:
            role = discord.utils.get(message.guild.roles, id = 750368477671325728)
            sent = await message.channel.send(role.mention)
            await sent.delete()
            channel = client.get_channel(714175791033876490)
            emb = discord.Embed(title = 'ОПОВЕЩЕНИЕ\_ОБ_ОБНОВЛЕНИИ', color = discord.Color.orange(), timestamp = datetime.datetime.utcnow())
            emb.add_field(name = 'ОПОВЕЩЕНЫ', value = role.mention)
            await channel.send(embed = emb)
    elif message.channel.id == 750371693779746826: #RSS
        if message.author.bot == True and message.author.id != 694170281270312991:
            role = discord.utils.get(message.guild.roles, id = 750372161134264400)
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
    elif message.channel.id == 750362487224008846: #L.O.L. HAHA
        if message.author.bot == True and message.author.id != 694170281270312991:
            role = discord.utils.get(message.guild.roles, id = 750056065474887852)
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
    elif message.channel.id == 750373213447389194: #DCP
        if message.author.bot == True and message.author.id != 694170281270312991:
            role = discord.utils.get(message.guild.roles, id = 750379151210446949)
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
            emb.add_field(name = 'НАПИСАНО', value = message.content, inline = False)
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
#Events

#Mod
@client.command()
@commands.has_permissions(view_audit_log = True)
@commands.cooldown(1, 5, commands.BucketType.user)
async def dm(ctx, member: discord.Member, *, text):
    await ctx.message.delete()
    emb = discord.Embed(description = f'{text}', colour = 0x2f3136)
    emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
    await member.send(embed = emb)

@client.command(aliases = ['Kick', 'KICK'])
@commands.cooldown(1, 10, commands.BucketType.user)
@commands.has_permissions(kick_members = True)
async def kick(ctx, member: discord.Member, *, reason = None):
    await ctx.message.delete()
    bot = discord.utils.get(ctx.guild.members, id = client.user.id)
    if member.id != 338714886001524737:
        if reason == None:
            reason = 'Не указана.'
        if ctx.author.top_role == member.top_role and ctx.message.author.id != 338714886001524737:
            emb = discord.Embed(description = f'{ctx.author.mention}, ваша высшая роль равна высшей роли {member.mention}. Кик отклонён.', colour = discord.Color.orange())
            if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
            await ctx.send(embed = emb)
        elif member.top_role > ctx.author.top_role and ctx.message.author.id != 338714886001524737:
                emb = discord.Embed(description = f'{ctx.author.mention}, ваша высшая роль ниже высшей роли {member.mention}. Кик отклонён.', colour = discord.Color.orange())
                if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                    emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
                await ctx.send(embed = emb)
        elif member.top_role > bot.top_role:
            emb = discord.Embed(description = f'МОЯ высшая роль ниже высшей роли {member.mention}. Кик невозможен.', color = 0xff0000)
            if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
            await ctx.send(embed = emb)
        elif member.top_role == bot.top_role:
            emb = discord.Embed(description = f'МОЯ высшая роль идентична высшей роли {member.mention}. Кик невозможен.', color = 0xff0000)
            if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
            await ctx.send(embed = emb)
        else:
            emb = discord.Embed(colour = 0x2f3136)
            emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            emb.add_field(name = 'Был кикнут', value = member.mention)
            emb.add_field(name = 'По причине', value = reason)
            if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
            await ctx.send(embed = emb)
            await member.kick(reason = reason)
    else:
        emb = discord.Embed(description = f'Извините, {ctx.author.mention}, но вы не можете кикнуть моего создателя!', colour = discord.Color.orange())
        if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
            emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb)

@client.command(aliases = ['Ban', 'BAN'])
@commands.cooldown(1, 10, commands.BucketType.user)
@commands.has_permissions(ban_members = True)
async def ban(ctx, member: discord.Member, *, reason = None):
    await ctx.message.delete()
    bot = discord.utils.get(ctx.guild.members, id = client.user.id)
    if member.id != 338714886001524737:
        if reason == None:
            reason = 'Не указана.'
        if ctx.author.top_role == member.top_role and ctx.message.author.id != 338714886001524737:
            emb = discord.Embed(description = f'{ctx.author.mention}, ваша высшая роль равна высшей роли {member.mention}. Бан отклонён.', colour = discord.Color.orange())
            if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
            await ctx.send(embed = emb)
        elif member.top_role > ctx.author.top_role and ctx.message.author.id != 338714886001524737:
            emb = discord.Embed(description = f'{ctx.author.mention}, ваша высшая роль ниже высшей роли {member.mention}. Бан отклонён.', colour = discord.Color.orange())
            if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
            await ctx.send(embed = emb)
        elif member.top_role > bot.top_role:
            emb = discord.Embed(description = f'МОЯ высшая роль ниже высшей роли {member.mention}. Бан невозможен.', color = 0xff0000)
            if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
            await ctx.send(embed = emb)
        elif member.top_role == bot.top_role:
            emb = discord.Embed(description = f'МОЯ высшая роль идентична высшей роли {member.mention}. Бан невозможен.', color = 0xff0000)
            if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
            await ctx.send(embed = emb)
        else:
            if '--soft' in reason:
                emb = discord.Embed(color = 0x00ff00)
                emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                emb.add_field(name = 'Упрощённо забанен', value = f'{member.mention} ({member.name})')
                if '--reason' in reason:
                    reason = reason.strip()[15:].strip()
                else:
                    reason = 'Не указана.'
                emb.add_field(name = 'По причине', value = reason)
                if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                    emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
                await ctx.send(embed = emb)
                await member.ban(reason = reason)
                await member.unban(reason = '--softban')
            else:
                emb = discord.Embed(colour = 0xff0000)
                emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                emb.add_field(name = 'Был забанен', value = member.mention)
                emb.add_field(name = 'По причине', value = reason)
                if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                    emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
                await ctx.send(embed = emb)
                await member.ban(reason = reason)
    else:
        emb = discord.Embed(description = f'Извините, {ctx.author.mention}, но вы не можете забанить моего создателя!', colour = discord.Color.orange())
        if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
            emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb)

@client.command(aliases = ['Give', 'GIVE'])
async def give(ctx, member: discord.Member, *, role: discord.Role):
    await ctx.message.delete()
    if ctx.message.author.guild_permissions.manage_channels or ctx.author.id == client.owner_id:
        if role != None:
            bot = ctx.guild.get_member(client.user.id)
            if role > member.top_role and ctx.message.author.id != 338714886001524737:
                emb = discord.Embed(description = f'Вы не можете выдать {role.mention}, так как она имеет более высокий ранг, чем ваша высшая роль.', color = discord.Color.orange())
                await ctx.send(embed = emb)
                if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                    emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
            elif role == ctx.author.top_role and ctx.message.author.id != 338714886001524737:
                emb = discord.Embed(description = f'Вы не можете выдать {role.mention} кому-либо, так как она равна вашей высшей роли.', color = discord.Color.orange())
                if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                    emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
                await ctx.send(embed = emb)
            elif role.is_default():
                emb = discord.Embed(description = 'Выдавать @everyone?', color = 0x2f3136)
                if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                    emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
                await ctx.send(embed = emb)
            else:
                await member.add_roles(role)
                emb = discord.Embed(colour = member.color, timestamp = ctx.message.created_at)
                emb.add_field(name = 'ВЫДАНА_РОЛЬ', value = f'{role.mention} | {role.name} | ID {role.id}')
                emb.add_field(name = 'ВЫДАНА:', value = member.mention, inline = False)
                emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                    emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
                await ctx.send(embed = emb)
        else:
            emb = discord.Embed(description = f'{ctx.author.mention}, я не могу найти {role.mention} в списке ролей.', colour = member.color, timestamp = ctx.message.created_at)
            if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
            await ctx.send(embed = emb)

@client.command(aliases = ['Take', 'TAKE'])
async def take(ctx, member: discord.Member, *, role: discord.Role):
    await ctx.message.delete()
    if ctx.message.author.guild_permissions.manage_channels or ctx.author.id == client.owner_id:
        if role != None:
            bot = ctx.guild.get_member(client.user.id)
            if role > member.top_role and ctx.message.author.id != 338714886001524737:
                emb = discord.Embed(description = f'Вы не можете забрать {role.mention}, так как она имеет более высокий ранг, чем ваша высшая роль. Забирание роли отменено.', color = 0xffffff)
                await ctx.send(embed = emb)
                if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                    emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
            elif role == ctx.author.top_role and ctx.message.author.id != 338714886001524737:
                emb = discord.Embed(description = f'Вы не можете забрать {role.mention}, так как она равна вашей высшей роли. Забирание роли отменено.', color = 0xffffff)
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
            elif role.is_default():
                emb = discord.Embed(description = 'Забирать @everyone?', color = 0x2f3136)
                if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                    emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
                await ctx.send(embed = emb)
            else:
                await member.remove_roles(role)
                emb = discord.Embed(colour = member.color, timestamp = ctx.message.created_at)
                emb.add_field(name = 'ЗАБРАНА_РОЛЬ', value = f'{role.mention} | {role.name} | ID {role.id}')
                emb.add_field(name = 'ЗАБРАНА_У:', value = member.mention, inline = False)
                emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                    emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
                await ctx.send(embed = emb)
        else:
            emb = discord.Embed(description = f'{ctx.author.mention}, я не могу найти {role.mention} в списке ролей.', colour = member.color, timestamp = ctx.message.created_at)
            if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
            await ctx.send(embed = emb)

@client.command(aliases = ['Mute', 'MUTE'])
@commands.has_permissions(view_audit_log = True)
async def mute(ctx, member: discord.Member, time: TimeConverter, *, reason: str = None):
    await ctx.message.delete()
    if time < 300:
        color = 0x2f3136
    if time >= 300:
        color = discord.Color.orange()
    if time >= 1200:
        color = 0xff0000
    if reason == None:
        reason = 'Не указана.'
    role = discord.utils.get(ctx.guild.roles, name = 'Muted')
    if member.id != 338714886001524737:
        if ctx.author.top_role == member.top_role and ctx.message.author.id != 338714886001524737:
            emb = discord.Embed(description = f'{ctx.author.mention}, ваша высшая роль равна высшей роли {member.mention}. Мут отклонён.', colour = 0xff0000)
            await ctx.send(embed = emb)
        elif ctx.author.top_role < member.top_role and ctx.message.author.id != 338714886001524737:
            emb = discord.Embed(description = f'{ctx.author.mention}, ваша высшая роль ниже высшей роли {member.mention}. Мут отклонён.', colour = 0xff0000)
            await ctx.send(embed = emb)
        else:
            if role != None:
                await member.add_roles(role)
                emb = discord.Embed(colour = color, timestamp = ctx.message.created_at)
                emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                emb.add_field(name = 'В муте', value = f'{member.mention}')
                emb.add_field(name = 'По причине', value = reason)
                emb.add_field(name = 'Время мута', value = f'{time}s')
                if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                    emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
                await ctx.send(embed = emb, delete_after = time)
                await asyncio.sleep(time)
                if role != None:
                    if role in member.roles:
                        emb = discord.Embed(colour = color, timestamp = ctx.message.created_at)
                        emb.add_field(name = 'Размучен по истечению времени', value = member.mention)
                        emb.add_field(name = 'Был в муте по причине', value = reason)
                        emb.add_field(name = 'Время мута составляло', value = f'{time}s')
                        if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                            emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
                        await member.remove_roles(role)
                        await ctx.send(f'{member.mention}', embed = emb)
                    else:
                        emb = discord.Embed(description = f'Снятие мута для {member.mention} не требуется. Роли Muted не обнаружено в списке ролей участника.', colour = 0x2f3136)
                        await ctx.send(embed = emb)
                else:
                    emb = discord.Embed(description = f'Невозможно снять мут с {member.mention}, роль Muted удалена.', colour = discord.Color.orange(), timestamp = ctx.message.created_at)
                    await ctx.send(embed = emb)
            else:
                await ctx.guild.create_role(name = 'Muted', colour = discord.Colour(0x000001))
                role = discord.utils.get(ctx.guild.roles, name = 'Muted')
                emb1 = discord.Embed(description = f'{ctx.author.mention}, По причине того, что я не нашёл нужную роль, была создана роль {role.name} с цветом {role.colour}.', colour = discord.Color.orange(), timestamp = ctx.message.created_at)
                emb1.set_footer(text = 'Это сообщение должно показываться только 1 раз. Иначе, роль была удалена.')
                await ctx.send(embed = emb1, delete_after = 3)
                await asyncio.sleep(3)
                await member.add_roles(role)
                emb = discord.Embed(colour = color, timestamp = ctx.message.created_at)
                emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                emb.add_field(name = 'В муте', value = f'{member.mention}')
                emb.add_field(name = 'По причине', value = reason)
                emb.add_field(name = 'Время мута', value = f'{time}s')
                if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                    emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
                await ctx.send(embed = emb, delete_after = time)
                await asyncio.sleep(time)
                if role != None:
                    if role in member.roles:
                        emb = discord.Embed(colour = color, timestamp = ctx.message.created_at)
                        emb.add_field(name = 'Размучен по истечению времени', value = member.mention)
                        emb.add_field(name = 'Был в муте по причине', value = reason)
                        emb.add_field(name = 'Время мута составляло', value = f'{time}s')
                        if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                            emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
                        await ctx.send(f'{member.mention}', embed = emb)
                        await member.remove_roles(role)
                    else:
                        emb = discord.Embed(description = f'Снятие мута для {member.mention} не требуется. Роли Muted не обнаружено в списке ролей участника.', colour = 0x2f3136)
                        await ctx.send(embed = emb)
                else:
                    emb = discord.Embed(description = f'Невозможно снять мут с {member.mention}, роль Muted удалена.', color = discord.Color.orange())
                    await ctx.send(embed = emb)
    else:
        emb = discord.Embed(description = f'Извините, {ctx.author.mention}, но вы не можете замутить моего создателя!', color = 0xff0000)
        await ctx.send(embed = emb)

@client.command(aliases = ['Unmute', 'UNMUTE'])
@commands.has_permissions(manage_channels = True)
async def unmute(ctx, member: discord.Member, *, reason = None):
    await ctx.message.delete()
    role = discord.utils.get(ctx.guild.roles, name = 'Muted')
    if role != None:
        if role in member.roles:
            await member.remove_roles(role)
            if reason == None:
                reason = 'Не указана.'
            emb = discord.Embed(title = f'Принудительное снятие мута у {member}', colour = 0x2f3136, timestamp = ctx.message.created_at)
            emb.add_field(name = 'Снял мут', value = ctx.author.mention)
            emb.add_field(name = 'По причине', value = reason)
            if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
            await ctx.send(embed = emb)
        else:
            emb = discord.Embed(description = f'Снятие мута не требуется, роли Muted не обнаружено в ролях {member.mention}.', colour = 0x2f3136)
            await ctx.send(embed = emb)
    else:
        emb = discord.Embed(description = f'Невозможно снять мут у {member.mention}, т.к. роль Muted была удалена.', colour = discord.Color.orange(), timestamp = ctx.message.created_at)
        await ctx.send(embed = emb)

@client.command(aliases = ['Clear', 'CLEAR', 'purge', 'Purge', 'PURGE', 'prune', 'Prune', 'PRUNE', 'clean', 'Clean', 'CLEAN'])
@commands.cooldown(1, 10, commands.BucketType.user)
@commands.has_permissions(administrator = True)
async def clear(ctx, amount: int, members = '--everyone', *, filt = None):
    await ctx.message.delete()
    authors = {}
    cleared = 0
    if "--everyone" not in members and '--bots' not in members and  '--users' not in members and '--silent' not in members:
        member_list = [x.strip() for x in members.split(", ")]
        for member in member_list:
            if "@" in member:
                member = member[3 if "!" in member else 2:-1]
            if member.isdigit():
                member_object = ctx.guild.get_member(int(member))
            else:
                member_object = ctx.guild.get_member_named(member)
            if not member_object:
                emb = discord.Embed(description = 'Невозможно найти участника.', color = discord.Color.orange())
                return await ctx.send(embed = emb)
    async for message in ctx.history(limit = amount):
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
        if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
            emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(f'{ctx.guild.owner.mention}', embed = emb)
    elif amount >= 250:
        if ctx.author != ctx.guild.owner:
            emb = discord.Embed(description = f'{ctx.author.mention}, операция с данным числом ({amount}) доступна только {ctx.guild.owner.mention}. Отмена.', colour = discord.Color.orange())
            if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
            await ctx.send(f'{ctx.guild.owner.mention}', embed = emb, delete_after = 5)
        else:
            emb = discord.Embed(description = f'{ctx.author.mention}, обнаружено слишком большое число для удаления сообщений ({amount}). Возможны дальнейшие ошибки в работе {client.user.mention}. Продолжить? (y/n)\n||Отмена через 10 секунд.||', colour = discord.Color.orange())
            if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
            sent = await ctx.send(embed = emb)
            try:
                msg = await client.wait_for('message', timeout = 10, check = lambda message: message.channel == ctx.message.channel and message.author.id == ctx.guild.owner.id)
                if msg.content.lower() == 'y' and msg.author.id == ctx.guild.owner.id:
                    await msg.delete()
                    await sent.delete()
                    if '--silent' not in members:
                        emb = discord.Embed(description = 'Проверяем..', color = discord.Color.orange())
                        if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                            emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
                        sent = await ctx.send(embed = emb)
                        if members == '--bots':
                            if filt == None:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == True, before = sent)
                            else:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.author.bot == True, before = sent)
                            emb = discord.Embed(title = 'Результаты удаления сообщений', color = discord.Color.orange())
                            emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{cleared}```')
                            if filt:
                                emb.add_field(name = 'Применён фильтр:', value = f'```{filt} ({members})```', inline = True)
                            emb.add_field(name = 'Удалены/Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                            if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                                emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c". Cephalon Cy by сасиска#2472')
                            else:
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
                                emb.add_field(name = 'Применён фильтр:', value = f'```{filt} ({members})```', inline = True)
                            emb.add_field(name = 'Удалены/Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                            if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                                emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c". Cephalon Cy by сасиска#2472')
                            else:
                                emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c".')
                            await sent.edit(embed = emb)
                        elif members != '--everyone':
                            if filt == None:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.author == member_object, before = sent)
                            else:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.author == member_object and m.content.lower() == filt.lower(), before = sent)
                            emb = discord.Embed(title = 'Результаты удаления сообщений', color = discord.Color.orange())
                            emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{cleared}```')
                            if filt:
                                emb.add_field(name = 'Применён фильтр:', value = f'```{filt} ({members})```', inline = True)
                            emb.add_field(name = 'Удалены/Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                            if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                                emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c". Cephalon Cy by сасиска#2472')
                            else:
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
                                emb.add_field(name = 'Применён фильтр:', value = f'```{filt} ({members})```', inline = True)
                            emb.add_field(name = 'Удалены/Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                            if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                                emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c". Cephalon Cy by сасиска#2472')
                            else:
                                emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c".')
                            await sent.edit(embed = emb)
                        try:
                            if '--silent' in members:
                                return
                            msg = await client.wait_for('message', timeout = 10, check = lambda message: message.channel == ctx.message.channel and message.author == ctx.author and message.content == 'c')
                            emb = discord.Embed(title = 'Результаты удаления сообщений', color = discord.Color.orange())
                            emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{cleared}```')
                            if filt:
                                emb.add_field(name = 'Применён фильтр:', value = f'```{filt} ({members})```', inline = True)
                            emb.add_field(name = 'Удалены/Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                            if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                                emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
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
                        elif '--everyone' not in members and members != '--silent':
                            if filt == None:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.author == member_object)
                            else:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.author == member_object and m.content.lower() == filt.lower())
                        elif '--bots' and '--users' in members:
                            if filt == None:
                                await ctx.channel.purge(limit = amount)
                            else:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower())
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
                    if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
                    await ctx.send(embed = emb, delete_after = 3)
                elif msg.content.lower() == 'n' or 'y' and msg.author.id != ctx.guild.owner.id:
                    await msg.delete()
                    await sent.delete()
                    emb = discord.Embed(description = f'{ctx.author.mention}, ты не являешься владельцем сервера.', colour = discord.Color.orange())
                    if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
                    await ctx.send(embed = emb, delete_after = 3)
                else:
                    await msg.delete()
                    await sent.delete()
                    emb = discord.Embed(description = f'Обнаружен недопустимый ответ ({msg.content})', colour = discord.Color.orange())
                    if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
                    await ctx.send(embed = emb, delete_after = 3)
            except asyncio.TimeoutError:
                await sent.delete()
                emb = discord.Embed(description = f'{ctx.author.mention}, Время вышло.', colour = discord.Color.orange())
                if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                    emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
                await ctx.send(f'{ctx.guild.owner.mention}', embed = emb, delete_after = 3)
    elif amount >= 100:
        if ctx.author != ctx.guild.owner:
            emb = discord.Embed(description = f'{ctx.author.mention}, создан запрос на удаление {amount} сообщений. Мне нужен ответ создателя сервера на это действие. Продолжаем? (y/n)\n||Запрос будет отменён через 1 минуту.||', colour = discord.Color.orange())
            if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
            sent = await ctx.send(f'{ctx.guild.owner.mention}', embed = emb)
            try:
                msg = await client.wait_for('message', timeout = 60, check = lambda message: message.channel == ctx.message.channel and message.author.id == ctx.guild.owner.id)
                if msg.content.lower() == 'y':
                    await msg.delete()
                    await sent.delete()
                    if '--silent' not in members:
                        emb = discord.Embed(description = 'Проверяем..', color = discord.Color.orange())
                        if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                            emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
                        sent = await ctx.send(embed = emb)
                        if members == '--bots':
                            if filt == None:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == True, before = sent)
                            else:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.author.bot == True, before = sent)
                            emb = discord.Embed(title = 'Результаты удаления сообщений', color = discord.Color.orange())
                            emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{cleared}```')
                            if filt:
                                emb.add_field(name = 'Применён фильтр:', value = f'```{filt} ({members})```', inline = True)
                            emb.add_field(name = 'Удалены/Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                            if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                                emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c". Cephalon Cy by сасиска#2472')
                            else:
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
                                emb.add_field(name = 'Применён фильтр:', value = f'```{filt} ({members})```', inline = True)
                            emb.add_field(name = 'Удалены/Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                            if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                                emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c". Cephalon Cy by сасиска#2472')
                            else:
                                emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c".')
                            await sent.edit(embed = emb)
                        elif members != '--everyone':
                            if filt == None:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.author == member_object, before = sent)
                            else:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.author == member_object and m.content.lower() == filt.lower(), before = sent)
                            emb = discord.Embed(title = 'Результаты удаления сообщений', color = discord.Color.orange())
                            emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{cleared}```')
                            if filt:
                                emb.add_field(name = 'Применён фильтр:', value = f'```{filt} ({members})```', inline = True)
                            emb.add_field(name = 'Удалены/Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                            if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                                emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c". Cephalon Cy by сасиска#2472')
                            else:
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
                                emb.add_field(name = 'Применён фильтр:', value = f'```{filt} ({members})```', inline = True)
                            emb.add_field(name = 'Удалены/Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                            if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                                emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c". Cephalon Cy by сасиска#2472')
                            else:
                                emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c".')
                            await sent.edit(embed = emb)
                        try:
                            if '--silent' in members:
                                return
                            msg = await client.wait_for('message', timeout = 10, check = lambda message: message.channel == ctx.message.channel and message.author == ctx.author and message.content == 'c')
                            emb = discord.Embed(title = 'Результаты удаления сообщений', color = discord.Color.orange())
                            emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{cleared}```')
                            if filt:
                                emb.add_field(name = 'Применён фильтр:', value = f'```{filt} ({members})```', inline = True)
                            emb.add_field(name = 'Удалены/Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                            if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                                emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
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
                        elif '--everyone' not in members and members != '--silent':
                            if filt == None:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.author == member_object)
                            else:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.author == member_object and m.content.lower() == filt.lower())
                        elif '--bots' and '--users' in members:
                            if filt == None:
                                await ctx.channel.purge(limit = amount)
                            else:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower())
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
                    if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
                    await ctx.send(embed = emb, delete_after = 3)
                elif msg.content.lower() == 'n' or 'y' and msg.author.id != ctx.guild.owner.id:
                    await msg.delete()
                    await sent.delete()
                    emb = discord.Embed(description = f'{ctx.author.mention}, ты не являешься владельцем сервера.', colour = discord.Color.orange())
                    if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
                    await ctx.send(embed = emb, delete_after = 3)
                else:
                    await msg.delete()
                    await sent.delete()
                    emb = discord.Embed(description = f'Обнаружен недопустимый ответ ({msg.content})', colour = discord.Color.orange())
                    if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
                    await ctx.send(embed = emb, delete_after = 3)
            except asyncio.TimeoutError:
                await sent.delete()
                emb = discord.Embed(description = f'{ctx.author.mention}, Время вышло.', colour = discord.Color.orange())
                if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                    emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
                await ctx.send(f'{ctx.guild.owner.mention}', embed = emb, delete_after = 3)
        else:
            emb = discord.Embed(description = f'{ctx.author.mention}, создан запрос на удаление {amount} сообщений. Продолжить? (y/n)\n||Запрос будет отменён через 10 секунд.||', colour = discord.Color.orange())
            if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
            sent = await ctx.send(embed = emb)
            try:
                msg = await client.wait_for('message', timeout = 10, check = lambda message: message.author == ctx.author and message.channel == ctx.message.channel)
                if msg.content.lower() == 'y':
                    await msg.delete()
                    await sent.delete()
                    if '--silent' not in members:
                        emb = discord.Embed(description = 'Проверяем..', color = discord.Color.orange())
                        if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                            emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
                        sent = await ctx.send(embed = emb)
                        if members == '--bots':
                            if filt == None:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == True, before = sent)
                            else:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.author.bot == True, before = sent)
                            emb = discord.Embed(title = 'Результаты удаления сообщений', color = discord.Color.orange())
                            emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{cleared}```')
                            if filt:
                                emb.add_field(name = 'Применён фильтр:', value = f'```{filt} ({members})```', inline = True)
                            emb.add_field(name = 'Удалены/Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                            if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                                emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c". Cephalon Cy by сасиска#2472')
                            else:
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
                                emb.add_field(name = 'Применён фильтр:', value = f'```{filt} ({members})```', inline = True)
                            emb.add_field(name = 'Удалены/Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                            if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                                emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c". Cephalon Cy by сасиска#2472')
                            else:
                                emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c".')
                            await sent.edit(embed = emb)
                        elif members != '--everyone':
                            if filt == None:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.author == member_object, before = sent)
                            else:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.author == member_object and m.content.lower() == filt.lower(), before = sent)
                            emb = discord.Embed(title = 'Результаты удаления сообщений', color = discord.Color.orange())
                            emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{cleared}```')
                            if filt:
                                emb.add_field(name = 'Применён фильтр:', value = f'```{filt} ({members})```', inline = True)
                            emb.add_field(name = 'Удалены/Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                            if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                                emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c". Cephalon Cy by сасиска#2472')
                            else:
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
                                emb.add_field(name = 'Применён фильтр:', value = f'```{filt} ({members})```', inline = True)
                            emb.add_field(name = 'Удалены/Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                            if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                                emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c". Cephalon Cy by сасиска#2472')
                            else:
                                emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c".')
                            await sent.edit(embed = emb)
                        try:
                            if '--silent' in members:
                                return
                            msg = await client.wait_for('message', timeout = 10, check = lambda message: message.channel == ctx.message.channel and message.author == ctx.author and message.content == 'c')
                            emb = discord.Embed(title = 'Результаты удаления сообщений', color = discord.Color.orange())
                            emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{cleared}```')
                            if filt:
                                emb.add_field(name = 'Применён фильтр:', value = f'```{filt} ({members})```', inline = True)
                            emb.add_field(name = 'Удалены/Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                            if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                                emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
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
                        elif '--everyone' not in members and members != '--silent':
                            if filt == None:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.author == member_object)
                            else:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.author == member_object and m.content.lower() == filt.lower())
                        elif '--bots' and '--users' in members:
                            if filt == None:
                                await ctx.channel.purge(limit = amount)
                            else:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower())
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
                    if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
                    await ctx.send(embed = emb, delete_after = 3)
                else:
                    await msg.delete()
                    await sent.delete()
                    emb = discord.Embed(description = f'Обнаружен недопустимый ответ ({msg.content})', colour = discord.Color.orange())
                    if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
                    await ctx.send(embed = emb, delete_after = 3)
            except asyncio.TimeoutError:
                await sent.delete()
                emb = discord.Embed(description = f'{ctx.author.mention}, Время вышло.', colour = discord.Color.orange())
                if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                    emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
                await ctx.send(embed = emb, delete_after = 3)
    elif amount >= 10:
        emb = discord.Embed(description = f'{ctx.author.mention}, создан запрос на удаление {amount} сообщений. Продолжить? (y/n)\n||Запрос будет отменён через 10 секунд.||', colour = discord.Color.orange())
        if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
            emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        sent = await ctx.send(embed = emb)
        try:
            msg = await client.wait_for('message', timeout = 10, check = lambda message: message.author == ctx.author and message.channel == ctx.message.channel)
            if msg.content.lower() == 'y':
                await msg.delete()
                await sent.delete()
                if '--silent' not in members:
                    emb = discord.Embed(description = 'Проверяем..', color = discord.Color.orange())
                    if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
                    sent = await ctx.send(embed = emb)
                    if members == '--bots':
                        if filt == None:
                            await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == True, before = sent)
                        else:
                            await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.author.bot == True, before = sent)
                        emb = discord.Embed(title = 'Результаты удаления сообщений', color = discord.Color.orange())
                        emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{cleared}```')
                        if filt:
                            emb.add_field(name = 'Применён фильтр:', value = f'```{filt} ({members})```', inline = True)
                        emb.add_field(name = 'Удалены/Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                        if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                            emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c". Cephalon Cy by сасиска#2472')
                        else:
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
                            emb.add_field(name = 'Применён фильтр:', value = f'```{filt} ({members})```', inline = True)
                        emb.add_field(name = 'Удалены/Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                        if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                            emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c". Cephalon Cy by сасиска#2472')
                        else:
                            emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c".')
                        await sent.edit(embed = emb)
                    elif members != '--everyone':
                        if filt == None:
                            await ctx.channel.purge(limit = amount, check = lambda m: m.author == member_object, before = sent)
                        else:
                            await ctx.channel.purge(limit = amount, check = lambda m: m.author == member_object and m.content.lower() == filt.lower(), before = sent)
                        emb = discord.Embed(title = 'Результаты удаления сообщений', color = discord.Color.orange())
                        emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{cleared}```')
                        if filt:
                            emb.add_field(name = 'Применён фильтр:', value = f'```{filt} ({members})```', inline = True)
                        emb.add_field(name = 'Удалены/Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                        if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                            emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c". Cephalon Cy by сасиска#2472')
                        else:
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
                            emb.add_field(name = 'Применён фильтр:', value = f'```{filt} ({members})```', inline = True)
                        emb.add_field(name = 'Удалены/Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                        if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                            emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c". Cephalon Cy by сасиска#2472')
                        else:
                            emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c".')
                        await sent.edit(embed = emb)
                    try:
                        if '--silent' in members:
                            return
                        msg = await client.wait_for('message', timeout = 10, check = lambda message: message.channel == ctx.message.channel and message.author == ctx.author and message.content == 'c')
                        emb = discord.Embed(title = 'Результаты удаления сообщений', color = discord.Color.orange())
                        emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{cleared}```')
                        if filt:
                            emb.add_field(name = 'Применён фильтр:', value = f'```{filt} ({members})```', inline = True)
                        emb.add_field(name = 'Удалены/Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                        if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                            emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
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
                    elif '--everyone' not in members and members != '--silent':
                        if filt == None:
                            await ctx.channel.purge(limit = amount, check = lambda m: m.author == member_object)
                        else:
                            await ctx.channel.purge(limit = amount, check = lambda m: m.author == member_object and m.content.lower() == filt.lower())
                    elif '--bots' and '--users' in members:
                        if filt == None:
                            await ctx.channel.purge(limit = amount)
                        else:
                            await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower())
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
                if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                    emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
                await ctx.send(embed = emb, delete_after = 3)
            else:
                await msg.delete()
                await sent.delete()
                emb = discord.Embed(description = f'Обнаружен недопустимый ответ ({msg.content})', colour = discord.Color.orange())
                if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                    emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
                await ctx.send(embed = emb, delete_after = 3)
        except asyncio.TimeoutError:
            await sent.delete()
            emb = discord.Embed(description = f'{ctx.author.mention}, Время вышло.', colour = discord.Color.orange())
            if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
            await ctx.send(embed = emb, delete_after = 3)
    elif amount == 0:
        emb = discord.Embed(description = 'Удалять 0 сообщений? Ты еблан?', colour = discord.Color.orange())
        if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
            emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb, delete_after = 1)
    else:
        if '--silent' not in members:
            emb = discord.Embed(description = 'Проверяем..', color = discord.Color.orange())
            if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
            sent = await ctx.send(embed = emb)
            if '--bots' in members:
                if filt == None:
                    await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == True, before = sent)
                else:
                    await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.author.bot == True, before = sent)
                emb = discord.Embed(title = 'Результаты удаления сообщений', color = discord.Color.orange())
                emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{cleared}```')
                if filt:
                    emb.add_field(name = 'Применён фильтр:', value = f'```{filt} ({members})```', inline = True)
                emb.add_field(name = 'Удалены/Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                    emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c". Cephalon Cy by сасиска#2472')
                else:
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
                    emb.add_field(name = 'Применён фильтр:', value = f'```{filt} ({members})```', inline = True)
                emb.add_field(name = 'Удалены/Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                    emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c". Cephalon Cy by сасиска#2472')
                else:
                    emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c".')
                await sent.edit(embed = emb)
            elif '--everyone' not in members:
                if filt == None:
                    await ctx.channel.purge(limit = amount, check = lambda m: m.author == member_object, before = sent)
                else:
                    await ctx.channel.purge(limit = amount, check = lambda m: m.author == member_object and m.content.lower() == filt.lower(), before = sent)
                emb = discord.Embed(title = 'Результаты удаления сообщений', color = discord.Color.orange())
                emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{cleared}```')
                if filt:
                    emb.add_field(name = 'Применён фильтр:', value = f'```{filt} ({members})```', inline = True)
                emb.add_field(name = 'Удалены/Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                    emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c". Cephalon Cy by сасиска#2472')
                else:
                    emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c".')
                await sent.edit(embed = emb)
            elif '--bots' and '--users' in members:
                if filt == None:
                    await ctx.channel.purge(limit = amount, before = sent)
                else:
                    await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower(), before = sent)
                emb = discord.Embed(title = 'Результаты удаления сообщений', color = discord.Color.orange())
                emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{cleared}```')
                if filt:
                    emb.add_field(name = 'Применён фильтр:', value = f'```{filt} ({members})```', inline = True)
                emb.add_field(name = 'Удалены/Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                    emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c". Cephalon Cy by сасиска#2472')
                else:
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
                    emb.add_field(name = 'Применён фильтр:', value = f'```{filt} ({members})```', inline = True)
                emb.add_field(name = 'Удалены/Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                    emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c". Cephalon Cy by сасиска#2472')
                else:
                    emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c".')
                await sent.edit(embed = emb)
            try:
                if '--silent' in members:
                    return
                msg = await client.wait_for('message', timeout = 10, check = lambda message: message.channel == ctx.message.channel and message.author == ctx.author and message.content == 'c')
                emb = discord.Embed(title = 'Результаты удаления сообщений', color = discord.Color.orange())
                emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{cleared}```')
                if filt:
                    emb.add_field(name = 'Применён фильтр:', value = f'```{filt} ({members})```', inline = True)
                emb.add_field(name = 'Удалены/Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                    emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
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
            elif '--everyone' not in members and members != '--silent':
                if filt == None:
                    await ctx.channel.purge(limit = amount, check = lambda m: m.author == member_object)
                else:
                    await ctx.channel.purge(limit = amount, check = lambda m: m.author == member_object and m.content.lower() == filt.lower())
            elif '--bots' and '--users' in members:
                if filt == None:
                    await ctx.channel.purge(limit = amount)
                else:
                    await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower())
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
@client.command()
@commands.cooldown(1, 60, commands.BucketType.user)
async def vote(ctx, *, text):
    await ctx.message.delete()
    emb = discord.Embed(description = 'ГОЛОСОВАНИЕ', colour = discord.Color.orange())
    emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
    emb.add_field(name = 'Голосуем за:', value = text)
    if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
        emb.set_footer(text = '🚫 - воздержусь. Cephalon Cy by сасиска#2472')
    else:
        emb.set_footer(text = '🚫 - воздержусь.')
    sent = await ctx.send(embed = emb)
    await sent.add_reaction('👍')
    await sent.add_reaction('👎')
    await sent.add_reaction('🚫')

@client.command()
async def someone(ctx, *, text: Slapper):
    await ctx.message.delete()
    await ctx.send(embed = text)

@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def rolemembers(ctx, role: discord.Role, member: discord.Member = None):
    await ctx.message.delete()
    emb = discord.Embed(colour = discord.Color.orange())
    if len(role.members) != 0:
        emb.add_field(name = f'Участники с ролью {role} ({len(role.members)})', value = ', '.join([member.mention for member in role.members]))
    else:
        if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
            emb.set_footer(text = 'Обнаружено 0 участников с этой ролью. Cephalon Cy by сасиска#2472')
        else:
            emb.set_footer(text = 'Обнаружено 0 участников с этой ролью.')
    await ctx.send(embed = emb)

@client.command(aliases = ['Guild', 'GUILD'])
@commands.cooldown(1, 5, commands.BucketType.user)
async def guild(ctx):
    await ctx.message.delete()
    guild = ctx.guild
    statuses = [len(list(filter(lambda m: str(m.status) == "online", ctx.guild.members))), len(list(filter(lambda m: str(m.status) == "idle", ctx.guild.members))), len(list(filter(lambda m: str(m.status) == "dnd", ctx.guild.members))), len(list(filter(lambda m: str(m.status) == "offline", ctx.guild.members)))]
    emb = discord.Embed(colour = discord.Color.orange(), timestamp = ctx.message.created_at)
    emb.set_author(name = guild, icon_url = guild.icon_url)
    emb.add_field(name = 'ID сервера', value = guild.id)
    emb.add_field(name = 'Голосовой регион', value = guild.region)
    emb.add_field(name = 'Владелец', value = guild.owner.mention)
    emb.add_field(name = 'Участников', value = guild.member_count)
    emb.add_field(name = 'Из них ботов', value = len(list(filter(lambda m: m.bot, ctx.guild.members))))
    emb.add_field(name = 'Из них людей', value = len(list(filter(lambda m: not m.bot, ctx.guild.members))))
    emb.add_field(name = 'Статусы', value = f"🟢 {statuses[0]} 🟠 {statuses[1]} 🔴 {statuses[2]} ⚫ {statuses[3]}")
    emb.add_field(name = 'Каналов', value = f'Текстовых {len(guild.text_channels)} | Голосовых {len(guild.voice_channels)}')
    emb.add_field(name = f'Роли ({len(guild.roles)-1})', value = ', '.join([role.name for role in guild.roles[1:]]), inline = False)
    now = datetime.datetime.today()
    then = guild.created_at
    delta = now - then
    d = guild.created_at.strftime('%d.%m.%Y %H:%M:%S UTC')
    emb.add_field(name = 'Дата создания сервера', value = f'{delta.days} дней назад. ({d})', inline = False)
    emb.set_thumbnail(url = guild.icon_url)
    if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
    await ctx.send(embed = emb)

@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def role(ctx, *, role: discord.Role):
    await ctx.message.delete()
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
    d = role.created_at.strftime('%d.%m.%Y %H:%M:%S UTC')
    emb.add_field(name = 'Создана', value = f'{delta.days} дня(ей) назад. ({d})', inline = False)
    emb.add_field(name = 'Показывает участников отдельно?', value = role.hoist)
    if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
    await ctx.send(embed = emb)

@client.command(aliases = ['Avatar', 'AVATAR'])
@commands.cooldown(1, 5, commands.BucketType.user)
async def avatar(ctx, member: discord.Member = None):
    await ctx.message.delete()
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
        if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
            emb.set_footer(text = 'По причине того, что аватар анимирован - ссылок на статичные форматы нет! Cephalon Cy by сасиска#2472')
        else:
            emb.set_footer(text = 'По причине того, что аватар анимирован - ссылок на статичные форматы нет!')
    emb.set_image(url = member.avatar_url)
    emb.set_author(name = member)
    await ctx.send(embed = emb)

@client.command(aliases = ['me', 'Me', 'ME', 'About', 'ABOUT'])
@commands.cooldown(1, 5, commands.BucketType.user)
async def about(ctx, member: discord.Member = None):
    await ctx.message.delete()
    if member == None:
        member = ctx.author
    if member.nick == None:
        member.nick = 'Н/Д'
    if member.bot == False:
        bot = 'Неа'
    elif member.bot == True:
        bot = 'Ага'
    emb = discord.Embed(colour = member.color, timestamp = ctx.message.created_at)
    emb.set_author(name = member)
    emb.add_field(name = 'ID', value = member.id)
    now = datetime.datetime.today()
    then = member.created_at
    delta = now - then
    d = member.created_at.strftime('%d.%m.%Y %H:%M:%S UTC')
    then1 = member.joined_at
    delta1 = now - then1
    d1 = member.joined_at.strftime('%d.%m.%Y %H:%M:%S UTC')
    emb.add_field(name = 'Создан', value = f'{delta.days} дня(ей) назад. ({d})', inline = False)
    emb.add_field(name = 'Вошёл', value = f'{delta1.days} дня(ей) назад. ({d1})', inline = False)
    emb.add_field(name = 'Упоминание', value = member.mention)
    emb.add_field(name = 'Raw имя', value = member.name)
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
    if len(member.roles) != 1:
        emb.add_field(name = f'Роли ({len(member.roles)-1})', value = roles, inline = False)
        emb.add_field(name = 'Высшая Роль', value = member.top_role.mention, inline = False)
    emb.set_thumbnail(url = member.avatar_url)
    if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
    await ctx.send(embed = emb)

@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def remind(ctx, time: TimeConverter, *, arg):
    await ctx.message.delete()
    emb = discord.Embed(colour = ctx.author.color, timestamp = ctx.message.created_at)
    emb.add_field(name = 'Напомню через', value = f'{time}s')
    emb.add_field(name = 'О чём напомню?', value = arg)
    if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
    await ctx.send(embed = emb, delete_after = time)
    await asyncio.sleep(time)
    emb = discord.Embed(colour = ctx.author.color, timestamp = ctx.message.created_at)
    emb.add_field(name = 'Напомнил через', value = f'{time}s')
    emb.add_field(name = 'Напоминаю о', value = arg)
    if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
    await ctx.send(f'{ctx.author.mention}', embed = emb)
#Misc

#Fun
@client.command()
async def roll(ctx, first: int = None, second: int = None):
    await ctx.message.delete()
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

@client.command()
async def dotersbrain(ctx):
    await ctx.message.delete()
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

@client.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def niggers(ctx):
    await ctx.message.delete()
    emb = discord.Embed(description = '[осуждающее видео](https://www.youtube.com/watch?v=167apVK8Suw)', colour = discord.Color.orange())
    if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
    await ctx.send(embed = emb)

@client.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def aye_balbec(ctx):
    await ctx.message.delete()
    emb = discord.Embed(colour = ctx.author.color)
    emb.set_image(url = 'https://sun9-61.userapi.com/tja5cuQthduwgxq2yMigLiUxfYq_5fqiA6cJWg/sZOkbPajoSY.jpg')
    if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
    await ctx.send(embed = emb)

@client.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def rp(ctx):
    await ctx.message.delete()
    emb = discord.Embed(description = '[Ныа](https://www.youtube.com/watch?v=idmTSW9mfYI)', colour = discord.Color.orange())
    if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
    await ctx.send(embed = emb)

@client.command(aliases = ['.rap'])
@commands.cooldown(1, 5, commands.BucketType.user)
async def rap(ctx):
    await ctx.message.delete()
    emb = discord.Embed(colour = ctx.author.color)
    emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
    emb.set_image(url = 'https://thumbs.gfycat.com/MessyCarefreeHousefly-size_restricted.gif')
    if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
    await ctx.send(embed = emb)

@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def zatka(ctx):
    await ctx.message.delete()
    emb = discord.Embed(title = 'Форма заявки для Набор кадров', colour = ctx.author.color)
    emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
    emb.add_field(name = '(1). ZATKA в STEAM.  ZATKA_KING#8406 в Discord.', value = 'возраст 14+  часовой пояс IL +0.', inline = False)
    emb.add_field(name = '(2). Интересующая управление:', value = 'Discord', inline = False)
    emb.add_field(name = '(3). Опыт администрирования:', value = 'Есть.', inline = False)
    emb.add_field(name = 'творческие:', value = 'Есть.', inline = False)
    emb.add_field(name = 'технические навыки:', value = 'Нет.', inline = False)
    emb.add_field(name = '(4). Сколько часов готовы уделять работе', value = '[ 15+ в неделю ]', inline = False)
    emb.add_field(name = 'в какое время дня свободны', value = '16:00 до 22:00+', inline = False)
    if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
    await ctx.send(embed = emb)

@client.command(aliases = ['Cu', 'CU'])
@commands.cooldown(1, 5, commands.BucketType.user)
async def cu(ctx):
    await ctx.message.delete()
    await ctx.send('Медь')

@client.command(aliases = ['c', 'C', 'coin', 'Coin', 'COIN', 'Coinflip', 'COINFLIP'])
@commands.cooldown(3, 3, commands.BucketType.user)
async def coinflip(ctx):
    await ctx.message.delete()
    emb = discord.Embed(description = 'Орёл!', colour = discord.Color.orange())
    emb.set_image(url = 'https://cdn.discordapp.com/attachments/524213591084105729/763835275930632252/-removebg-preview.png')
    emb1 = discord.Embed(description = 'Решка!', colour = discord.Color.orange())
    emb1.set_image(url = 'https://cdn.discordapp.com/attachments/524213591084105729/763837699240099890/-removebg-preview.png')
    choices = [emb, emb1]
    rancoin = random.choice(choices)
    if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        emb1.set_footer(text = 'Cephalon Cy by сасиска#2472')
    await ctx.send(embed = rancoin)
#Fun

#Embeds
@client.command(aliases = ['ctx'])
@commands.cooldown(1, 5, commands.BucketType.user)
async def content(ctx, arg, channel: discord.TextChannel = None):
    await ctx.message.delete()
    if channel == None:
        channel = ctx.message.channel
    message = await channel.fetch_message(id = arg)
    if message.author.id in botversions:
        if message.embeds == []:
            if '@everyone' in message.content:
                await ctx.send(f'```cy/say --everyone {message.content.strip()[10:].strip()}```')
            else:
                await ctx.send(f'```cy/say {message.content}```')
        else:
            for emb in message.embeds:
                if '@everyone' in message.content:
                    if emb.image.url != emb.Empty:
                        img = f' | img& {emb.image.url}'
                    else:
                        img = ''
                    if emb.thumbnail.url != emb.Empty:
                        th = f' | th& {emb.thumbnail.url}'
                    else:
                        th = ''
                    if emb.description != emb.Empty:
                        d = f' | d& {emb.description}'
                    else:
                        d = ''
                    if emb.title != emb.Empty:
                        t = f'| t& {emb.title}'
                    else:
                        t = ''
                    await ctx.send(f'```py\ncy/say --everyone {t}{d}{th}{img}```')
                else:
                    if emb.image.url != emb.Empty:
                        img = f' | img& {emb.image.url}'
                    else:
                        img = ''
                    if emb.thumbnail.url != emb.Empty:
                        th = f' | th& {emb.thumbnail.url}'
                    else:
                        th = ''
                    if emb.description != emb.Empty:
                        d = f' | d& {emb.description}'
                    else:
                        d = ''
                    if emb.title != emb.Empty:
                        t = f't& {emb.title}'
                    else:
                        t = ''
                    await ctx.send(f'```cy/say {t}{d}{th}{img}```')
    else:
        if message.embeds == []:
            if '```' in message.content:
                await ctx.send(f'{message.author} {message.content}')
            else:
                await ctx.send(f'```@{message.author} {message.content}```')
        else:
            for emb in message.embeds:
                if message.content == None:
                    content = ''
                else:
                    content = f'content {message.content}'
                if emb.title != emb.Empty:
                    title = f' title {emb.title}'
                else:
                    title = ''
                if emb.description != emb.Empty:
                    description = f' description {emb.description}'
                else:
                    description = ''
                if emb.footer.text != emb.Empty:
                    footer = f' footer {emb.footer.text}'
                else:
                    footer = ''
                if emb.image.url != emb.Empty:
                    image = f' image {emb.image.url}'
                else:
                    image = ''
                if emb.thumbnail.url != emb.Empty:
                    thumb = f' thumbnail {emb.thumbnail.url}'
                else:
                    thumb = ''
                if emb.color != emb.Empty:
                    color = f' color {emb.color}'
                else:
                    color = ''
                if emb.author.name != emb.Empty:
                    author = f' author {emb.author.name}'
                else:
                    author = ''
                await ctx.send(f'```{content}{title}{description}{footer}{color}{author}{image}{thumb}```')

@client.command(aliases = ['Say', 'SAY'])
@commands.has_permissions(manage_channels = True)
async def say(ctx, *, msg):
    await ctx.message.delete()
    title = description = image = thumbnail = color = None
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
        elif i.strip().lower().startswith('c&'):
            color = i.strip()[2:].strip()
    if color == None:
        color = 0x2f3136
    else:
        color = int('0x' + color, 16)
    emb = discord.Embed(title = title, description = description, color = color)
    for i in embed_values:
        if ctx.author.id != 338714886001524737:
            emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
        if ctx.author.id == 338714886001524737 and ctx.guild.id != 693929822543675455:
            choices = ['х̙̣̲̪͋̃ͬͫ́͞͡ы̢͇̳̽̋͌ͨͪ͟͠х̩̜̞̝̗͌ͪͦ͆а̘͔̮̍͆ͮͫ̎͘', 'а͖̂͐̄̓͗͗̇ͪ̀̕͜а̷̨͙̩͔̜̹̗̎а́͋̐͆́͝҉̛̩̳̰̲̳̭̟̖͕а̘̠͖̝̰͇̜̭͌̿̂̋ͫ̂ͯ͊́̕͝ӓ́͒̾̇҉͎͙̙̮͓ͅа̙͖̻͈̘ͣ̾̊̊̾̊̍́͢а̼̬͇̱̞ͬ̌̏̉̋̚̚͘͝а̌̅̓͆͊̆҉̤̲̦̰̹̘͚̼͈͘͢а͈̹͔̜͓̙͖̍ͯ̽̓͜͞а̷̞̟̦̮͉̺̹͊̿̊̽̄̆͒̕ͅ', 'ч̮̲̤͒̂͌͠м͔̗̳̤͈̘̻̦̪͊̂͘͟͜о͚̭ͬ͗ͯ͢']
            author = random.choice(choices)
            emb.set_author(name = author, icon_url = client.user.avatar_url)
        else:
            emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
        if image:
            emb.set_image(url = image)
        if thumbnail:
            emb.set_thumbnail(url = thumbnail)
        if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
            emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        if 't&' not in msg and 'd&' not in msg and 'img&' not in msg and 'th&' not in msg and 'c&' not in msg:
            if '--everyone' in msg:
                return await ctx.send(f'@everyone {msg.strip()[10:].strip()}')
            else:
                return await ctx.send(msg)
        else:
            if '--everyone' in msg:
                return await ctx.send('@everyone', embed = emb)
            else:
                return await ctx.send(embed = emb)

@client.command(aliases = ['Edit', 'EDIT'])
@commands.has_permissions(manage_channels = True)
async def edit(ctx, arg, *, msg = None):
    await ctx.message.delete()
    message = await ctx.fetch_message(id = arg)
    if message:
        title = description = image = thumbnail = color = author = None
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
            elif i.strip().lower().startswith('c&'):
                color = i.strip()[2:].strip()
        if color == None:
            color = 0x2f3136
        else:
            color = int('0x' + color, 16)
        emb = discord.Embed(title = title, description = description, color = color)
        for i in embed_values:
            if ctx.author.id != 338714886001524737:
                emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            if ctx.author.id == 338714886001524737 and ctx.guild.id != 693929822543675455:
                choices = ['х̙̣̲̪͋̃ͬͫ́͞͡ы̢͇̳̽̋͌ͨͪ͟͠х̩̜̞̝̗͌ͪͦ͆а̘͔̮̍͆ͮͫ̎͘', 'а͖̂͐̄̓͗͗̇ͪ̀̕͜а̷̨͙̩͔̜̹̗̎а́͋̐͆́͝҉̛̩̳̰̲̳̭̟̖͕а̘̠͖̝̰͇̜̭͌̿̂̋ͫ̂ͯ͊́̕͝ӓ́͒̾̇҉͎͙̙̮͓ͅа̙͖̻͈̘ͣ̾̊̊̾̊̍́͢а̼̬͇̱̞ͬ̌̏̉̋̚̚͘͝а̌̅̓͆͊̆҉̤̲̦̰̹̘͚̼͈͘͢а͈̹͔̜͓̙͖̍ͯ̽̓͜͞а̷̞̟̦̮͉̺̹͊̿̊̽̄̆͒̕ͅ', 'ч̮̲̤͒̂͌͠м͔̗̳̤͈̘̻̦̪͊̂͘͟͜о͚̭ͬ͗ͯ͢']
                author = random.choice(choices)
                emb.set_author(name = author, icon_url = client.user.avatar_url)
            else:
                emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            if image:
                emb.set_image(url = image)
            if thumbnail:
                emb.set_thumbnail(url = thumbnail)
            if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
            if 't&' not in msg and 'd&' not in msg and 'img&' not in msg and 'th&' not in msg and 'c&' not in msg:
                if message.author == client.user:
                    if '--clean' in msg:
                        await message.edit(content = None)
                    if '--delete' in msg:
                        await message.delete()
                    if '--noembed' in msg:
                        if message.embeds != []:
                            await message.edit(embed = None)
                        else:
                            return await ctx.send(f'{ctx.author.mention}, нечего удалять. Возможно, вы имели ввиду cy/edit {message.id} --delete ?', delete_after = 8)
                    if '--empty-embed' in msg:
                        if message.embeds != []:
                            emb = discord.Embed(title = None, description = None, color = ctx.author.color)
                            emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                            await message.edit(embed = emb)
                        else:
                            return await ctx.send(f'{ctx.author.mention}, нечего очищать. Возможно, вы имели ввиду cy/edit {message.id} --delete ?')
                    else:
                        await message.edit(content = msg)
                else:
                    return await ctx.send(f'{message.id} не является сообщением от {client.user}')
            else:
                if message.author == client.user:
                    if '--clean' in msg:
                        await message.edit(content = None, embed = emb)
                    if '--noembed' in msg:
                        if message.embeds != []:
                            await message.edit(embed = None)
                        else:
                            return await ctx.send(f'{ctx.author.mention}, нечего удалять. Возможно, вы имели ввиду cy/edit {message.id} --delete ?', delete_after = 8)
                    else:
                        await message.edit(embed = emb)
                else:
                    return await ctx.send(f'{message.id} не является сообщением от {client.user}')
    else:
        await ctx.send(f'сообщение {message.id} не обнаружено.')
#Embeds

#Cephalon
@client.command()
async def setup(ctx):
    await ctx.message.delete()
    role3 = discord.utils.get(ctx.guild.roles, name = '----------Предупреждения----------')
    role1 = discord.utils.get(ctx.guild.roles, name = '1')
    role2 = discord.utils.get(ctx.guild.roles, name = '2')
    role = discord.utils.get(ctx.guild.roles, name = 'Muted')
    if role and role1 and role2 and role3 != None:
        emb = discord.Embed(description = 'Все нужные роли уже присутсвуют на сервере.', color = discord.Color.orange())
        await ctx.send(embed = emb)
    emb = discord.Embed(description = 'С написанием этой команды на сервер будут добавлены несколько ролей, если их нет (4). Они нужны для правильной работы авто и обычного мута. Не следует их изменять или удалять, так как они будут созданы снова, из-за чего будет много одинаковых ролей.', color = discord.Color.orange())
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
    await ctx.message.delete()
    token = ''.join([secrets.choice('QWERTYUIOPASDFGHJKLZXCVBNM1234567890') for i in range(4)])
    token1 = ''.join([secrets.choice('QWERTYUIOPASDFGHJKLZXCVBNM1234567890') for i in range(4)])
    token2 = ''.join([secrets.choice('QWERTYUIOPASDFGHJKLZXCVBNM1234567890') for i in range(4)])
    await ctx.send(f'```{token}-{token1}-{token2}```')

@client.command(aliases = ['Join', 'JOIN'])
async def join(ctx):
    await ctx.message.delete()
    if ctx.author.voice and ctx.author.voice.channel:
        channel = ctx.author.voice.channel
    else:
        emb = discord.Embed(description = 'Ты должен быть в канале, чтобы использовать это.', colour = discord.Color.orange())
        if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
            emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb)
    global vc
    vc = await channel.connect()

@client.command()
async def leave(ctx):
    await ctx.message.delete()
    if ctx.author.voice and ctx.author.voice.channel:
        pass
    else:
        emb = discord.Embed(description = 'Ты должен быть в канале, чтобы использовать это.', colour = discord.Color.orange())
        if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
            emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb)
    await vc.disconnect()

@client.command(aliases = ['Ping', 'PING'])
@commands.cooldown(1, 5, commands.BucketType.user)
async def ping(ctx):
    await ctx.message.delete()
    emb = discord.Embed(description = f'`fetching..`', colour = discord.Color.orange())
    emb1 = discord.Embed(description = f'Pong!  `{round(client.latency * 1000)} ms`', colour = discord.Color.orange())
    message = await ctx.send(embed = emb)
    if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        emb1.set_footer(text = 'Cephalon Cy by сасиска#2472')
    await asyncio.sleep(client.latency)
    await message.edit(embed = emb1)

@client.command(aliases = ['invcy'])
@commands.cooldown(1, 3, commands.BucketType.user)
async def invite(ctx, arg = None):
    await ctx.message.delete()
    if arg == None:
        emb = discord.Embed(description = '[Ссылка](https://discord.com/api/oauth2/authorize?client_id=694170281270312991&permissions=8&scope=bot%20applications.commands) для приглашения Cy на сервера.', colour = discord.Color.orange())
        if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
            emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb)
    if arg == 'beta':
        emb = discord.Embed(description = '[Ссылка](https://discord.com/oauth2/authorize?client_id=764882153812787250&scope=bot&permissions=8&scope=bot%20applications.commands) для приглашения Cy Beta на сервера.', color = discord.Color.orange())
        if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
            emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb)
    if arg == 'pro':
        if ctx.guild.id not in guilds:
            emb = discord.Embed(description = f'Сервер `{ctx.guild}` не имеет активных подписок. Купить можно по [Ссылке](https://www.patreon.com/cephaloncy) Преимущества: пинг не более 25ms, больший аптайм, защита от несанкционированного добавления на сервера.', colour = discord.Color.orange())
            await ctx.send(embed = emb)
        else:
            emb = discord.Embed(description = '[Ссылка](https://discord.com/oauth2/authorize?client_id=762015251264569352&scope=bot&permissions=8&scope=bot%20applications.commands) для приглашения Cy PRO на сервера.', color = discord.Color.orange())
            await ctx.send(embed = emb)

@client.command(aliases = ['Info', 'INFO'])
@commands.cooldown(1, 5, commands.BucketType.user)
async def info(ctx):
    await ctx.message.delete()
    emb = discord.Embed(colour = discord.Color.orange())
    emb.set_author(name = client.user.name, url = 'https://warframe.fandom.com/wiki/Cephalon_Cy', icon_url = client.user.avatar_url)
    emb.add_field(name = 'Версия', value = '0.12.9.10519')
    emb.add_field(name = 'Написан на', value = 'discord.py v1.6.0')
    emb.add_field(name = 'Разработчик', value = '[сасиска#2472](https://discord.com/users/338714886001524737)')
    if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
        emb.add_field(name = 'Сервер', value = 'Данный сервер не принадлежит моему создателю или его знакомым. Все эмбед выводы будут иметь футер с текстом `Cephalon Cy by сасиска#2472`')
    if ctx.guild.id == 693929822543675455:
        emb.add_field(name = 'Принадлежность', value = 'Это - мой основной сервер.')
    if ctx.guild.id == 735874149578440855:
        emb.add_field(name = 'Тестирование', value = 'Это - мой тестовый сервер.')
    emb.add_field(name = 'Веб-сайт', value = '```http://ru-unioncraft.ru/```', inline = False)
    emb.add_field(name = 'Раздражаю', value = f'{len(client.users)} человек')
    emb.add_field(name = 'Существую на', value = f'{len(client.guilds)} серверах')
    if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
        emb.set_footer(text = 'Данное приложение не имеет никакого причастия к игре Warframe. Cephalon Cy by сасиска#2472', icon_url = 'https://i.playground.ru/p/yVaOZNSTdgUTxmzy_qvzzQ.png')
    else:
        emb.set_footer(text = 'Данное приложение не имеет никакого причастия к игре Warframe.', icon_url = 'https://i.playground.ru/p/yVaOZNSTdgUTxmzy_qvzzQ.png')
    await ctx.send(embed = emb)

@client.command(aliases = ['version'])
@commands.cooldown(1, 3, commands.BucketType.user)
async def botver(ctx):
    emb = discord.Embed(title = '0.12.9.10519', description = 'Небольшие исправления, в целом никак не связанные с работой бота', color = discord.Color.orange())
    await ctx.send(embed = emb)
    
@client.command(aliases = ['Help', 'HELP'])
@commands.cooldown(1, 3, commands.BucketType.user)
async def help(ctx, arg = None):
    await ctx.message.delete()
    if arg == None:
        emb = discord.Embed(title = client.user.name, description = 'Вот команды, что я могу исполнить.\n||Некоторые улучшения появятся после верификации.||', colour = discord.Color.orange())
        emb.add_field(name = 'Cephalon', value = '`info`, `invite`, `join`, `leave`, `ping`, `setup`', inline = False)
        emb.add_field(name = 'Embeds', value = '`content`, `edit`, `say`', inline = False)
        emb.add_field(name = 'Fun', value = '`aye_balbec`, `cu`, `coinflip`, `dotersbrain`, `niggers`, `rp`, `rap`, `roll`, `zatka`', inline = False)
        emb.add_field(name = 'Mod', value = '`ban`, `clear`, `dm`, `give`, `kick`, `mute`, `take`, `unmute`', inline = False)
        emb.add_field(name = 'Misc', value = '`about`, `avatar`, `guild`, `remind`, `role`, `rolemembers`, `someone`, `vote`', inline = False)
        emb.add_field(name = 'ᅠ', value = 'Назовите комнату `Создать канал` (**регистр обязателен**), чтобы бот автоматически создавал для вас временные каналы, которые будут удаляться после того, как все люди выйдут из канала.', inline = False)
        emb.add_field(name = 'ᅠ', value = '**Используйте** `cy/help [команда/категория]` **для подробностей использования.**\n\n**[Ссылка-приглашение](https://discord.com/oauth2/authorize?client_id=694170281270312991&scope=bot&permissions=8)**', inline = False)
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb)
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
        await ctx.send('```apache\ncy/say [t& title текст] | [d& description текст] | [c& HEX цвет] | [th& ссылка на картинку справа] | [img& ссылка на картинку снизу]\ncy/say t& title | d& description | img& https://cdn.discordapp.com/avatars/694170281270312991/e27e0909a72cdc6a98d4234ecbfe9a91.webp?size=1024\ncy/say --everyone | t& title | d& description\ncy/say [текст]\ncy/say --everyone [текст]\n(вам НЕ обязательно писать все аргументы в данном порядке, пишите только те, что вам нужны в любом порядке) ([] - опционально, / - или)\nperms = manage_channels```')
    elif arg == 'edit':
        await ctx.send('```apache\ncy/edit <ID> [t& title текст] | [d& description текст] | [c& HEX цвет] | [th& ссылка на картинку справа] | [img& ссылка на картинку снизу]\ncy/edit <ID> [текст]\ncy/edit <ID> --clean | d& description\ncy/edit <ID> --clean\ncy/edit <ID> --noembed\ncy/edit <ID> --empty-embed\ncy/edit <ID> --delete\n(--clean удалит контент над эмбедом, --noembed удалит эмбед, работает только если есть эмбед, --empty-embed опустошит эмбед, --delete удалит сообщение) ([] - опционально, <> - обязательно, / - или)\nperms = manage_channels```')
    elif arg == 'give':
        await ctx.send('```apache\ncy/give <@пинг/имя/ID> <@роль/имя роли/ID роли> (<> - обязательно, / - или)\nperms = manage_channels```')
    elif arg == 'kick':
        await ctx.send('```apache\ncy/kick <@пинг/имя/ID> [причина] ([] - опционально, <> - обязательно, / - или)\nperms = kick_members```')
    elif arg == 'mute':
        await ctx.send('```apache\ncy/mute <@пинг/имя/ID> <время(s/m/h/d(15s, 5m, 1h, 5d))> [причина] ([] - опционально, <> - обязательно, / - или)\nperms = view_audit_log```')
    elif arg == 'remind':
        await ctx.send('```apache\ncy/remind <время(s/m/h/d(15s, 5m, 1h, 5d))> <текст> (<> - обязательно, / - или)```')
    elif arg == 'role':
        await ctx.send('```apache\ncy/role <@роль/имя роли/ID роли> (<> - обязательно, / - или)```')
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
        await ctx.send('```py\ncontent(ctx) - позволяет увидеть raw контент сообщения\nedit - редактирует сообщение, отправленное от лица бота. Иные сообщения редактировать нельзя.\nsay - используется для написания как текстов, так и эмбедов.```')
    elif arg == 'Cephalon' or arg == 'cephalon':
        await ctx.send('```py\ninfo - информация о боте\ninvite - ссылка-приглашения бота\njoin - бот зайдёт в ваш голосовой канал\nleave - бот из него выйдет\nping - проверяет задержку клиента бота.```')
    elif arg == 'Fun' or arg == 'fun':
        await ctx.send('```py\naye_balbec - я не ангел и не бес, просто..\ncu - медь\ncoinflip(c, coin) - подкидывает монетку\ndotersbrain - проверка на мозг дотера\nniggers - осуждаем!\nrp - ультимативный гайд по рп отыгровке\nrap - .rap\nzatka - Форма заявки для набор кадров```')
    elif arg == 'Mod' or arg == 'mod':
        await ctx.send('```py\nban - бан участника\nclear - очистка чата, не более 300!\ndm - пишет в лс участнику написанный текст\ngive - выдаёт роль\nkick - кик участника\nmute - мут участника\ntake - забирает роль\nunmute - снятие мута участника.```')
    elif arg == 'Misc' or arg == 'misc':
        await ctx.send('```py\nabout - информация о человеке\navatar - аватар человека\nguild - информация о сервере\nremind - напоминание о событии\nrole - информация о роли\nrolemembers - участники роли\nsomeone - упоминание someone\nvote - голосование за что-то.```')
    elif arg == 'All' or arg == 'all':
        await ctx.send('```py\ninfo - информация о боте\ninvite - ссылка-приглашения бота\njoin - бот зайдёт в ваш голосовой канал\nleave - бот из него выйдет\nping - проверяет задержку клиента бота.```')
        await ctx.send('```py\ncontent(ctx) - позволяет увидеть raw контент сообщения\nedit - редактирует сообщение, отправленное от лица бота. Иные сообщения редактировать нельзя.\nsay - используется для написания как текстов, так и эмбедов.```')
        await ctx.send('```py\naye_balbec - я не ангел и не бес, просто..\ncu - медь\ncoinflip(c, coin) - подкидывает монетку\ndotersbrain - проверка на мозг дотера\nniggers - осуждаем!\nrp - ультимативный гайд по рп отыгровке\nrap - .rap\nzatka - Форма заявки для набор кадров```')
        await ctx.send('```py\nban - бан участника\nclear - очистка чата, не более 300!\ndm - пишет в лс участнику написанный текст\ngive - выдаёт роль\nkick - кик участника\nmute - мут участника\ntake - забирает роль\nunmute - снятие мута участника.```')
        await ctx.send('```py\nabout - информация о человеке\navatar - аватар человека\nguild - информация о сервере\nremind - напоминание о событии\nrole - информация о роли\nrolemembers - участники роли\nsomeone - упоминание someone\nvote - голосование за что-то.```')
    else:
        emb = discord.Embed(description = f'Команда `{arg}` не обнаружена.', color = discord.Color.orange())
        await ctx.send(embed = emb)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.message.delete()
        emb = discord.Embed(description = f'{ctx.author.mention}, команда не обнаружена. Может, пропишите cy/help?\n||{ctx.message.content}||', colour = discord.Color.orange())
        await ctx.send(embed = emb)
    elif isinstance(error, commands.MissingPermissions):
        await ctx.message.delete()
        emb = discord.Embed(description = f'{ctx.author.mention}, у вас недостаточно прав на выполнение команды `{ctx.command.name}`', colour = discord.Color.orange())
        await ctx.send(embed = emb)
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.message.delete()
        s = error.retry_after
        choises = ['Its not time yet..', 'I am not ready..', 'Not yet..']
        choices1 = ['Its. Not. Time. Yet.', 'I. Am. Not. Ready.', 'Not. Yet.']
        choices2 = ['ITS NOT TIME YET!', 'I AM NOT READY!', 'NOT YET!']
        rand = random.choice(choises)
        rand1 = random.choice(choices1)
        rand2 = random.choice(choices2)
        if round(s) >= 5:
            emb = discord.Embed(description = f'{rand} Команда `{ctx.command.name}` будет доступна через {round(s)} секунд..', colour = discord.Color.orange())
            if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
            await ctx.send(embed = emb)
        elif round(s) >= 2:
            emb = discord.Embed(description = f'{rand1} Команда `{ctx.command.name}` будет доступна через {round(s)} секунды.', colour = discord.Color.orange())
            if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
            await ctx.send(embed = emb)
        elif round(s) >= 1:
            emb = discord.Embed(description = f'{rand2} Команда `{ctx.command.name}` будет доступна через {round(s)} секунду!', colour = discord.Color.orange())
            if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
            await ctx.send(embed = emb)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.message.delete()
        if ctx.command.name == 'clear':
            await ctx.send('```apache\ncy/clear <количество> [автор] [фильтр]\ncy/clear 100\ncy/clear 10 @сасиска\ncy/clear 50 --everyone хыха\ncy/clear 30 --bots\ncy/clear 15 --users\ncy/clear 5 --silent\ncy/clear 200 "--silent --everyone" хыха\n\n--everyone удалит сообщения от всех\n--bots удалит сообщения только от ботов\n--users удалит сообщения только от участников\n--silent не оставит доказательств выполнения команды, исключение - количество >= 10\n\nПри указании автора не будет удалено столько сообщений, сколько было указано, будет удалено столько, сколько будет найдено в пределах этих сообщений.\nСообщения старше 2 недель будут удалены не сразу - лимит discord API\nПри удалении более 100 сообщений нужно подтверждение владельца сервера.\nТолько владелец может удалять от 250 сообщений за раз.\nНе более 300!\n([] - опционально, <> - обязательно, / - или)\nperms = adminstrator```')
        elif ctx.command.name == 'say':
            await ctx.send('```apache\ncy/say [t& title текст] | [d& description текст] | [c& HEX цвет] | [th& ссылка на картинку справа] | [img& ссылка на картинку снизу]\ncy/say t& title | d& description\ncy/say --everyone | t& title | d& description\ncy/say [текст]\ncy/say --everyone [текст]\n(вам НЕ обязательно писать все аргументы в данном порядке, пишите только те, что вам нужны в любом порядке) ([] - опционально)\nperms = manage_channels```')
        elif ctx.command.name == 'edit':
            await ctx.send('```apache\ncy/edit <ID> [t& title текст] | [d& description текст] | [c& HEX цвет] | [th& ссылка на картинку справа] | [img& ссылка на картинку снизу]\ncy/edit <ID> [текст]\ncy/edit <ID> --clean | d& description\ncy/edit <ID> --clean\ncy/edit <ID> --noembed\ncy/edit <ID> --empty-embed\ncy/edit <ID> --delete\n(--clean удалит контент над эмбедом, --noembed удалит эмбед, работает только если есть эмбед, --empty-embed опустошит эмбед, --delete удалит сообщение) ([] - опционально, <> - обязательно)\nperms = manage_channels```')
        elif ctx.command.name == 'ban':
            await ctx.send('```apache\ncy/ban <@пинг/имя/ID> [причина/--soft --reason]\ncy/ban 185476724627210241 --soft --reason лошара\ncy/ban @сасиска чмо\ncy/ban "Sgt White"\ncy/ban @крипочек --soft\n\nПри использовании --soft обязательно указывать --reason ПОСЛЕ --soft\n\n([] - опционально, <> - обязательно, / - или)\nperms = ban_members```')
        else:
            emb = discord.Embed(description = f'{ctx.author.mention}, обнаружен недостаток аргументов для `{ctx.command.name}`. Попробуйте cy/help `{ctx.command.name}`', colour = discord.Color.orange())
            if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
                emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
            await ctx.send(embed = emb)
    elif isinstance(error, commands.BadArgument):
        await ctx.message.delete()
        emb = discord.Embed(description = f'{ctx.author.mention}, обнаружен неверный аргумент для `{ctx.command.name}`. Попробуйте cy/help `{ctx.command.name}`', colour = discord.Color.orange())
        if ctx.guild.owner.id != client.owner_id and ctx.guild.owner.id not in friends:
            emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb)

t = os.environ.get('t')
client.run(t)
