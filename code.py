import asyncio
import random
import datetime
import os
import discord
from discord.ext import commands
from discord.utils import get

client = commands.Bot(command_prefix = commands.when_mentioned_or('cephalon/'))
client.remove_command('help')

#test commands space

#test commands space

@client.command()
async def info(ctx, amount = 1):
    await ctx.channel.purge(limit = amount)
    await ctx.send(f'Cy в сети, пинг равен `{round(client.latency * 1000)} ms`')
    
@client.command()
@commands.has_permissions(manage_roles = True)
async def about(ctx, member:discord.Member, amount = 1):
    await ctx.channel.purge(limit = amount)
    if member.name == 'Cy':
        emb = discord.Embed(title = f'Информация обо мне? Вот:', colour = discord.Color.red())
        emb.add_field(name = 'ID', value = member.id)
        emb.add_field(name = 'Created', value = member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline = False)
        emb.add_field(name = 'Joined', value = member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline = False)
        emb.add_field(name = 'Mention', value = member.mention, inline = False)
        emb.add_field(name = 'Nickname', value = member.nick, inline = False)
        emb.add_field(name = 'Status', value = member.status, inline = False)
        emb.set_thumbnail(url = member.avatar_url)
        emb.set_footer(text = 'Зачем вам эта информация?')
        await ctx.send(embed = emb)
    else:
        emb = discord.Embed(title = f'Информация о {member.name}', colour = member.color)
        emb.add_field(name = 'ID', value = member.id)
        emb.add_field(name = 'Created', value = member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline = False)
        emb.add_field(name = 'Joined', value = member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline = False)
        emb.add_field(name = 'Mention', value = member.mention, inline = False)
        emb.add_field(name = 'Nickname', value = member.nick, inline = False)
        emb.add_field(name = 'Status', value = member.status, inline = False)
        emb.set_thumbnail(url = member.avatar_url)
        emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
        await ctx.send(embed = emb)
    
@client.event
async def on_voice_state_update(member, before, after):
    if after.channel.id == 694212304165929101:
        maincategory = discord.utils.get(guild.categories, id = 693937532550774824)
        userchannel = await guild.create_voice_channel(name = f'{member.name}', category = None)
        await userchannel.set_permissions(member, manage_channels = True)
        await member.move_to(userchannel)
        def check(a,b,c):
            return len(userchannel.members) == 0
        await client.wait_for('voice_state_update', check = check)
        await userchannel.delete()
    
@client.command()
@commands.has_permissions(mute_members = True)
async def mute(ctx, member: discord.Member, amount = 1):
    await ctx.channel.purge(limit = amount)
    emb = discord.Embed(title = f'Мут от {ctx.author.name}', colour = discord.Color.red())
    role = discord.utils.get(ctx.message.guild.roles, name = 'Muted')
    await member.add_roles(role)
    emb.add_field(name = 'В муте', value = '{}'.format(member.mention))
    emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
    await ctx.send(embed = emb)

@client.command()
@commands.has_permissions(mention_everyone = True)
async def gaystvo_embed(ctx, *, arg, amount = 1):
    await ctx.channel.purge(limit = amount)
    await ctx.send('@everyone')
    await asyncio.sleep(0,1)
    emb = discord.Embed(title = None, colour = ctx.author.color)
    emb.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
    emb.add_field(name = 'Cephalon', value = arg)
    emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
    await ctx.send(embed = emb)
    
@client.command()
@commands.has_permissions(manage_messages = True)
async def embed(ctx, *, arg, amount = 1):
    await ctx.channel.purge(limit = amount)
    emb = discord.Embed(title = None, colour = ctx.author.color)
    emb.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
    emb.add_field(name = 'Cephalon', value = arg)
    emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
    await ctx.send(embed = emb)

@client.command()
@commands.has_permissions(mention_everyone = True)
async def gaystvo(ctx, *, arg, amount = 1):
    await ctx.channel.purge(limit = amount)
    await ctx.send('@everyone ' + arg)
    
@client.command()
@commands.has_permissions(manage_messages = True)
async def say(ctx, *, arg, amount = 1):
    await ctx.channel.purge(limit = amount)
    await ctx.send(arg)
    
@client.command()
async def coinflip(ctx, amount = 1):
    await ctx.channel.purge(limit = amount)
    choices = ['Орёл!', 'Решка!']
    rancoin = random.choice(choices)
    await ctx.send(rancoin)

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
@client.command()
async def join(ctx):
    if ctx.author.voice and ctx.author.voice.channel:
        channel = ctx.author.voice.channel
    else:
        await ctx.send("Ты должен быть в канале, чтобы использовать это.")
        return
    global vc
    try:
        vc = await channel.connect()
    except:
        TimeoutError

@client.command()
async def leave(ctx):
    try:
        if vc.is_connected():
            await vc.disconnect()
    except:
        pass

@client.command()
@commands.has_permissions(administrator = True)
async def pm(ctx, member: discord.Member, amount = 1):
    await ctx.channel.purge(limit = amount)
    await member.send(f'Адамант сука')

@client.event
async def on_member_join(member):
    channel = client.get_channel(693929823030214658)

    role = discord.utils.get(member.guild.roles, id = 693933516294979704)
    role1 = discord.utils.get(member.guild.roles, id = 693933510523879454)
    role2 = discord.utils.get(member.guild.roles, id = 693933514198089838)

    await member.add_roles(role, role1, role2)
    await channel.send(embed = discord.Embed(description = f'{member.name} Зашёл в комплекс, 👋', colour = discord.Color.orange()))

