import random
import youtube_dl
import datetime
import json
import os
import discord
from discord.ext import commands
from discord.utils import get

client = commands.Bot(command_prefix = "cephalon/")
#like cephalon/support

@client.event
async def on_message(message):
    with open('users.json', 'r') as f:
            users = json.load(f)
 
 
    await update_data(users, message.author)
    await add_experience(users, message.author, 5)
    await level_up(users, message.author, message)
   
   
    with open('users.json', 'w') as f:
        json.dump(users, f)

async def update_data(users, user):
    if not f'{user.id}' in users:
        users[f'{user.id}'] = {}
        users[f'{user.id}']['experience'] = 0
        users[f'{user.id}']['level'] = 1
 

async def add_experience(users, user, exp):
    users[f'{user.id}']['experience'] += exp
    
    

async def level_up(users, user, message):
    experience = users[f'{user.id}']['experience']
    lvl_start = users[f'{user.id}']['level']
    lvl_end = int(experience ** (1/4))
    if lvl_start < lvl_end:
        await message.channel.send(f'{user.mention} достигнул {lvl_end} уровня!')
        users[f'{user.id}']['level'] = lvl_end            
            
#проверка подключения
@client.command()
async def test(ctx, amount = 1):
    await ctx.channel.purge(limit = amount)
    await ctx.send(f'Cephalon online!')

#получение роли по эмодзи
@client.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    if message_id == 697162136761139331:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)

        if payload.emoji.name == 'strashilka':
            role = discord.utils.get(guild.roles, name = 'Discord(А)')
        elif payload.emoji.name == 'durka':
            role = discord.utils.get(guild.roles, name = 'YouTube(А)')

        if role is not None:
            member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
            if member is not None:
                await member.add_roles(role)

async def on_raw_reaction_remove(payload):
    message_id = payload.message_id
    if message_id == 697162136761139331:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)

        if payload.emoji.name == 'strashilka':
            role = discord.utils.get(guild.roles, name = 'Discord(А)')
        elif payload.emoji.name == 'durka':
            role = discord.utils.get(guild.roles, name = 'YouTube(А)')

        if role is not None:
            member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
            if member is not None:
                await member.remove_roles(role)

#альтернатива Groovy(которая сука не работает)
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

client.command()
async def play(ctx, url : str):
    song_there = os.path.isfile('song.mp3')

    try:
        if song_there:
            os.remove('song.mp3')
            print('[log] ДАННЫЕ УДАЛЕНЫ')

    except PermissionError:
        print('[log] не удалось удалить данные')

    await ctx.send('Ща скачаю, падажжи')

    voice = get(client.voice_clients, guild = ctx.guild)
    ydl_opts = {
        'format' : 'bestaudio/best',
        'postprocessors' : [{
            'key' : 'FFmpegExtractAudio',
            'preferredcodec' : 'mp3',
            'preferredquality' : '192'
            }]
    }


    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print('[log] Загрузка...')
        ydl.download([url])

    for file in os.listdir('./'):
        if file.endswith('.mp3'):
            name = file
            print('[log] Переименовываю: {file}')
            os.rename(file, 'song.mp3')

    voice.play(discord.FFmpegPCMAudio('song.mp3'), after = lambda e: print(f'[log] {name}, время на прослушивание музыки кончилось'))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    song_name = name.rsplit('-', 2)
    await ctx.send(f'Сейчас играет: {song_name[0]}')

#я не знаю что это
@client.event
async def on_command_error(ctx, error):
    pass

#personal messages
@client.command()
async def pm(ctx, member: discord.Member, amount = 1):
    await ctx.channel.purge(limit = amount)
    await member.send(f'Адамант лох')

#member joined the server
@client.event
async def on_member_join(member):
    with open('users.json', 'r') as f:
        users = json.load(f)
 
 
    await update_data(users, member)
 
   
    with open('users.json', 'w') as f:
        json.dump(users, f)
    
    
    channel = client.get_channel(693929823030214658)

    role = discord.utils.get(member.guild.roles, id = 693933516294979704)
    role1 = discord.utils.get(member.guild.roles, id = 693933510523879454)
    role2 = discord.utils.get(member.guild.roles, id = 693933513459892245)

    await member.add_roles(role, role1, role2)
    await channel.send(embed = discord.Embed(description = f'{member.name} has entered the facility', colour = discord.Color.orange()))

