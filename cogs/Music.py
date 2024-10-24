import asyncio

import discord
import yt_dlp
import os
import logging
from pathlib import Path
from functions import translate, get_locale
from discord.ext import commands
logging.getLogger('yt_dlp').setLevel(logging.WARNING)

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
        message = await ctx.send(embed = discord.Embed(description = f'{translate(locale, 'play_downloading')}'.format(url = url), color = 0xff8000))
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download = True)
            title = info['title']
            duration = info['duration_string']
            video_id = info['id']
        for i in os.listdir(cwd):
            if i.endswith(".mp3"):
                os.rename(f'{cwd}\{i}', f'{cwd}\{video_id}.mp3')
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
            await message.edit(embed = discord.Embed(description = f"{translate(locale, 'play_now_playing')}".format(player_title = title, player_url = url, player_duration = duration), color = 0xff8000))
            while ctx.voice_client.is_playing():
                await asyncio.sleep(1)
            os.remove(file)

    @commands.command()
    async def resume(self, ctx):
        locale = get_locale(ctx.author.id)
        if not ctx.author.voice:
            return await ctx.send(embed = discord.Embed(description = translate(locale, 'resume_not_in_voice_channel'), color = 0xff8000))
        if not ctx.guild.voice_client:
            return await ctx.send(embed = discord.Embed(description = translate(locale, 'resume_not_connected'), color = 0xff0000))
        if ctx.guild.voice_client:
            if ctx.guild.voice_client.channel != ctx.author.voice.channel:
                return await ctx.send(embed = discord.Embed(description = translate(locale, 'resume_diff_channel'), color = 0xff0000))
            ctx.guild.voice_client.resume()
            await ctx.send(embed = discord.Embed(description = translate(locale, 'resume_success'), color = 0xff8000))

    @commands.command()
    async def volume(self, ctx, volume: int):
        raise commands.DisabledCommand()
        # locale = get_locale(ctx.author.id)
        # if 0 <= volume <= 100:
        #     if not ctx.author.voice:
        #         return await ctx.send(embed = discord.Embed(description = 'Ты должен быть в канале, чтобы использовать volume', color = 0xff8000))
        #     if not ctx.guild.voice_client:
        #         return await ctx.send(embed = discord.Embed(description = 'Я не нахожусь в канале!', color = 0xff0000))
        #     if ctx.guild.voice_client:
        #         if ctx.guild.voice_client.channel != ctx.author.voice.channel:
        #             return await ctx.send(embed = discord.Embed(description = 'Ты должен быть в том же канале, что и я!', color = 0xff0000))
        #         ctx.voice_client.source.volume = volume / 100
        #         await ctx.send(embed = discord.Embed(description = f"Громкость изменена: {volume}%", color = 0xff8000))
        # else:
        #     await ctx.send(embed = discord.Embed(description = f'Недопустимое значение: {volume}%', color = 0xff0000))

    @commands.command()
    async def pause(self, ctx):
        locale = get_locale(ctx.author.id)
        if not ctx.author.voice:
            return await ctx.send(embed = discord.Embed(description = translate(locale, 'pause_not_in_voice_channel'), color = 0xff8000))
        if not ctx.guild.voice_client:
            return await ctx.send(embed = discord.Embed(description = translate(locale, 'pause_not_connected'), color = 0xff0000))
        if ctx.guild.voice_client:
            if ctx.guild.voice_client.channel != ctx.author.voice.channel:
                return await ctx.send(embed = discord.Embed(description = translate(locale, 'pause_diff_channel'), color = 0xff0000))
            ctx.guild.voice_client.pause()
            await ctx.send(embed = discord.Embed(description = translate(locale, 'pause_success'), color = 0xff8000))

    @commands.command(aliases = ['s', 'ass'])
    async def stop(self, ctx):
        locale = get_locale(ctx.author.id)
        if not ctx.author.voice:
            return await ctx.send(embed = discord.Embed(description = translate(locale, 'stop_not_in_voice_channel'), color = 0xff8000))
        if not ctx.guild.voice_client:
            return await ctx.send(embed = discord.Embed(description = translate(locale, 'stop_not_connected'), color = 0xff0000))
        if ctx.guild.voice_client:
            if ctx.guild.voice_client.channel != ctx.author.voice.channel:
                return await ctx.send(embed = discord.Embed(description = translate(locale, 'stop_diff_channel'), color = 0xff0000))
            ctx.guild.voice_client.stop()
            await ctx.send(embed = discord.Embed(description = translate(locale, 'stop_success'), color = 0xff8000))

    @commands.command()
    async def join(self, ctx):
        locale = get_locale(ctx.author.id)
        if not ctx.author.voice:
            await ctx.send(embed = discord.Embed(description = translate(locale, 'join_not_in_voice_channel'), color = 0xff8000))
        else:
            if not ctx.voice_client:
                await ctx.author.voice.channel.connect(self_deaf = True)
                return await ctx.send(embed = discord.Embed(description = f'{translate(locale, "join_success")}'.format(ctx_author_voice_channel_name = ctx.author.voice.channel.name), color = 0xff8000))
            if ctx.voice_client.channel == ctx.author.voice.channel:
                return await ctx.send(embed = discord.Embed(description = translate(locale, 'join_already_in_author_voice_channel'), color = 0xff8000))
            await ctx.send(embed = discord.Embed(description = translate(locale, 'join_already_connected'), color = 0xff8000))

    @commands.command()
    async def leave(self, ctx):
        locale = get_locale(ctx.author.id)
        if ctx.guild.voice_client:
            if ctx.guild.voice_client.channel == ctx.author.voice.channel:
                await ctx.send(embed = discord.Embed(description = f'{translate(locale, "leave_success")}'.format(ctx_author_voice_channel_name = ctx.author.voice.channel.name), color = 0xff8000))
                for file in os.listdir(cwd):
                    if file.endswith(".mp3"):
                        os.remove(f'{cwd}\{file}')
                await ctx.voice_client.disconnect(force = True)
                await ctx.voice_client.clean_up()
            else:
                await ctx.send(embed = discord.Embed(description = translate(locale, 'leave_diff_channel'), color = 0xff0000))
        else:
            emb = discord.Embed(description = translate(locale, 'leave_already_not_connected'), colour = 0xff0000)
            await ctx.send(embed = emb)

async def setup(client):
    await client.add_cog(Music(client))
