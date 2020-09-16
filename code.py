import asyncio
import random
import datetime
import os
import discord
from discord.ext import commands
from discord.utils import get

client = commands.Bot(command_prefix = commands.when_mentioned_or('cy/'))
client.remove_command('help')
client.owner_id = 338714886001524737

#test commands space

#test commands space

@client.command(aliases = ['.пуленепробиваемое-стекло'])
@commands.cooldown(1, 5, commands.BucketType.default)
async def bulletproofglass(ctx):
    await ctx.message.delete()
    await ctx.send('https://cdn.discordapp.com/attachments/694530056281915392/752563367549468882/unknown.png')

@client.command()
@commands.cooldown(1, 5, commands.BucketType.default)
async def rp(ctx):
    await ctx.message.delete()
    emb = discord.Embed(title = 'Ныа', description = 'https://www.youtube.com/watch?v=idmTSW9mfYI', colour = discord.Color.orange())
    await ctx.send(embed = emb)

@client.command()
@commands.cooldown(1, 5, commands.BucketType.default)
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
    emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
    await ctx.send(embed = emb)

@client.command(aliases = ['Info', 'INFO'])
@commands.cooldown(1, 5, commands.BucketType.default)
async def info(ctx):
    await ctx.message.delete()
    emb = discord.Embed(title = 'Welcome to the cum zone', colour = discord.Color.orange())
    emb.set_author(name = client.user.name, icon_url = client.user.avatar_url)
    emb.add_field(name = 'Cephalon', value = '[Cy](https://warframe.fandom.com/wiki/Cephalon_Cy)')
    emb.add_field(name = 'Версия', value = '0.12.7.8824')
    emb.add_field(name = 'Написан на', value = 'discord.py')
    emb.add_field(name = 'Разработчик', value = 'Написано в футере, ха!')
    emb.add_field(name = 'Веб-сайт', value = '```http://ru-unioncraft.ru/```')
    emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
    await ctx.send(embed = emb)
    
@client.command()
@commands.cooldown(1, 5, commands.BucketType.default)
async def aliases(ctx):
    await ctx.message.delete()
    emb = discord.Embed(description = 'Неочевидные *никнеймы* команд', colour = discord.Color.orange())
    emb.add_field(name = 'invite_cy', value = 'invite, invcy')
    emb.add_field(name = 'rap', value = '.rap')
    emb.add_field(name = 'about', value = 'me')
    emb.add_field(name = 'image', value = 'img&')
    emb.add_field(name = 'emb_edit', value = 'emb_ed')
    emb.add_field(name = 'embed', value = 'emb')
    emb.add_field(name = 'coinflip', value = 'c, coin')
    emb.add_field(name = 'content', value = 'ctx')
    emb.add_field(name = 'А также', value = 'Для остальных команд также есть *никнеймы*, их можно писать с заглавной буквы или полностью капсом')
    emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
    await ctx.send(embed = emb)
    
@client.command(aliases = ['invite', 'invcy'])
@commands.cooldown(1, 5, commands.BucketType.default)
async def invite_cy(ctx):
    await ctx.message.delete()
    emb = discord.Embed(colour = discord.Color.orange(), timestamp = ctx.message.created_at)
    emb.add_field(name = 'Ссылка для быстрого приглашения Cy на сервера', value = 'https://discordapp.com/oauth2/authorize?&client_id=694170281270312991&scope=bot&permissions=8')
    emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
    await ctx.send(embed = emb)
    
@client.command(aliases = ['Ping', 'PING'])
@commands.cooldown(1, 5, commands.BucketType.default)
async def ping(ctx):
    await ctx.message.delete()
    emb = discord.Embed(description = f'Pong! `{round(client.latency * 1000)} ms`', colour = discord.Color.orange(), timestamp = ctx.message.created_at)
    emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
    await ctx.send(embed = emb)
    
@client.command(aliases = ['.rap'])
@commands.cooldown(1, 5, commands.BucketType.default)
async def rap(ctx):
    await ctx.message.delete()
    emb = discord.Embed(colour = ctx.author.color, timestamp = ctx.message.created_at)
    emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
    emb.set_image(url = 'https://thumbs.gfycat.com/MessyCarefreeHousefly-size_restricted.gif')
    emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
    await ctx.send(embed = emb)
    
@client.command(aliases = ['ctx'])
@commands.cooldown(1, 5, commands.BucketType.default)
async def content(ctx, arg):
    await ctx.message.delete()
    message = await ctx.fetch_message(id = arg)
    await ctx.send(f'```{message.content}```')
    
