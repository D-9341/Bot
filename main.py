import asyncio
import discord
import os

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
owner_commands = ['guilds', 'reset', 'status', 'generate', 'invite', 'disable', 'enable', 'reload', 'list', 'pull', 'tts', 'update']
cogs = ['Cephalon', 'Embeds', 'Events', 'Fun', 'Kernel', 'Mod', 'Misc', 'Music', 'sCephalon', 'sEmbeds', 'sFun', 'sMod', 'sMisc']

def bot_owner_or_has_permissions(**perms):
    origin = commands.has_permissions(**perms).predicate
    async def extended_check(ctx: commands.Context):
        return ctx.author.id in client.owner_ids or await origin(ctx)
    return commands.check(extended_check)

@client.event
async def on_ready():
    await client.tree.sync()

async def init():
    for file in os.listdir(CWD + "/cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            await client.load_extension(f"cogs.{file[:-3]}")

async def main():
    await init()
    await client.start(os.getenv('TOKEN'))

if __name__ == "__main__":
    asyncio.run(main())
