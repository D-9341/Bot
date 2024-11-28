# coding=utf-8
import asyncio
import os
import discord

from dotenv import load_dotenv
from pathlib import Path
from discord.ext import commands

intents = discord.Intents.all()

client = commands.Bot(command_prefix = commands.when_mentioned_or('cy/'), intents = intents, status = discord.Status.idle, activity = discord.Activity(type = discord.ActivityType.watching, name = 'в никуда'), owner_ids = {338714886001524737, 417012231406878720}, case_insensitive = True, allowed_mentions = discord.AllowedMentions(everyone = False))
client.remove_command('help')
CWD = Path(__file__).parents[0]
CWD = str(CWD)
load_dotenv(CWD + '\\vars.env')

@client.command()
async def reload(ctx):
    for name in list(client.extensions):
        await client.reload_extension(name)
    await ctx.send(embed = discord.Embed(description = 'Модули перезагружены', color = 0xff8000))

async def load():
    for file in os.listdir(CWD+"/cogs"):
        if file.endswith(".py"):
            await client.load_extension(f"cogs.{file[:-3]}")

async def main():
    await load()
    await client.start(os.getenv('TOKEN'))

asyncio.run(main())
