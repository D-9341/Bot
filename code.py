import datetime
import json
import os
import discord
from discord.ext import commands
from discord.utils import get

client = commands.Bot(command_prefix = "cephalon/")
#like cephalon/support

#проверка подключения
@client.command()
async def test(ctx, amount = 1):
    await ctx.channel.purge(limit = amount)
    await ctx.send(f'Bot online!')

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
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
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
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            if member is not None:
                await member.remove_roles(role)

#альтернатива Groovy
@client.command()
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild = ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        await ctx.send(f'successfully connected to {channel}')

@client.command()
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild = ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
    else:
        voice = await channel.connect()
        await ctx.send(f'disconnected from {channel}')


@client.command(pass_context = True)
async def general(ctx, amount = 1):
    await ctx.channel.purge(limit = amount)
    emb = discord.Embed(title ='Здраствуйте!')

    emb.add_field(name ='/', value = 'Сервер SPELL - это сервер где происходит общение. Также, на сервере есть уникальный бот, написанный одним из создателей сервера. От лица всего админ состава надеюсь, что мы произведём хорошое впечатление на вас!')

    await ctx.send(embed = emb)

@client.command(pass_context = True)
async def send_nudes(ctx, amount = 1):
    await ctx.channel.purge(limit = amount)
    emb = discord.Embed(title = 'Внимание!')

    emb.add_field(name = '/'.format('/'), value = f'тебе пытались послать нудесы, однако я лох, и я не могу их отправить')
    
    await ctx.author.send(embed = emb)

#я не знаю что это
@client.event
async def on_command_error(ctx, error):
    pass

#personal messages
@client.command()
async def pm(ctx, member: discord.Member, amount = 1):
    await ctx.channel.purge(limit = amount)
    
    await member.send(f'адамант лох')
    
#member joined the server
@client.event
async def on_member_join(member):
    channel = client.get_channel(693929823030214658)

    role = discord.utils.get(member.guild.roles, id = 693933516294979704)
    role1 = discord.utils.get(member.guild.roles, id = 693933510523879454)
    role2 = discord.utils.get(member.guild.roles, id = 693933513459892245)

    await member.add_roles(role, role1, role2)
    await channel.send(embed = discord.Embed(description = f'{member.name} has entered the facility', colour = discord.Color.orange()))

#help command
@client.command(pass_context = True)
@commands.has_permissions(administrator = True)

async def support(ctx, amount = 1):
    await ctx.channel.purge(limit = amount)
    emb = discord.Embed(title = "Команды")

    emb.add_field(name = 'Инфо'.format('/'), value = "Cy, или же сай - бот, написанный сасиска") 
    emb.add_field(name = "{}clear".format("cephalon/"), value = "очистка чата, доступна только администраторам")
    emb.add_field(name = "{}ban".format("cephalon/"), value = "бан игрока, доступна только администраторам" )
    emb.add_field(name = "{}kick".format("cephalon/"), value = "кик игрока, доступна только администраторам")
    emb.add_field(name = "{}hello".format("cephalon/"), value = "бот приветствует написавшего сообщение")
    emb.add_field(name = "{}time".format("cephalon/"), value = "показывает время")
    emb.add_field(name = '{}say'.format('cephalon/'), value = 'пишет сообщение от лица бота, пишите в двойных ковычках')
    emb.add_field(name = '{}ping'.format('cephalon/'), value = 'pong!')
    await ctx.send(embed = emb)

@client.command(pass_context = True)
@commands.has_permissions(administrator = True)

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
@client.command(pass_context = True)
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
@client.command(pass_context = True)
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
@client.command(pass_context = True)
@commands.has_permissions(administrator = True)
async def clear(ctx, amount : int):
    await ctx.channel.purge(limit = amount)


#command delete
@client.command(pass_context = True)
async def hello(ctx, amount = 1):
    await ctx.channel.purge(limit = amount)

    author = ctx.message.author
    await ctx.send(f"Приветствую, {author.mention}")

@client.command(pass_context = True)

async def say(ctx, arg, amount = 1):
    await ctx.channel.purge(limit = amount)

    await ctx.send(arg)

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.name}, нет аргумента!')

@client.command()
async def ping(ctx, amount = 1):
    await ctx.channel.purge(limit = amount)
    await ctx.send(f'Pong! {round(client.latency * 1000)} ms')

token = os.environ.get('BOT_TOKEN')

client.run(token)

#потом, когда приеду к нормальному компу, буду фиксить все баги и дорабатывать сая
