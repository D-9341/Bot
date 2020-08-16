import youtube_dl
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

@client.command(aliases = ['Info', 'INFO'])
async def info(ctx, amount = 1):
    await ctx.channel.purge(limit = amount)
    emb = discord.Embed(title = 'Привет! Я Cephalon Cy!', colour = discord.Color.orange())
    emb.add_field(name = 'Версия', value = '0.12.7.8631')
    emb.add_field(name = 'Написан на', value = 'discord.py')
    emb.add_field(name = 'Разработчик', value = 'Написано в футере, ха!')
    emb.add_field(name = 'Веб-сайт', value = 'http://ru-unioncraft.ru/')
    emb.add_field(name = 'Шард', value = client.shard_count)
    emb.set_author(name = client.user.name, icon_url = client.user.avatar_url)
    emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
    await ctx.send(embed = emb)
    
@client.command(aliases = ['Ping', 'PING'])
async def ping(ctx, amount = 1):
    await ctx.channel.purge(limit = amount)
    emb = discord.Embed(description = f'Pong! `{round(client.latency * 1000)} ms`', colour = discord.Color.orange(), timestamp = ctx.message.created_at)
    emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
    await ctx.send(embed = emb)
    
@client.command()
@commands.cooldown(1, 5, commands.BucketType.default)
async def remind(ctx, time:int, *, arg, amount = 1):
    await ctx.channel.purge(limit = amount)
    emb = discord.Embed(colour = ctx.author.color, timestamp = ctx.message.created_at)
    emb.add_field(name = 'Напомню через', value = f'{time} минут(у, ы)')
    emb.add_field(name = 'О чём напомню?', value = arg)
    emb.add_field(name = 'Кому?', value = ctx.author.mention)
    emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
    await ctx.send(embed = emb)
    await asyncio.sleep(time*60)
    await ctx.send(f'{ctx.author.mention}')
    emb = discord.Embed(title = 'Напоминание', colour = ctx.author.color)
    emb.add_field(name = 'Напомнил через', value = f'{time} минут(у, ы)')
    emb.add_field(name = 'Напоминаю о', value = arg)
    emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
    await ctx.send(embed = emb) 
   
@client.command(aliases = ['Guild', 'GUILD'])
@commands.cooldown(1, 5, commands.BucketType.default)
async def guild(ctx, guild : discord.Guild = None, amount = 1):
    guild = ctx.guild if not guild else guild
    await ctx.channel.purge(limit = amount)
    emb = discord.Embed(title = f'Информация о {guild}', colour = discord.Color.orange(), timestamp = ctx.message.created_at)
    emb.add_field(name = 'ID сервера', value = guild.id)
    emb.add_field(name = 'Уровень сервера', value = guild.premium_tier)
    emb.add_field(name = 'Люди, бустящие сервер', value = guild.premium_subscribers)
    emb.add_field(name = 'Владелец сервера', value = guild.owner.mention, inline = False)
    emb.add_field(name = 'Количество человек на сервере', value = guild.member_count)
    emb.add_field(name = 'Дата создания сервера', value = guild.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline = False)
    emb.set_thumbnail(url = guild.icon_url)
    emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
    await ctx.send(embed = emb)
    
@client.command(aliases = ['.rap'])
@commands.cooldown(1, 5, commands.BucketType.default)
async def rap(ctx, amount = 1):
    await ctx.channel.purge(limit = amount)
    emb = discord.Embed(colour = ctx.author.color, timestamp = ctx.message.created_at)
    emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
    emb.set_image(url = 'https://thumbs.gfycat.com/MessyCarefreeHousefly-size_restricted.gif')
    emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
    await ctx.send(embed = emb)
    