#help command
@client.command()
@commands.has_permissions(administrator = True)
async def support(ctx, amount = 1):
    await ctx.channel.purge(limit = amount)
    emb = discord.Embed(title = "Команды", colour = discord.Color.orange())

    emb.add_field(name = 'Инфо'.format('/'), value = "Cy, или же сай - бот, написанный сасиска")
    emb.add_field(name = "{}clear".format("cephalon/"), value = "очистка чата, доступна только администраторам")
    emb.add_field(name = "{}ban".format("cephalon/"), value = "бан игрока, доступна только администраторам" )
    emb.add_field(name = "{}kick".format("cephalon/"), value = "кик игрока, доступна только администраторам")
    emb.add_field(name = "{}hello".format("cephalon/"), value = "бот приветствует написавшего сообщение")
    emb.add_field(name = "{}time".format("cephalon/"), value = "показывает время")
    emb.add_field(name = '{}say'.format('cephalon/'), value = 'пишет сообщение от лица бота')
    emb.add_field(name = '{}ping'.format('cephalon/'), value = 'pong!')
    await ctx.send(embed = emb)

@client.command()
async def time(ctx, amount = 1):
    await ctx.channel.purge(limit = amount)

    emb = discord.Embed(title = 'Time', description = 'Точное время' , colour = discord.Color.orange(), url = 'https://www.timeserver.ru')

    emb.set_author(name = client.user.name, icon_url = client.user.avatar_url)
    emb.set_footer(text = ctx.author.name, icon_url = ctx.author.avatar_url)

    now_date = datetime.datetime.now()
    emb.add_field(name = 'Time', value = 'Time : {}'.format(now_date))

    await ctx.author.send(embed = emb)

#проверка на подключение
@client.event
async def on_ready():
    await client.change_presence(status = discord.Status.online, activity = discord.Game('cephalon/support'))

#kick
@client.command()
@commands.has_permissions(administrator = True)
async def kick(ctx , member: discord.Member, *, reason = None):
    emb = discord.Embed(title = 'Kick', colour = discord.Color.green())
    await ctx.channel.purge(limit = 1)

    await member.kick(reason = reason)

    emb.set_author(name = member.name, icon_url = member.avatar_url)
    emb.add_field(name = '-', value =  'Kicked user : {}'.format(member.mention))
    emb.set_footer(text = 'Был кикнут администратором {}'.format(ctx.author.name), icon_url = ctx.author.avatar_url)

    await ctx.send(embed = emb)

#ban
@client.command()
@commands.has_permissions(administrator = True)
async def ban(ctx , member: discord.Member, *, reason = None):
    emb = discord.Embed(title = 'Ban', colour = discord.Color.red())
    await ctx.channel.purge(limit = 1)

    await member.ban(reason = reason)

    emb.set_author(name = member.name, icon_url = member.avatar_url)
    emb.add_field(name = '-', value =  'Banned user : {}'.format(member.mention))
    emb.set_footer(text = 'Был забанен администратором {}'.format(ctx.author.name), icon_url = ctx.author.avatar_url)

    await ctx.send(embed = emb)

#message delete
@client.command()
@commands.has_permissions(administrator = True)
async def clear(ctx, amount : int):
    await ctx.channel.purge(limit = amount)

#hello
@client.command(pass_context = True)
async def hello(ctx, amount = 1):
    await ctx.channel.purge(limit = amount)
    author = ctx.message.author
    await ctx.send(f'👋')

#say
@client.command()
async def say(ctx, *, arg, amount = 1):
    await ctx.channel.purge(limit = amount)
    await ctx.send(arg)

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.name}, нет аргумента!')

#pong!
@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! `{round(client.latency * 1000)} ms`')
token = os.environ.get('BOT_TOKEN')

client.run(token)
