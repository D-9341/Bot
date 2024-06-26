import asyncio

import discord
import yt_dlp
from functions import translate, get_locale
from discord.ext import commands

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

ytdl = yt_dlp.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume = 0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop = None, stream = False):
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
        locale = get_locale(ctx.author.id)
        if not ctx.author.voice:
            return await ctx.send(embed = discord.Embed(description = translate(locale, 'play_not_in_voice_channel'), color = 0xff8000))
        if not ctx.guild.voice_client:
            await ctx.author.voice.channel.connect(self_deaf = True, cls = lambda _, __: YTDLSource)
            await ctx.send(embed = discord.Embed(description = f'{translate(locale, "play_connected")}'.format(ctx_author_voice_channel_name = ctx.author.voice.channel.name), color = 0xff8000))
        if ctx.guild.voice_client:
            if ctx.guild.voice_client.channel != ctx.author.voice.channel:
                return await ctx.send(embed = discord.Embed(description = translate(locale, 'play_already_in_use'), color = 0xff0000))
            player = await YTDLSource.from_url(url, loop = self.client.loop, stream = True)
            ctx.voice_client.play(player, after = lambda _: ctx.voice_client.play(player))
            await ctx.send(embed = discord.Embed(description = f"{translate(locale, 'play_now_playing')}".format(player_title = player.title), color = 0xff8000))

    @commands.command()
    async def resume(self, ctx):
        locale = get_locale(ctx.author.id)
        if not ctx.author.voice:
            return await ctx.send(embed = discord.Embed(description = 'Ты должен быть в канале, чтобы использовать resume', color = 0xff8000))
        if not ctx.guild.voice_client:
            return await ctx.send(embed = discord.Embed(description = 'Я не нахожусь в канале!', color = 0xff0000))
        if ctx.guild.voice_client:
            if ctx.guild.voice_client.channel != ctx.author.voice.channel:
                return await ctx.send(embed = discord.Embed(description = 'Ты должен быть в том же канале, что и я!', color = 0xff0000))
            ctx.guild.voice_client.resume()
            await ctx.send(embed = discord.Embed(description = 'Проигрывание возобновлено.', color = 0xff8000))

    @commands.command()
    async def volume(self, ctx, volume: int):
        locale = get_locale(ctx.author.id)
        if 0 <= volume <= 100:
            if not ctx.author.voice:
                return await ctx.send(embed = discord.Embed(description = 'Ты должен быть в канале, чтобы использовать volume', color = 0xff8000))
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
        locale = get_locale(ctx.author.id)
        if not ctx.author.voice:
            return await ctx.send(embed = discord.Embed(description = 'Ты должен быть в канале, чтобы использовать pause', color = 0xff8000))
        if not ctx.guild.voice_client:
            return await ctx.send(embed = discord.Embed(description = 'Я не нахожусь в канале!', color = 0xff0000))
        if ctx.guild.voice_client:
            if ctx.guild.voice_client.channel != ctx.author.voice.channel:
                return await ctx.send(embed = discord.Embed(description = 'Ты должен быть в том же канале, что и я!', color = 0xff0000))
            ctx.guild.voice_client.pause()
            await ctx.send(embed = discord.Embed(description = 'Проигрывание приостановлено', color = 0xff8000))

    @commands.command(aliases = ['s', 'ass'])
    async def stop(self, ctx):
        locale = get_locale(ctx.author.id)
        if not ctx.author.voice:
            return await ctx.send(embed = discord.Embed(description = 'Ты должен быть в канале, чтобы использовать stop', color = 0xff8000))
        if not ctx.guild.voice_client:
            return await ctx.send(embed = discord.Embed(description = 'Я не нахожусь в канале!', color = 0xff0000))
        if ctx.guild.voice_client:
            if ctx.guild.voice_client.channel != ctx.author.voice.channel:
                return await ctx.send(embed = discord.Embed(description = 'Ты должен быть в том же канале, что и я!', color = 0xff0000))
            ctx.guild.voice_client.stop()
            await ctx.send(embed = discord.Embed(description = 'Плеер остановлен', color = 0xff8000))

    @commands.command()
    async def join(self, ctx):
        locale = get_locale(ctx.author.id)
        if not ctx.author.voice:
            await ctx.send(embed = discord.Embed(description = 'Ты должен быть в канале, чтобы использовать join', color = 0xff8000))
        else:
            if not ctx.voice_client:
                await ctx.author.voice.channel.connect(self_deaf = True)
                return await ctx.send(embed = discord.Embed(description = f'Присоединён к каналу {ctx.author.voice.channel.name}', color = 0xff8000))
            else:
                return await ctx.send(embed = discord.Embed(description = f'Я уже используюсь в другом канале!', color = 0xff8000))

    @commands.command()
    async def leave(self, ctx):
        locale = get_locale(ctx.author.id)
        if ctx.guild.voice_client:
            if ctx.guild.voice_client.channel == ctx.author.voice.channel:
                await ctx.send(embed = discord.Embed(description = f'Покинул канал {ctx.author.voice.channel.name}', color = 0xff8000))
                await ctx.voice_client.disconnect(force = True)
                await ctx.voice_client.clean_up()
            else:
                await ctx.send(embed = discord.Embed(description = 'Ты должен быть в том же канале, что и я!', color = 0xff0000))
        else:
            emb = discord.Embed(description = 'Я уже не нахожусь в канале!', colour = 0xff0000)
            await ctx.send(embed = emb)

async def setup(client):
    await client.add_cog(Music(client))