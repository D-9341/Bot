import asyncio
import os
import json

import discord
from discord.ext import commands
from gtts import gTTS

from cogs.Constants import colors
from functions import get_locale, translate
from main import CWD

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
        self._queue = []
        self._title_list = []
        self._loop = False
        self.temp_dir = CWD / "temp"
        self.temp_dir.mkdir(exist_ok = True)

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
            video_id = None
            if 'youtube.com/watch?v=' in url:
                video_id = url.split('v=')[1].split('&')[0]
            elif 'youtu.be/' in url:
                video_id = url.split('youtu.be/')[1].split('?')[0]
            if not video_id or len(video_id) != 11:
                video_id = url[-11:] if len(url) >= 11 else 'unknown'
            audio = self.temp_dir / f'{video_id}.mp3'
            if audio.exists():
                cmd = ['yt-dlp', '--js-runtimes', 'node', '--skip-download', '--dump-json', '--quiet', '--no-warnings', url]
                process = await asyncio.create_subprocess_exec(*cmd, stdout = asyncio.subprocess.PIPE, stderr = asyncio.subprocess.PIPE)
                stdout, stderr = await process.communicate()
                if process.returncode == 0:
                    info = json.loads(stdout.decode('utf-8'))
                    title = info['title']
                    duration = info.get('duration_string', 'N/A')
                else:
                    title = f"Video {video_id}"
                    duration = "N/A"
            else:
                await ctx.send(embed = discord.Embed(description = translate(locale, "play_downloading", url = url), color = colors.JDH))
                cmd = ['yt-dlp', '--js-runtimes', 'node', '-x', '--audio-format', 'mp3', '--audio-quality', '320K', '--output', str(self.temp_dir / '%(id)s.%(ext)s'), '--quiet', '--no-warnings', url]
                process = await asyncio.create_subprocess_exec(*cmd, stdout = asyncio.subprocess.PIPE, stderr = asyncio.subprocess.PIPE)
                stdout, stderr = await process.communicate()
                if process.returncode != 0:
                    error_msg = stderr.decode('utf-8', errors = 'ignore')
                    if "Sign in to confirm your age" in error_msg:
                        return await ctx.send(embed = discord.Embed(description = translate(locale, 'play_video_age_restricted'), color = colors.ERROR))
                    if "This video contains content from" in error_msg:
                        return await ctx.send(embed = discord.Embed(description = translate(locale, 'play_video_country_restricted'), color = colors.ERROR))
                    if "unavailable" in error_msg.lower() or "timeout" in error_msg.lower():
                        return await ctx.send(embed = discord.Embed(description = translate(locale, 'play_video_downloading_error'), color = colors.ERROR))
                    raise Exception(f"Download failed: {error_msg[:200]}")
                cmd = ['yt-dlp', '--skip-download', '--dump-json', '--quiet', url]
                process = await asyncio.create_subprocess_exec(*cmd, stdout = asyncio.subprocess.PIPE, stderr = asyncio.subprocess.PIPE)
                stdout, stderr = await process.communicate()
                if process.returncode == 0:
                    info = json.loads(stdout.decode('utf-8'))
                    title = info['title']
                    duration = info.get('duration_string', 'N/A')
                else:
                    title = f"Video {video_id}"
                    duration = "N/A"
                
                if not audio.exists():
                    for file in self.temp_dir.glob(f"*{video_id}*.mp3"):
                        audio = file
                        break

        except Exception as error:
            error_str = str(error)
            if "Sign in to confirm your age" in error_str:
                return await ctx.send(embed = discord.Embed(description = translate(locale, 'play_video_age_restricted'), color = colors.ERROR))
            if "This video contains content from" in error_str:
                return await ctx.send(embed = discord.Embed(description = translate(locale, 'play_video_country_restricted'), color = colors.ERROR))
            if "Remote end closed connection" in error_str or "The read operation timed out" in error_str:
                return await ctx.send(embed = discord.Embed(description = translate(locale, 'play_video_downloading_error'), color = colors.ERROR))
            return await ctx.send(embed = discord.Embed(description = translate(locale, "play_video_unknown_error", error = error), color = colors.ERROR))
        
        self._queue.append(str(audio))
        self._title_list.append(title)
        await ctx.send(embed = discord.Embed(description = translate(locale, "play_added_to_queue", title = title, pos = len(self._queue)), color = colors.JDH))

        if not ctx.author.voice:
            return await ctx.send(embed = discord.Embed(description = translate(locale, 'not_in_voice_channel', command = ctx.command.name), color = colors.JDH))
        if not ctx.guild.voice_client:
            await ctx.author.voice.channel.connect(self_deaf = True)
            await ctx.send(embed = discord.Embed(description = translate(locale, "play_connected", ctx_author_voice_channel_name = ctx.author.voice.channel.name), color = colors.JDH))
        if ctx.guild.voice_client:
            if ctx.guild.voice_client.channel != ctx.author.voice.channel:
                return await ctx.send(embed = discord.Embed(description = translate(locale, 'play_already_in_use'), color = colors.ERROR))
            
            while self._queue:
                if not ctx.guild.voice_client.is_playing():
                    ffmpeg_options = {'options': '-vn -b:a 320k'}
                    ctx.voice_client.play(discord.FFmpegPCMAudio(self._queue[0], **ffmpeg_options))
                    await ctx.send(embed = discord.Embed(description = translate(locale, 'play_now_playing', player_title = self._title_list[0], player_url = url, player_duration = duration), color = colors.JDH))

                while ctx.voice_client.is_playing():
                    await asyncio.sleep(1)

                if not self._loop:
                    self._queue.pop(0)
                    self._title_list.pop(0)

    @commands.group(aliases = ['q'], invoke_without_command = True)
    async def queue(self, ctx: commands.Context):
        locale = get_locale(ctx.author.id)
        queue_display = [f'{index + 1}. {title}' for index, title in enumerate(self._title_list)]
        await ctx.send(embed = discord.Embed(description = translate(locale, "queue_list", queue_list = '\n'.join(queue_display)) if self._title_list else translate(locale, 'queue_empty'), color = colors.JDH))

    @queue.command(name = 'clear')
    async def queue_clear(self, ctx: commands.Context):
        locale = get_locale(ctx.author.id)
        self._title_list.clear(); self._queue.clear()
        if ctx.guild.voice_client:
            ctx.guild.voice_client.stop()
        await ctx.send(embed = discord.Embed(description = translate(locale, 'queue_clear'), color = colors.JDH))

    @queue.command(aliases = ['next', 'skip'])
    async def queue_skip(self, ctx: commands.Context):
        locale = get_locale(ctx.author.id)
        if len(self._queue) > 1:
            ctx.guild.voice_client.stop()
            self._queue.pop(0)
            self._title_list.pop(0)
            ctx.guild.voice_client.play(discord.FFmpegPCMAudio(self._queue[0], **{'options': '-vn'}))
            await ctx.send(embed = discord.Embed(description = translate(locale, "queue_skip", title = self._title_list[0]), color = colors.JDH))
        else:
            await ctx.send(embed = discord.Embed(description = translate(locale, 'queue_skip_empty'), color = colors.JDH))

    @queue.command(name = 'loop')
    async def queue_loop(self, ctx: commands.Context, action: str = 'toggle'):
        locale = get_locale(ctx.author.id)
        if action != 'status':
            self._loop = not self._loop
        await ctx.send(embed = discord.Embed(description = translate(locale, 'queue_loop_on') if self._loop else translate(locale, 'queue_loop_off'), color = colors.JDH))

    @queue.command(name = 'remove')
    async def queue_remove(self, ctx: commands.Context, index: int):
        locale = get_locale(ctx.author.id)
        if index == 1:
            return await self.queue_skip(ctx)
        if 2 <= index <= len(self._queue):
            self._queue.pop(index - 1)
            track = self._title_list.pop(index - 1)
            await ctx.send(embed = discord.Embed(description = translate(locale, "queue_remove_success", title = track), color = colors.JDH))
        else:
            await ctx.send(embed = discord.Embed(description = translate(locale, 'queue_remove_no_such_track'), color = colors.ERROR))

    @commands.command()
    async def resume(self, ctx: commands.Context):
        locale = get_locale(ctx.author.id)
        if not ctx.author.voice:
            return await ctx.send(embed = discord.Embed(description = translate(locale, 'not_in_voice_channel', command = ctx.command.name), color = colors.JDH))
        if not ctx.guild.voice_client:
            return await ctx.send(embed = discord.Embed(description = translate(locale, 'not_connected', command = ctx.command.name), color = colors.ERROR))
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
            return await ctx.send(embed = discord.Embed(description = translate(locale, 'not_in_voice_channel', command = ctx.command.name), color = colors.JDH))
        if not ctx.guild.voice_client:
            return await ctx.send(embed = discord.Embed(description = translate(locale, 'not_connected', command = ctx.command.name), color = colors.ERROR))
        if ctx.guild.voice_client:
            if ctx.guild.voice_client.channel != ctx.author.voice.channel:
                return await ctx.send(embed = discord.Embed(description = translate(locale, 'diff_channel'), color = colors.ERROR))
            ctx.guild.voice_client.pause()
            await ctx.send(embed = discord.Embed(description = translate(locale, 'pause_success'), color = colors.JDH))

    @commands.command(aliases = ['s', 'ass'])
    async def stop(self, ctx: commands.Context):
        locale = get_locale(ctx.author.id)
        if not ctx.author.voice:
            return await ctx.send(embed = discord.Embed(description = translate(locale, 'not_in_voice_channel', command = ctx.command.name), color = colors.JDH))
        if not ctx.guild.voice_client:
            return await ctx.send(embed = discord.Embed(description = translate(locale, 'not_connected', command = ctx.command.name), color = colors.ERROR))
        if ctx.guild.voice_client:
            if ctx.guild.voice_client.channel != ctx.author.voice.channel:
                return await ctx.send(embed = discord.Embed(description = translate(locale, 'diff_channel'), color = colors.ERROR))
            ctx.guild.voice_client.stop()
            self._queue.pop(0)
            self._title_list.pop(0)
            await ctx.send(embed = discord.Embed(description = translate(locale, 'stop_success'), color = colors.JDH))

    @commands.command()
    async def join(self, ctx: commands.Context):
        locale = get_locale(ctx.author.id)
        if not ctx.author.voice:
            await ctx.send(embed = discord.Embed(description = translate(locale, 'not_in_voice_channel', command = ctx.command.name), color = colors.JDH))
        else:
            if not ctx.voice_client:
                await ctx.author.voice.channel.connect(self_deaf = True)
                return await ctx.send(embed = discord.Embed(description = translate(locale, "join_success", ctx_author_voice_channel_name = ctx.author.voice.channel.name), color = colors.JDH))
            if ctx.voice_client.channel == ctx.author.voice.channel:
                return await ctx.send(embed = discord.Embed(description = translate(locale, 'join_already_in_author_voice_channel'), color = colors.JDH))
            await ctx.send(embed = discord.Embed(description = translate(locale, 'join_already_connected'), color = colors.JDH))

    @commands.command()
    async def leave(self, ctx: commands.Context):
        locale = get_locale(ctx.author.id)
        if ctx.guild.voice_client:
            if ctx.guild.voice_client.channel == ctx.author.voice.channel:
                ctx.guild.voice_client.stop()
                await ctx.send(embed = discord.Embed(description = translate(locale, "leave_success", ctx_author_voice_channel_name = ctx.author.voice.channel.name), color = colors.JDH))
                for file in os.listdir(CWD / 'temp'):
                    if file.endswith(".mp3"):
                        os.remove(CWD / f'temp/{file}')
                await ctx.voice_client.disconnect(force = True)
            else:
                await ctx.send(embed = discord.Embed(description = translate(locale, 'diff_channel'), color = colors.ERROR))
        else:
            emb = discord.Embed(description = translate(locale, 'not_connected', command = ctx.command.name), colour = colors.ERROR)
            await ctx.send(embed = emb)

async def setup(client):
    await client.add_cog(Music(client))
