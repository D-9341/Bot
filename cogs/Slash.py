import asyncio
import datetime
import json
import os
import random
import re
import regex
import secrets

import discord
import discord_slash
from pymongo import MongoClient
from discord.ext import commands
from discord.utils import get
from discord_slash import SlashCommand, SlashContext

class Slash(commands.Cog):
    def __init__:
        self.client = client
        
def setup(client):
    client.add_cog(Slash(client))