@client.command(aliases = ['me', 'Me', 'ME', 'About', 'ABOUT'])
@commands.cooldown(1, 5, commands.BucketType.default)
async def about(ctx, member:discord.Member = None, amount = 1):
    await ctx.channel.purge(limit = amount)
    if member == None:
        member = ctx.message.author
    emb = discord.Embed(title = f'Информация о {member.name}', colour = member.color, timestamp = ctx.message.created_at)
    emb.add_field(name = 'ID', value = member.id)
    emb.add_field(name = 'Создан', value = member.created_at.strftime("%A, %#d %B %Y, %I:%M %p UTC"), inline = False)
    emb.add_field(name = 'Вошёл', value = member.joined_at.strftime("%A, %#d %B %Y, %I:%M %p UTC"), inline = False)
    emb.add_field(name = 'Упоминание', value = member.mention)
    emb.add_field(name = 'Имя', value = member.name)
    emb.add_field(name = 'Никнейм', value = member.nick)
    emb.add_field(name = 'Статус', value = member.status)
    emb.add_field(name = 'Пользовательский статус', value = member.activity, inline = False)
    emb.add_field(name = f'Роли [{len(member.roles)-1}]', value=' '.join([role.mention for role in member.roles[1:]]))
    emb.add_field(name = 'Высшая Роль', value = member.top_role.mention, inline = False)
    emb.add_field(name = 'Бот?', value = member.bot)
    emb.set_thumbnail(url = member.avatar_url)
    emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
    await ctx.send(embed = emb)
    