@client.event
async def on_member_remove(member):
    channel = client.get_channel(693929823030214658)
    await channel.send(embed = discord.Embed(description = f'{member.name} Вышел из комплекса...', colour = discord.Color.red()))
    
#help command
@client.command()
@commands.has_permissions(manage_messages = True)
async def help(ctx, amount = 1):
    await ctx.channel.purge(limit = amount)
    emb = discord.Embed(title = "Меню команд для администраторов", colour = discord.Color.orange())
    emb.add_field(name = 'Инфо', value = "Cy, или же сай - бот, написанный сасиска")
    emb.add_field(name = '{}info'.format('cephalon/'), value = 'команда для определения, в сети ли бот')
    emb.add_field(name = "{}clear".format("cephalon/"), value = "очистка чата")
    emb.add_field(name = "{}ban".format("cephalon/"), value = "бан игрока")
    emb.add_field(name = "{}kick".format("cephalon/"), value = "кик игрока")
    emb.add_field(name = '{}mute'.format('cephalon/'), value = 'мут игрока')
    emb.add_field(name = '{}say'.format('cephalon/'), value = 'пишет сообщение от лица бота. Всё.')
    emb.add_field(name = '{}gaystvo'.format('cephalon/'), value = 'пишет от лица бота и пингует @everyone')
    emb.add_field(name = '{}embed'.format('cephalon/'), value = 'от лица бота отправляется эмбед')
    emb.add_field(name = '{}gaystvo_embed'.format('cephalon/'), value = 'Совмещает в себе команды gaystvo и embed')
    emb.add_field(name = '{}pm'.format('cephalon/'), value = 'пишет выбраному участнику **Адамант сука**')
    emb.add_field(name = '{}about'.format('cephalon/'), value = 'показывает инфу о человеке. В отличии от Ayana пишет только необходимую инфу')
    emb.add_field(name = '{}join'.format('cephalon/'), value = 'приказывает зайти боту в голосовой канал')
    emb.add_field(name = '{}leave'.format('cephalon/'), value = 'приказывает боту выйти из голосового канала')
    emb.add_field(name = 'жыж', value = 'также, для написания команд необязательно писать префикс, можно пингануть ~~@everyone~~ бота')
    emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
    await ctx.send(embed = emb)

@client.command()
async def time(ctx, amount = 1):
    await ctx.channel.purge(limit = amount)
    emb = discord.Embed(title = None, colour = discord.Color.orange())
    emb.set_footer(text = 'Cephalon Cy от сасиска#2472')
    now_date = datetime.datetime.now()
    emb.add_field(name = 'Время по Гринвичу равняется ', value = '{}'.format(now_date))
    await ctx.author.send(embed = emb)

#проверка на подключение
@client.event
async def on_ready():
    await client.change_presence(status = discord.Status.idle, activity = discord.Game('Discord API'))

#kick
@client.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx , member: discord.Member, *, reason = None):
    await ctx.channel.purge(limit = 1)
    emb = discord.Embed(title = f'Кик от {ctx.author.name}', colour = discord.Color.orange())
    await member.kick(reason = reason)
    emb.add_field(name = 'Кикнут', value = '{}'.format(member.mention))
    emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
    await ctx.send(embed = emb)

#ban
@client.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx , member: discord.Member, *, reason = None):
    await ctx.channel.purge(limit = 1)
    emb = discord.Embed(title = f'Бан от {ctx.author.name}', colour = discord.Color.red())
    await member.ban(reason = reason)
    emb.add_field(name = 'Забанен', value = '{}'.format(member.mention))
    emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
    await ctx.send(embed = emb)

#message delete
@client.command()
@commands.has_permissions(manage_messages = True)
async def clear(ctx, amount : int):
    await ctx.channel.purge(limit = amount + 1)
    if amount == 1:
        await ctx.send(f'удалено {amount} сообщение')
    elif amount == 2:
        await ctx.send(f'удалено {amount} сообщения')
    elif amount == 3:
        await ctx.send(f'удалено {amount} сообщения')
    elif amount == 4:
        await ctx.send(f'удалено {amount} сообщения')
    else:
        await ctx.send(f'удалено {amount} сообщений')
    await asyncio.sleep(1)
    await ctx.channel.purge(limit = 1)
    
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f'{ctx.author.mention}, чё это за команда?')
    
@about.error
async def about_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.mention}, о ком инфа то?')

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.author.mention} пытался вызвать комманду about. Хаха')
    
@pm.error
async def pm_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.mention}, кому написать то?')

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.author.mention} пытался вызвать комманду Pm. Хаха')
        
@gaystvo_embed.error
async def gaystvo_embed_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.mention}, чё сказать то?')

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.author.mention} пытался вызвать комманду gaystvo_embed. Хаха')
        
@embed.error
async def embed_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.mention}, чё сказать то?')

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.author.mention} пытался вызвать комманду Embed. Хаха')

@gaystvo.error
async def gaystvo_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.mention}, ты так не шути')

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.author.mention} пытался пингануть \@everyone. Ой')

@say.error
async def say_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.mention}, чё сказать то?')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.author.mention} пытался вызвать комманду Say. Хаха')
        
@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.mention}, кого мутить то?')

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.author.mention} пытался вызвать комманду Mute. Хаха')

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.mention}, кого кикать то?')

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{cctx.author.mention} пытался вызвать комманду Kick. Хаха')

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.mention}, кого банить то?')

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.author.mention} пытался вызвать комманду Ban. Хаха')

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.mention}, нет аргумента!')

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.author.mention} пытался вызвать комманду Clear. Хаха')
    
t = os.environ.get('t')

client.run(t)
