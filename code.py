import asyncio
import random
import youtube_dl
import datetime
import json
import os
import discord
from discord.ext import commands
from discord.utils import get

client = commands.Bot(command_prefix = commands.when_mentioned_or("cephalon/"))
client.remove_command('help')
#like cephalon/help

@client.command()
@commands.has_permissions(administrator = True)
async def mute(ctx, member: discord.Member, amount = 1):
    await ctx.channel.purge(limit = amount)
    emb = discord.Embed(title = 'Mute', colour = discord.Color.red())
    role = discord.utils.get(ctx.message.guild.roles, name = 'Muted')
    await member.add_roles(role)
    emb.add_field(name = 'Muted ', value = '{}'.format(member.mention))
    emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
    await ctx.send(embed = emb)

@client.command()
@commands.has_permissions(administrator = True)
async def embed(ctx, *, arg, amount = 1):
    await ctx.channel.purge(limit = amount)
    emb = discord.Embed(title = ctx.author.name, colour = discord.Color.orange())
    emb.add_field(name = 'SPELL', value = arg)
    emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
    await ctx.send(embed = emb)

@client.command()
@commands.has_permissions(administrator = True)
async def info(ctx, amount = 1):
    await ctx.channel.purge(limit = amount)
    await ctx.send(f'Cephalon online, Ping equals `{round(client.latency * 1000)} ms`')

@client.command()
@commands.has_permissions(administrator = True)
async def gaystvo(ctx, *, arg, amount = 1):
    await ctx.channel.purge(limit = amount)
    await ctx.send('@everyone ' + arg)
    
@client.event
async def on_message(message):
    if 'discord.gg' in message.content.lower():
        await message.delete()
        await message.channel.send('пашол нахуй со своей рекламой')
    await client.process_commands(message)   
 
@client.command()
async def coinflip(ctx, amount = 1):
    await ctx.channel.purge(limit = amount)
    choices = ['Орёл', 'Решка']
    rancoin = random.choice(choices)
    await ctx.send(rancoin)

#получение роли по эмодзи
@client.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    if message_id == 707985429944860773:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)

        if payload.emoji.name == 'Discordy':
            role = discord.utils.get(guild.roles, name = 'Discord')
        

        if role is not None:
            member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
            if member is not None:
                await member.add_roles(role)

@client.event
async def on_raw_reaction_remove(payload):
    message_id = payload.message_id
    if message_id == 707985429944860773:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)

        if payload.emoji.name == 'Discordy':
            role = discord.utils.get(guild.roles, name = 'Discord')

        if role is not None:
            member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
            if member is not None:
                await member.remove_roles(role)

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
    
#альтернатива Groovy(которая, сука не работает)
@client.command()
async def join(ctx):
    if ctx.author.voice and ctx.author.voice.channel:
        channel = ctx.author.voice.channel
    else:
        await ctx.send("Ты в канал то зайди")
        return
    global vc
    try:
        vc=await channel.connect()
    except:
        TimeoutError

@client.command()
async def leave(ctx):
    try:
        if vc.is_connected():
            await vc.disconnect()
    except:
        TimeoutError
        pass

#я не знаю что это
@client.event
async def on_command_error(ctx, error):
    pass

#personal messages
@client.command()
@commands.has_permissions(administrator = True)
async def pm(ctx, arg, *, member: discord.Member, amount = 1):
    await ctx.channel.purge(limit = amount)
    await member.send(arg)

#member joined the server
@client.event
async def on_member_join(member):
    channel = client.get_channel(693929823030214658)

    role = discord.utils.get(member.guild.roles, id = 693933516294979704)
    role1 = discord.utils.get(member.guild.roles, id = 693933510523879454)
    role2 = discord.utils.get(member.guild.roles, id = 693933514198089838)

    await member.add_roles(role, role1, role2)
    await channel.send(embed = discord.Embed(description = f'{member.name} has entered the facility, 👋', colour = discord.Color.orange()))

@client.event
async def on_member_remove(member):
    channel = client.get_channel(693929823030214658)
    await channel.send(embed = discord.Embed(description = f'{member.name} has exited the facility...', colour = discord.Color.red()))
    
#help command
@client.command()
@commands.has_permissions(administrator = True)
async def help(ctx, amount = 1):
    await ctx.channel.purge(limit = amount)
    emb = discord.Embed(title = "Меню команд для администраторов", colour = discord.Color.orange())

    emb.add_field(name = 'Инфо'.format('/'), value = "Cy, или же сай - бот, написанный сасиска")
    emb.add_field(name = "{}clear".format("cephalon/"), value = "очистка чата")
    emb.add_field(name = "{}ban".format("cephalon/"), value = "бан игрока")
    emb.add_field(name = "{}kick".format("cephalon/"), value = "кик игрока")
    emb.add_field(name = '{}mute'.format('cephalon/'), value = 'мут игрока')
    emb.add_field(name = "{}time".format("cephalon/"), value = "показывает время по гринвичу")
    emb.add_field(name = '{}say'.format('cephalon/'), value = 'пишет сообщение от лица бота')
    emb.add_field(name = '{}gaystvo'.format('cephalon/'), value = 'как cephalon/say, но пингует @everyone')
    emb.add_field(name = '{}embed'.format('cephalon/'), value = 'как cephalon/say, но пишет через эмбед')
    emb.add_field(name = 'жыж', value = 'также, для написания команд необязательно писать префикс, можно пингануть бота')
    emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
    await ctx.send(embed = emb)

@client.command()
async def time(ctx, amount = 1):
    await ctx.channel.purge(limit = amount)

    emb = discord.Embed(title = 'Time', colour = discord.Color.orange(), url = 'https://www.timeserver.ru')

    emb.set_author(name = client.user.name, icon_url = client.user.avatar_url)
    emb.set_footer(text = 'Cephalon Cy by сасиска#2472')

    now_date = datetime.datetime.now()
    emb.add_field(name = 'GMT 0 Time is ', value = '{}'.format(now_date))

    await ctx.author.send(embed = emb)

#проверка на подключение
@client.event
async def on_ready():
    await client.change_presence(status = discord.Status.online, activity = discord.Game('cephalon/help'))

#kick
@client.command()
@commands.has_permissions(administrator = True)
async def kick(ctx , member: discord.Member, *, reason = None):
    await ctx.channel.purge(limit = 1)
    emb = discord.Embed(title = 'Kick', colour = discord.Color.orange())

    await member.kick(reason = reason)

    emb.add_field(name = 'Kicked ', value = '{}'.format(member.mention))
    emb.set_footer(text = 'Cephalon Cy by сасиска#2472')

    await ctx.send(embed = emb)

#ban
@client.command()
@commands.has_permissions(administrator = True)
async def ban(ctx , member: discord.Member, *, reason = None):
    await ctx.channel.purge(limit = 1)
    emb = discord.Embed(title = 'Ban', colour = discord.Color.red())

    await member.ban(reason = reason)

    emb.add_field(name = 'Banned ', value = '{}'.format(member.mention))
    emb.set_footer(text = 'Cephalon Cy by сасиска#2472')

    await ctx.send(embed = emb)

#message delete
@client.command()
@commands.has_permissions(administrator = True)
async def clear(ctx, amount : int):
    await ctx.channel.purge(limit = amount)

#say
@client.command()
@commands.has_permissions(administrator = True)
async def say(ctx, *, arg, amount = 1):
    await ctx.channel.purge(limit = amount)
    await ctx.send(arg)

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.name}, нет аргумента!')
    
token = os.environ.get('BOT_TOKEN')

client.run(token)
