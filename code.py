import asyncio
import datetime
import json
import os
import random
import re
import discord
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
async def on_member_join(member):
    channel = client.get_channel(693929823030214658)
    emb = discord.Embed(description = f'{member.mention} ({member.name}) has entered the `{member.guild.name}`', colour = discord.Color.orange())
    await channel.send(embed = emb)

@client.event
async def on_member_remove(member):
    channel = client.get_channel(693929823030214658)
    emb = discord.Embed(description = f'{member.mention} ({member.name}) has exited the `{member.guild.name}`...', colour = discord.Color.orange())
    await channel.send(embed = emb)

@client.event
async def on_guild_remove(guild):
    channel = client.get_channel(693929823030214658)
    emb = discord.Embed(description = f'Меня выгнали с сервера `{guild.name}`...', colour = discord.Color.red())
    emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
    await channel.send(embed = emb)

@client.event
async def on_guild_join(guild):
    channel = client.get_channel(693929823030214658)
    emb = discord.Embed(description = f'Меня добавили на сервер `{guild.name}`!', colour = discord.Color.green())
    emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
    await channel.send(embed = emb)

@client.event
async def on_voice_state_update(member, before, after):
    try:
        if after.channel.id == 742647888424730735: 
            category = discord.utils.get(member.guild.categories, id = 742647888101769236)
            channel = await member.guild.create_voice_channel(name = f'Комната {member}', category = category)
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
    if ('чё') in message.content.lower() and message.author.bot == False:
        await message.channel.send('хуй через плечо')
    def _check(m):
        return (m.author == message.author and len(m.mentions) and (datetime.datetime.utcnow() - m.created_at).seconds < 5)
    if not message.author.bot:
        if len(list(filter(lambda m: _check(m), client.cached_messages))) >= 3 and message.author.id != client.owner_id:
            role = discord.utils.get(message.guild.roles, name = 'Muted')
            if role is not None:
                await message.channel.send(f'{message.author.mention} Был замучен на 10 минут за спам упоминаниями. Больше так не делай!')
                await message.author.add_roles(role)
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
        emb = discord.Embed(colour = discord.Color.orange(), timestamp = datetime.datetime.utcnow())
        emb.set_author(name = message.author, icon_url = message.author.avatar_url)
        if isinstance(message.channel, discord.channel.DMChannel):
            emb.add_field(name = 'На сервере', value = 'в ЛС')
        else:
            emb.add_field(name = 'На сервере', value = message.guild)
            emb.add_field(name = 'В канале', value = f'{message.channel.mention} ({message.channel.name})')
        emb.add_field(name = 'Было написано', value = message.content)
        emb.set_footer(text = f'Cephalon Cy by сасиска#2472')
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
            emb = discord.Embed(description = f'[Сообщение]({before.jump_url}) было изменено', colour = discord.Color.orange(), timestamp = datetime.datetime.utcnow())
            emb.set_author(name = before.author, icon_url = before.author.avatar_url)
            emb.add_field(name = 'На сервере', value = before.guild)
            emb.add_field(name = 'Было', value = f'```{before.content}```')
            emb.add_field(name = 'Стало', value = f'```{after.content}```')
            emb.set_footer(text = f'Cephalon Cy by сасиска#2472')
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
            channel = client.get_channel(714175791033876490)
            emb = discord.Embed(colour = member.color, timestamp = ctx.message.created_at)
            emb.add_field(name = 'Была выдана роль', value = f'{role.mention} | {role.name} | ID {role.id}')
            emb.add_field(name = 'Выдана:', value = member.mention)
            emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            await channel.send(embed = emb)
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
            channel = client.get_channel(714175791033876490)
            emb = discord.Embed(colour = member.color, timestamp = ctx.message.created_at)
            emb.add_field(name = 'Была забрана роль', value = f'{role.mention} | {role.name} | ID {role.id}')
            emb.add_field(name = 'Забрана:', value = member.mention)
            emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            await channel.send(embed = emb)
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
 