@client.command()
@commands.cooldown(1, 5, commands.BucketType.default)
async def remind(ctx, time:int, *, arg):
    await ctx.message.delete()
    emb = discord.Embed(colour = ctx.author.color, timestamp = ctx.message.created_at)
    emb.add_field(name = 'Напомню через', value = f'{time} минут(у, ы)')
    emb.add_field(name = 'О чём напомню?', value = arg)
    emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
    await ctx.send(embed = emb)
    await asyncio.sleep(time*60)
    emb = discord.Embed(title = 'Напоминание', colour = ctx.author.color)
    emb.add_field(name = 'Напомнил через', value = f'{time} минут(у, ы)')
    emb.add_field(name = 'Напоминаю о', value = arg)
    emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
    await ctx.send(f'{ctx.author.mention}', embed = emb) 
   
@client.command(aliases = ['Guild', 'GUILD'])
@commands.cooldown(1, 5, commands.BucketType.default)
async def guild(ctx, guild : discord.Guild = None):
    if guild == None:
        guild = ctx.guild
    await ctx.message.delete()
    emb = discord.Embed(title = f'Информация о {guild}', colour = discord.Color.orange(), timestamp = ctx.message.created_at)
    emb.add_field(name = 'ID сервера', value = guild.id)
    emb.add_field(name = 'Уровень сервера', value = guild.premium_tier)
    emb.add_field(name = 'Люди, бустящие сервер', value = guild.premium_subscribers)
    emb.add_field(name = 'Владелец сервера', value = guild.owner.mention, inline = False)
    emb.add_field(name = 'Количество человек на сервере', value = guild.member_count)
    emb.add_field(name = 'Дата создания сервера', value = guild.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline = False)
    emb.set_thumbnail(url = guild.icon_url)
    emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
    await ctx.send(embed = emb)
    
@client.command()
@commands.cooldown(1, 5, commands.BucketType.default)
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
    emb.add_field(name = 'Создана', value = role.created_at.strftime("%A, %#d %B %Y, %I:%M %p UTC"), inline = False)
    emb.add_field(name = 'Показывает участников отдельно?', value = role.hoist)
    emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
    await ctx.send(embed = emb)
    
@client.command(aliases = ['Avatar', 'AVATAR'])
@commands.cooldown(1, 5, commands.BucketType.default)
async def avatar(ctx, member : discord.Member = None):
    await ctx.message.delete()
    if member == None:
        member = ctx.author
    emb = discord.Embed(description = f'[Прямая ссылка]({member.avatar_url})', colour = member.color)
    emb.set_author(name = member)
    emb.set_image(url = member.avatar_url)
    emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
    await ctx.send(embed = emb)
    
@client.command(aliases = ['me', 'Me', 'ME', 'About', 'ABOUT'])
@commands.cooldown(1, 5, commands.BucketType.default)
async def about(ctx, member: discord.Member = None):
    await ctx.message.delete()
    if member == None:
        member = ctx.author
    if member.nick == None:
        member.nick = 'Не указан'
    if member.bot == False:
        bot = 'Неа'
    elif member.bot == True:
        bot = 'Ага'
    emb = discord.Embed(title = f'Информация о {member.name}', colour = member.color, timestamp = ctx.message.created_at)
    emb.add_field(name = 'ID', value = member.id)
    emb.add_field(name = 'Создан', value = member.created_at.strftime("%A, %#d %B %Y, %I:%M %p UTC"), inline = False)
    emb.add_field(name = 'Вошёл', value = member.joined_at.strftime("%A, %#d %B %Y, %I:%M %p UTC"), inline = False)
    emb.add_field(name = 'Упоминание', value = member.mention)
    emb.add_field(name = 'Имя', value = member.name)
    emb.add_field(name = 'Никнейм', value = member.nick)
    emb.add_field(name = 'Статус', value = member.status)
    emb.add_field(name = f'Роли [{len(member.roles)-1}]', value=' '.join([role.mention for role in member.roles[1:]]), inline = False)
    emb.add_field(name = 'Высшая Роль', value = member.top_role.mention, inline = False)
    emb.add_field(name = 'Бот?', value = bot)
    emb.set_thumbnail(url = member.avatar_url)
    emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
    await ctx.send(embed = emb)
    
