import asyncio
import datetime

import discord
import discord_slash
from discord.ext import commands
from discord_slash import cog_ext as slash

friends = [351071668241956865, 417362845303439360]

botversions = [764882153812787250, 694170281270312991, 762015251264569352]

class sEmbeds(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Группа Slash-команд Embeds загружена')

    @slash.cog_slash(name = 'content', description = 'Позволяет получить необработанный контент сообщения, в том числе и эмбедов', options = [{'name': 'arg', 'description': 'ID сообщения', 'required': True, 'type': 3}, {'name': 'channel', 'description': 'Канал, из которого нужно достать сообщение', 'required': False, 'type': 7}, {'name': 'to_dict', 'description': 'Должен ли контент вывестись в словарь? Работает только в сообщениях у которых есть эмбед', 'required': False, 'type': 5}])
    async def _content(self, ctx, arg, channel: discord.TextChannel = None, to_dict: bool = None):
        if channel == None:
            channel = ctx.channel
        message = await channel.fetch_message(id = arg)
        if not message:
            await ctx.send(f'Сообщение {arg} не найдено.')
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
                img = f' | img& {emb.image.url}'
                image = f' image {emb.image.url}'
            else:
                img = ''
                image = ''
            if emb.thumbnail.url != emb.Empty:
                th = f' | th& {emb.thumbnail.url}'
                thumb = f' thumbnail {emb.thumbnail.url}'
            else:
                th = ''
                thumb = ''
            if emb.description != emb.Empty:
                d = f' | d& {emb.description}'
                description = f' description {emb.description}'
            else:
                d = ''
                description = ''
            if emb.title != emb.Empty:
                t = f't& {emb.title}'
                title = f' title {emb.title}'
            else:
                t = ''
                title = ''
            if emb.footer.text != emb.Empty:
                f = f' | f& {emb.footer.text}'
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

    @slash.cog_slash(name = 'edit', description = 'Изменяет сообщение, отправленое ботом.', options = [{'name': 'arg', 'description': 'ID сообщения', 'required': True, 'type': 3}, {'name': 'msg', 'description': 'аргументы или текст, на который нужно заменить исходный', 'required': True, 'type': 3}])
    @commands.has_permissions(manage_messages = True)
    async def _edit(self, ctx, arg, *, msg):
        message = await ctx.channel.fetch_message(id = arg)
        if message != None:
            title = ''
            description = ''
            image = thumbnail = footer = None
            embed_values = msg.split('|')
            for i in embed_values:
                if i.strip().lower().startswith('t&'):
                    title = i.strip()[2:].strip()
                elif i.strip().lower().startswith('d&'):
                    description = i.strip()[2:].strip()
                elif i.strip().lower().startswith('img&'):
                    image = i.strip()[4:].strip()
                elif i.strip().lower().startswith('th&'):
                    thumbnail = i.strip()[3:].strip()
                elif i.strip().lower().startswith('f&'):
                    footer = i.strip()[2:].strip()
            emb = discord.Embed(title = title, description = description, color = 0x2f3136, timestamp = datetime.datetime.utcnow())
            for i in embed_values:
                emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                if image:
                    emb.set_image(url = image)
                if thumbnail:
                    emb.set_thumbnail(url = thumbnail)
                if footer:
                    emb.set_footer(text = footer)
                if 't&' not in msg and 'd&' not in msg and 'img&' not in msg and 'th&' not in msg and 'c&' not in msg:
                    if message.author == self.client.user:
                        if '--clean' in msg:
                            return await message.edit(content = None)
                        if '--delete' in msg:
                            return await message.delete()
                        if '--noembed' in msg:
                            if message.embeds != []:
                                return await message.edit(embed = None)
                            else:
                                return await ctx.send(f'{ctx.author.mention}, нечего удалять. Возможно, вы имели ввиду cy/edit {message.id} --delete ?')
                        if '--empty-embed' in msg:
                            if message.embeds != []:
                                emb = discord.Embed(title = None, description = None, color = ctx.author.color)
                                emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                                return await message.edit(embed = emb)
                            else:
                                return await ctx.send(f'{ctx.author.mention}, нечего очищать. Возможно, вы имели ввиду cy/edit {message.id} --delete ?')
                        else:
                            return await message.edit(content = msg)
                    else:
                        return await ctx.send(f'{message.id} не является сообщением от {self.client.user}')
                else:
                    if message.author == self.client.user:
                        if '--clean' in msg:
                            return await message.edit(content = None, embed = emb)
                        if '--noembed' in msg:
                            if message.embeds != []:
                                await message.edit(embed = None)
                            else:
                                return await ctx.send(f'{ctx.author.mention}, нечего удалять. Возможно, вы имели ввиду cy/edit {message.id} --delete ?')
                        else:
                            await message.edit(embed = emb)
                    else:
                        return await ctx.send(f'{message.id} не является сообщением от {self.client.user}')
        else:
            await ctx.send(f'сообщение {message.id} не обнаружено.')

    @slash.cog_slash(name = 'say', description = 'Пишет от лица бота сообщение или эмбед. Используйте cy/help say для подробностей использования.', options = [{'name': 'msg', 'description': 'Аргументы/текст для написания', 'required': True, 'type': 3}])
    async def _say(self, ctx, *, msg):
        title = ''
        description = ''
        image = thumbnail = message = footer = None
        embed_values = msg.split('|')
        for i in embed_values:
            if i.strip().lower().startswith('t&'):
                title = i.strip()[2:].strip()
            elif i.strip().lower().startswith('d&'):
                description = i.strip()[2:].strip()
            elif i.strip().lower().startswith('img&'):
                image = i.strip()[4:].strip()
            elif i.strip().lower().startswith('th&'):
                thumbnail = i.strip()[3:].strip()
            elif i.strip().lower().startswith('msg&'):
                message = i.strip()[4:].strip()
            elif i.strip().lower().startswith('f&'):
                footer = i.strip()[2:].strip()
        emb = discord.Embed(title = title, description = description, color = 0x2f3136)
        for i in embed_values:
            emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            if image:
                emb.set_image(url = image)
            if thumbnail:
                emb.set_thumbnail(url = thumbnail)
            if footer:
                emb.set_footer(text = footer)
            if ctx.guild.owner.id != self.client.owner_id and ctx.guild.owner.id not in friends:
                emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
            if 't&' not in msg and 'd&' not in msg and 'img&' not in msg and 'th&' not in msg and 'msg&' not in msg and 'f&' not in msg:
                return await ctx.send(msg)
            else:
                if message:
                    return await ctx.send(f'{message}', embed = emb)
                else:
                    return await ctx.send(embed = emb)

def setup(client):
    client.add_cog(sEmbeds(client))
