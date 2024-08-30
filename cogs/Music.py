import asyncio

import discord
import ffmpeg
import yt_dlp
import os
import shutil
from pathlib import Path
from functions import translate, get_locale
from discord.ext import commands

cwd = Path(__file__).parents[0].parents[0]
cwd = str(cwd)

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

loop = False

def remove_restricted_chars(filename):
    restricted_chars = '<>:"/\\|?*'
    for char in restricted_chars:
        filename = filename.replace(char, '')
    filename = filename.split()
    filename = ' '.join(filename)
    return filename.encode('ascii', errors = 'ignore').decode()

class Music(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Модуль Music загружен')

    @commands.command(aliases = ['p'])
    async def play(self, ctx, *, url):
        url = url.lstrip('<').rstrip('>')
        locale = get_locale(ctx.author.id)
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            title = ydl.extract_info(url, download = False)['title']
            duration = ydl.extract_info(url, download = False)['duration_string']
        for i in os.listdir(cwd):
            if i.endswith(".mp3"):
                os.rename(f'{cwd}\{i}', f'{cwd}\{remove_restricted_chars(i)}')
        for i in os.listdir(cwd):
            if i.endswith(".mp3"):
                file = i
        if not ctx.author.voice:
            return await ctx.send(embed = discord.Embed(description = translate(locale, 'play_not_in_voice_channel'), color = 0xff8000))
        if not ctx.guild.voice_client:
            await ctx.author.voice.channel.connect(self_deaf = True)
            await ctx.send(embed = discord.Embed(description = f'{translate(locale, "play_connected")}'.format(ctx_author_voice_channel_name = ctx.author.voice.channel.name), color = 0xff8000))
        if ctx.guild.voice_client:
            if ctx.guild.voice_client.channel != ctx.author.voice.channel:
                return await ctx.send(embed = discord.Embed(description = translate(locale, 'play_already_in_use'), color = 0xff0000))
            ctx.voice_client.play(discord.FFmpegPCMAudio(file, **{'options': '-vn'}))
            await ctx.send(embed = discord.Embed(description = f"{translate(locale, 'play_now_playing')}".format(player_title = title, player_url = url, player_duration = duration), color = 0xff8000))
            while ctx.voice_client.is_playing():
                await asyncio.sleep(1)
            os.remove(file)

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
            await ctx.send(embed = discord.Embed(description = 'Проигрывание возобновлено', color = 0xff8000))

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
                for file in os.listdir(cwd):
                    if file.endswith(".mp3"):
                        os.remove(f'{cwd}\{file}')
                await ctx.voice_client.disconnect(force = True)
                await ctx.voice_client.clean_up()
            else:
                await ctx.send(embed = discord.Embed(description = 'Ты должен быть в том же канале, что и я!', color = 0xff0000))
        else:
            emb = discord.Embed(description = 'Я уже не нахожусь в канале!', colour = 0xff0000)
            await ctx.send(embed = emb)

async def setup(client):
    await client.add_cog(Music(client))