@client.command(aliases = ['Clear', 'CLEAR', 'purge', 'Purge', 'PURGE'])
@commands.cooldown(1, 15, commands.BucketType.guild)
@commands.has_permissions(administrator = True)
async def clear(ctx, amount: int):
    await ctx.message.delete()
    if amount >= 300:
        if ctx.author == ctx.guild.owner:
            a = 'владелец блять'
        else:
            a = 'еблан сука'
        emb = discord.Embed(description = f'{ctx.author.mention}, при таком числе удаления сообщений ({amount} блять) неизбежны ошибки в работе {client.user.mention}.\n Нахуй иди, {a}', colour = discord.Color.orange())
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
                    emb = discord.Embed(description = f'С разрешения {ctx.guild.owner.mention} удалено {amount} сообщений.', colour = discord.Color.orange())
                    await ctx.send(embed = emb, delete_after = 3)
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
                    emb = discord.Embed(description = f'С разрешения {ctx.guild.owner.mention} удалено {amount} сообщений.', colour = discord.Color.orange())
                    await ctx.send(embed = emb, delete_after = 3)
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
        else:
            emb = discord.Embed(description = f'{ctx.author.mention}, создан запрос на удаление {amount} сообщений. Продолжить? (y/n)\n ||Запрос будет отменён через 10 секунд.||', colour = discord.Color.orange())
            sent = await ctx.send(embed = emb)
            try:
                msg = await client.wait_for('message', timeout = 10, check = lambda message: message.author == ctx.author and message.channel == ctx.message.channel)
                if msg.content.lower() == 'y':
                    await msg.delete()
                    await sent.delete()
                    await ctx.channel.purge(limit = amount)
                    emb = discord.Embed(description = f'Удалено {amount} сообщений.', colour = discord.Color.orange())
                    await ctx.send(embed = emb, delete_after = 3)
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
                emb = discord.Embed(description = f'Удалено {amount} сообщений.', colour = discord.Color.orange())
                await ctx.send(embed = emb, delete_after = 3)
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
        emb = discord.Embed(description = f'Удалено {amount} сообщений.', colour = discord.Color.orange())
        await ctx.send(embed = emb, delete_after = 3)
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
    emb = discord.Embed(colour = discord.Color.orange(), timestamp = ctx.message.created_at)
    emb.set_author(name = guild, icon_url = guild.icon_url)
    emb.add_field(name = 'ID сервера', value = guild.id)
    emb.add_field(name = 'Голосовой регион', value = guild.region)
    emb.add_field(name = 'Участников', value = guild.member_count)
    emb.add_field(name = 'Каналов', value = f'Текстовых {len(guild.text_channels)} | Голосовых {len(guild.voice_channels)}')
    limit = len(guild.roles)
    if limit > 21:
        emb.add_field(name = 'Роли', value = f'Слишком много для отрисовки ({len(guild.roles)-1}) [лимит 20]', inline = False)
    elif limit == 21:
        emb.add_field(name = f'Роли ({len(guild.roles)-1}) [лимит достигнут]', value = ', '.join([role.mention for role in guild.roles[1:]]), inline = False)
    elif limit == 20:
        emb.add_field(name = f'Роли ({len(guild.roles)-1}) [1 до лимита]', value = ', '.join([role.mention for role in guild.roles[1:]]), inline = False)
    elif limit == 19:
        emb.add_field(name = f'Роли ({len(guild.roles)-1}) [2 до лимита]', value = ', '.join([role.mention for role in guild.roles[1:]]), inline = False)
    elif limit == 18:
        emb.add_field(name = f'Роли ({len(guild.roles)-1}) [3 до лимита]', value = ', '.join([role.mention for role in guild.roles[1:]]), inline = False)
    else:
        emb.add_field(name = f'Роли ({len(guild.roles)-1})', value = ', '.join([role.mention for role in guild.roles[1:]]), inline = False)
    now = datetime.datetime.today()
    then = guild.created_at
    delta = now - then
    d = guild.created_at.strftime('%d/%m/%Y %H:%M:%S UTC')
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
    d = role.created_at.strftime('%d/%m/%Y %H:%M:%S UTC')
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
@commands.cooldown(1, 5, commands.BucketType.guild)
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
    d = member.created_at.strftime('%d/%m/%Y %H:%M:%S UTC')
    then1 = member.joined_at
    delta1 = now - then1
    d1 = member.joined_at.strftime('%d/%m/%Y %H:%M:%S UTC')
    emb.add_field(name = 'Создан', value = f'{delta.days} дня(ей) назад. ({d})', inline = False)
    emb.add_field(name = 'Вошёл', value = f'{delta1.days} дня(ей) назад. ({d1})', inline = False)
    emb.add_field(name = 'Упоминание', value = member.mention)
    emb.add_field(name = 'Raw имя', value = member.name)
    emb.add_field(name = 'Никнейм', value = member.nick)
    emb.add_field(name = 'Статус', value = member.status)
    if member.activities != None and member.status != 'offline':
        emb.add_field(name = 'Активности', value = ', '.join([activity.name for activity in member.activities]))
    limit = len(member.roles)
    if limit != 1: 
        if limit > 21:
            emb.add_field(name = 'Роли', value = f'Слишком много для отрисовки ({len(member.roles)-1}) [лимит 20]', inline = False)
            emb.add_field(name = 'Высшая Роль', value = member.top_role.mention, inline = False)
        elif limit == 21:
            emb.add_field(name = f'Роли ({len(member.roles)-1}) [лимит достигнут]', value = ', '.join([role.mention for role in member.roles[1:]]), inline = False)
            emb.add_field(name = 'Высшая Роль', value = member.top_role.mention, inline = False)
        elif limit == 20:
            emb.add_field(name = f'Роли ({len(member.roles)-1}) [1 до лимита]', value = ', '.join([role.mention for role in member.roles[1:]]), inline = False)
            emb.add_field(name = 'Высшая Роль', value = member.top_role.mention, inline = False)
        elif limit == 19:
            emb.add_field(name = f'Роли ({len(member.roles)-1}) [2 до лимита]', value = ', '.join([role.mention for role in member.roles[1:]]), inline = False)
            emb.add_field(name = 'Высшая Роль', value = member.top_role.mention, inline = False)
        elif limit == 18:
            emb.add_field(name = f'Роли ({len(member.roles)-1}) [3 до лимита]', value = ', '.join([role.mention for role in member.roles[1:]]), inline = False)
            emb.add_field(name = 'Высшая Роль', value = member.top_role.mention, inline = False)
        else:
            emb.add_field(name = f'Роли ({len(member.roles)-1})', value = ', '.join([role.mention for role in member.roles[1:]]), inline = False)
            emb.add_field(name = 'Высшая Роль', value = member.top_role.mention, inline = False)
    else:
        emb.add_field(name = 'Роли', value = 'Ролей не обнаружено.')
    emb.add_field(name = 'Бот?', value = bot)
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
        if msg.content == 'хуй через плечо' and sent.content == 'чё':
            await ctx.send(f'Поздравляю, у вас 3 стадия рака!')
            await sent1.delete()
            await sent.delete()
        elif sent.content == 'а' and msg.content == 'хуй на':
            await ctx.send(f'Поздравляю, у вас 3 стадия рака!')
            await sent1.delete()
            await sent.delete()
        elif sent.content == 'чего' and msg.content == 'хуй на воротничок': #чего бля
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
    emb = discord.Embed(description = '[осуждающее видео](https://vk.com/video-184856829_456240358)', colour = discord.Color.orange())
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
@commands.cooldown(1, 5, commands.BucketType.guild)
async def content(ctx, msg):
    await ctx.message.delete()
    message = await ctx.fetch_message(id = msg)
    if message.author == client.user:
        if message.embeds == []:
            await ctx.send(f'```cy/say noembed "{message.content}"```')
        else:
            for emb in message.embeds:
                await ctx.send(f'```cy/say "" "" "{emb.title}" "{emb.description}" {emb.image.url} {emb.thumbnail.url} {emb.colour} @{emb.author.name}```')
    else:
        if message.embeds == []:
            await ctx.send(f'```@{message.author} {message.content}```')
        else:
            for emb in message.embeds:
                await ctx.send(f'```content {message.content} title {emb.title} description {emb.description} footer {emb.footer.text} color {emb.colour} author {emb.author.name} image {emb.image.url} footer img {emb.thumbnail.url}```')