@client.command(aliases = ['Unmute', 'UNMUTE'])
@commands.has_permissions(manage_channels = True)
async def unmute(ctx, member : discord.Member, *, reason = None):
    await ctx.message.delete()
    role = discord.utils.get(ctx.message.guild.roles, name = 'Muted')
    if role is not None:
        await member.remove_roles(role)
        if reason == None:
            reason = 'Не указана'
        emb = discord.Embed(title = f'Принудительное снятие мута у {member.name}', colour = member.color, timestamp = ctx.message.created_at)
        emb.add_field(name = 'Снял мут', value = ctx.author.mention)
        emb.add_field(name = 'По причине', value = reason)
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb)
    else:
        emb = discord.Embed(description = f'{ctx.author.mention}, Я не могу снять мут у {member.mention} из-за того, что роль {role.mention} была удалена/отредактирована!', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb)
        
@client.command(aliases = ['Mute', 'MUTE'])
@commands.has_permissions(manage_channels = True)
@commands.cooldown(1, 10, commands.BucketType.default)
async def mute(ctx, member: discord.Member, time : int, *, reason = None):
    await ctx.message.delete()
    guild = ctx.guild
    if member.id != client.owner_id:
        role = discord.utils.get(guild.roles, name = 'Muted')
        if role is not None:
            await member.add_roles(role)
            if reason == None:
                reason = 'Не указана'
            emb = discord.Embed(colour = member.color, timestamp = ctx.message.created_at)
            emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            emb.add_field(name = 'В муте', value = f'{member.mention}')
            emb.add_field(name = 'По причине', value = reason)
            emb.add_field(name = 'Время мута в минутах', value = time)
            emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
            await ctx.send(embed = emb, delete_after = time*60)
            await asyncio.sleep(time*60)
            if role is not None:
                emb = discord.Embed(colour = member.color, timestamp = ctx.message.created_at)
                emb.add_field(name = 'Размучен по истечению времени', value = member.mention)
                emb.add_field(name = 'По причине', value = reason)
                emb.add_field(name = 'Время мута в минутах составляло', value = time)
                emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
                await ctx.send(f'{member.mention}', embed = emb)
                await member.remove_roles(role)
            else:
                emb = discord.Embed(description = f'{ctx.author.mention}, Я не могу снять мут у {member.mention} из-за того, что роль Muted была удалена/отредактирована!', colour = discord.Color.orange())
                emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
                await ctx.send(embed = emb)
        else:
            await guild.create_role(name = 'Muted', colour = discord.Colour(0x000001))
            emb1 = discord.Embed(description = f'{ctx.author.mention}, По причине того, что я не нашёл нужную роль, была создана роль {role.mention} с цветом 0x000001.', colour = discord.Color.orange())
            emb1.set_footer(text = 'Это сообщение должно показываться только 1 раз. Иначе, роль была удалена/отредактирована')
            await ctx.send(embed = emb1)
            await asyncio.sleep(3)
            role = discord.utils.get(guild.roles, name = 'Muted')
            await member.add_roles(role)
            emb = discord.Embed(colour = member.color, timestamp = ctx.message.created_at)
            emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            emb.add_field(name = 'В муте', value = f'{member.mention}')
            emb.add_field(name = 'По причине', value = reason)
            emb.add_field(name = 'Время мута в минутах', value = time)
            emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
            await ctx.send(embed = emb, delete_after = time*60)
            await asyncio.sleep(time*60)
            if role is not None:
                emb = discord.Embed(colour = member.color, timestamp = ctx.message.created_at)
                emb.add_field(name = 'Размучен по истечению времени', value = member.mention)
                emb.add_field(name = 'По причине', value = reason)
                emb.add_field(name = 'Время мута в минутах составляло', value = time)
                emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
                await ctx.send(f'{member.mention}', embed = emb)
                await member.remove_roles(role)
    else:
        emb = discord.Embed(description = f'Извините, {ctx.author.mention}, но вы не можете замутить моего создателя!', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb)
        
@client.command(aliases = ['Give', 'GIVE'])
@commands.has_permissions(manage_channels = True)
async def give(ctx, member: discord.Member, *, role: discord.Role):
    await ctx.message.delete()
    if role is not None:
        await member.add_roles(role)
        channel = client.get_channel(714175791033876490)
        emb = discord.Embed(colour = member.color, timestamp = ctx.message.created_at)
        emb.add_field(name = 'Была выдана роль', value = role)
        emb.add_field(name = 'Выдана:', value = member.mention)
        emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await channel.send(embed = emb)
    else:
        emb = discord.Embed(description = f'{ctx.author.mention}, я не могу найти подходящую роль!', colour = member.color, timestamp = ctx.message.created_at)
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb)
    
