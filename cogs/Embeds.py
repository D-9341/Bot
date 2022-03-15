import asyncio

import disnake
from disnake.ext import commands

friends = [351071668241956865, 417362845303439360]

botversions = [764882153812787250, 694170281270312991, 762015251264569352]

class Embeds(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Модуль Embeds загружен')

    @commands.command()
    async def say(self, ctx, *, msg):
        title = ''
        description = ''
        image = thumbnail = message = footer = None
        embed_values = msg.split('&')
        for i in embed_values:
            if i.strip().lower().startswith('t'):
                title = i.strip()[1:].strip()
            elif i.strip().lower().startswith('d'):
                description = i.strip()[1:].strip()
            elif i.strip().lower().startswith('img'):
                image = i.strip()[3:].strip()
            elif i.strip().lower().startswith('th'):
                thumbnail = i.strip()[2:].strip()
            elif i.strip().lower().startswith('msg'):
                message = i.strip()[3:].strip()
            elif i.strip().lower().startswith('f'):
                footer = i.strip()[1:].strip()
        emb = disnake.Embed(title = title, description = description, color = 0x2f3136)
        for i in embed_values:
            emb.set_author(name = ctx.author, icon_url = ctx.author.avatar.url)
            if image:
                emb.set_image(url = image)
            if thumbnail:
                emb.set_thumbnail(url = thumbnail)
            if footer:
                emb.set_footer(text = footer)
            if 't' not in msg and 'd' not in msg and 'img' not in msg and 'th' not in msg and 'msg' not in msg and 'f' not in msg:
                await ctx.send(msg)
            else:
                if message:
                    return await ctx.send(f'{message}', embed = emb)
                else:
                    return await ctx.send(embed = emb)

    @commands.command()
    async def edit(self, ctx, arg, *, msg = None):
        message = await ctx.fetch_message(arg)
        if message != None:
            old_embed = message.embeds[0]
            title = old_embed.title
            description = old_embed.description
            image = thumbnail = footer = None
            embed_values = msg.split('&')
            for i in embed_values:
                if i.strip().lower().startswith('t'):
                    title = i.strip()[1:].strip()
                elif i.strip().lower().startswith('d'):
                    description = i.strip()[1:].strip()
                elif i.strip().lower().startswith('img'):
                    image = i.strip()[3:].strip()
                elif i.strip().lower().startswith('th'):
                    thumbnail = i.strip()[2:].strip()
                elif i.strip().lower().startswith('f'):
                    footer = i.strip()[1:].strip()
            emb = disnake.Embed(title = title, description = description, color = 0x2f3136, timestamp = disnake.utils.utcnow())
            for i in embed_values:
                emb.set_author(name = ctx.author, icon_url = ctx.author.avatar.url)
                if image:
                    emb.set_image(url = image)
                if thumbnail:
                    emb.set_thumbnail(url = thumbnail)
                if footer:
                    emb.set_footer(text = footer)
                if 't' not in msg and 'd' not in msg and 'img' not in msg and 'th' not in msg and 'f' not in msg:
                    if message.author == self.client.user:
                        if '--clean' in msg:
                            await message.edit(content = None)
                        if '--delete' in msg:
                            await message.delete()
                        else:
                            await message.edit(content = msg)
                    else:
                        return await ctx.send(f'{message.id} не является сообщением от {self.client.user}')
                else:
                    if message.author == self.client.user:
                        if '--clean' in msg:
                            await message.edit(content = None, embed = emb)
                        if '--noembed' in msg:
                            if message.embeds != []:
                                await message.edit(embed = None)
                            else:
                                return await ctx.send(f'{ctx.author.mention}, нечего удалять. Возможно, вы имели ввиду cy/edit {message.id} --delete ?', delete_after = 5)
                        else:
                            await message.edit(embed = emb)
                    else:
                        return await ctx.send(f'{message.id} не является сообщением от {self.client.user}')
        else:
            await ctx.send(f'сообщение {message.id} не обнаружено.')

    @commands.command(aliases = ['ctx'])
    async def content(self, ctx, arg, channel: disnake.TextChannel = None):
        if channel == None:
            channel = ctx.message.channel
        message = await channel.fetch_message(arg)
        for emb in message.embeds:
            if emb.color != emb.Empty:
                color = f' color {emb.color}'
            else:
                color = ''
            if emb.author.name != emb.Empty:
                author = f' author {emb.author.name}'
            else:
                author = ''
            if message.content == '':
                content = ''
            else:
                content = f'content {message.content}'
            if emb.image.url != emb.Empty:
                img = f' &img {emb.image.url}'
                image = f' image {emb.image.url}'
            else:
                img = ''
                image = ''
            if emb.thumbnail.url != emb.Empty:
                th = f' &th {emb.thumbnail.url}'
                thumb = f' thumbnail {emb.thumbnail.url}'
            else:
                th = ''
                thumb = ''
            if emb.description != emb.Empty:
                d = f' &d {emb.description}'
                description = f' description {emb.description}'
            else:
                d = ''
                description = ''
            if emb.title != emb.Empty:
                t = f'&t {emb.title}'
                title = f' title {emb.title}'
            else:
                t = ''
                title = ''
            if emb.footer.text != emb.Empty:
                f = f' &f {emb.footer.text}'
                footer = f' footer {emb.footer.text}'
            else:
                f = ''
                footer = ''
        if message.author.id in botversions:
            if message.embeds == []:
                await ctx.send(f'```cy/say {message.content}```')
            else:
                await ctx.send(f'```cy/say {t}{d}{f}{th}{img}```')
        else:
            if message.embeds == []:
                if '```' in message.content:
                    await ctx.send(f'@{message.author} {message.content}')
                else:
                    await ctx.send(f'```@{message.author} {message.content}```')
            else:
                await ctx.send(f'```{content}{title}{description}{footer}{color}{author}{image}{thumb}```')

def setup(client):
    client.add_cog(Embeds(client))