@client.command(aliases = ['say_e'])
@commands.has_permissions(mention_everyone = True)
@commands.cooldown(1, 20, commands.BucketType.guild)
async def say_everyone(ctx, embed = None, text = None, t = None, d = None, img = None, f = None, c = None, a: discord.Member = None):
    await ctx.message.delete()
    if c == None:
        c = ctx.author.color
    else:
        c = int('0x' + c, 16)
    if img == None:
        img = ('')
    if f == None:
        f = ('')
    emb = discord.Embed(title = t, description = d, colour = c)
    if a != None and a.id != ctx.author.id:
        emb.set_author(name = f'{a} ({ctx.author})', icon_url = a.avatar_url)
    else:
        emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
    emb.set_image(url = img)
    emb.set_thumbnail(url = f)
    if embed == 'noembed':
        await ctx.send(f'@everyone {text}')
    elif embed != 'noembed':
        await ctx.send('@everyone', embed = emb)
    
@client.command(aliases = ['Say', 'SAY'])
@commands.has_permissions(manage_channels = True)
async def say(ctx, embed = None, text = None, t = None, d = None, img = None, f = None, c = None, a: discord.Member = None, *, role: discord.Role = None):
    await ctx.message.delete()
    if c == None:
        c = ctx.author.color
    else:
        c = int('0x' + c, 16)
    if img == None:
        img = ('')
    if f == None:
        f = ('')
    if role != None:
        c = role.color
    emb = discord.Embed(title = t, description = d, colour = c)
    if a != None and a.id != ctx.author.id:
        emb.set_author(name = f'{a} ({ctx.author})', icon_url = a.avatar_url)
    else:
        emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
    emb.set_image(url = img)
    emb.set_thumbnail(url = f)
    if role != None and embed != 'noembed':
        await ctx.send(role.mention, embed = emb)
    elif role == None and embed != 'noembed':
        await ctx.send(embed = emb)
    if embed == 'noembed':
        await ctx.send(text)

