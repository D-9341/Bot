import asyncio
import discord
import os
import psycopg2

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
PASSWORD = os.getenv('DB_PASS')

def bot_owner_or_has_permissions(**perms):
    origin = commands.has_permissions(**perms).predicate
    async def extended_check(ctx: commands.Context):
        return ctx.author.id in client.owner_ids or await origin(ctx)
    return commands.check(extended_check)

@client.event
async def on_ready():
    await client.tree.sync()

@client.command()
async def disable(ctx, *, target: str):
    if ctx.author.id not in client.owner_ids:
        raise commands.NotOwner()
    if target.lower() in client.all_commands:
        command = client.get_command(target)
        if command.enabled:
            command.enabled = False
            return await ctx.send(embed = discord.Embed(description = f'Команда `{target}` отключена', color = 0xff8000))
        else:
            return await ctx.send(embed = discord.Embed(description = f'Команда `{target}` уже отключена', color = 0xff0000))
    elif f'cogs.{target.title()}' in client.extensions:
        extension = f'cogs.{target.title()}'
        if extension == 'cogs.Events':
            return await ctx.send(embed = discord.Embed(description = 'Модуль `Events` не может быть выгружен', color = 0xff0000))
        if extension not in client.extensions:
            return await ctx.send(embed = discord.Embed(description = f'Модуль `{target}` уже выгружен или не найден', color = 0xff0000))
        try:
            await client.unload_extension(extension)
        except commands.ExtensionNotFound:
            return await ctx.send(embed = discord.Embed(description = f'Модуль `{target}` не найден', color = 0xff0000))
        else:
            await ctx.send(embed = discord.Embed(description = f'Модуль `{target}` выгружен', color = 0xff8000))
    else:
        return await ctx.send(embed = discord.Embed(description = f'Объект `{target}` не найден или уже отключён', color = 0xff0000))

@client.command()
async def enable(ctx, *, target: str):
    if ctx.author.id not in client.owner_ids:
        raise commands.NotOwner()
    if target.lower() in client.all_commands:
        command = client.get_command(target)
        if not command.enabled:
            command.enabled = True
            await ctx.send(embed = discord.Embed(description = f'Команда `{target}` включена', color = 0xff8000))
        else:
            await ctx.send(embed = discord.Embed(description = f'Команда `{target}` уже включена', color = 0xff0000))
    else:
        extension = f'cogs.{target.title()}'
        try:
            await client.load_extension(extension)
        except commands.ExtensionNotFound:
            await ctx.send(embed = discord.Embed(description = f'Объект `{target}` не найден', color = 0xff0000))
        except commands.ExtensionAlreadyLoaded:
            await ctx.send(embed = discord.Embed(description = f'Модуль `{target}` уже загружен', color = 0xff0000))
        except commands.ExtensionFailed as error:
            await ctx.send(embed = discord.Embed(description = f'Модуль `{target}` не может быть загружен: `{error}`', color = 0xff0000))
        else:
            await ctx.send(embed = discord.Embed(description = f'Модуль `{target}` загружен', color = 0xff8000))

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

@client.command()
async def pull(ctx):
    if ctx.author.id not in client.owner_ids:
        raise commands.NotOwner()
    process = await asyncio.create_subprocess_shell('git pull', stdout = asyncio.subprocess.PIPE, stderr = asyncio.subprocess.PIPE)
    stdout, stderr = await process.communicate()
    if process.returncode != 0:
        await ctx.send(embed = discord.Embed(description = f'Не удалось получить обновления: `{stderr.decode("utf-8")}`', color = 0xff0000))
    else:
        await ctx.send(embed = discord.Embed(description = f'Обновления получены:\n`{stdout.decode("utf-8").strip()}`', color = 0xff8000))
        await asyncio.sleep(client.latency)
        await ctx.send(embed = discord.Embed(description = 'Перезагрузка...', color = 0xff8000))
        await asyncio.sleep(client.latency)
        await reload(ctx)

@client.command()
async def access_db(ctx, db, *, query: str = None):
    if ctx.author.id not in client.owner_ids:
        raise commands.NotOwner()
    conn = psycopg2.connect(host = "localhost", database = db, user = "postgres", password = PASSWORD, port = 5432)
    cur = conn.cursor()
    cur.execute(query)
    result = cur.fetchall()
    conn.close()
    await ctx.send(f'```{result}```')

async def init():
    for file in os.listdir(CWD + "/cogs"):
        if file.endswith(".py"):
            await client.load_extension(f"cogs.{file[:-3]}")

async def main():
    await init()
    await client.start(os.getenv('TOKEN'))

if __name__ == "__main__":
    asyncio.run(main())
