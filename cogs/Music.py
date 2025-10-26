import asyncio
import os
from pathlib import Path

import discord
import yt_dlp
from discord.ext import commands
from gtts import gTTS

from cogs.Constants import colors
from functions import get_locale, translate

yt_dlp.utils.bug_reports_message = lambda: ''

cwd = Path(__file__).parents[0].parents[0]
cwd = str(cwd)

queue = []
title_list = []
loop = False

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
        self.client: commands.Bot = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Модуль Music загружен')

    @commands.command()
    async def tts(self, ctx: commands.Context, *, text: str):
        if ctx.author.id not in self.client.owner_ids:
            raise commands.NotOwner()
        if not text:
            return await ctx.send(embed = discord.Embed(description = 'Вы должны указать текст для произнесения', color = colors.ERROR))
        if not ctx.voice_client:
            return await ctx.send(embed = discord.Embed(description = 'Я не подключён к голосовому каналу', color = colors.ERROR))
        speech = gTTS(text = text, lang = 'ru', slow = True)
        speech.save('temp/speech.mp3')
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio('temp/speech.mp3'))
        ctx.voice_client.play(source)
        message = await ctx.send(embed = discord.Embed(description = 'Говорю...', color = colors.JDH))
        while ctx.voice_client.is_playing():
            await asyncio.sleep(1)
        os.remove('temp/speech.mp3')
        await message.edit(embed = discord.Embed(description = f'Текст `{text}` произнесён', color = colors.JDH))

    @commands.command(aliases = ['p'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def play(self, ctx: commands.Context, *, url: str):
        locale = get_locale(ctx.author.id)
        url = url.lstrip('<').rstrip('>')
        try:
            if os.path.exists(f'{cwd}/{url[-11:]}.mp3'):
                audio = os.path.join(cwd, f'{url[-11:]}.mp3')
                info = await self.client.loop.run_in_executor(None, lambda: yt_dlp.YoutubeDL(ydl_opts).extract_info(url, download = False))
                title = info['title']
                duration = info['duration_string']
            else:
                await ctx.send(embed = discord.Embed(description = f'{translate(locale, "play_downloading")}'.format(url = url), color = colors.JDH))
                info = await self.client.loop.run_in_executor(None, lambda: yt_dlp.YoutubeDL(ydl_opts).extract_info(url, download = True))
                title = info['title']
                duration = info['duration_string']
                video_id = info['id']
                for file in os.listdir(cwd):
                    if file.endswith("].mp3"):
                        os.rename(os.path.join(cwd, file), os.path.join(cwd, f'{video_id}.mp3'))
                        audio = os.path.join(cwd, f'{video_id}.mp3')
                        break
        except Exception as error:
            if "Sign in to confirm your age" in str(error):
                return await ctx.send(embed = discord.Embed(description = translate(locale, 'play_video_age_restricted'), color = colors.ERROR))
            if "This video contains content from" in str(error):
                return await ctx.send(embed = discord.Embed(description = translate(locale, 'play_video_country_restricted'), color = colors.ERROR))
            if "Remote end closed connection" in str(error) or "The read operation timed out" in str(error):
                return await ctx.send(embed = discord.Embed(description = translate(locale, 'play_video_downloading_error'), color = colors.ERROR))
            return await ctx.send(embed = discord.Embed(description = f'{translate(locale, "play_video_unknown_error")}'.format(error = error), color = colors.ERROR))
        queue.append(audio)
        title_list.append(title)
        await ctx.send(embed = discord.Embed(description = f'{translate(locale, "play_added_to_queue")}'.format(title = title, pos = len(queue)), color = colors.JDH))
        if not ctx.author.voice:
            return await ctx.send(embed = discord.Embed(description = f'{translate(locale, 'not_in_voice_channel')}'.format(command = 'play'), color = colors.JDH))
        if not ctx.guild.voice_client:
            await ctx.author.voice.channel.connect(self_deaf = True)
            await ctx.send(embed = discord.Embed(description = f'{translate(locale, "play_connected")}'.format(ctx_author_voice_channel_name = ctx.author.voice.channel.name), color = colors.JDH))
        if ctx.guild.voice_client:
            if ctx.guild.voice_client.channel != ctx.author.voice.channel:
                return await ctx.send(embed = discord.Embed(description = translate(locale, 'play_already_in_use'), color = colors.ERROR))
            while queue:
                if not ctx.guild.voice_client.is_playing():
                    ctx.voice_client.play(discord.FFmpegPCMAudio(queue[0], **{'options': '-vn'}))
                    await ctx.send(embed = discord.Embed(description = f"{translate(locale, 'play_now_playing')}".format(player_title = title_list[0], player_url = url, player_duration = duration), color = colors.JDH))
                while ctx.voice_client.is_playing():
                    await asyncio.sleep(1)
                if not loop:
                    queue.pop(0)
                    title_list.pop(0)

    @commands.group(aliases = ['q'], invoke_without_command = True)
    async def queue(self, ctx: commands.Context):
        locale = get_locale(ctx.author.id)
        queue_display = [f'{index + 1}. {title}' for index, title in enumerate(title_list)]
        await ctx.send(embed = discord.Embed(description = f'{translate(locale, "queue_list")}'.format(queue_list='\n'.join(queue_display)) if title_list else translate(locale, 'queue_empty'), color = colors.JDH))

    @queue.command(name = 'clear')
    async def queue_clear(self, ctx: commands.Context):
        locale = get_locale(ctx.author.id)
        title_list.clear(); queue.clear()
        if ctx.guild.voice_client:
            ctx.guild.voice_client.stop()
        await ctx.send(embed = discord.Embed(description = translate(locale, 'queue_clear'), color = colors.JDH))

    @queue.command(aliases = ['next', 'skip'])
    async def queue_skip(self, ctx: commands.Context):
        locale = get_locale(ctx.author.id)
        if len(queue) > 1:
            ctx.guild.voice_client.stop()
            queue.pop(0)
            title_list.pop(0)
            ctx.guild.voice_client.play(discord.FFmpegPCMAudio(queue[0], **{'options': '-vn'}))
            await ctx.send(embed = discord.Embed(description = f'{translate(locale, "queue_skip")}'.format(title = title_list[0]), color = colors.JDH))
        else:
            await ctx.send(embed = discord.Embed(description = translate(locale, 'queue_skip_empty'), color = colors.JDH))

    @queue.command(name = 'loop')
    async def queue_loop(self, ctx: commands.Context, action: str = 'toggle'):
        locale = get_locale(ctx.author.id)
        global loop
        if action != 'status':
            loop = not loop
        await ctx.send(embed = discord.Embed(description = translate(locale, 'queue_loop_on') if loop else translate(locale, 'queue_loop_off'), color = colors.JDH))

    @queue.command(name = 'remove')
    async def queue_remove(self, ctx: commands.Context, index: int):
        locale = get_locale(ctx.author.id)
        if index == 1:
            return await ctx.send(embed=discord.Embed(description = translate(locale, 'queue_remove_first'), color = colors.ERROR))
        if 2 <= index <= len(queue):
            queue.pop(index - 1)
            track = title_list.pop(index - 1)
            await ctx.send(embed = discord.Embed(description = f'{translate(locale, "queue_remove_success")}'.format(title = track), color = colors.JDH))
        else:
            await ctx.send(embed = discord.Embed(description = translate(locale, 'queue_remove_no_such_track'), color = colors.ERROR))

    @commands.command()
    async def resume(self, ctx: commands.Context):
        locale = get_locale(ctx.author.id)
        if not ctx.author.voice:
            return await ctx.send(embed = discord.Embed(description = f'{translate(locale, 'not_in_voice_channel')}'.format(command = 'resume'), color = colors.JDH))
        if not ctx.guild.voice_client:
            return await ctx.send(embed = discord.Embed(description = f'{translate(locale, 'not_connected')}'.format(command = 'resume'), color = colors.ERROR))
        if ctx.guild.voice_client:
            if ctx.guild.voice_client.channel != ctx.author.voice.channel:
                return await ctx.send(embed = discord.Embed(description = translate(locale, 'diff_channel'), color = colors.ERROR))
            ctx.guild.voice_client.resume()
            await ctx.send(embed = discord.Embed(description = translate(locale, 'resume_success'), color = colors.JDH))

    @commands.command(enabled = False)
    async def volume(self, ctx: commands.Context, volume: int):
        locale = get_locale(ctx.author.id)
        if 0 <= volume <= 100:
            if not ctx.author.voice:
                return await ctx.send(embed = discord.Embed(description = 'Ты должен быть в канале, чтобы использовать volume', color = colors.JDH))
            if not ctx.guild.voice_client:
                return await ctx.send(embed = discord.Embed(description = 'Я не нахожусь в канале!', color = colors.ERROR))
            if ctx.guild.voice_client:
                if ctx.guild.voice_client.channel != ctx.author.voice.channel:
                    return await ctx.send(embed = discord.Embed(description = 'Ты должен быть в том же канале, что и я!', color = colors.ERROR))
                ctx.guild.voice_client.source.volume = volume / 100
                await ctx.send(embed = discord.Embed(description = f"Громкость изменена: {volume}%", color = colors.JDH))
        else:
            await ctx.send(embed = discord.Embed(description = f'Недопустимое значение: {volume}%', color = colors.ERROR))

    @commands.command()
    async def pause(self, ctx: commands.Context):
        locale = get_locale(ctx.author.id)
        if not ctx.author.voice:
            return await ctx.send(embed = discord.Embed(description = f'{translate(locale, 'not_in_voice_channel')}'.format(command = 'pause'), color = colors.JDH))
        if not ctx.guild.voice_client:
            return await ctx.send(embed = discord.Embed(description = f'{translate(locale, 'not_connected')}'.format(command = 'pause'), color = colors.ERROR))
        if ctx.guild.voice_client:
            if ctx.guild.voice_client.channel != ctx.author.voice.channel:
                return await ctx.send(embed = discord.Embed(description = translate(locale, 'diff_channel'), color = colors.ERROR))
            ctx.guild.voice_client.pause()
            await ctx.send(embed = discord.Embed(description = translate(locale, 'pause_success'), color = colors.JDH))

    @commands.command(aliases = ['s', 'ass'])
    async def stop(self, ctx: commands.Context):
        locale = get_locale(ctx.author.id)
        if not ctx.author.voice:
            return await ctx.send(embed = discord.Embed(description = f'{translate(locale, 'not_in_voice_channel')}'.format(command = 'stop'), color = colors.JDH))
        if not ctx.guild.voice_client:
            return await ctx.send(embed = discord.Embed(description = f'{translate(locale, 'not_connected')}'.format(command = 'stop'), color = colors.ERROR))
        if ctx.guild.voice_client:
            if ctx.guild.voice_client.channel != ctx.author.voice.channel:
                return await ctx.send(embed = discord.Embed(description = translate(locale, 'diff_channel'), color = colors.ERROR))
            ctx.guild.voice_client.stop()
            queue.pop(0)
            title_list.pop(0)
            await ctx.send(embed = discord.Embed(description = translate(locale, 'stop_success'), color = colors.JDH))

    @commands.command()
    async def join(self, ctx: commands.Context):
        locale = get_locale(ctx.author.id)
        if not ctx.author.voice:
            await ctx.send(embed = discord.Embed(description = f'{translate(locale, 'not_in_voice_channel')}'.format(command = 'join'), color = colors.JDH))
        else:
            if not ctx.voice_client:
                await ctx.author.voice.channel.connect(self_deaf = True)
                return await ctx.send(embed = discord.Embed(description = f'{translate(locale, "join_success")}'.format(ctx_author_voice_channel_name = ctx.author.voice.channel.name), color = colors.JDH))
            if ctx.voice_client.channel == ctx.author.voice.channel:
                return await ctx.send(embed = discord.Embed(description = translate(locale, 'join_already_in_author_voice_channel'), color = colors.JDH))
            await ctx.send(embed = discord.Embed(description = translate(locale, 'join_already_connected'), color = colors.JDH))

    @commands.command()
    async def leave(self, ctx: commands.Context):
        locale = get_locale(ctx.author.id)
        if ctx.guild.voice_client:
            if ctx.guild.voice_client.channel == ctx.author.voice.channel:
                ctx.guild.voice_client.stop()
                await ctx.send(embed = discord.Embed(description = f'{translate(locale, "leave_success")}'.format(ctx_author_voice_channel_name = ctx.author.voice.channel.name), color = colors.JDH))
                for file in os.listdir(cwd):
                    if file.endswith(".mp3"):
                        os.remove(f'{cwd}/{file}')
                await ctx.voice_client.disconnect(force = True)
                await ctx.voice_client.clean_up()
            else:
                await ctx.send(embed = discord.Embed(description = translate(locale, 'diff_channel'), color = colors.ERROR))
        else:
            emb = discord.Embed(description = f'{translate(locale, 'not_connected')}'.format(command = 'leave'), colour = colors.ERROR)
            await ctx.send(embed = emb)

async def setup(client):
    await client.add_cog(Music(client))
