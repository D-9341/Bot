import datetime
import json
import os
import discord
from discord.ext import commands
from discord.utils import get

client = commands.Bot(command_prefix = "cephalon/")
#like cephalon/support

@client.event
async def ping(ctx):
    await ctx.send(f'pong!')