@client.command(aliases = ['Take', 'TAKE'])
@commands.has_permissions(manage_channels = True)
async def take(ctx, member: discord.Member, *, role: discord.Role):
    await ctx.message.delete()
    if role is not None:
        await member.remove_roles(role)
        channel = client.get_channel(714175791033876490)
        emb = discord.Embed(colour = member.color, timestamp = ctx.message.created_at)
        emb.add_field(name = 'Была забрана роль', value = role)
        emb.add_field(name = 'Забрана у:', value = member.mention)
        emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await channel.send(embed = emb)
    else:
        emb = discord.Embed(description = f'{ctx.author.mention}, я не могу найти подходящую роль!', colour = member.color, timestamp = ctx.message.created_at)
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb) 
    
@client.command(aliases = ['emb_ctx'])
@commands.cooldown(1, 5, commands.BucketType.default)
async def emb_content(ctx, arg):
    await ctx.message.delete()
    message = await ctx.fetch_message(id = arg)
    for emb in message.embeds:
        await ctx.send(f'```cy/emb t& {emb.title} d& {emb.description} f& {emb.footer.text} c& {emb.colour} a& @{emb.author.name} img& {emb.image.url} fu& {emb.thumbnail.url}```')
            
@client.command(aliases = ['emb_e'])
@commands.has_permissions(mention_everyone = True)
@commands.cooldown(1, 20, commands.BucketType.default)
async def say_everyone(ctx, arg = None, text = None, t = None, d = None, fu = None, img = None, f = None, a = None, au : discord.Member = None):
    await ctx.message.delete()
    if a == None:
        a = ctx.author.color
    else:
        a = int('0x' + a, 16)
    if au == None:
        au = ctx.author
    if fu == None or 'Embed.Empty':
        fu = ('Cephalon Cy by сасиска#2472')
    if img == None:
        img = ('')
    if f == None:
        f = ('')
    emb = discord.Embed(title = t, description = d, colour = a)
    emb.set_author(name = au, icon_url = au.avatar_url)
    emb.set_image(url = img)
    emb.set_thumbnail(url = f)
    emb.set_footer(text = fu)
    if arg == 'noembed':
        await ctx.send('@everyone ' + text)
    elif arg != 'noembed':
        await ctx.send('@everyone', embed = emb)
    
@client.command(aliases = ['Say', 'SAY'])
@commands.has_permissions(manage_channels = True)
async def say(ctx, arg = None, text = None, t = None, d = None, fu = None, img = None, f = None, a = None, au : discord.Member = None, *, role: discord.Role = None):
    await ctx.message.delete()
    if a == None:
        a = ctx.author.color
    else:
        a = int('0x' + a, 16)
    if au == None:
        au = ctx.author
    if fu == None or 'Embed.Empty':
        fu = ('Cephalon Cy by сасиска#2472')
    if img == None:
        img = ('')
    if f == None:
        f = ('')
    if role != None:
        a = role.color
    emb = discord.Embed(title = t, description = d, colour = a)
    emb.set_author(name = au, icon_url = au.avatar_url)
    emb.set_image(url = img)
    emb.set_thumbnail(url = f)
    emb.set_footer(text = fu)
    if role is not None and arg != 'noembed':
        await ctx.send(f'{role.mention}', embed = emb)
    elif role is None and arg != 'noembed':
        await ctx.send(embed = emb)
    if arg == 'noembed':
        await ctx.send(text)

@client.command(aliases = ['emb_ed'])
@commands.has_permissions(manage_channels = True)
async def emb_edit(ctx, arg, t = None, d = None, fu = None, img = None, f = None, a = None, au : discord.Member = None):
    await ctx.message.delete()
    m = await ctx.fetch_message(id = arg)
    if a == None:
        a = ctx.author.color
    else:
        a = int('0x' + a, 16)
    if au == None:
        au = ctx.author
    if fu == None or 'Embed.Empty':
        fu = ('Cephalon Cy by сасиска#2472')
    if img == None:
        img = ('')
    if f == None:
        f = ('')
    emb = discord.Embed(title = t, description = d, colour = a)
    emb.set_author(name = au, icon_url = au.avatar_url)
    emb.set_image(url = img)
    emb.set_thumbnail(url = f)
    emb.set_footer(text = fu)
    await m.edit(embed = emb)
    await ctx.send('👌', delete_after = 1)
    
@client.command(aliases = ['Edit', 'EDIT'])
@commands.has_permissions(manage_channels = True)
async def edit(ctx, arg, *, text):
    await ctx.message.delete()
    m = await ctx.fetch_message(id = arg)
    await m.edit(content = text)
    await ctx.send('👌', delete_after = 1)
    
