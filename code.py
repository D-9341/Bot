import asyncio
import datetime
import json
import os
import random
import re
import discord
import secrets
from discord.ext import commands
from discord.utils import get

client = commands.Bot(command_prefix = commands.when_mentioned_or('cy/'), intents = discord.Intents.all(), owner_id = 338714886001524737)
client.remove_command('help')

time_regex = re.compile(r"(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {'h': 3600, 's': 1, 'm': 60, 'd': 86400}

class TimeConverter(commands.Converter):
    async def convert(self, ctx, argument):
        args = argument.lower()
        time = 0
        matches = re.findall(time_regex, args)
        for key, value in matches:
            try:
                time += time_dict[value] * float(key)
            except KeyError:
                await ctx.send(f'{value} не является правильным аргументом! Правильные: h|m|s|d')
            except ValueError:
                await ctx.send(f'{key} не число!')
        return time

class Slapper(commands.Converter):
    async def convert(self, ctx, argument):
        mention = random.choice(ctx.guild.members)
        emb = discord.Embed(description = f'{argument}', colour =  ctx.author.colour, timestamp = ctx.message.created_at)
        emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
        return await ctx.send(f'@someone ||{mention.mention}||', embed = emb)

#Events
@client.event
async def on_command_completion(ctx):
    lchannel = client.get_channel(714175791033876490)
    emb = discord.Embed(title = 'ВЫПОЛНЕНИЕ_КОМАНДЫ', color = discord.Color.orange())
    emb.add_field(name = 'НАЗВАНИЕ', value = f'```{ctx.command.name}```')
    emb.add_field(name = 'ИСПОЛНИТЕЛЬ', value = f'{ctx.author.mention} ({ctx.author})')
    emb.add_field(name = 'СЕРВЕР', value = ctx.guild.name, inline = False)
    emb.add_field(name = 'КАНАЛ', value = f'{ctx.channel.name} ({ctx.channel.mention})', inline = False)
    await lchannel.send(embed = emb)

@client.event
async def on_guild_channel_delete(channel):
    if channel.guild.id == 693929822543675455:
        lchannel = client.get_channel(714175791033876490)
        emb = discord.Embed(title = 'УДАЛЕНИЕ_КАНАЛА', color = discord.Color.orange(), timestamp = datetime.datetime.utcnow())
        emb.add_field(name = 'НАЗВАНИЕ', value = channel.name)
        if channel.type == discord.ChannelType.voice:
            typ = 'ГОЛОСОВОЙ'
        if channel.type == discord.ChannelType.text:
            typ = 'ТЕКСТОВЫЙ'
        emb.add_field(name = 'ТИП', value = typ)
        emb.set_footer(text = f'ID: {channel.id}')
        await lchannel.send(embed = emb)

@client.event
async def on_guild_channel_create(channel):
    if channel.guild.id == 693929822543675455:
        lchannel = client.get_channel(714175791033876490)
        emb = discord.Embed(title = 'СОЗДАНИЕ_КАНАЛА', color = discord.Color.orange(), timestamp = datetime.datetime.utcnow())
        emb.add_field(name = 'НАЗВАНИЕ', value = channel.name)
        if channel.type == discord.ChannelType.voice:
            typ = 'ГОЛОСОВОЙ'
        if channel.type == discord.ChannelType.text:
            typ = 'ТЕКСТОВЫЙ'
        emb.add_field(name = 'ТИП', value = typ)
        emb.set_footer(text = f'ID: {channel.id}')
        await lchannel.send(embed = emb)

@client.event
async def on_guild_channel_update(before, after):
    channel = client.get_channel(714175791033876490)
    if before.guild.id == 693929822543675455:
        if before.type == discord.ChannelType.voice:
            emb = discord.Embed(title = r'ИЗМЕНЕНИЕ\_ГОЛОСОВОГО_КАНАЛА', color = discord.Color.orange(), timestamp = datetime.datetime.utcnow())
            if before.name != after.name:
                emb.add_field(name = 'НАЗВАНИЕ_ДО', value = before.name)
                emb.add_field(name = 'НАЗВАНИЕ_ПОСЛЕ', value = after.name)
                emb.set_footer(text = f'ID: {before.id}')
                await channel.send(embed = emb)
            if before.position != after.position:
                emb.add_field(name = 'НАЗВАНИЕ', value = before.name, inline = False)
                emb.add_field(name = 'ПОЗИЦИЯ_ДО', value = before.position)
                emb.add_field(name = 'ПОЗИЦИЯ_ПОСЛЕ', value = after.position)
                emb.set_footer(text = f'ID: {before.id}')
                await channel.send(embed = emb)
        elif before.type == discord.ChannelType.text:
            emb = discord.Embed(title = r'ИЗМЕНЕНИЕ\_ТЕКСТОВОГО_КАНАЛА', color = discord.Color.orange(), timestamp = datetime.datetime.utcnow())
            if before.name != after.name:
                emb.add_field(name = 'НАЗВАНИЕ_ДО', value = before.name)
                emb.add_field(name = 'НАЗВАНИЕ_ПОСЛЕ', value = after.name)
                emb.set_footer(text = f'ID: {before.id}')
                await channel.send(embed = emb)
            if before.position != after.position:
                emb.add_field(name = 'НАЗВАНИЕ', value = before.name, inline = False)
                emb.add_field(name = 'ПОЗИЦИЯ_ДО', value = before.position)
                emb.add_field(name = 'ПОЗИЦИЯ_ПОСЛЕ', value = after.position)
                emb.set_footer(text = f'ID: {before.id}')
                await channel.send(embed = emb)

@client.event
async def on_member_update(before, after):
    channel = client.get_channel(714175791033876490)
    if before.bot == False:
        chmo = 'УЧАСТНИК'
    else:
        chmo = 'БОТ'
    if before.guild.id == 693929822543675455:
        if before.nick != after.nick:
            emb = discord.Embed(title = 'ИЗМЕНЕНИЕ_НИКНЕЙМА', color = discord.Colour.orange(), timestamp = datetime.datetime.utcnow())
            if before.nick == None:
                before.nick = 'НЕ\_БЫЛ_УКАЗАН'
            if after.nick == None:
                after.nick = 'НЕ_УКАЗАН'
            emb.add_field(name = f'{chmo}', value = before)
            emb.add_field(name = 'БЫЛ', value = before.nick)
            emb.add_field(name = 'СТАЛ', value = after.nick)
            emb.set_footer(text = f'ID: {before.id}')
            await channel.send(embed = emb)
        if before.roles != after.roles:
            a = set(before.roles)
            b = set(after.roles)
            async for event in before.guild.audit_logs(limit = 1, action = discord.AuditLogAction.member_role_update):
                if a > b:
                    emb = discord.Embed(title = 'РОЛЬ_ЗАБРАНА', description = ', '.join([getattr(r, "mention", r.id) for r in event.before.roles or event.after.roles]), colour = discord.Color.orange(), timestamp = datetime.datetime.utcnow())
                elif a < b:
                    emb = discord.Embed(title = 'РОЛЬ_ВЫДАНА', description = ', '.join([getattr(r, "mention", r.id) for r in event.before.roles or event.after.roles]), colour = discord.Color.orange(), timestamp = datetime.datetime.utcnow())
                emb.set_author(name = before, icon_url = before.avatar_url)
                emb.set_footer(text = f'ID: {before.id}')
            await channel.send(embed = emb)

@client.event
async def on_member_join(member):
    if member.bot == False:
        chmo = 'УЧАСТНИК'
    else:
        chmo = 'БОТ'
    lchannel = client.get_channel(714175791033876490)
    emb = discord.Embed(title = f'{chmo}\_ЗАШЁЛ\_НА_СЕРВЕР', colour = discord.Color.orange(), timestamp = datetime.datetime.utcnow())
    emb.add_field(name = f'{chmo}', value = member)
    emb.add_field(name = 'УПОМИНАНИЕ', value = member.mention)
    emb.add_field(name = 'СЕРВЕР', value = member.guild.name)
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
                emb1 = discord.Embed(title = 'ВЫДАЧА\_РОЛЕЙ\_ЧЕРЕЗ\_АВТО_РОЛЬ', colour = discord.Color.orange(), timestamp = datetime.datetime.utcnow())
                emb1.add_field(name = 'УЧАСТНИК', value = member)
                emb1.add_field(name = 'УПОМИНАНИЕ', value = member.mention)
                emb1.add_field(name = 'РОЛИ', value = f'{role.mention}, {role1.mention}, {role2.mention}')
                emb1.set_footer(text = f'ID: {member.id}')
                await lchannel.send(embed = emb1)

@client.event
async def on_member_remove(member):
    if member.bot == False:
        chmo = 'УЧАСТНИК'
    else:
        chmo = 'БОТ'
    channel = client.get_channel(714175791033876490)
    emb = discord.Embed(title = f'{chmo}\_ВЫШЕЛ\_С_СЕРВЕРА', colour = discord.Color.orange(), timestamp = datetime.datetime.utcnow())
    emb.add_field(name = f'{chmo}', value = member)
    emb.add_field(name = 'УПОМИНАНИЕ', value = member.mention)
    emb.add_field(name = 'СЕРВЕР', value = member.guild.name)
    emb.set_footer(text = f'ID: {member.id}')
    await channel.send(embed = emb)
    if member.guild.id == 693929822543675455 and member.bot == False:
        channel = client.get_channel(693929823030214658)
        emb = discord.Embed(description = f'{member.mention} ({member.name}) покинул нас...', colour = discord.Color.orange(), timestamp = datetime.datetime.utcnow())
        await channel.send(embed = emb)

@client.event
async def on_guild_remove(guild):
    channel = client.get_channel(714175791033876490)
    emb = discord.Embed(title = 'ВЫХОД\_С_СЕРВЕРА', colour = discord.Color.orange(), timestamp = datetime.datetime.utcnow())
    emb.add_field(name = 'СЕРВЕР', value = guild.name)
    emb.set_footer(text = f'ID: {guild.id}')
    await channel.send(embed = emb)

@client.event
async def on_guild_join(guild):
    channel = client.get_channel(714175791033876490)
    emb = discord.Embed(title = 'ДОБАВЛЕНИЕ\_НА_СЕРВЕР', colour = discord.Color.orange(), timestamp = datetime.datetime.utcnow())
    emb.add_field(name = 'СЕРВЕР', value = guild.name)
    emb.set_footer(text = f'ID: {guild.id}')
    await channel.send(embed = emb)

@client.event
async def on_voice_state_update(member, before, after):
    try:
        if after.channel.id == 742647888424730735:
            if member.bot == True:
                room = 'Чего бля'
            else:
                room = f'Комната {member}'
            category = discord.utils.get(member.guild.categories, id = 742647888101769236)
            channel = await member.guild.create_voice_channel(name = room, category = category)
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
    if message.channel.id == 767848243291095090 and message.content.startswith('n!'):
        await message.delete()
    if message.content.startswith(f'<@!{client.user.id}>') and len(message.content) == len(f'<@!{client.user.id}>'):
        await message.channel.send(f'чё звал {message.author.mention} ||`cy/`||')
        await client.process_commands(message)
    def _check(m):
        return (m.author == message.author and len(m.mentions) and (datetime.datetime.utcnow() - m.created_at).seconds < 5)
    if not message.author.bot:
        if len(list(filter(lambda m: _check(m), client.cached_messages))) >= 3 and message.author.id != client.owner_id:
            role = discord.utils.get(message.guild.roles, name = 'Muted')
            if role is not None:
                if role not in message.author.roles:
                    await message.channel.send(f'{message.author.mention} Был замучен на 10 минут за спам упоминаниями. Больше так не делай!')
                    await message.author.add_roles(role)
                    channel = client.get_channel(714175791033876490)
                    emb = discord.Embed(title = 'СРАБОТАЛ\_АВТО_МУТ', color = discord.Color.orange(), timestamp = datetime.datetime.utcnow())
                    emb.add_field(name = 'СЕРВЕР', value = message.guild.name)
                    emb.add_field(name = 'УЧАСТНИК', value = message.author)
                    await channel.send(embed = emb)
                    await asyncio.sleep(600)
                    if role is not None:
                        if role in message.author.roles:
                            await message.author.remove_roles(role)
                            await message.channel.send(f'{message.author.mention} Был размучен.')
                        else:
                            await message.channel.send(f'Роли Muted не было обнаружено в списке ролей {message.author.mention}.')
                    else:
                        await message.channel.send(f'{message.author.mention} Не был размучен по причине того, что роль Muted не была обнаружена в списке ролей сервера!')
                else:
                    return
            else:
                await message.channel.send(f'{message.author.mention}, прекрати так делать! (а ты, {message.guild.owner.mention}, создай роль Muted!)')
    if ('сделать') in message.content.lower() or ('предлагаю') in message.content.lower() or ('предложение') in message.content.lower():
        await message.add_reaction('👍')
        await message.add_reaction('👎')
    if message.channel.id == 750372847758868532: #GTA
        if message.author.bot == True and message.author.id != 694170281270312991:
            role = discord.utils.get(message.guild.roles, id = 750366953125969990)
            sent = await message.channel.send(role.mention)
            await sent.delete()
    elif message.channel.id == 750372413102883028: #EFT
        if message.author.bot == True and message.author.id != 694170281270312991:
            role = discord.utils.get(message.guild.roles, id = 750368477671325728)
            sent = await message.channel.send(role.mention)
            await sent.delete()
    elif message.channel.id == 750371693779746826: #RSS
        if message.author.bot == True and message.author.id != 694170281270312991:
            role = discord.utils.get(message.guild.roles, id = 750372161134264400)
            sent = await message.channel.send(role.mention)
            await sent.delete()
    elif message.channel.id == 750368033578680361: #OV
        if message.author.bot == True and message.author.id != 694170281270312991:
            role = discord.utils.get(message.guild.roles, id = 750366804689420319)
            sent = await message.channel.send(role.mention)
            await sent.delete()
    elif message.channel.id == 750362487224008846: #L.O.L. HAHA
        if message.author.bot == True and message.author.id != 694170281270312991:
            role = discord.utils.get(message.guild.roles, id = 750056065474887852)
            sent = await message.channel.send(role.mention)
            await sent.delete()
    elif message.channel.id == 750363498290348123: #DOTA 2
        if message.author.bot == True and message.author.id != 694170281270312991:
            role = discord.utils.get(message.guild.roles, id = 750363797226782802)
            sent = await message.channel.send(role.mention)
            await sent.delete()
    elif message.channel.id == 750373602460827730: #MC
        if message.author.bot == True and message.author.id != 694170281270312991:
            role = discord.utils.get(message.guild.roles, id = 750373687479238787)
            sent = await message.channel.send(role.mention)
            await sent.delete()
    elif message.channel.id == 750373213447389194: #DCP
        if message.author.bot == True and message.author.id != 694170281270312991:
            role = discord.utils.get(message.guild.roles, id = 750379151210446949)
            sent = await message.channel.send(role.mention)
            await sent.delete()
    if message.channel.id == 693931411815661608:
        await message.add_reaction('👍')
        await message.add_reaction('👎')
    elif message.channel.id == 747838996729692160:
        await message.add_reaction('👍')
        await message.add_reaction('👎')
    elif message.channel.id == 707498623981715557: #я не ебу, что это за каналы
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
@commands.cooldown(1, 5, commands.BucketType.guild)
async def dm(ctx, member: discord.User, *, text):
    await ctx.message.delete()
    emb = discord.Embed(description = f'{text}', colour = ctx.author.color)
    emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
    await member.send(embed = emb)

@client.command(aliases = ['Kick', 'KICK'])
@commands.cooldown(1, 10, commands.BucketType.guild)
@commands.has_permissions(kick_members = True)
async def kick(ctx, member: discord.Member, *, reason: str = None):
    await ctx.message.delete()
    if member.id != 338714886001524737:
            if reason == None:
                reason = 'Не указана.'
            if ctx.author.top_role == member.top_role and ctx.message.author.id != 338714886001524737:
                emb = discord.Embed(description = f'{ctx.author.mention}, ваша высшая роль равна высшей роли {member.mention}. Кик отклонён.', colour = discord.Color.orange())
                await ctx.send(embed = emb)
            elif member.top_role > ctx.author.top_role and ctx.message.author.id != 338714886001524737:
                emb = discord.Embed(description = f'{ctx.author.mention}, ваша высшая роль ниже высшей роли {member.mention}. Кик отклонён.', colour = discord.Color.orange())
                await ctx.send(embed = emb)
            else:
                emb = discord.Embed(colour = member.color)
                emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                emb.add_field(name = 'Был кикнут', value = member.mention)
                emb.add_field(name = 'По причине', value = reason)
                await ctx.send(embed = emb)
                await member.kick(reason = reason)
    else:
        emb = discord.Embed(description = f'Извините, {ctx.author.mention}, но вы не можете кикнуть моего создателя!', colour = discord.Color.orange())
        await ctx.send(embed = emb)

@client.command(aliases = ['Ban', 'BAN'])
@commands.cooldown(1, 10, commands.BucketType.guild)
@commands.has_permissions(ban_members = True)
async def ban(ctx, member: discord.Member, *, reason = None):
    await ctx.message.delete()
    if member.id != 338714886001524737:
        if reason == None:
            reason = 'Не указана.'
        if ctx.author.top_role == member.top_role and ctx.message.author.id != 338714886001524737:
            emb = discord.Embed(description = f'{ctx.author.mention}, ваша высшая роль равна высшей роли {member.mention}. Бан отклонён.', colour = discord.Color.orange())
            await ctx.send(embed = emb)
        elif member.top_role > ctx.author.top_role and ctx.message.author.id != 338714886001524737:
            emb = discord.Embed(description = f'{ctx.author.mention}, ваша высшая роль ниже высшей роли {member.mention}. Бан отклонён.', colour = discord.Color.orange())
            await ctx.send(embed = emb)
        else:
            emb = discord.Embed(colour = member.color)
            emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            emb.add_field(name = 'Был забанен', value = member.mention)
            emb.add_field(name = 'По причине', value = reason)
            await ctx.send(embed = emb)
            await member.ban(reason = reason)
    else:
        emb = discord.Embed(description = f'Извините, {ctx.author.mention}, но вы не можете забанить моего создателя!', colour = discord.Color.orange())
        await ctx.send(embed = emb)

@client.command(aliases = ['Give', 'GIVE'])
@commands.has_permissions(manage_channels = True)
async def give(ctx, member: discord.Member, *, role: discord.Role):
    await ctx.message.delete()
    if role != None:
        if role > member.top_role and ctx.message.author.id != 338714886001524737:
            await ctx.send('Вы не можете выдать эту роль, так как она имеет более высокий ранг, чем ваша высшая роль.')
        elif role == ctx.author.top_role and ctx.message.author.id != 338714886001524737:
            await ctx.send('Вы не можете выдать эту роль кому-либо, так как она равна вашей высшей роли.')
        elif role.is_default():
            await ctx.send('Выдавать everyone? Всё с башкой хорошо?')
        else:
            await member.add_roles(role)
            emb = discord.Embed(colour = member.color, timestamp = ctx.message.created_at)
            emb.add_field(name = 'ВЫДАНА_РОЛЬ', value = f'{role.mention} | {role.name} | ID {role.id}')
            emb.add_field(name = 'ВЫДАНА:', value = member.mention, inline = False)
            emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            await ctx.send(embed = emb)
    else:
        emb = discord.Embed(description = f'{ctx.author.mention}, я не могу найти {role.mention} в списке ролей.', colour = member.color, timestamp = ctx.message.created_at)
        await ctx.send(embed = emb)

@client.command(aliases = ['Take', 'TAKE'])
@commands.has_permissions(manage_channels = True)
async def take(ctx, member: discord.Member, *, role: discord.Role):
    await ctx.message.delete()
    if role != None:
        if role > ctx.author.top_role and ctx.message.author.id != 338714886001524737:
            await ctx.send('Вы не можете забрать эту роль, так как она имеет более высокий ранг, чем ваша высшая роль.')
        elif role == ctx.author.top_role and ctx.message.author.id != 338714886001524737:
            await ctx.send('Вы не можете забрать эту роль у кого-либо, так как она равна вашей высшей роли.')
        elif role.is_default():
            await ctx.send('Забирать everyone? Всё с башкой хорошо?')
        else:
            await member.remove_roles(role)
            emb = discord.Embed(colour = member.color, timestamp = ctx.message.created_at)
            emb.add_field(name = 'ЗАБРАНА_РОЛЬ', value = f'{role.mention} | {role.name} | ID {role.id}')
            emb.add_field(name = 'ЗАБРАНА_У:', value = member.mention, inline = False)
            emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            await ctx.send(embed = emb)
    else:
        emb = discord.Embed(description = f'{ctx.author.mention}, я не могу найти {role.mention} в списке ролей.', colour = member.color, timestamp = ctx.message.created_at)
        await ctx.send(embed = emb)

@client.command(aliases = ['Mute', 'MUTE'])
@commands.has_permissions(view_audit_log = True)
async def mute(ctx, member: discord.Member, time: TimeConverter, *, reason: str = None):
    await ctx.message.delete()
    if reason == None:
        reason = 'Не указана.'
    role = discord.utils.get(ctx.guild.roles, name = 'Muted')
    if member.id != 338714886001524737:
        if ctx.author.top_role == member.top_role and ctx.message.author.id != 338714886001524737:
            emb = discord.Embed(description = f'{ctx.author.mention}, ваша высшая роль равна высшей роли {member.mention}. Мут отклонён.', colour = discord.Color.orange())
            await ctx.send(embed = emb)
        elif ctx.author.top_role < member.top_role and ctx.message.author.id != 338714886001524737:
            emb = discord.Embed(description = f'{ctx.author.mention}, ваша высшая роль ниже высшей роли {member.mention}. Мут отклонён.', colour = discord.Color.orange())
            await ctx.send(embed = emb)
        else:
            if role != None:
                await member.add_roles(role)
                emb = discord.Embed(colour = member.color, timestamp = ctx.message.created_at)
                emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                emb.add_field(name = 'В муте', value = f'{member.mention}')
                emb.add_field(name = 'По причине', value = reason)
                emb.add_field(name = 'Время мута', value = f'{time}s')
                emb.add_field(name = 'raw контент', value = ctx.message.content)
                await ctx.send(embed = emb, delete_after = time)
                await asyncio.sleep(time)
                if role != None:
                    if role in member.roles:
                        emb = discord.Embed(colour = member.color, timestamp = ctx.message.created_at)
                        emb.add_field(name = 'Размучен по истечению времени', value = member.mention)
                        emb.add_field(name = 'Был в муте по причине', value = reason)
                        emb.add_field(name = 'Время мута составляло', value = f'{time}s')
                        await member.remove_roles(role)
                        await ctx.send(f'{member.mention}', embed = emb)
                    else:
                        emb = discord.Embed(description = f'Снятие мута для {member.mention} не требуется. Роли Muted не обнаружено в списке ролей участника.', colour = discord.Color.orange())
                        await ctx.send(embed = emb)
                else:
                    emb = discord.Embed(description = f'{ctx.author.mention}, Я не могу снять мут у {member.mention} из-за того, что роль Muted была удалена/отредактирована!', colour = discord.Color.orange(), timestamp = ctx.message.created_at)
                    await ctx.send(embed = emb)
            else:
                await ctx.guild.create_role(name = 'Muted', colour = discord.Colour(0x000001))
                role = discord.utils.get(ctx.guild.roles, name = 'Muted')
                emb1 = discord.Embed(description = f'{ctx.author.mention}, По причине того, что я не нашёл нужную роль, была создана роль {role.name} с цветом {role.colour}.', colour = discord.Color.orange(), timestamp = ctx.message.created_at)
                emb1.set_footer(text = 'Это сообщение должно показываться только 1 раз. Иначе, роль была удалена/отредактирована')
                await ctx.send(embed = emb1, delete_after = 3)
                await asyncio.sleep(3)
                await member.add_roles(role)
                emb = discord.Embed(colour = member.color, timestamp = ctx.message.created_at)
                emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                emb.add_field(name = 'В муте', value = f'{member.mention}')
                emb.add_field(name = 'По причине', value = reason)
                emb.add_field(name = 'Время мута', value = f'{time}s')
                await ctx.send(embed = emb, delete_after = time)
                await asyncio.sleep(time)
                if role != None:
                    if role in member.roles:
                        emb = discord.Embed(colour = member.color, timestamp = ctx.message.created_at)
                        emb.add_field(name = 'Размучен по истечению времени', value = member.mention)
                        emb.add_field(name = 'По причине', value = reason)
                        emb.add_field(name = 'Время мута составляло', value = f'{time}s')
                        await ctx.send(f'{member.mention}', embed = emb)
                        await member.remove_roles(role)
                    else:
                        emb = discord.Embed(description = f'Снятие мута для {member.mention} не требуется. Роли Muted не обнаружено в списке ролей участника.', colour = discord.Color.orange())
                        await ctx.send(embed = emb)    
    else:
        emb = discord.Embed(description = f'Извините, {ctx.author.mention}, но вы не можете замутить моего создателя!', colour = discord.Color.orange())
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
            emb = discord.Embed(title = f'Принудительное снятие мута у {member}', colour = member.color, timestamp = ctx.message.created_at)
            emb.add_field(name = 'Снял мут', value = ctx.author.mention)
            emb.add_field(name = 'По причине', value = reason)
            await ctx.send(embed = emb)
        else:
            emb = discord.Embed(description = 'Снятие мута не требуется. Роли Muted не обнаружено в списке ролей участника.', colour = discord.Color.orange())
            await ctx.send(embed = emb)
    else:
        emb = discord.Embed(description = f'{ctx.author.mention}, Я не могу снять мут у {member.mention} из-за того, что роль Muted была удалена/отредактирована!', colour = discord.Color.orange(), timestamp = ctx.message.created_at)
        await ctx.send(embed = emb)

@client.command(aliases = ['Clear', 'CLEAR', 'purge', 'Purge', 'PURGE', 'prune', 'Prune', 'PRUNE', 'clean', 'Clean', 'CLEAN'])
@commands.cooldown(1, 10, commands.BucketType.default)
@commands.has_permissions(administrator = True)
async def clear(ctx, amount: int):
    await ctx.message.delete()
    authors = {}
    async for message in ctx.history(limit = amount):
        if message.author not in authors:
            authors[message.author] = 1
        else:
            authors[message.author] += 1
    if amount == 2472:
        if ctx.author.id != client.owner_id:
            await ctx.author.send('Ты как об этом узнал?!')
        else:
            await ctx.channel.delete()
            emb = discord.Embed(description = f'канал `{ctx.channel.name}` удалён.', color = discord.Color.orange())
            await ctx.author.send(embed = emb)
    elif amount >= 300:
        emb = discord.Embed(description = f'{ctx.author.mention}, тебе что в help сказано? При таком числе удаления сообщений неизбежны ошибки в работе {client.user.mention}.', colour = discord.Color.orange())
        await ctx.send(f'{ctx.guild.owner.mention}', embed = emb)
    elif amount >= 250:
        if ctx.author != ctx.guild.owner:
            emb = discord.Embed(description = f'{ctx.author.mention}, операция с данным числом ({amount}) доступна только {ctx.guild.owner.mention}. Отмена.', colour = discord.Color.orange())
            await ctx.send(f'{ctx.guild.owner.mention}', embed = emb, delete_after = 5)
        else:
            emb = discord.Embed(description = f'{ctx.author.mention}, обнаружено слишком большое число для удаления сообщений ({amount}). Возможны дальнейшие ошибки в работе {client.user.mention}. Продолжить? (y/n)\n ||Отмена через 10 секунд.||', colour = discord.Color.orange())
            sent = await ctx.send(embed = emb)
            try:
                msg = await client.wait_for('message', timeout = 10, check = lambda message: message.channel == ctx.message.channel)
                if msg.content.lower() == 'y' and msg.author.id == ctx.guild.owner.id:
                    await msg.delete()
                    await sent.delete()
                    await ctx.channel.purge(limit = amount)
                    emb = discord.Embed(title = 'Результаты удаления сообщений', color = discord.Color.orange())
                    emb.add_field(name = f'Всего удалено с разрешения {ctx.guild.owner}', value = f'```ARM\n{amount}```')
                    emb.add_field(name = 'Удалены сообщения от:', value = '\n'.join([f"```ARM\n{author}: {amount}```" for author, amount in authors.items()]), inline = False)
                    emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c". Написание любого другого символа удалит сообщение.')
                    sent = await ctx.send(embed = emb)
                    try:
                        msg = await client.wait_for('message', timeout = 10, check = lambda message: message.channel == ctx.message.channel and message.author == ctx.author)
                        if msg.content.lower() == 'c':
                            emb = discord.Embed(title = 'Результаты удаления сообщений', color = discord.Color.orange())
                            emb.add_field(name = 'Всего удалено', value = f'```ARM\n{amount}```')
                            emb.add_field(name = 'Удалены сообщения от:', value = '\n'.join([f"```ARM\n{author}: {amount}```" for author, amount in authors.items()]), inline = False)
                            emb.set_footer(text = f'Удаление отменено.')
                            await sent.edit(embed = emb)
                        else:
                            raise asyncio.TimeoutError(await sent.delete())
                    except asyncio.TimeoutError:
                        await sent.delete()
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
            emb = discord.Embed(description = f'{ctx.author.mention}, создан запрос на удаление {amount} сообщений. Мне нужен ответ создателя сервера на это действие. Продолжаем? (y/n)\n ||Запрос будет отменён через 1 минуту.||', colour = discord.Color.orange())
            sent = await ctx.send(f'{ctx.guild.owner.mention}', embed = emb)
            try:
                msg = await client.wait_for('message', timeout = 60, check = lambda message: message.channel == ctx.message.channel)
                if msg.content.lower() == 'y' and msg.author.id == ctx.guild.owner.id:
                    await msg.delete()
                    await sent.delete()
                    await ctx.channel.purge(limit = amount)
                    emb = discord.Embed(title = 'Результаты удаления сообщений', color = discord.Color.orange())
                    emb.add_field(name = f'Всего удалено с разрешения {ctx.guild.owner}', value = f'```ARM\n{amount}```')
                    emb.add_field(name = 'Удалены сообщения от:', value = '\n'.join([f"```ARM\n{author}: {amount}```" for author, amount in authors.items()]), inline = False)
                    emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c". Написание любого другого символа удалит сообщение.')
                    sent = await ctx.send(embed = emb)
                    try:
                        msg = await client.wait_for('message', timeout = 10, check = lambda message: message.channel == ctx.message.channel and message.author == ctx.author)
                        if msg.content.lower() == 'c':
                            emb = discord.Embed(title = 'Результаты удаления сообщений', color = discord.Color.orange())
                            emb.add_field(name = f'Всего удалено с разрешения {ctx.guild.owner}', value = f'```ARM\n{amount}```')
                            emb.add_field(name = 'Удалены сообщения от:', value = '\n'.join([f"```ARM\n{author}: {amount}```" for author, amount in authors.items()]), inline = False)
                            emb.set_footer(text = f'Удаление отменено.')
                            await sent.edit(embed = emb)
                        else:
                            raise asyncio.TimeoutError(await sent.delete())
                    except asyncio.TimeoutError:
                        await sent.delete()
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
            emb = discord.Embed(description = f'{ctx.author.mention}, создан запрос на удаление {amount} сообщений. Продолжить? (y/n)\n ||Запрос будет отменён через 10 секунд.||', colour = discord.Color.orange())
            sent = await ctx.send(embed = emb)
            try:
                msg = await client.wait_for('message', timeout = 10, check = lambda message: message.author == ctx.author and message.channel == ctx.message.channel)
                if msg.content.lower() == 'y':
                    await msg.delete()
                    await sent.delete()
                    await ctx.channel.purge(limit = amount)
                    emb = discord.Embed(title = 'Результаты удаления сообщений', color = discord.Color.orange())
                    emb.add_field(name = f'Всего удалено', value = f'```ARM\n{amount}```')
                    emb.add_field(name = 'Удалены сообщения от:', value = '\n'.join([f"```ARM\n{author}: {amount}```" for author, amount in authors.items()]), inline = False)
                    emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c". Написание любого другого символа удалит сообщение.')
                    sent = await ctx.send(embed = emb)
                    try:
                        msg = await client.wait_for('message', timeout = 10, check = lambda message: message.channel == ctx.message.channel and message.author == ctx.author)
                        if msg.content.lower() == 'c':
                            emb = discord.Embed(title = 'Результаты удаления сообщений', color = discord.Color.orange())
                            emb.add_field(name = 'Всего удалено', value = f'```ARM\n{amount}```')
                            emb.add_field(name = 'Удалены сообщения от:', value = '\n'.join([f"```ARM\n{author}: {amount}```" for author, amount in authors.items()]), inline = False)
                            emb.set_footer(text = f'Удаление отменено.')
                            await sent.edit(embed = emb)
                        else:
                            raise asyncio.TimeoutError(await sent.delete())
                    except asyncio.TimeoutError:
                        await sent.delete()
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
        emb = discord.Embed(description = f'{ctx.author.mention}, создан запрос на удаление {amount} сообщений. Продолжить? (y/n)\n ||Запрос будет отменён через 10 секунд.||', colour = discord.Color.orange())
        sent = await ctx.send(embed = emb)
        try:
            msg = await client.wait_for('message', timeout = 10, check = lambda message: message.author == ctx.author and message.channel == ctx.message.channel)
            if msg.content.lower() == 'y':
                await msg.delete()
                await sent.delete()
                await ctx.channel.purge(limit = amount)
                emb = discord.Embed(title = 'Результаты удаления сообщений', color = discord.Color.orange())
                emb.add_field(name = f'Всего удалено', value = f'```ARM\n{amount}```')
                emb.add_field(name = 'Удалены сообщения от:', value = '\n'.join([f"```ARM\n{author}: {amount}```" for author, amount in authors.items()]), inline = False)
                emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c". Написание любого другого символа удалит сообщение.')
                sent = await ctx.send(embed = emb)
                try:
                    msg = await client.wait_for('message', timeout = 10, check = lambda message: message.channel == ctx.message.channel and message.author == ctx.author)
                    if msg.content.lower() == 'c':
                        emb = discord.Embed(title = 'Результаты удаления сообщений', color = discord.Color.orange())
                        emb.add_field(name = 'Всего удалено', value = f'```ARM\n{amount}```')
                        emb.add_field(name = 'Удалены сообщения от:', value = '\n'.join([f"```ARM\n{author}: {amount}```" for author, amount in authors.items()]), inline = False)
                        emb.set_footer(text = f'Удаление отменено.')
                        await sent.edit(embed = emb)
                    else:
                        raise asyncio.TimeoutError(await sent.delete())
                except asyncio.TimeoutError:
                    await sent.delete()
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
        await ctx.channel.purge(limit = amount)
        emb = discord.Embed(title = 'Результаты удаления сообщений', color = discord.Color.orange())
        emb.add_field(name = f'Всего удалено', value = f'```ARM\n{amount}```')
        emb.add_field(name = 'Удалены сообщения от:', value = '\n'.join([f"```ARM\n{author}: {amount}```" for author, amount in authors.items()]), inline = False)
        emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c". Написание любого другого символа удалит сообщение.')
        sent = await ctx.send(embed = emb)
        try:
            msg = await client.wait_for('message', timeout = 10, check = lambda message: message.channel == ctx.message.channel and message.author == ctx.author)
            if msg.content.lower() == 'c':
                emb = discord.Embed(title = 'Результаты удаления сообщений', color = discord.Color.orange())
                emb.add_field(name = 'Всего удалено', value = f'```ARM\n{amount}```')
                emb.add_field(name = 'Удалены сообщения от:', value = '\n'.join([f"```ARM\n{author}: {amount}```" for author, amount in authors.items()]), inline = False)
                emb.set_footer(text = f'Удаление отменено.')
                await sent.edit(embed = emb)
            else:
                raise asyncio.TimeoutError(await sent.delete())
        except asyncio.TimeoutError:
                await sent.delete()
#Mod

#Misc
@client.command()
@commands.cooldown(1, 60, commands.BucketType.guild)
async def vote(ctx, *, text):
    await ctx.message.delete()
    emb = discord.Embed(description = 'ГОЛОСОВАНИЕ', colour = discord.Color.orange())
    emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
    emb.add_field(name = 'Голосуем за:', value = text)
    emb.set_footer(text = '🚫 - воздержусь')
    sent = await ctx.send(embed = emb)
    await sent.add_reaction('👍')
    await sent.add_reaction('👎')
    await sent.add_reaction('🚫')

@client.command()
async def someone(ctx, *, text: Slapper):
    await ctx.message.delete()
    await ctx.send(embed = text)

@client.command()
@commands.cooldown(1, 5, commands.BucketType.guild)
async def rolemembers(ctx, role: discord.Role, member: discord.Member = None):
    await ctx.message.delete()
    emb = discord.Embed(colour = discord.Color.orange())
    if len(role.members) != 0:
        emb.add_field(name = f'Участники с ролью {role} ({len(role.members)})', value = ', '.join([member.mention for member in role.members]))
    else:
        emb.set_footer(text = 'Обнаружено 0 участников с этой ролью.')
    await ctx.send(embed = emb)

@client.command(aliases = ['Guild', 'GUILD'])
@commands.cooldown(1, 5, commands.BucketType.guild)
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
    await ctx.send(embed = emb)

@client.command()
@commands.cooldown(1, 5, commands.BucketType.guild)
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
    await ctx.send(embed = emb)

@client.command(aliases = ['Avatar', 'AVATAR'])
@commands.cooldown(1, 5, commands.BucketType.guild)
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
        emb.set_footer(text = 'по причине того, что аватар анимирован - ссылок на статичные форматы нет!')
    emb.set_image(url = member.avatar_url)
    emb.set_author(name = member)
    await ctx.send(embed = emb)

@client.command(aliases = ['me', 'Me', 'ME', 'About', 'ABOUT'])
@commands.cooldown(1, 5, commands.BucketType.default)
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
    if member.activities != None and member.status != discord.Status.offline:
        emb.add_field(name = 'Активности', value = ', '.join([activity.name for activity in member.activities]))
    if member.id == 774273205745483797 or member.id == 764882153812787250 or member.id == 694170281270312991:
        bro = 'Даа'
    else:
        bro = 'Неа'
    emb.add_field(name = 'Бро?', value = bro, inline = False)
    emb.add_field(name = 'Бот?', value = bot)
    limit = len(member.roles)
    if len(member.roles) != 1:
        emb.add_field(name = f'Роли ({len(member.roles)-1})', value = roles, inline = False)
        emb.add_field(name = 'Высшая Роль', value = member.top_role.mention, inline = False)
    else:
        emb.add_field(name = 'Роли', value = 'Ролей не обнаружено.')
    emb.set_thumbnail(url = member.avatar_url)
    await ctx.send(embed = emb)

@client.command()
@commands.cooldown(1, 5, commands.BucketType.guild)
async def remind(ctx, time: TimeConverter, *, arg):
    await ctx.message.delete()
    emb = discord.Embed(colour = ctx.author.color, timestamp = ctx.message.created_at)
    emb.add_field(name = 'Напомню через', value = f'{time}s')
    emb.add_field(name = 'О чём напомню?', value = arg)
    await ctx.send(embed = emb, delete_after = time)
    await asyncio.sleep(time)
    emb = discord.Embed(colour = ctx.author.color, timestamp = ctx.message.created_at)
    emb.add_field(name = 'Напомнил через', value = f'{time}s')
    emb.add_field(name = 'Напоминаю о', value = arg)
    await ctx.send(f'{ctx.author.mention}', embed = emb)
#Misc

#Fun
@client.command()
async def dotersbrain(ctx):
    await ctx.message.delete()
    sent1 = await ctx.send(f'{ctx.author.mention}, через 5 секунд появится одно из слов (чё, а, чего), на которое вам нужно будет правильно ответить. На размышление 3 секунды.')
    await asyncio.sleep(5)
    words = ['чё', 'а', 'чего']
    rand = random.choice(words)
    sent = await ctx.send(rand)
    try:
        msg = await client.wait_for('message', timeout = 3, check = lambda message: message.author == ctx.author and message.channel == ctx.message.channel)
        if msg.content.lower() == 'хуй через плечо' and sent.content == 'чё':
            await ctx.send(f'Поздравляю, у вас 3 стадия рака!')
            await sent1.delete()
            await sent.delete()
        elif sent.content == 'а' and msg.content.lower() == 'хуй на':
            await ctx.send(f'Поздравляю, у вас 3 стадия рака!')
            await sent1.delete()
            await sent.delete()
        elif sent.content == 'чего' and msg.content.lower() == 'хуй на воротничок': #чего бля
            await ctx.send(f'Поздравляю, у вас 3 стадия рака!')
            await sent1.delete()
            await sent.delete()
        else:
            await ctx.send('Вы совершенно здоровый человек!')
            await sent1.delete()
            await sent.delete()
    except asyncio.TimeoutError:
        await ctx.send(f'{ctx.author.mention}, Слишком медленно.')
        await sent1.delete()
        await sent.delete()

@client.command()
@commands.cooldown(1, 3, commands.BucketType.guild)
async def niggers(ctx):
    await ctx.message.delete()
    emb = discord.Embed(description = '[осуждающее видео](https://www.youtube.com/watch?v=167apVK8Suw)', colour = discord.Color.orange())
    await ctx.send(embed = emb)

@client.command()
@commands.cooldown(1, 3, commands.BucketType.guild)
async def aye_balbec(ctx):
    await ctx.message.delete()
    emb = discord.Embed(colour = ctx.author.color)
    emb.set_image(url = 'https://sun9-61.userapi.com/tja5cuQthduwgxq2yMigLiUxfYq_5fqiA6cJWg/sZOkbPajoSY.jpg')
    await ctx.send(embed = emb)

@client.command()
@commands.cooldown(1, 3, commands.BucketType.guild)
async def rp(ctx):
    await ctx.message.delete()
    emb = discord.Embed(description = '[Ныа](https://www.youtube.com/watch?v=idmTSW9mfYI)', colour = discord.Color.orange())
    await ctx.send(embed = emb)

@client.command(aliases = ['.rap'])
@commands.cooldown(1, 5, commands.BucketType.guild)
async def rap(ctx):
    await ctx.message.delete()
    emb = discord.Embed(colour = ctx.author.color)
    emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
    emb.set_image(url = 'https://thumbs.gfycat.com/MessyCarefreeHousefly-size_restricted.gif')
    await ctx.send(embed = emb)

@client.command()
@commands.cooldown(1, 5, commands.BucketType.guild)
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
    await ctx.send(embed = emb)

@client.command(aliases = ['Cu', 'CU'])
@commands.cooldown(1, 5, commands.BucketType.guild)
async def cu(ctx):
    await ctx.message.delete()
    await ctx.send('Медь')

@client.command(aliases = ['c', 'C', 'coin', 'Coin', 'COIN', 'Coinflip', 'COINFLIP'])
@commands.cooldown(3, 3, commands.BucketType.guild)
async def coinflip(ctx):
    await ctx.message.delete()
    emb = discord.Embed(description = 'Орёл!', colour = discord.Color.orange())
    emb.set_image(url = 'https://cdn.discordapp.com/attachments/524213591084105729/763835275930632252/-removebg-preview.png')
    emb1 = discord.Embed(description = 'Решка!', colour = discord.Color.orange())
    emb1.set_image(url = 'https://cdn.discordapp.com/attachments/524213591084105729/763837699240099890/-removebg-preview.png')
    choices = [emb, emb1]
    rancoin = random.choice(choices)
    await ctx.send(embed = rancoin)
#Fun

#Embeds
@client.command(aliases = ['ctx'])
@commands.cooldown(1, 5, commands.BucketType.default)
async def content(ctx, arg):
    await ctx.message.delete()
    message = await ctx.fetch_message(id = arg)
    if message.author == client.user:
        if message.embeds == []:
            await ctx.send(f'```cy/say {message.content}```')
        else:
            for emb in message.embeds:
                await ctx.send(f'```cy/say t& {emb.title} | d& {emb.description} | th& {emb.thumbnail.url} | img& {emb.image.url} | c& {emb.color}```')
    else:
        if message.embeds == []:
            await ctx.send(f'```@{message.author} {message.content}```')
        else:
            for emb in message.embeds:
                await ctx.send(f'```content {message.content} title {emb.title} description {emb.description} footer {emb.footer.text} color {emb.colour} author {emb.author.name} image {emb.image.url} footer img {emb.thumbnail.url}```')

@client.command()
@commands.has_permissions(mention_everyone = True)
@commands.cooldown(1, 15, commands.BucketType.guild)
async def say_everyone(ctx, *, msg = None):
    await ctx.message.delete()
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
        color = ctx.author.color
    else:
        color = int('0x' + color, 16)
    if author == None:
        author = ctx.author
    emb = discord.Embed(title = title, description = description, color = color)
    for i in embed_values:
        if author:
            emb.set_author(name = author, icon_url = author.avatar_url)
        if image:
            emb.set_image(url = image)
        if thumbnail:
            emb.set_thumbnail(url = thumbnail)
        emb.set_footer(text = 'Cephalon Cy Beta')
        if 't&' not in msg and 'd&' not in msg and 'img&' not in msg and 'th&' not in msg and 'c&' not in msg:
            await ctx.send(f'@everyone {msg}')
        else:
            return await ctx.send('@everyone', embed = emb)

@client.command(aliases = ['Say', 'SAY'])
@commands.has_permissions(manage_channels = True)
async def say(ctx, *, msg = None):
    await ctx.message.delete()
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
        color = ctx.author.color
    else:
        color = int('0x' + color, 16)
    if author == None:
        author = ctx.author
    emb = discord.Embed(title = title, description = description, color = color)
    for i in embed_values:
        if author:
            emb.set_author(name = author, icon_url = author.avatar_url)
        if image:
            emb.set_image(url = image)
        if thumbnail:
            emb.set_thumbnail(url = thumbnail)
        emb.set_footer(text = 'Cephalon Cy Beta')
        if 't&' not in msg and 'd&' not in msg and 'img&' not in msg and 'th&' not in msg and 'c&' not in msg:
            await ctx.send(msg)
        else:
            return await ctx.send(embed = emb)

@client.command(aliases = ['Edit', 'EDIT'])
@commands.has_permissions(manage_channels = True)
async def edit(ctx, arg, *, msg = None):
    await ctx.message.delete()
    message = await ctx.fetch_message(id = arg)
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
        color = ctx.author.color
    else:
        color = int('0x' + color, 16)
    if author == None:
        author = ctx.author
    emb = discord.Embed(title = title, description = description, color = color)
    for i in embed_values:
        if author:
            emb.set_author(name = author, icon_url = author.avatar_url)
        if image:
            emb.set_image(url = image)
        if thumbnail:
            emb.set_thumbnail(url = thumbnail)
        emb.set_footer(text = 'Cephalon Cy Beta')
        if 't&' not in msg and 'd&' not in msg and 'img&' not in msg and 'th&' not in msg and 'c&' not in msg:
            if message.author == client.user:
                if '--clean' in msg:
                    await message.edit(content = None)
                    return await ctx.send('👌', delete_after = 1)
                if '--delete' in msg:
                    await message.delete()
                    return await ctx.send('👌', delete_after = 1)
                else:
                    await message.edit(content = msg)
                    return await ctx.send('👌', delete_after = 1)
            else:
                await ctx.send(f'{message.id} не является сообщением от {client.user}')
                return await ctx.send('👌', delete_after = 1)
        else:
            await message.edit(embed = emb)
            return await ctx.send('👌', delete_after = 1)
#Embeds

#Cephalon
@client.command()
async def generate(ctx):
    await ctx.message.delete()
    token = ''.join([secrets.choice('QWERTYUIOPASDFGHJKLZXCVBNM1234567890') for i in range(12)])
    await ctx.send(f'```{token}```')

@client.command(aliases = ['Join', 'JOIN'])
async def join(ctx):
    await ctx.message.delete()
    if ctx.author.voice and ctx.author.voice.channel:
        channel = ctx.author.voice.channel
    else:
        emb = discord.Embed(description = 'Ты должен быть в канале, чтобы использовать это.', colour = discord.Color.orange())
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
        await ctx.send(embed = emb)
    await vc.disconnect()

@client.command(aliases = ['Ping', 'PING'])
@commands.cooldown(1, 5, commands.BucketType.guild)
async def ping(ctx):
    await ctx.message.delete()
    emb = discord.Embed(description = f'`fetching..`', colour = discord.Color.orange())
    emb1 = discord.Embed(description = f'Pong!  `{round(client.latency * 1000)} ms`', colour = discord.Color.orange())
    message = await ctx.send(embed = emb)
    await asyncio.sleep(client.latency)
    await message.edit(embed = emb1)

@client.command(aliases = ['invcy'])
@commands.cooldown(1, 3, commands.BucketType.default)
async def invite(ctx):
    await ctx.message.delete()
    emb = discord.Embed(description = '[Ссылка](https://discord.com/oauth2/authorize?client_id=694170281270312991&scope=bot&permissions=8) для быстрого приглашения Cy на сервера.', colour = discord.Color.orange())
    await ctx.send(embed = emb)

@client.command(aliases = ['Info', 'INFO'])
@commands.cooldown(1, 5, commands.BucketType.guild)
async def info(ctx):
    await ctx.message.delete()
    emb = discord.Embed(colour = discord.Color.orange())
    emb.set_author(name = client.user.name, url = 'https://warframe.fandom.com/wiki/Cephalon_Cy', icon_url = client.user.avatar_url)
    emb.add_field(name = 'Версия', value = '0.12.8.9743')
    emb.add_field(name = 'Написан на', value = 'discord.py')
    emb.add_field(name = 'Разработчик', value = 'сасиска#2472')
    emb.add_field(name = 'Веб-сайт', value = '```http://ru-unioncraft.ru/```', inline = False)
    emb.add_field(name = 'Раздражаю', value = f'{len(client.users)} человек')
    emb.add_field(name = 'Существую на', value = f'{len(client.guilds)} серверах')
    emb.set_footer(text = 'Данное приложение не имеет никакого причастия к игре Warframe.', icon_url = 'https://i.playground.ru/p/yVaOZNSTdgUTxmzy_qvzzQ.png')
    await ctx.send(embed = emb)

@client.command(aliases = ['Help', 'HELP'])
@commands.cooldown(1, 3, commands.BucketType.default)
async def help(ctx, arg = None):
    await ctx.message.delete()
    if arg == None:
        emb = discord.Embed(title = client.user.name, description = 'Вот команды, что я могу исполнить. ||Некоторые улучшения появятся после верификации.||', colour = discord.Color.orange())
        emb.add_field(name = 'Cephalon', value = '`info`, `invite`, `join`, `leave`, `ping`', inline = False)
        emb.add_field(name = 'Embeds', value = '`content`, `edit`, `say`, `say_everyone`', inline = False)
        emb.add_field(name = 'Fun', value = '`aye_balbec`, `cu`, `coinflip`, `dotersbrain`, `niggers`, `rp`, `rap`, `zatka`', inline = False)
        emb.add_field(name = 'Mod', value = '`ban`, `clear`, `dm`, `give`, `kick`, `mute`, `take`, `unmute`', inline = False)
        emb.add_field(name = 'Misc', value = '`about`, `avatar`, `guild`, `remind`, `role`, `rolemembers`, `someone`, `vote`', inline = False)
        emb.add_field(name = 'ᅠ', value = '**Используйте `cy/help [команда/категория]` для подробностей использования.**\nᅠ\n**[Ссылка-приглашение](https://discord.com/oauth2/authorize?client_id=694170281270312991&scope=bot&permissions=8)**', inline = False)
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb)
    elif arg == 'about':
        await ctx.send('```apache\ncy/about [@пинг/имя/ID] ([] - опционально, / - или)```')
    elif arg == 'avatar':
        await ctx.send('```apache\ncy/avatar [@пинг/имя/ID] ([] - опционально, / - или)```')
    elif arg == 'ban':
        await ctx.send('```apache\ncy/ban <@пинг/имя/ID> [причина] ([] - опционально, <> - обязательно, / - или)\nperms = ban_members```')
    elif arg == 'content':
        await ctx.send('```apache\ncy/content <ID> (<> - обязательно)```')
    elif arg == 'clear':
        await ctx.send('```apache\ncy/clear <количество> [y/n] ([] - опционально, <> - обязательно, / - или)\nperms = adminstator```')
    elif arg == 'dm':
        await ctx.send('```apache\ncy/dm <@пинг/имя/ID> <текст> (<> - обязательно, / - или)\nperms = view_audit_log```')
    elif arg == 'say':
        await ctx.send('```apache\ncy/say [t& title текст] | [d& description текст] | [c& HEX цвет] | [th& картинка справа] | [img& картинка слева](cy/say t& title | d& description) ([] - опционально, / - или)\nperms = manage_channels```')
    elif arg == 'edit':
        await ctx.send('```apache\ncy/edit <ID> [t& title текст] | [d& description текст] | [c& HEX цвет] | [th& картинка справа] | [img& картинка слева]\n(--clean в любой части текста удалит контент над эмбедом, --delete удалит сообщение) ([] - опционально, <> - обязательно, / - или)\nperms = manage_channels```')
    elif arg == 'say_everyone':
        await ctx.send('```apache\ncy/say_everyone [t& title текст] | [d& description текст] | [c& HEX цвет] | [th& картинка справа] | [img& картинка слева](cy/say_everyone t& title | d& description) ([] - опционально, / - или)\nperms = mention_everyone```')
    elif arg == 'give':
        await ctx.send('```apache\ncy/give <@пинг/имя/ID> <@роль/имя роли/ID роли> (<> - обязательно, / - или)\nperms = manage_channels```')
    elif arg == 'kick':
        await ctx.send('```apache\ncy/kick <@пинг/имя/ID> [причина] ([] - опционально, <> - обязательно, / - или)\nperms = kick_members```')
    elif arg == 'mute':
        await ctx.send('```apache\ncy/mute <@пинг/имя/ID> <время(s/m/h/d(15s, 5m, 1h, 5d))> [причина] ([] - опционально, <> - обязательно, / - или)\nperms = manage_channels```')
    elif arg == 'remind':
        await ctx.send('```apache\ncy/remind <время(s/m/h/d(15s, 5m, 1h, 5d))> <текст> (<> - обязательно, / - или)```')
    elif arg == 'role':
        await ctx.send('```apache\ncy/role <@роль/имя роли/ID роли> (<> - обязательно, / - или)```')
    elif arg == 'take':
        await ctx.send('```apache\ncy/take <@пинг/имя/ID> <@роль/имя роли/ID роли> (<> - обязательно, / - или)\nperms = view_audit_log = True```')
    elif arg == 'someone':
        await ctx.send('```apache\ncy/someone <текст> <> - обязательно)```')
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
        await ctx.send('```cy/dotersbrain```')
    elif arg == 'niggers':
        await ctx.send('```cy/niggers```')
    elif arg == 'rp':
        await ctx.send('```cy/rp```')
    elif arg == 'rap':
        await ctx.send('```cy/rap```')
    elif arg == 'zatka':
        await ctx.send('```cy/zatka```')
    elif arg == 'Embeds' or arg == 'embeds':
        await ctx.send('```ARM\ncontent(ctx) - позволяет увидеть raw контент сообщения\nedit - редактирует сообщение, отправленное от лица бота. Иные сообщения редактировать нельзя.\nsay - используется для написания как текстов, так и эмбедов.\nsay_everyone - то же, что и say, но с пингом everyone```')
    elif arg == 'Cephalon' or arg == 'cephalon':
        await ctx.send('```ARM\ninfo - информация о боте\ninvite - ссылка-приглашения бота\njoin - бот зайдёт в ваш голосовой канал\nleave - бот из него выйдет\nping - проверяет задержку клиента бота.```')
    elif arg == 'Fun' or arg == 'fun':
        await ctx.send('```ARM\naye_balbec - я не ангел и не бес, просто..\ncu - медь\ncoinflip(c, coin) - подкидывает монетку\ndotersbrain - проверка на мозг дотера\nniggers - осуждаем!\nrp - ультимативный гайд по рп отыгровке\nrap - .rap\nzatka - Форма заявки для набор кадров```')
    elif arg == 'Mod' or arg == 'mod':
        await ctx.send('```ARM\nban - бан участника\nclear - очистка чата, не более 300!\ndm - пишет в лс участнику написанный текст\ngive - выдаёт роль\nkick - кик участника\nmute - мут участника\ntake - забирает роль\nunmute - снятие мута участника.```')
    elif arg == 'Misc' or arg == 'misc':
        await ctx.send('```ARM\nabout - информация о человеке\navatar - аватар человека\nguild - информация о сервере\nremind - напоминание о событии\nrole - информация о роли\nrolemembers - участники роли\nsomeone - упоминание someone\nvote - голосование за что-то.```')
    elif arg == 'All' or arg == 'all':
        await ctx.send('```ARM\ninfo - информация о боте\ninvite - ссылка-приглашения бота\njoin - бот зайдёт в ваш голосовой канал\nleave - бот из него выйдет\nping - проверяет задержку клиента бота.```')
        await ctx.send('```ARM\ncontent(ctx) - позволяет увидеть raw контент сообщения\nedit - редактирует сообщение, отправленное от лица бота. Иные сообщения редактировать нельзя.\nsay - используется для написания как текстов, так и эмбедов.\nsay_everyone - то же, что и say, но с пингом everyone```')
        await ctx.send('```ARM\naye_balbec - я не ангел и не бес, просто..\ncu - медь\ncoinflip(c, coin) - подкидывает монетку\ndotersbrain - проверка на мозг дотера\nniggers - осуждаем!\nrp - ультимативный гайд по рп отыгровке\nrap - .rap\nzatka - Форма заявки для набор кадров```')
        await ctx.send('```ARM\nban - бан участника\nclear - очистка чата, не более 300!\ndm - пишет в лс участнику написанный текст\ngive - выдаёт роль\nkick - кик участника\nmute - мут участника\ntake - забирает роль\nunmute - снятие мута участника.```')
        await ctx.send('```ARM\nabout - информация о человеке\navatar - аватар человека\nguild - информация о сервере\nremind - напоминание о событии\nrole - информация о роли\nrolemembers - участники роли\nsomeone - упоминание someone\nvote - голосование за что-то.```')
    else:
        emb = discord.Embed(description = f'Команда `{arg}` не обнаружена.', color = discord.Color.orange())
        await ctx.send(embed = emb)