@client.command(aliases = ['Edit', 'EDIT'])
@commands.has_permissions(manage_channels = True)
async def edit(ctx, msg, embed = None, text = None, t = None, d = None, img = None, f = None, c = None, a : discord.Member = None):
    await ctx.message.delete()
    message = await ctx.fetch_message(id = msg)
    if c == None:
        c = ctx.author.color
    else:
        c = int('0x' + c, 16)
    if img == None:
        img = ('')
    if f == None:
        f = ('')
    emb = discord.Embed(title = t, description = d, colour = c)
    if a != None:
        emb.set_author(name = f'{a} ({ctx.author})', icon_url = a.avatar_url)
    else:
        emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
    emb.set_image(url = img)
    emb.set_thumbnail(url = f)
    if embed == 'noembed':
        if message.author == client.user:
            if text == '--clean':
                await message.edit(content = None)
                await ctx.send('👌', delete_after = 1)
            elif text == '--delete':
                await message.delete()
                await ctx.send('👌', delete_after = 1)
            else:
                await message.edit(content = text)
                await ctx.send('👌', delete_after = 1)
        else:
            await ctx.send(f'{message.id} не является сообщением от {client.user.mention}.')
    else:
        if message.author == client.user:
            await message.edit(embed = emb)
            await ctx.send('👌', delete_after = 1)
        else:
            await ctx.send(f'{message.id} не является сообщением от {client.user.mention}.')
#Embeds

#Cephalon
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
    emb.add_field(name = 'Версия', value = '0.12.8.9457')
    emb.add_field(name = 'Написан на', value = 'discord.py')
    emb.add_field(name = 'Разработчик', value = 'сасиска#2472')
    emb.add_field(name = 'Веб-сайт', value = '```http://ru-unioncraft.ru/```')
    emb.add_field(name = 'Существую на', value = f'{len(client.guilds)} серверах')
    emb.set_footer(text = 'Данное приложение не имеет никакого причастия к игре Warframe.', icon_url = 'https://i.playground.ru/p/yVaOZNSTdgUTxmzy_qvzzQ.png')
    await ctx.send(embed = emb)