@client.command(aliases = ['c', 'C', 'coin', 'Coin', 'COIN', 'Coinflip', 'COINFLIP'])
@commands.cooldown(5, 10, commands.BucketType.default)
async def coinflip(ctx):
    await ctx.message.delete()
    choices = ['Орёл!', 'Решка!']
    rancoin = random.choice(choices)
    await ctx.send(rancoin)

@client.command(aliases = ['Cu', 'CU'])
@commands.cooldown(1, 5, commands.BucketType.default)
async def cu(ctx):
    await ctx.message.delete()
    await ctx.send('Медь')
    
#бесполезное говно
@client.command(aliases = ['Join', 'JOIN'])
async def join(ctx):
    await ctx.message.delete()
    if ctx.author.voice and ctx.author.voice.channel:
        channel = ctx.author.voice.channel
    else:
        emb = discord.Embed(description = 'Ты должен быть в канале, чтобы использовать это.', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb)
        return
    global vc
    vc = await channel.connect()

@client.command(aliases = ['Leave', 'LEAVE'])
async def leave(ctx):
    await ctx.message.delete()
    if vc.is_connected():
        await vc.disconnect()
            
@client.command()
@commands.has_permissions(administrator = True)
@commands.cooldown(1, 5, commands.BucketType.default)
async def dm(ctx, member: discord.Member, *, arg):
    await ctx.message.delete()
    emb = discord.Embed(description = f'{arg}', colour = member.color)
    emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
    emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
    await member.send(embed = emb)

#ИВЕНТЫ       
@client.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    if message_id == 707496056505761802:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)

        if payload.emoji.name == 'strashilka':
            role = discord.utils.get(guild.roles, name = 'Пробивший дно')

        if role is not None:
            member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
            if member is not None:
                await member.add_roles(role)

@client.event
async def on_raw_reaction_remove(payload):
    message_id = payload.message_id
    if message_id == 707496056505761802:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)

        if payload.emoji.name == 'strashilka':
            role = discord.utils.get(guild.roles, name = 'Пробивший дно')

        if role is not None:
            member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
            if member is not None:
                await member.remove_roles(role)        

