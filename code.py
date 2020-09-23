import asyncio
import random
import datetime
from pathlib import Path
import os
import discord
from discord.ext import commands
from discord.utils import get

client = commands.Bot(command_prefix = commands.when_mentioned_or('cy/'), owner_id = 338714886001524737)
client.remove_command('help')
cwd = Path(__file__).parents[0]
cwd = str(cwd)

#test commands space

#test commands space

@client.command(aliases = ['Info', 'INFO'])
@commands.cooldown(1, 5, commands.BucketType.default)
async def info(ctx):
    await ctx.message.delete()
    emb = discord.Embed(title = 'Welcome to the cum zone', colour = discord.Color.orange())
    emb.set_author(name = client.user.name, url = 'https://warframe.fandom.com/wiki/Cephalon_Cy', icon_url = client.user.avatar_url)
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
    emb = discord.Embed(description = '[Ссылка](https://discordapp.com/oauth2/authorize?&client_id=694170281270312991&scope=bot&permissions=8) для приглашения Cy на сервера', colour = discord.Color.orange(), timestamp = ctx.message.created_at)
    emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
    await ctx.send(embed = emb)
    
@client.command(aliases = ['Ping', 'PING'])
@commands.cooldown(1, 5, commands.BucketType.default)
async def ping(ctx):
    await ctx.message.delete()
    emb = discord.Embed(description = f'Pong! `{round(client.latency * 1000)} ms`', colour = discord.Color.orange(), timestamp = ctx.message.created_at)
    emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
    await ctx.send(embed = emb)
    
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
        await ctx.send('```cy/clear <количество> |confirm|```')
    elif arg == 'dm':
        await ctx.send('```cy/dm <@пинг/имя/ID> <текст>```')
    elif arg == 'edit':
        await ctx.send('```cy/edit <ID> <новый текст>```')
    elif arg == 'say':
        await ctx.send('```cy/say |noembed| |text| |title текст| |description текст| |footer текст| |ссылка| |ссылка| |цвет| |@пинг/имя/ID| |@роль/имя роли/ID роли|```')
    elif arg == 'emb_ctx':
        await ctx.send('```cy/emb_ctx <ID>```')
    elif arg == 'emb_edit':
        await ctx.send('```cy/emb_edit <ID> |title текст| |description текст| |footer текст| |ссылка| |ссылка| |цвет| |@пинг/имя/ID| |@роль/имя роли/ID роли|```')
    elif arg == 'say_everyone':
        await ctx.send('```cy/say_everyone |title текст| |description текст| |footer текст| |ссылка| |ссылка| |цвет| |@пинг/имя/ID| |@роль/имя роли/ID роли|```')
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

@client.event
async def on_ready():
    await client.change_presence(status = discord.Status.idle, activity = discord.Activity(type = discord.ActivityType.watching, name = 'В Discord API'))
    
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.message.delete()
        emb = discord.Embed(description = f'{ctx.author.mention}, я не знаю такую команду!', colour = discord.Color.orange())
        emb.set_footer(text = 'Считаете, что такая команда должна быть? Напишите сасиска#2472 и опишите её суть!')
        await ctx.send(embed = emb)

if __name__ == '__main__':
    for file in os.listdir(cwd+"/cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            client.load_extension(f"cogs.{file[:-3]}")
t = os.environ.get('t')
client.run(t)
