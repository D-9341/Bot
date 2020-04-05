import datetime
import json
import os
import discord
from discord.ext import commands
from discord.utils import get

client = commands.Bot(command_prefix = "cephalon/")
#like cephalon/support

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
    
    await member.send(f'почему я не могу писать своё сообщение?!')
    
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
    role1 = discord.utils.get(member.guild.roles, id = 693933511412940800)

    await member.add_roles(role, role1)
    await channel.send(embed = discord.Embed(description = f'{member.name} has entered the facility'))

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
    print("successfully connected")

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
async def ping(ctx):
    await ctx.send(f'pong!')

token = os.environ.get('BOT_TOKEN')

client.run(token)