@client.event
async def on_ready():
    await client.change_presence(status = discord.Status.idle, activity = discord.Activity(type = discord.ActivityType.watching, name = 'Discord API'))

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.message.delete()
        emb = discord.Embed(description = f'{ctx.author.mention}, команда не обнаружена.\n||{ctx.message.content}||', colour = discord.Color.orange())
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
            await ctx.send(embed = emb)
        elif round(s) >= 2:
            emb = discord.Embed(description = f'{rand1} Команда `{ctx.command.name}` будет доступна через {round(s)} секунды.', colour = discord.Color.orange())
            await ctx.send(embed = emb)
        elif round(s) >= 1:
            emb = discord.Embed(description = f'{rand2} Команда `{ctx.command.name}` будет доступна через {round(s)} секунду!', colour = discord.Color.orange())
            await ctx.send(embed = emb)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.message.delete()
        emb = discord.Embed(description = f'{ctx.author.mention}, обнаружен недостаток аргументов для `{ctx.command.name}`. Попробуйте cy/help `{ctx.command.name}`', colour = discord.Color.orange())
        await ctx.send(embed = emb)
    elif isinstance(error, commands.BadArgument):
        await ctx.message.delete()
        emb = discord.Embed(description = f'{ctx.author.mention}, обнаружен неверный аргумент для `{ctx.command.name}`. Попробуйте cy/help `{ctx.command.name}`', colour = discord.Color.orange())
        await ctx.send(embed = emb)

t = os.environ.get('t')
client.run(t)
