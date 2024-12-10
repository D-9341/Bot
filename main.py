# coding=utf-8
import asyncio
import os
import discord

from dotenv import load_dotenv
from pathlib import Path
from discord.ext import commands

intents = discord.Intents.all()
uptime = discord.utils.utcnow()

client = commands.Bot(command_prefix = commands.when_mentioned_or('cy/'), intents = intents, status = discord.Status.idle, activity = discord.Activity(type = discord.ActivityType.watching, name = 'в никуда'), owner_ids = {338714886001524737, 417012231406878720}, case_insensitive = True, allowed_mentions = discord.AllowedMentions(everyone = False))
client.remove_command('help')
CWD = Path(__file__).parents[0]
CWD = str(CWD)
load_dotenv(CWD + '\\vars.env')

@client.event
async def on_ready():
    await client.tree.sync()

@client.command()
async def disable(ctx, cmd: str):
    if ctx.author.id not in client.owner_ids:
        raise commands.NotOwner()
    client.get_command(cmd).enabled = False
    await ctx.send(embed = discord.Embed(description = f'Команда `{cmd}` выключена', color = 0xff8000))

@client.command()
async def enable(ctx, cmd: str):
    if ctx.author.id not in client.owner_ids:
        raise commands.NotOwner()
    client.get_command(cmd).enabled = True
    await ctx.send(embed = discord.Embed(description = f'Команда `{cmd}` включена', color = 0xff8000))

@client.command()
async def unload(ctx, extension: str):
    if ctx.author.id not in client.owner_ids:
        raise commands.NotOwner()
    ext = f'cogs.{ext}'
    if ext == 'cogs.Events': return await ctx.send(embed = discord.Embed(description = 'Модуль `Events` не может быть выгружен', color = 0xff0000))
    if ext not in client.extensions:
        return await ctx.send(embed = discord.Embed(description = f'Модуль `{extension}` уже выгружен или не найден', color = 0xff0000))
    try:
        await client.unload_extension(ext)
    except commands.ExtensionNotFound:
        return await ctx.send(embed = discord.Embed(description = f'Модуль `{extension}` не найден', color = 0xff0000))
    await ctx.send(embed = discord.Embed(description = f'Модуль `{extension}` выгружен', color = 0xff8000))

@client.command()
async def load(ctx, extension: str):
    if ctx.author.id not in client.owner_ids:
        raise commands.NotOwner()
    ext = f'cogs.{ext}'
    if ext in client.extensions:
        return await ctx.send(embed = discord.Embed(description = f'Модуль `{extension}` уже загружен', color = 0xff0000))
    try:
        await client.load_extension(ext)
    except commands.ExtensionNotFound:
        return await ctx.send(embed = discord.Embed(description = f'Модуль `{extension}` не найден', color = 0xff0000))
    except commands.ExtensionAlreadyLoaded:
        return await ctx.send(embed = discord.Embed(description = f'Модуль `{extension}` уже загружен', color = 0xff0000))
    except commands.ExtensionFailed as error:
        return await ctx.send(embed = discord.Embed(description = f'Модуль `{extension}` не может быть загружен: `{error}`', color = 0xff0000))
    await ctx.send(embed = discord.Embed(description = f'Модуль `{extension}` загружен', color = 0xff8000))

@client.command()
async def reload(ctx):
    if ctx.author.id not in client.owner_ids:
        raise commands.NotOwner()
    excepted_modules = {}
    for name in list(client.extensions):
        try:
            await client.reload_extension(name)
        except commands.ExtensionFailed as error:
            excepted_modules[f'`{name[5:]}`'] = str(error).replace('cogs.', '')
    if len(excepted_modules) == len(client.extensions):
        return await ctx.send(embed = discord.Embed(description = 'Все модули выдали ошибку', color = 0xff0000))
    if excepted_modules:
        return await ctx.send(embed = discord.Embed(description = f'{'Модуль' if len(excepted_modules) == 1 else 'Модули'} {', '.join(excepted_modules.keys())} не {'может быть перезагружен' if len(excepted_modules) == 1 else 'могут быть перезагружены'}, {f'пингани {client.get_user(338714886001524737).mention}' if ctx.author.id != 338714886001524737 else 'необходимо исправить'}:\n{''.join([f'`{name}`: `{error}`\n' for name, error in excepted_modules.items()])}', color = 0xff0000))
    await ctx.send(embed = discord.Embed(description = 'Модули перезагружены', color = 0xff8000))

async def init():
    for file in os.listdir(CWD + "/cogs"):
        if file.endswith(".py"):
            await client.load_extension(f"cogs.{file[:-3]}")

async def main():
    await init()
    await client.start(os.getenv('TOKEN'))

if __name__ == "__main__":
    asyncio.run(main())