@client.command(aliases = ['Unmute', 'UNMUTE'])
@commands.has_permissions(manage_channels = True)
async def unmute(ctx, member : discord.Member, *, arg, amount = 1):
    await ctx.channel.purge(limit = amount)
    role = discord.utils.get(ctx.message.guild.roles, name = 'Muted')
    if role is not None:
        await member.remove_roles(role)
        emb = discord.Embed(title = f'Принудительное снятие мута у {member.name}', colour = member.color, timestamp = ctx.message.created_at)
        emb.add_field(name = 'Снял мут', value = ctx.author.mention)
        emb.add_field(name = 'По причине', value = arg)
        emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
        await ctx.send(embed = emb)
    else:
        emb = discord.Embed(description = f'{ctx.author.mention}, Я не могу снять мут у {member.mention} из-за того, что роль Muted была удалена/отредактирована!', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
        await ctx.send(embed = emb)
        
    
@client.command(aliases = ['Mute', 'MUTE'])
@commands.has_permissions(manage_channels = True)
@commands.cooldown(1, 10, commands.BucketType.default)
async def mute(ctx, member: discord.Member, time : int, *, arg, amount = 1):
    await ctx.channel.purge(limit = amount)
    if member.id != client.owner_id:
        role = discord.utils.get(ctx.message.guild.roles, name = 'Muted')
        if role is not None:
            await member.add_roles(role)
            emb = discord.Embed(title = f'Мут от {ctx.author}', colour = member.color, timestamp = ctx.message.created_at)
            emb.add_field(name = 'В муте', value = f'{member.mention}')
            emb.add_field(name = 'По причине', value = arg)
            emb.add_field(name = 'Время мута в минутах', value = time)
            emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
            await ctx.send(embed = emb)
            await asyncio.sleep(time*60)
            if role is not None:
                for role in member.roles:
                    if role.name == 'Muted':
                        await ctx.send(f'{member.mention}')
                        emb = discord.Embed(colour = member.color, timestamp = ctx.message.created_at)
                        emb.add_field(name = 'Размучен по истечению времени', value = member.mention)
                        emb.add_field(name = 'По причине', value = arg)
                        emb.add_field(name = 'Время мута в минутах составляло', value = time)
                        emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
                        await ctx.send(embed = emb)
                        await member.remove_roles(role)
                    else:
                        break
            else:
                emb = discord.Embed(description = f'{ctx.author.mention}, Я не могу снять мут у {member.mention} из-за того, что роль Muted была удалена/отредактирована!', colour = discord.Color.orange())
                emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
                await ctx.send(embed = emb)
        else:
            emb = discord.Embed(description = f'{ctx.author.mention}, Я не смог найти подходящую для этой команды роль. Роль должна называться Muted', colour = discord.Color.orange())
            emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
            await ctx.send(embed = emb)
    else:
        emb = discord.Embed(description = f'Извините, {ctx.author.mention}, но вы не можете замутить моего создателя!', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
        await ctx.send(embed = emb)
        
@client.command(aliases = ['Give', 'GIVE'])
@commands.has_permissions(manage_channels = True)
async def give(ctx, arg, member: discord.Member, *, amount = 1):
    await ctx.channel.purge(limit = amount)
    role = discord.utils.get(ctx.message.guild.roles, name = arg)
    await member.add_roles(role)
    channel = client.get_channel(714175791033876490)
    emb = discord.Embed(colour = member.color, timestamp = ctx.message.created_at)
    emb.add_field(name = 'Была выдана роль', value = role)
    emb.add_field(name = 'Выдана:', value = member.mention)
    emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
    emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
    await channel.send(embed = emb)
    
@client.command(aliases = ['Take', 'TAKE'])
@commands.has_permissions(manage_channels = True)
async def take(ctx, arg, member: discord.Member, *, amount = 1):
    await ctx.channel.purge(limit = amount)
    role = discord.utils.get(ctx.message.guild.roles, name = arg)
    await member.remove_roles(role)
    channel = client.get_channel(714175791033876490)
    emb = discord.Embed(colour = member.color, timestamp = ctx.message.created_at)
    emb.add_field(name = 'Была забрана роль', value = role)
    emb.add_field(name = 'Забрана у:', value = member.mention)
    emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
    emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
    await channel.send(embed = emb)
    
@client.command(aliases = ['img&'])
@commands.has_permissions(manage_channels = True)
async def image(ctx, arg, *, amount = 1):
    await ctx.channel.purge(limit = amount)
    emb = discord.Embed(colour = ctx.author.color)
    emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
    emb.set_image(url = arg)
    emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
    await ctx.send(embed = emb)
    
@client.command(aliases = ['emb_e'])
@commands.has_permissions(mention_everyone = True)
@commands.cooldown(1, 20, commands.BucketType.default)
async def everyone_embed(ctx, d, t, img, f, *, amount = 1):
    await ctx.channel.purge(limit = amount)
    await ctx.send('@everyone')
    emb = discord.Embed(colour = ctx.author.color)
    emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
    emb.add_field(name = d, value = t)
    emb.set_image(url = img)
    emb.set_thumbnail(url = f)
    emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
    await ctx.send(embed = emb)
    
@client.command(aliases = ['Embed', 'EMBED', 'emb' , 'Emb', 'EMB'])
@commands.has_permissions(manage_channels = True)
async def embed(ctx, d, t, img, f, *, amount = 1):
    await ctx.channel.purge(limit = amount)
    emb = discord.Embed(colour = ctx.author.color)
    emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
    emb.add_field(name = d, value = t)
    emb.set_image(url = img)
    emb.set_thumbnail(url = f)
    emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
    await ctx.send(embed = emb)

@client.command(aliases = ['emb_ed'])
@commands.has_permissions(manage_channels = True)
async def emb_edit(ctx, arg, d, t, img, f, *, amount = 1):
    await ctx.channel.purge(limit = amount)
    emb = discord.Embed(colour = ctx.author.color)
    m = await ctx.fetch_message(id = arg)
    emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
    emb.add_field(name = d, value = t)
    emb.set_image(url = img)
    emb.set_thumbnail(url = f)
    emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
    await m.edit(embed = emb)
    await ctx.send('👌', delete_after = 1)
    
@client.command(aliases = ['Edit', 'EDIT'])
@commands.has_permissions(manage_channels = True)
async def edit(ctx, arg, *, arg1, amount = 1):
    await ctx.channel.purge(limit = amount)
    m = await ctx.fetch_message(id = arg)
    await m.edit(content = arg1)
    await ctx.send('👌', delete_after = 1)
    
@client.command(aliases = ['Everyone', 'EVERYONE'])
@commands.cooldown(1, 20, commands.BucketType.default)
@commands.has_permissions(mention_everyone = True)
async def everyone(ctx, *, arg, amount = 1):
    await ctx.channel.purge(limit = amount)
    await ctx.send('@everyone ' + arg)
    
@client.command(aliases = ['Say', 'SAY'])
@commands.cooldown(1, 10, commands.BucketType.default)
@commands.has_permissions(manage_channels = True)
async def say(ctx, *, arg, amount = 1):
    await ctx.channel.purge(limit = amount)
    await ctx.send(arg)
    
@client.command(aliases = ['c', 'C', 'coin', 'Coin', 'COIN', 'Coinflip', 'COINFLIP'])
@commands.cooldown(5, 10, commands.BucketType.default)
async def coinflip(ctx, amount = 1):
    await ctx.channel.purge(limit = amount)
    choices = ['Орёл!', 'Решка!']
    rancoin = random.choice(choices)
    await ctx.send(rancoin)

@client.event
async def on_voice_state_update(member, after, before):
    if before.channel.id == 742457421456343272:
        channel = client.get_channel(id = 742469905755930705)
        await member.move_to(channel)
    elif before.channel.id == 742470426487160863:
        channel = client.get_channel(id = 742469942963732582)
        await member.move_to(channel)
    elif before.channel.id == 742470517805809745:
        channel = client.get_channel(id = 742469986458533889)
        await member.move_to(channel)
    
#получение роли по эмодзи       
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
    
#бесполезное говно
@client.command(aliases = ['Join', 'JOIN'])
async def join(ctx):
    if ctx.author.voice and ctx.author.voice.channel:
        channel = ctx.author.voice.channel
    else:
        emb = discord.Embed(description = 'Ты должен быть в канале, чтобы использовать это.', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
        await ctx.send(embed = emb)
        return
    global vc
    try:
        vc = await channel.connect()
        await change_voice_state(self_deaf = True)
    except:
        pass

@client.command(aliases = ['Leave', 'LEAVE'])
async def leave(ctx):
    try:
        if vc.is_connected():
            await vc.disconnect()
    except:
        pass

@client.command()
@commands.has_permissions(administrator = True)
@commands.cooldown(1, 5, commands.BucketType.default)
async def pm(ctx, member: discord.Member, *, arg, amount = 1):
    await ctx.channel.purge(limit = amount)
    emb = discord.Embed(description = f'{arg}', colour = member.color)
    emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
    emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
    await member.send(embed = emb)

@client.event
async def on_member_join(member):
    channel = client.get_channel(693929823030214658)
    if member.bot == False:
        role = discord.utils.get(member.guild.roles, id = 693933516294979704)
        role1 = discord.utils.get(member.guild.roles, id = 693933510523879454)
        role2 = discord.utils.get(member.guild.roles, id = 693933514198089838)
        if role is not None:
            await member.add_roles(role, role1, role2)
        emb = discord.Embed(description = f'{member.mention} Has entered the facility, 👋', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
        await channel.send(embed = emb)
    else:
        role = discord.utils.get(member.guild.roles, id = 693933516831850527)
        role1 = discord.utils.get(member.guild.roles, id = 693933511412940800)
        if role is not None:
            await member.add_roles(role, role1)
        emb = discord.Embed(description = f'А, {member.mention} - очередной ботяра? ок', colour = discord.Color.orange())
        await channel.send(embed = emb)

@client.event
async def on_member_remove(member):
    channel = client.get_channel(693929823030214658)
    if member.bot == False:
        emb = discord.Embed(description = f'{member.mention} Has exited the facility...', colour = discord.Color.red())
        emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
        await channel.send(embed = emb)
    else:
        emb = discord.Embed(description = f'{member.mention}, ну и вали, ботаря, хаха!', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
        await channel.send(embed = emb)

@client.event
async def on_message(message):
    guild = message.guild
    channel = client.get_channel(714175791033876490)
    if channel is None:
        await client.process_commands(message)
        return
    if not message.author.bot:
        emb = discord.Embed(colour = discord.Color.orange(), timestamp = datetime.datetime.utcnow())
        emb.set_author(name = message.author, icon_url = message.author.avatar_url)
        emb.add_field(name = 'В канале', value = message.channel.mention)
        emb.add_field(name = 'Было написано', value = message.content)
        emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
        await channel.send(embed = emb)
        await client.process_commands(message)
    
@client.event
async def on_message_edit(before, after):
    channel = client.get_channel(714175791033876490)
    if channel is None:
        return
    if not before.author.bot:
        emb = discord.Embed(title = 'Сообщение было изменено', colour = discord.Color.orange(), timestamp = datetime.datetime.utcnow())
        emb.set_author(name = before.author.name, icon_url = before.author.avatar_url)
        emb.add_field(name = 'Было', value = before.content)
        emb.add_field(name = 'Стало', value = after.content)
        emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
        await channel.send(embed = emb)
    
#help command
@client.command(aliases = ['Help', 'HELP'])
@commands.cooldown(1, 10, commands.BucketType.default)
@commands.has_permissions(kick_members = True)
async def help(ctx, amount = 1):
    await ctx.channel.purge(limit = amount)
    emb = discord.Embed(title = "Меню команд для администраторов", colour = discord.Color.orange())
    emb.add_field(name = 'Инфо', value = 'Cy, или же сай - бот, написанный сасиска#2472')
    emb.add_field(name = 'cy/info', value = 'Команда для определения - в сети ли бот', inline = False)
    emb.add_field(name = 'cy/clear', value = 'Очистка чата.')
    emb.add_field(name = 'cy/rap', value = '.rap')
    emb.add_field(name = 'cy/ping', value = 'Pong!')
    emb.add_field(name = 'cy/ban', value = 'Бан игрока. Формат - cy/ban @StakanDudka64 дебил')
    emb.add_field(name = 'cy/kick', value = 'Кик игрока. Формат - cy/kick @StakanDudka64 дебил')
    emb.add_field(name = 'cy/mute', value = 'Мут игрока. Формат - cy/mute @StakanDudka64 10 (время измеряется в минутах) дубил. По прошествии времени мут автоматически слетает.~~(ВНИМАНИЕ! ПЕРЕД СНЯТИЕМ МУТА ЧЕЛОВЕКА ПИНГУЕТ НЕСКОЛЬКО РАЗ! НЕ ИСПОЛЬЗУЙТЕ ЭТУ КОМАНДУ СЛИШКОМ ЧАСТО!)~~ исправлено вырезанием этого куска кода', inline = False)
    emb.add_field(name = 'cy/unmute', value = 'Размут игрока. Пример: cy/unmute @StakanDudka64 админ дебил')
    emb.add_field(name = 'cy/remind', value = 'Может напомнить вам что угодно. Формат - cy/remind 10 напоминание')
    emb.add_field(name = 'cy/say', value = 'Пишет сообщение от лица бота. Всё.')
    emb.add_field(name = 'cy/everyone', value = 'Пишет от лица бота и пингует @everyone')
    emb.add_field(name = 'cy/edit', value = 'Редактирует сообщение. Формат - cy/edit (id сообщения) сообщение. При использовании на cy/everyone требует повторного пинга everyone', inline = False)
    emb.add_field(name = 'cy/emb_edit', value = 'Редактирует эмбед. Формат - cy/emb_edit (id), аргументы те же самые, что и на эмбед. Работает как и VAULTBOT', inline = False)
    emb.add_field(name = 'cy/embed', value = 'От лица бота отправляется эмбед. Прочтите #инструкции-cy-бот , чтобы узнать подробнее.')
    emb.add_field(name = 'cy/everyone_embed', value = 'Совмещает в себе команды everyone и embed.')
    emb.add_field(name = 'cy/image', value = 'Бот может прикрепить изображение, в аргумент нужно указать ссылку.')
    emb.add_field(name = 'cy/about', value = 'Показывает информацию о человеке.')
    emb.add_field(name = 'cy/guild', value = 'Показывает информацию о сервере.')
    emb.add_field(name = 'cy/pm', value = 'Пишет участнику любой написанный текст. Формат - cy/pm @пинг "сообщение"')
    emb.add_field(name = 'cy/join', value = 'Бот заходит в голосовой канал.')
    emb.add_field(name = 'cy/leave', value = 'Бот выходит из голосового канала.')
    emb.add_field(name = 'cy/give', value = 'Выдаёт роль, писать в формате: give "выдаваемая роль" @пинг', inline = False)
    emb.add_field(name = 'cy/take', value = 'Забирает роль, писать в формате: take "забираемая роль" @пинг', inline = False)
    emb.add_field(name = 'Послесловие', value = 'Также, для написания команд необязательно писать префикс, можно пингануть бота.')
    emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
    await ctx.send(embed = emb)

@client.command()
async def time(ctx, amount = 1):
    await ctx.channel.purge(limit = amount)
    date_now = datetime.datetime.now()
    emb = discord.Embed(colour = discord.Color.orange())
    emb.set_footer(text = 'Cephalon Cy от сасиска#2472')
    emb.add_field(name = 'Время по Гринвичу равняется', value = date_now)
    await ctx.author.send(embed = emb)

#проверка на подключение
@client.event
async def on_ready():
    await client.change_presence(status = discord.Status.idle, activity = discord.Activity(type = discord.ActivityType.watching, name = 'В Discord API'))

#kick
@client.command(aliases = ['Kick', 'KICK'])
@commands.cooldown(1, 10, commands.BucketType.default)
@commands.has_permissions(kick_members = True)
async def kick(ctx , member: discord.Member, *, reason: str):
    await ctx.channel.purge(limit = 1)
    if member.id != client.owner_id:
        emb = discord.Embed(title = f'Кик от {ctx.author.name}', colour = member.color)
        await member.kick(reason = reason)
        emb.add_field(name = 'Был кикнут', value = member.mention)
        emb.add_field(name = 'По причине', value = reason)
        emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
        await ctx.send(embed = emb)
    else:
        emb = discord.Embed(description = f'Извините, {ctx.author.mention}, но вы не можете кикнуть моего создателя!', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
        await ctx.send(embed = emb)
#ban
@client.command(aliases = ['Ban', 'BAN'])
@commands.cooldown(1, 10, commands.BucketType.default)
@commands.has_permissions(ban_members = True)
async def ban(ctx , member: discord.Member, *, reason: str):
    await ctx.channel.purge(limit = 1)
    if member.id != client.owner_id:
        emb = discord.Embed(title = f'Бан от {ctx.author.name}', colour = member.color)
        await member.ban(reason = reason)
        emb.add_field(name = 'Был забанен', value = member.mention)
        emb.add_field(name = 'По причине', value = reason)
        emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
        await ctx.send(embed = emb)
    else:
        emb = discord.Embed(description = f'Извините, {ctx.author.mention}, но вы не можете забанить моего создателя!', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
        await ctx.send(embed = emb)
        
#message delete
@client.command(aliases = ['Clear', 'CLEAR'])
@commands.cooldown(1, 10, commands.BucketType.default)
@commands.has_permissions(administrator = True)
async def clear(ctx, amount : int):
    await ctx.channel.purge(limit = amount + 1)
    if amount == 1:
        emb = discord.Embed(description = f'удалено {amount} сообщение', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
        await ctx.send(embed = emb, delete_after = 1)
    elif amount == 2:
        emb = discord.Embed(description = f'удалено {amount} сообщения', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
        await ctx.send(embed = emb, delete_after = 1)
    elif amount == 3:
        emb = discord.Embed(description = f'удалено {amount} сообщения', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
        await ctx.send(embed = emb, delete_after = 1)
    elif amount == 4:
        emb = discord.Embed(description = f'удалено {amount} сообщения', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
        await ctx.send(embed = emb, delete_after = 1)
    else:
        emb = discord.Embed(description = f'удалено {amount} сообщений', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
        await ctx.send(embed = emb, delete_after = 1)
    
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        emb = discord.Embed(description = f'{ctx.author.mention}, я не знаю такую команду!', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
        await ctx.send(embed = emb)
        
    if isinstance(error, commands.CommandOnCooldown):
        emb = discord.Embed(description = f'{ctx.author.mention}, команда в кд, потерпи чутка!', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
        await ctx.send(embed = emb)
    
@pm.error
async def pm_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        emb = discord.Embed(description = f'{ctx.author.mention}, укажите, кому и что написать!', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
        await ctx.send(embed = emb)

    if isinstance(error, commands.MissingPermissions):
        emb = discord.Embed(description = f'{ctx.author.mention} пытался вызвать команду pm', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
        await ctx.send(embed = emb)
        
@everyone_embed.error
async def everyone_embed_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        emb = discord.Embed(description = f'{ctx.author.mention}, так шутить не нужно', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
        await ctx.send(embed = emb)

    if isinstance(error, commands.MissingPermissions):
        emb = discord.Embed(description = f'{ctx.author.mention} пытался вызвать команду everyone_embed', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
        await ctx.send(embed = emb)
        
    if isinstance(error, commands.TooManyArguments):
        emb = discord.Embed(description = f'{ctx.author.mention}, возможно, вы забыли кавычки?', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
        await ctx.send(embed = emb)
        
@embed.error
async def embed_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        emb = discord.Embed(description = f'{ctx.author.mention}, укажите, что закрепить!', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
        await ctx.send(embed = emb)

    if isinstance(error, commands.MissingPermissions):
        emb = discord.Embed(description = f'{ctx.author.mention} пытался вызвать команду embed', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
        await ctx.send(embed = emb)
        
    if isinstance(error, commands.TooManyArguments):
        emb = discord.Embed(description = f'{ctx.author.mention}, возможно, вы забыли кавычки?', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
        await ctx.send(embed = emb)
        
@everyone.error
async def everyone_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        emb = discord.Embed(description = f'{ctx.author.mention}, так шутить не нужно', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
        await ctx.send(embed = emb)

    if isinstance(error, commands.MissingPermissions):
        emb = discord.Embed(description = f'{ctx.author.mention} пытался пингануть everyone', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
        await ctx.send(embed = emb)

@say.error
async def say_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        emb = discord.Embed(description = f'{ctx.author.mention}, укажите, что я должен сказать!', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
        await ctx.send(embed = emb)
            
    if isinstance(error, commands.MissingPermissions):
        emb = discord.Embed(description = f'{ctx.author.mention} пытался вызвать команду say', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
        await ctx.send(embed = emb)
        
@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        emb = discord.Embed(description = f'{ctx.author.mention}, укажите, кого и на сколько мутить!', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
        await ctx.send(embed = emb)
        
    if isinstance(error, commands.BadArgument):
        emb = discord.Embed(description = f'{ctx.author.mention}, проверьте правильность написания команды!', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
        await ctx.send(embed = emb)
                       
    if isinstance(error, commands.MissingPermissions):
        emb = discord.Embed(description = f'{ctx.author.mention} пытался вызвать команду mute', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
        await ctx.send(embed = emb)

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        emb = discord.Embed(description = f'{ctx.author.mention}, укажите, кого нужно кикнуть!', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
        await ctx.send(embed = emb)

    if isinstance(error, commands.MissingPermissions):
        emb = discord.Embed(description = f'{ctx.author.mention} пытался вызвать команду kick', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
        await ctx.send(embed = emb)

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        emb = discord.Embed(description = f'{ctx.author.mention}, укажите, кого нужно забанить!', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
        await ctx.send(embed = emb)

    if isinstance(error, commands.MissingPermissions):
        emb = discord.Embed(description = f'{ctx.author.mention} пытался вызвать команду ban', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
        await ctx.send(embed = emb)

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        emb = discord.Embed(description = f'{ctx.author.mention}, укажите, сколько сообщений нужно удалить!', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
        await ctx.send(embed = emb)

    if isinstance(error, commands.MissingPermissions):
        emb = discord.Embed(description = f'{ctx.author.mention} пытался вызвать команду clear', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
        await ctx.send(embed = emb)
        
    if isinstance(error, commands.BadArgument):
        emb = discord.Embed(description = f'{ctx.author.mention}, проверьте правильность написания команды!', colour = discord.Color.orange())
        emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
        await ctx.send(embed = emb)
    
t = os.environ.get('t')

client.run(t)