@client.event
async def on_member_join(member):
    channel = client.get_channel(693929823030214658)
    if member.bot == False:
        role = discord.utils.get(member.guild.roles, id = 693933516294979704)
        role1 = discord.utils.get(member.guild.roles, id = 693933510523879454)
        role2 = discord.utils.get(member.guild.roles, id = 693933514198089838)
        if role is not None:
            await member.add_roles(role, role1, role2)
        emb = discord.Embed(description = f'{member.mention} ({member.name}) Has entered the ♂️dungeon♂️, 👋', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await channel.send(embed = emb)
    else:
        role = discord.utils.get(member.guild.roles, id = 693933516831850527)
        role1 = discord.utils.get(member.guild.roles, id = 693933511412940800)
        if role is not None:
            await member.add_roles(role, role1)
        emb = discord.Embed(description = f'А, {member.mention} ({member.name}) - очередной ботяра? ок', colour = discord.Color.orange())
        await channel.send(embed = emb)

@client.event
async def on_member_remove(member):
    channel = client.get_channel(693929823030214658)
    if member.bot == False:
        emb = discord.Embed(description = f'{member.mention} ({member.name}) Has exited the ♂️dungeon♂️...', colour = discord.Color.red())
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await channel.send(embed = emb)
    else:
        emb = discord.Embed(description = f'{member.mention} ({member.name}), ну и вали, ботаря, хаха!', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await channel.send(embed = emb)

@client.event
async def on_voice_state_update(member, before, after):
    if after.channel.id == 742647888424730735:
        category = discord.utils.get(member.guild.categories, id = 742647888101769236)
        channel = await member.guild.create_voice_channel(name = f'Комната {member}', category = category)
        await member.move_to(channel)
        await channel.set_permissions(member, mute_members = True, move_members = True, manage_channels = True)
        def check(a,b,c):
            return len(channel.members) == 0
        await client.wait_for('voice_state_update', check = check)
        await channel.delete()

@client.event
async def on_message(message):
    channel = client.get_channel(714175791033876490)
    if channel is None:
        await client.process_commands(message)
        return
    if not message.author.bot:
        emb = discord.Embed(colour = discord.Color.orange(), timestamp = datetime.datetime.utcnow())
        emb.set_author(name = message.author, icon_url = message.author.avatar_url)
        emb.add_field(name = 'В канале', value = f'{message.channel.mention} ({message.channel.name})')
        emb.add_field(name = 'Было написано', value = message.content)
        emb.set_footer(text = f'Cephalon Cy by сасиска#2472 || guild - {message.guild}')
        await client.process_commands(message)
        await channel.send(embed = emb)
    
@client.event
async def on_message_edit(before, after):
    channel = client.get_channel(714175791033876490)
    if channel is None:
        return
    if not before.author.bot:
        emb = discord.Embed(description = f'[Сообщение]({before.jump_url}) было изменено', colour = discord.Color.orange(), timestamp = datetime.datetime.utcnow())
        emb.set_author(name = before.author.name, icon_url = before.author.avatar_url)
        emb.add_field(name = 'Было', value = f'```{before.content}```')
        emb.add_field(name = 'Стало', value = f'```{after.content}```')
        emb.set_footer(text = f'Cephalon Cy by сасиска#2472 || guild - {before.guild}')
        await channel.send(embed = emb)
#ИВЕНТЫ    

#help command
@client.command(aliases = ['Help', 'HELP'])
@commands.cooldown(1, 3, commands.BucketType.default)
@commands.has_permissions(kick_members = True)
async def help(ctx, arg = None):
    await ctx.message.delete()
    if arg == None:
        emb = discord.Embed(title = "Меню команд Cephalon Cy", description = 'Существует дополнительная помощь по командам, пропишите cy/help |команда|', colour = discord.Color.orange())
        emb.add_field(name = 'cy/about', value = 'Показывает информацию о человеке.')
        emb.add_field(name = 'cy/aliases', value = 'Для просмотра **никнеймов** команд', inline = False)
        emb.add_field(name = 'cy/avatar', value = 'Показывает аватар человека.')
        emb.add_field(name = 'cy/ban', value = 'Бан игрока.')
        emb.add_field(name = 'cy/clear', value = 'Очистка чата.')
        emb.add_field(name = 'cy/dm', value = 'Пишет участнику любой написанный текст.')
        emb.add_field(name = 'cy/edit', value = 'Редактирует сообщение.', inline = False)
        emb.add_field(name = 'cy/say', value = 'От лица бота отправляется высоконастраеваемый эмбед. Может использоваться как say, так и emb')
        emb.add_field(name = 'cy/emb_ctx', value = 'Позволяет увидеть контент эмбеда.')
        emb.add_field(name = 'cy/emb_edit', value = 'Редактирует эмбед. Работает как VAULTBOT', inline = False)
        emb.add_field(name = 'cy/say_everyone', value = 'Совмещает в себе команды everyone и emb.')
        emb.add_field(name = 'cy/everyone', value = 'Пишет сообщение от лица бота и пингует @everyone')
        emb.add_field(name = 'cy/give', value = 'Выдаёт роль.', inline = False)
        emb.add_field(name = 'cy/guild', value = 'Показывает информацию о сервере.')
        emb.add_field(name = 'cy/join', value = 'Бот заходит в голосовой канал.')
        emb.add_field(name = 'cy/kick', value = 'Кик игрока.')
        emb.add_field(name = 'cy/leave', value = 'Бот выходит из голосового канала.')
        emb.add_field(name = 'cy/mute', value = 'Мут игрока.', inline = False)
        emb.add_field(name = 'cy/remind', value = 'Может напомнить вам о событии, которое вы не хотите пропустить.')
        emb.add_field(name = 'cy/role', value = 'Показывает информацию о роли')
        emb.add_field(name = 'cy/take', value = 'Забирает роль.', inline = False)
        emb.add_field(name = 'cy/unmute', value = 'Принудительный размут игрока.')
        emb.add_field(name = 'Обозначение символов cy/help', value = '|| - опционально, <> - обязательно')
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb)
    elif arg == 'about':
        await ctx.send('```cy/about |@пинг/имя/ID|```')
    elif arg == 'avatar':
        await ctx.send('```cy/avatar |@пинг/имя/ID|```')
    elif arg == 'ban':
        await ctx.send('```cy/ban <@пинг/имя/ID> |причина|```')
    elif arg == 'clear':
        await ctx.send('```cy/clear <количество>```')
    elif arg == 'dm':
        await ctx.send('```cy/dm <@пинг/имя/ID> <текст>```')
    elif arg == 'edit':
        await ctx.send('```cy/edit <ID> <новый текст>```')
    elif arg == 'say':
        await ctx.send('```cy/say |noembed| |text| |title текст| |description текст| |footer текст| |ссылка| |ссылка| |цвет| |@пинг| |@роль/имя роли/ID роли|```')
    elif arg == 'emb_ctx':
        await ctx.send('```cy/emb_ctx <ID>```')
    elif arg == 'emb_edit':
        await ctx.send('```cy/emb_edit <ID> |title текст| |description текст| |footer текст| |ссылка| |ссылка| |цвет| |@пинг| |@роль/имя роли/ID роли|```')
    elif arg == 'say_everyone':
        await ctx.send('```cy/say_everyone |title текст| |description текст| |footer текст| |ссылка| |ссылка| |цвет| |@пинг| |@роль/имя роли/ID роли|```')
    elif arg == 'give':
        await ctx.send('```cy/give <@пинг/имя/ID> <@роль/имя роли/ID роли>```')
    elif arg == 'kick':
        await ctx.send('```cy/kick <@пинг/имя/ID> |причина|```')
    elif arg == 'mute':
        await ctx.send('```cy/mute <@пинг/имя/ID> <время> |причина|```')
    elif arg == 'remind':
        await ctx.send('```cy/remind <время> <текст>```')
    elif arg == 'role':
        await ctx.send('```cy/role <@роль/имя роли/ID роли>```')
    elif arg == 'take':
        await ctx.send('```cy/take <@пинг/имя/ID> <@роль/имя роли/ID роли>```')
    elif arg == 'unmute':
        await ctx.send('```cy/unmute <@пинг/имя/ID> |причина|```')
    else:
        emb = discord.Embed(description = 'Для этой команды не нужны аргументы', colour = discord.Color.orange())
        emb.set_footer(text = 'Хотя, возможно, вы ввели команду неправильно?')
        await ctx.send(embed = emb)

@client.command()
async def time(ctx):
    await ctx.message.delete()
    date_now = datetime.datetime.now()
    emb = discord.Embed(colour = discord.Color.orange())
    emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
    emb.add_field(name = 'Время по Гринвичу равняется', value = date_now)
    await ctx.send(embed = emb)

#проверка на подключение
@client.event
async def on_ready():
    await client.change_presence(status = discord.Status.idle, activity = discord.Activity(type = discord.ActivityType.watching, name = 'В Discord API'))

#kick
@client.command(aliases = ['Kick', 'KICK'])
@commands.cooldown(1, 10, commands.BucketType.default)
@commands.has_permissions(kick_members = True)
async def kick(ctx , member: discord.Member, *, reason: str = None):
    await ctx.message.delete()
    if member.id != client.owner_id:
        emb = discord.Embed(colour = member.color)
        await member.kick(reason = reason)
        emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
        emb.add_field(name = 'Был кикнут', value = member.mention)
        emb.add_field(name = 'По причине', value = reason)
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb)
    else:
        emb = discord.Embed(description = f'Извините, {ctx.author.mention}, но вы не можете кикнуть моего создателя!', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb)