@client.command(aliases = ['Help', 'HELP'])
@commands.cooldown(1, 3, commands.BucketType.guild)
async def help(ctx, arg = None):
    await ctx.message.delete()
    if arg == None:
        emb = discord.Embed(title = client.user.name, description = 'Вот команды, что я могу выполнить. ||Несколько команд ниже требуют некоторых прав.||', colour = discord.Color.orange())
        emb.add_field(name = 'Cephalon', value = '`info`, `invite`, `join`, `leave`, `ping`', inline = False)
        emb.add_field(name = 'Embeds', value = '`content`, `edit`, `say`, `say_everyone`', inline = False)
        emb.add_field(name = 'Fun', value = '`aye_balbec`, `cu`, `coinflip`, `dotersbrain`, `niggers`, `rp`, `rap`, `zatka`', inline = False)
        emb.add_field(name = 'Mod', value = '`ban`, `clear`, `dm`, `give`, `kick`, `mute`, `take`, `unmute`', inline = False)
        emb.add_field(name = 'Misc', value = '`about`, `avatar`, `guild`, `remind`, `role`, `rolemembers`, `someone`, `vote`', inline = False)
        emb.add_field(name = 'ᅠ', value = 'Используйте `cy/help [команда]` для подробностей.', inline = False)
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb)
    elif arg == 'about':
        await ctx.send('```cy/about [@пинг/имя/ID] ([] - опционально, / - или)```')
    elif arg == 'avatar':
        await ctx.send('```cy/avatar [@пинг/имя/ID] ([] - опционально, / - или)```')
    elif arg == 'ban':
        await ctx.send('```cy/ban <@пинг/имя/ID> [причина] ([] - опционально, <> - обязательно, / - или)```')
    elif arg == 'content':
        await ctx.send('```cy/content <ID> (<> - обязательно)```')
    elif arg == 'clear':
        await ctx.send('```cy/clear <количество> [y/n] ([] - опционально, <> - обязательно, / - или)```')
    elif arg == 'dm':
        await ctx.send('```cy/dm <@пинг/имя/ID> <текст> (<> - обязательно, / - или)```')
    elif arg == 'say':
        await ctx.send('```cy/say [noembed] [text] [title текст] [description текст] [ссылка] [ссылка] [цвет] [@пинг/имя/ID] [@роль/имя роли/ID роли](cy/say "" "" "title" "description") ([] - опционально, / - или)```')
    elif arg == 'edit':
        await ctx.send('```cy/edit <ID> [noembed] [text] [title текст] [description текст] [ссылка] [ссылка] [цвет] [@пинг/имя/ID]\n(--clean в text удалит контент над эмбедом, --delete удалит сообщение) ([] - опционально, <> - обязательно, / - или)```')
    elif arg == 'say_everyone':
        await ctx.send('```cy/say_everyone [noembed] [text] [title текст] [description текст] [ссылка] [ссылка] [цвет] [@пинг/имя/ID](cy/say_everyone "" "" "title" "description") ([] - опционально, / - или)```')
    elif arg == 'give':
        await ctx.send('```cy/give <@пинг/имя/ID> <@роль/имя роли/ID роли> (<> - обязательно, / - или)```')
    elif arg == 'kick':
        await ctx.send('```cy/kick <@пинг/имя/ID> [причина] ([] - опционально, <> - обязательно, / - или)```')
    elif arg == 'mute':
        await ctx.send('```cy/mute <@пинг/имя/ID> <время(s/m/h/d(15s, 5m, 1h, 5d))> [причина] ([] - опционально, <> - обязательно, / - или)```')
    elif arg == 'remind':
        await ctx.send('```cy/remind <время(s/m/h/d(15s, 5m, 1h, 5d))> <текст> (<> - обязательно, / - или)```')
    elif arg == 'role':
        await ctx.send('```cy/role <@роль/имя роли/ID роли> (<> - обязательно, / - или)```')
    elif arg == 'take':
        await ctx.send('```cy/take <@пинг/имя/ID> <@роль/имя роли/ID роли> (<> - обязательно, / - или)```')
    elif arg == 'someone':
        await ctx.send('```cy/someone <текст> (<> - обязательно)```')
    elif arg == 'unmute':
        await ctx.send('```cy/unmute <@пинг/имя/ID> [причина] ([] - опционально, <> - обязательно, / - или)```')
    elif arg == 'insult':
        await ctx.send('```cy/insult [@пинг/имя/ID] ([] - опционально, / - или)```')
    elif arg == 'vote':
        await ctx.send('```cy/vote <текст> (<> - обязательно)```')
    else:
        emb = discord.Embed(description = f'Команда `{arg}` не обнаружена.', colour = discord.Color.orange())
        await ctx.send(embed = emb)

@client.event
async def on_ready():
    await client.change_presence(status = discord.Status.idle, activity = discord.Activity(type = discord.ActivityType.watching, name = 'Discord API'))
    
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.message.delete()
        emb = discord.Embed(description = f'{ctx.author.mention}, я не знаю такую команду!\n||raw контент - {ctx.message.content}||', colour = discord.Color.orange())
        emb.set_footer(text = 'Считаете, что такая команда должна быть? Напишите сасиска#2472 и опишите её суть!')
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
