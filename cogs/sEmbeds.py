import asyncio
import datetime

import disnake
from disnake.ext import commands

friends = [351071668241956865, 417362845303439360]

botversions = [764882153812787250, 694170281270312991, 762015251264569352]

class sEmbeds(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Группа Slash-команд Embeds загружена')

    @commands.slash_command(name = 'content')
    async def _content(self, inter, arg, channel: disnake.TextChannel = None):
        '''Позволяет получить необработанный контент сообщения, в том числе и эмбедов
        Parameters
        ----------
        arg:
            ID сообщения
        amount: :class:`disnake.TextChannel`
            Канал
        '''
        if channel == None:
            channel = inter.channel
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
                await inter.response.send_message(f'```cy/say {message.content}```')
            else:
                await inter.response.send_message(f'```cy/say {t}{d}{f}{th}{img}```')
        else:
            if message.embeds == []:
                if '```' in message.content:
                    await inter.response.send_message(f'@{message.author} {message.content}')
                else:
                    await inter.response.send_message(f'```@{message.author} {message.content}```')
            else:
                await inter.response.send_message(f'```{content}{title}{description}{footer}{color}{author}{image}{thumb}```')

    @commands.slash_command(name = 'edit')
    @commands.has_permissions(manage_messages = True)
    async def _edit(self, inter, arg, *, msg: str):
        '''Изменяет сообщение, отправленое ботом.
        Parameters
        ----------
        arg:
            ID сообщения
        msg: class: `str`
            Новый текст/аргументы для вывода эмбеда
        '''
        message = await inter.channel.fetch_message(arg)
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
            color = 0x2f3136
            emb = disnake.Embed(title = title, description = description, color = color, timestamp = disnake.utils.utcnow())
            for i in embed_values:
                emb.set_author(name = inter.author, icon_url = inter.author.avatar.url)
                if image:
                    emb.set_image(url = image)
                if thumbnail:
                    emb.set_thumbnail(url = thumbnail)
                if footer:
                    emb.set_footer(text = footer)
                if 't&' not in msg and 'd&' not in msg and 'img&' not in msg and 'th&' not in msg and 'f&' not in msg:
                    if message.author == self.client.user:
                        if '--clean' in msg:
                            await message.edit(content = None)
                        if '--delete' in msg:
                            await message.delete()
                        if '--noembed' in msg:
                            if message.embeds != []:
                                await message.edit(embed = None)
                            else:
                                return await inter.response.send_message(f'{inter.author.mention}, нечего удалять. Возможно, вы имели ввиду cy/edit {message.id} --delete ?')
                        if '--empty-embed' in msg:
                            if message.embeds != []:
                                emb = disnake.Embed(title = None, description = None, color = 0x2f3136)
                                emb.set_author(name = inter.author, icon_url = inter.author.avatar.url)
                                await message.edit(embed = emb)
                            else:
                                return await inter.response.send_message(f'{inter.author.mention}, нечего очищать. Возможно, вы имели ввиду cy/edit {message.id} --delete ?')
                        else:
                            await message.edit(content = msg)
                    else:
                        return await inter.response.send_message(f'{message.id} не является сообщением от {self.client.user}')
                else:
                    if message.author == self.client.user:
                        if '--clean' in msg:
                            await message.edit(content = None, embed = emb)
                        if '--noembed' in msg:
                            if message.embeds != []:
                                await message.edit(embed = None)
                            else:
                                return await inter.response.send_message(f'{inter.author.mention}, нечего удалять. Возможно, вы имели ввиду cy/edit {message.id} --delete ?')
                        else:
                            await message.edit(embed = emb)
                    else:
                        return await inter.response.send_message(f'{message.id} не является сообщением от {self.client.user}')
        else:
            await inter.response.send_message(f'сообщение {message.id} не обнаружено.')

    @commands.slash_command(name = 'say', description = 'Пишет от лица бота сообщение или эмбед. Используйте cy/help say для подробностей использования.')
    async def _say(self, inter, *, msg: str):
        '''        
        Parameters
        ----------
        msg: :class: `str`
            Текст/аргументы для вывода эмбеда
        '''
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
        emb = disnake.Embed(title = title, description = description, color = 0x2f3136)
        for i in embed_values:
            emb.set_author(name = inter.author, icon_url = inter.author.avatar.url)
            if image:
                emb.set_image(url = image)
            if thumbnail:
                emb.set_thumbnail(url = thumbnail)
            if footer:
                emb.set_footer(text = footer)
            if 't&' not in msg and 'd&' not in msg and 'img&' not in msg and 'th&' not in msg and 'msg&' not in msg and 'f&' not in msg:
                return await inter.response.send_message(msg)
            else:
                if message:
                    return await inter.response.send_message(f'{message}', embed = emb)
                else:
                    return await inter.response.send_message(embed = emb)

def setup(client):
    client.add_cog(sEmbeds(client))
