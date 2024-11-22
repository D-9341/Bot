import asyncio

import discord
import yt_dlp
import os
from pathlib import Path
from functions import translate, get_locale
from discord.ext import commands
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
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Модуль Music загружен')

    @commands.command(aliases = ['p'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def play(self, ctx, *, url):
        locale = get_locale(ctx.author.id)
        url = url.lstrip('<').rstrip('>')
        try:
            if os.path.exists(f'{cwd}\{url[-11:]}.mp3'):
                audio = os.path.join(cwd, f'{url[-11:]}.mp3')
                info = await self.client.loop.run_in_executor(None, lambda: yt_dlp.YoutubeDL(ydl_opts).extract_info(url, download = False))
                title = info['title']
                duration = info['duration_string']
            else:
                await ctx.send(embed = discord.Embed(description = f'{translate(locale, "play_downloading")}'.format(url = url), color = 0xff8000))
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
                return await ctx.send(embed = discord.Embed(description = translate(locale, 'play_video_age_restricted'), color = 0xff0000))
            if "This video contains content from" in str(error):
                return await ctx.send(embed = discord.Embed(description = translate(locale, 'play_video_country_restricted'), color = 0xff0000))
            if "Remote end closed connection" in str(error) or "The read operation timed out" in str(error):
                return await ctx.send(embed = discord.Embed(description = translate(locale, 'play_video_downloading_error'), color = 0xff0000))
            return await ctx.send(embed = discord.Embed(description = f'{translate(locale, "play_video_unknown_error")}'.format(error = error), color = 0xff0000))
        queue.append(audio)
        title_list.append(title)
        await ctx.send(embed = discord.Embed(description = f'{translate(locale, "play_added_to_queue")}'.format(title = title, pos = len(queue)), color = 0xff8000))
        if not ctx.author.voice:
            return await ctx.send(embed = discord.Embed(description = translate(locale, 'play_not_in_voice_channel'), color = 0xff8000))
        if not ctx.guild.voice_client:
            await ctx.author.voice.channel.connect(self_deaf = True)
            await ctx.send(embed = discord.Embed(description = f'{translate(locale, "play_connected")}'.format(ctx_author_voice_channel_name = ctx.author.voice.channel.name), color = 0xff8000))
        if ctx.guild.voice_client:
            if ctx.guild.voice_client.channel != ctx.author.voice.channel:
                return await ctx.send(embed = discord.Embed(description = translate(locale, 'play_already_in_use'), color = 0xff0000))
            while queue:
                if not ctx.guild.voice_client.is_playing():
                    ctx.voice_client.play(discord.FFmpegPCMAudio(queue[0], **{'options': '-vn'}))
                    await ctx.send(embed = discord.Embed(description = f"{translate(locale, 'play_now_playing')}".format(player_title = title_list[0], player_url = url, player_duration = duration), color = 0xff8000))
                while ctx.voice_client.is_playing():
                    await asyncio.sleep(1)
                if not loop:
                    queue.pop(0)
                    title_list.pop(0)

    @commands.command(aliases = ['q'])
    async def queue(self, ctx, argument = 'list', *, action: int | str = 0):
        locale = get_locale(ctx.author.id)
        if argument == 'list':
            queue_display = [f'{index + 1}. {title}' for index, title in enumerate(title_list)]
            await ctx.send(embed = discord.Embed(description = f'{translate(locale, "queue_list")}'.format(queue_list = '\n'.join(queue_display)) if title_list else translate(locale, 'queue_empty'), color = 0xff8000))
        if argument == 'clear':
            title_list.clear(); queue.clear()
            if ctx.guild.voice_client:
                ctx.guild.voice_client.stop()
            await ctx.send(embed = discord.Embed(description = translate(locale, 'queue_clear'), color = 0xff8000))
        if argument in ['next', 'skip']:
            if len(queue) > 1:
                ctx.guild.voice_client.stop()
                queue.pop(0)
                title_list.pop(0)
                ctx.guild.voice_client.play(discord.FFmpegPCMAudio(queue[0], **{'options': '-vn'}))
                await ctx.send(embed = discord.Embed(description = f'{translate(locale, "queue_next")}'.format(title = title_list[0]), color = 0xff8000))
            else:
                await ctx.send(embed = discord.Embed(description = translate(locale, 'queue_skip_empty'), color = 0xff8000))
        if argument == 'loop':
            global loop
            if action != 'status':
                loop = not loop
            await ctx.send(embed = discord.Embed(description = translate(locale, 'queue_loop_on') if loop else translate(locale, 'queue_loop_off'), color = 0xff8000))
        if argument == 'remove':
            if action == 1:
                return await ctx.send(embed = discord.Embed(description = translate(locale, 'queue_remove_first'), color = 0xff8000))
            if 2 <= action <= len(queue):
                queue.pop(action - 1)
                track = title_list.pop(action - 1)
                await ctx.send(embed = discord.Embed(description = f'{translate(locale, "queue_remove_success")}'.format(title = track), color = 0xff8000))
            else:
                await ctx.send(embed = discord.Embed(description = translate(locale, 'queue_remove_no_such_track'), color = 0xff8000))

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
            queue.pop(0)
            title_list.pop(0)
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
                ctx.guild.voice_client.stop()
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
