import asyncio
import random
import datetime
import os
import discord
from discord.ext import commands
from discord.utils import get

client = commands.Bot(command_prefix = commands.when_mentioned_or('cephalon/'))
client.remove_command('help')
#like cephalon/help

#test commands space

#test commands space

@client.command()
@commands.has_permissions(administrator = True)
async def info(ctx, amount = 1):
    await ctx.channel.purge(limit = amount)
    await ctx.send(f'Cy в сети, пинг равен `{round(client.latency * 1000)} ms`')

@client.command()
@commands.has_permissions(administrator = True)
async def zatka(ctx, amount = 1):
    await ctx.channel.purge(limit = amount)
    await ctx.send('Форма заявки для Набор кадров (1). ZATKA в STEAM.  ZATKA_KING8406 в Discord. возраст 14 часовой пояс IL 0. (2). Интересующая игра: Discord (3). Опыт администрирования: Есть.  творческие:  Есть.технические навыки: нет. (4). Сколько часов готовы уделять работе [15 в неделю] в какое время дня свободны 16 00 до 22 00')
                   
@client.command()
async def about(ctx, member:discord.Member, amount = 1):
    await ctx.channel.purge(limit = amount)
    emb = discord.Embed(title = f'Информация о {member.name}', colour = discord.Color.orange())
    emb.add_field(name = 'ID', value = member.id)
    emb.add_field(name = 'Created', value = member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline = False)
    emb.add_field(name = 'Joined', value = member.joined_at, inline = False)
    emb.add_field(name = 'Roles', value = member.roles, inline = False)
    emb.set_thumbnail(url = member.avatar_url)
    emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
    await ctx.send(embed = emb)
    
@client.event
async def on_voice_state_update(member, before, after):
    if after.channel.id == 694212304165929101:
        maincategory = discord.utils.get(guild.categories, id = 693937532550774824)
        userchannel = await guild.create_voice_channel(name = f'{member.name}', category = maincategory)
        await userchannel.set_permissions(member, manage_channels = True)
        await member.move_to(userchannel)
        def check(a,b,c):
            return len(userchannel.members) == 0
        await client.wait_for('voice_state_update', check = check)
        await userchannel.delete()
    
@client.command()
@commands.has_permissions(administrator = True)
async def mute(ctx, member: discord.Member, amount = 1):
    await ctx.channel.purge(limit = amount)
    emb = discord.Embed(title = f'Мут от {ctx.author.name}', colour = discord.Color.red())
    role = discord.utils.get(ctx.message.guild.roles, name = 'Muted')
    await member.add_roles(role)
    emb.add_field(name = 'В муте', value = '{}'.format(member.mention))
    emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
    await ctx.send(embed = emb)

@client.command()
@commands.has_permissions(administrator = True)
async def embed(ctx, *, arg, amount = 1):
    await ctx.channel.purge(limit = amount)
    emb = discord.Embed(title = f'{ctx.author.avatar_url} {ctx.author.name}', colour = discord.Color.orange())
    emb.add_field(name = 'Cephalon', value = arg)
    emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
    await ctx.send(embed = emb)

@client.command()
@commands.has_permissions(administrator = True)
async def gaystvo(ctx, *, arg, amount = 1):
    await ctx.channel.purge(limit = amount)
    if ctx.author.name == 'сасиска':
        await ctx.send('@everyone ' + arg)
    else:
        await ctx.send(f'было написано {ctx.author.name}: @everyone ' + arg)
    
@client.command()
@commands.has_permissions(administrator = True)
async def say(ctx, *, arg, amount = 1):
    await ctx.channel.purge(limit = amount)
    if ctx.author.name == 'сасиска':
        await ctx.send(arg)
    else:
        await ctx.send(f'было написано {ctx.author.name}: ' + arg)
    
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
    
#альтернатива Groovy(которая, сука не работает)
@client.command()
async def join(ctx):
    if ctx.author.voice and ctx.author.voice.channel:
        channel = ctx.author.voice.channel
    else:
        await ctx.send("Ты должен быть в канале, чтобы использовать это.")
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
async def pm(ctx, member: discord.Member, amount = 1):
    await ctx.channel.purge(limit = amount)
    await member.send(f'Адамант сука')

#member joined the server
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
@commands.has_permissions(administrator = True)
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
    emb.add_field(name = '{}pm'.format('cephalon/'), value = 'пишет выбраному участнику **Адамант сука**')
    emb.add_field(name = '{}zatka'.format('cephalon/'), value = 'форма заявки набор кадров')
    emb.add_field(name = '{}about'.format('cephalon/'), value = 'показывает инфу о человеке. В отличии от Ayana пишет только необходимую инфу')
    emb.add_field(name = '{}join'.format('cephalon/'), value = 'приказывает зайти боту в голосовой канал')
    emb.add_field(name = '{}leave'.format('cephalon/'), value = 'приказывает боту выйти из голосового канала')
    emb.add_field(name = 'фыв', value = '~~Бот записывает все удалённые сообщения в #логи, исключая Groovy~~. **На доработке**')
    emb.add_field(name = 'жыж', value = 'также, для написания команд необязательно писать префикс, можно пингануть ~~@everyone~~ бота')
    emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
    await ctx.send(embed = emb)

@client.command()
async def time(ctx, amount = 1):
    await ctx.channel.purge(limit = amount)
    emb = discord.Embed(title = 'Время', colour = discord.Color.orange())
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
@commands.has_permissions(administrator = True)
async def kick(ctx , member: discord.Member, *, reason = None):
    await ctx.channel.purge(limit = 1)
    emb = discord.Embed(title = f'Кик от {ctx.author.name}', colour = discord.Color.orange())
    await member.kick(reason = reason)
    emb.add_field(name = 'Кикнут', value = '{}'.format(member.mention))
    emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
    await ctx.send(embed = emb)

#ban
@client.command()
@commands.has_permissions(administrator = True)
async def ban(ctx , member: discord.Member, *, reason = None):
    await ctx.channel.purge(limit = 1)
    emb = discord.Embed(title = f'Бан от {ctx.author.name}', colour = discord.Color.red())
    await member.ban(reason = reason)
    emb.add_field(name = 'Забанен', value = '{}'.format(member.mention))
    emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
    await ctx.send(embed = emb)

#message delete
@client.command()
@commands.has_permissions(administrator = True)
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
    await asyncio.sleep(2)
    await ctx.channel.purge(limit = 1)
    
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
        
@embed.error
async def embed_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.mention}, чё сказать то?')

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.author.mention} пытался вызвать комманду Embed. Хаха')

@gaystvo.error
async def gaystvo_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.mention}, чё сказать то?')

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.author.mention} пытался вызвать комманду Gaystvo. Хаха')

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
    
token = os.environ.get('BOT_TOKEN')

client.run(token)