#ban
@client.command(aliases = ['Ban', 'BAN'])
@commands.cooldown(1, 10, commands.BucketType.default)
@commands.has_permissions(ban_members = True)
async def ban(ctx , member: discord.Member, *, reason: str = None):
    await ctx.message.delete()
    if member.id != client.owner_id:
        emb = discord.Embed(colour = member.color)
        await member.ban(reason = reason)
        emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
        emb.add_field(name = 'Был забанен', value = member.mention)
        emb.add_field(name = 'По причине', value = reason)
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb)
    else:
        emb = discord.Embed(description = f'Извините, {ctx.author.mention}, но вы не можете забанить моего создателя!', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb)
        
#message delete
@client.command(aliases = ['Clear', 'CLEAR'])
@commands.cooldown(1, 10, commands.BucketType.default)
@commands.has_permissions(administrator = True)
async def clear(ctx, amount : int, confirm : str = None):
    await ctx.message.delete()
    if amount == 0:
        emb = discord.Embed(description = 'Удалять 0 сообщений? Ты еблан?', colour = discord.Color.red())
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb, delete_after = 3)
    elif amount == 1:
        emb = discord.Embed(description = f'удалено {amount} сообщение', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.channel.purge(limit = amount)
        await ctx.send(embed = emb, delete_after = 1)
    elif amount == 2:
        emb = discord.Embed(description = f'удалено {amount} сообщения', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.channel.purge(limit = amount)
        await ctx.send(embed = emb, delete_after = 1)
    elif amount == 3:
        emb = discord.Embed(description = f'удалено {amount} сообщения', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.channel.purge(limit = amount)
        await ctx.send(embed = emb, delete_after = 1)
    elif amount == 4:
        emb = discord.Embed(description = f'удалено {amount} сообщения', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.channel.purge(limit = amount)
        await ctx.send(embed = emb, delete_after = 1)
    elif amount >= 10:
        if confirm == 'CONFIRM':
            await ctx.send(f'Через 3 секунды будет удалено {amount} сообщений')
            await asyncio.sleep(3)
            await ctx.channel.purge(limit = amount + 1)
            await ctx.send(f'удалено {amount} сообщений', delete_after = 2)
        if confirm == None:
            emb = discord.Embed(description = f'{ctx.author.mention}, для выполнения этой команды мне нужно ваше подтвеждение! (чувствительно к регистру)', colour = discord.Color.orange())
            emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
            await ctx.send(embed = emb)
    else:
        emb = discord.Embed(description = f'удалено {amount} сообщений', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.channel.purge(limit = amount)
        await ctx.send(embed = emb, delete_after = 1)
    
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.message.delete()
        emb = discord.Embed(description = f'{ctx.author.mention}, я не знаю такую команду!', colour = discord.Color.orange())
        emb.set_footer(text = 'Считаете, что такая команда должна быть? Напишите сасиска#2472 и опишите её суть!')
        await ctx.send(embed = emb)
        
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.message.delete()
        emb = discord.Embed(description = f'{ctx.author.mention}, команда в кд, потерпи чутка!', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb)
    
@dm.error
async def dm_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.message.delete()
        emb = discord.Embed(description = f'{ctx.author.mention}, укажите, кому и что написать!', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb)

    if isinstance(error, commands.MissingPermissions):
        await ctx.message.delete()
        emb = discord.Embed(description = f'{ctx.author.mention} пытался вызвать команду dm', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb)
        
@say_everyone.error
async def say_everyone_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.message.delete()
        emb = discord.Embed(description = f'{ctx.author.mention}, так шутить не нужно', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb)

    if isinstance(error, commands.MissingPermissions):
        await ctx.message.delete()
        emb = discord.Embed(description = f'{ctx.author.mention} пытался вызвать команду emb_everyone', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb)
        
@give.error
async def give_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.message.delete()
        emb = discord.Embed(description = f'{ctx.author.mention}, укажите роль, которую нужно выдать!', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb)

    if isinstance(error, commands.MissingPermissions):
        await ctx.message.delete()
        emb = discord.Embed(description = f'{ctx.author.mention} пытался вызвать команду give', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb)
        
@take.error
async def take_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.message.delete()
        emb = discord.Embed(description = f'{ctx.author.mention}, укажите роль, которую нужно забрать!', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb)

    if isinstance(error, commands.MissingPermissions):
        await ctx.message.delete()
        emb = discord.Embed(description = f'{ctx.author.mention} пытался вызвать команду take', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb)
        
@say.error
async def say_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.message.delete()
        emb = discord.Embed(description = f'{ctx.author.mention}, укажите, что я должен сказать!', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb)
            
    if isinstance(error, commands.MissingPermissions):
        await ctx.message.delete()
        emb = discord.Embed(description = f'{ctx.author.mention} пытался вызвать команду say', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb)
        
@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.message.delete()
        emb = discord.Embed(description = f'{ctx.author.mention}, укажите, кого и на сколько мутить!', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb)
        
    if isinstance(error, commands.BadArgument):
        await ctx.message.delete()
        emb = discord.Embed(description = f'{ctx.author.mention}, проверьте правильность написания команды!', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb)
                       
    if isinstance(error, commands.MissingPermissions):
        await ctx.message.delete()
        emb = discord.Embed(description = f'{ctx.author.mention} пытался вызвать команду mute', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb)

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.message.delete()
        emb = discord.Embed(description = f'{ctx.author.mention}, укажите, кого нужно кикнуть!', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb)

    if isinstance(error, commands.MissingPermissions):
        await ctx.message.delete()
        emb = discord.Embed(description = f'{ctx.author.mention} пытался вызвать команду kick', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb)

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.message.delete()
        emb = discord.Embed(description = f'{ctx.author.mention}, укажите, кого нужно забанить!', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb)

    if isinstance(error, commands.MissingPermissions):
        await ctx.message.delete()
        emb = discord.Embed(description = f'{ctx.author.mention} пытался вызвать команду ban', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb)

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.message.delete()
        emb = discord.Embed(description = f'{ctx.author.mention}, укажите, сколько сообщений нужно удалить!', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb)

    if isinstance(error, commands.MissingPermissions):
        await ctx.message.delete()
        emb = discord.Embed(description = f'{ctx.author.mention} пытался вызвать команду clear', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb)
        
    if isinstance(error, commands.BadArgument):
        await ctx.message.delete()
        emb = discord.Embed(description = f'{ctx.author.mention}, проверьте правильность написания команды!', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb)
    
t = os.environ.get('t')

client.run(t)
