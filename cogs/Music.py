import asyncio

import discord
import youtube_dl
import os
from discord.ext import commands
from pymongo import MongoClient

passw = os.environ['passw']
cluster = MongoClient(f"mongodb+srv://cephalon:{passw}@locale.ttokw.mongodb.net/Locale?retryWrites=true&w=majority")
collection = cluster.Locale.locale

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',
}

ffmpeg_options = {
    'options': '-vn',
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume = 0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop = None, stream = True):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download = not stream))
        if 'entries' in data:
            data = data['entries'][0]
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data = data)

class Music(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Модуль Music загружен')

    @commands.command(aliases = ['p'])
    async def play(self, ctx, *, url):
        rlocale = collection.find_one({"_id": ctx.author.id})["locale"]
        if not ctx.author.voice:
            if rlocale == 'ru':
                await ctx.send(embed = discord.Embed(description = 'Ты должен быть в канале, чтобы использовать play.', color = 0xff8000))
            if rlocale == 'gnida':
                await ctx.send(embed = discord.Embed(description = 'Чтобы применить play тебе надо в канале быть, еблан.', color = 0xff8000))
        if not ctx.guild.voice_client:
            await ctx.author.voice.channel.connect(self_deaf = True)
            if rlocale == 'ru':
                await ctx.send(embed = discord.Embed(description = f'Присоединён к каналу {ctx.author.voice.channel.name}.', color = 0xff8000))
            if rlocale == 'gnida':
                await ctx.send(embed = discord.Embed(description = f'Присосался к {ctx.author.voice.channel.name}', color = 0xff8000))
        if ctx.guild.voice_client:
            if ctx.guild.voice_client.channel != ctx.author.voice.channel:
                if rlocale == 'ru':
                    return await ctx.send(embed = discord.Embed(description = 'Я уже используюсь в другом канале!', color = 0xff0000))
                if rlocale == 'gnida':
                    return await ctx.send(embed = discord.Embed(description = 'Ты чё слепой нахуй? Меня уже используют в другом канале, ебалай.', color = 0xff0000))
            player = await YTDLSource.from_url(url, loop = self.client.loop, stream = True)
            ctx.voice_client.play(player, after = ctx.voice_client.play(player))
            if rlocale == 'ru' or rlocale == 'gnida':
                await ctx.send(embed = discord.Embed(description = f"Сейчас играет: {player.title}", color = 0xff8000))
            if rlocale == 'en':
                await ctx.send(embed = discord.Embed(description = f"Now playing: {player.title}", color = 0xff8000))

    @commands.command()
    async def resume(self, ctx):
        rlocale = collection.find_one({"_id": ctx.author.id})["locale"]
        if not ctx.author.voice:
            return await ctx.send(embed = discord.Embed(description = 'Ты должен быть в канале, чтобы использовать resume.', color = 0xff8000))
        if not ctx.guild.voice_client:
            return await ctx.send(embed = discord.Embed(description = 'Я не нахожусь в канале!', color = 0xff0000))
        if ctx.guild.voice_client:
            if ctx.guild.voice_client.channel != ctx.author.voice.channel:
                return await ctx.send(embed = discord.Embed(description = 'Ты должен быть в том же канале, что и я!', color = 0xff0000))
            ctx.guild.voice_client.resume()
            await ctx.send(embed = discord.Embed(description = 'Проигрывание возобновлено.', color = 0xff8000))

    @commands.command()
    async def volume(self, ctx, volume: int):
        rlocale = collection.find_one({"_id": ctx.author.id})["locale"]
        if 0 < volume <= 100:
            if not ctx.author.voice:
                return await ctx.send(embed = discord.Embed(description = 'Ты должен быть в канале, чтобы использовать volume.', color = 0xff8000))
            if not ctx.guild.voice_client:
                return await ctx.send(embed = discord.Embed(description = 'Я не нахожусь в канале!', color = 0xff0000))
            if ctx.guild.voice_client:
                if ctx.guild.voice_client.channel != ctx.author.voice.channel:
                    return await ctx.send(embed = discord.Embed(description = 'Ты должен быть в том же канале, что и я!', color = 0xff0000))
                ctx.voice_client.source.volume = volume / 100
                await ctx.send(embed = discord.Embed(description = f"Громкость изменена: {volume}%", color = 0xff8000))
        else:
            await ctx.send(embed = discord.Embed(description = f'Недопустимое значение: {volume}%', color = 0xff0000))

    @commands.command()
    async def pause(self, ctx):
        rlocale = collection.find_one({"_id": ctx.author.id})["locale"]
        if not ctx.author.voice:
            return await ctx.send(embed = discord.Embed(description = 'Ты должен быть в канале, чтобы использовать pause.', color = 0xff8000))
        if not ctx.guild.voice_client:
            return await ctx.send(embed = discord.Embed(description = 'Я не нахожусь в канале!', color = 0xff0000))
        if ctx.guild.voice_client:
            if ctx.guild.voice_client.channel != ctx.author.voice.channel:
                return await ctx.send(embed = discord.Embed(description = 'Ты должен быть в том же канале, что и я!', color = 0xff0000))
            ctx.guild.voice_client.pause()
            await ctx.send(embed = discord.Embed(description = 'Проигрывание приостановлено.', color = 0xff8000))

    @commands.command(aliases = ['s', 'ass'])
    async def stop(self, ctx):
        rlocale = collection.find_one({"_id": ctx.author.id})["locale"]
        if not ctx.author.voice:
            return await ctx.send(embed = discord.Embed(description = 'Ты должен быть в канале, чтобы использовать stop.', color = 0xff8000))
        if not ctx.guild.voice_client:
            return await ctx.send(embed = discord.Embed(description = 'Я не нахожусь в канале!', color = 0xff0000))
        if ctx.guild.voice_client:
            if ctx.guild.voice_client.channel != ctx.author.voice.channel:
                return await ctx.send(embed = discord.Embed(description = 'Ты должен быть в том же канале, что и я!', color = 0xff0000))
            ctx.guild.voice_client.stop()
            await ctx.send(embed = discord.Embed(description = 'Плеер остановлен.', color = 0xff8000))

    @commands.command()
    async def join(self, ctx):
        rlocale = collection.find_one({"_id": ctx.author.id})["locale"]
        if not ctx.author.voice:
            await ctx.send(embed = discord.Embed(description = 'Ты должен быть в канале, чтобы использовать join.', color = 0xff8000))
        else:
            if not ctx.voice_client:
                await ctx.author.voice.channel.connect(self_deaf = True)
                return await ctx.send(embed = discord.Embed(description = f'Присоединён к каналу {ctx.author.voice.channel.name}.', color = 0xff8000))
            else:
                return await ctx.send(embed = discord.Embed(description = f'Я уже используюсь в другом канале!', color = 0xff8000))

    @commands.command()
    async def leave(self, ctx):
        rlocale = collection.find_one({"_id": ctx.author.id})["locale"]
        if ctx.guild.voice_client:
            if ctx.guild.voice_client.channel == ctx.author.voice.channel:
                await ctx.send(embed = discord.Embed(description = f'Покинул канал {ctx.author.voice.channel.name}.', color = 0xff8000))
                await ctx.voice_client.disconnect(force = True)
                await ctx.voice_client.clean_up()
            else:
                await ctx.send(embed = discord.Embed(description = 'Ты должен быть в том же канале, что и я!', color = 0xff0000))
        else:
            emb = discord.Embed(description = 'Я уже не нахожусь в канале!', colour = 0xff0000)
            await ctx.send(embed = emb)

async def setup(client):
    await client.add_cog(Music(client))
