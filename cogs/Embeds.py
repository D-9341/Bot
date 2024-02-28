import discord
from discord.ext import commands

botversions = [764882153812787250, 694170281270312991, 762015251264569352]

class Embeds(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Модуль Embeds загружен')

    @commands.command()
    async def say(self, ctx, *, msg):
        title = description = ''
        image = thumbnail = message = footer = color = None
        embed_values = msg.split('&')
        for i in embed_values:
            if i.strip().lower().startswith('th'):
                thumbnail = i.strip()[2:].strip()
            elif i.strip().lower().startswith('d'):
                description = i.strip()[1:].strip()
            elif i.strip().lower().startswith('c'):
                color = i.strip()[1:].strip()
            elif i.strip().lower().startswith('img'):
                image = i.strip()[3:].strip()
            elif i.strip().lower().startswith('t'):
                title = i.strip()[1:].strip()
            elif i.strip().lower().startswith('msg'):
                message = i.strip()[3:].strip()
            elif i.strip().lower().startswith('f'):
                footer = i.strip()[1:].strip()
        if color is None:
            color = 0x2f3136
        else:
            if '#' not in color:
                color = int('0x' + color, 16)
            else:
                color = int('0x' + color.lstrip('#'), 16)
        emb = discord.Embed(title = title, description = description, color = color)
        for i in embed_values:
            emb.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar.url)
            if image:
                emb.set_image(url = image)
            if thumbnail:
                emb.set_thumbnail(url = thumbnail)
            if footer:
                emb.set_footer(text = footer)
            if not any(keyword in msg for keyword in ['&t', '&d', '&img', '&th', '&msg', '&f', '&c']):
                return await ctx.send(msg)
            else:
                if message:
                    return await ctx.send(f'{message}', embed = emb)
                else:
                    return await ctx.send(embed = emb)

    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def edit(self, ctx, arg, *, msg = None):
        message = await ctx.channel.fetch_message(arg)
        if not any(keyword in msg for keyword in ['&t', '&d', '&img', '&th', '&f', '&c']):
            if message.author == self.client.user:
                if '--delete' in msg:
                    await message.delete()
                    return await ctx.send('Сообщение удалено')
                if '--clean' in msg:
                    return await message.edit(content = None)
                if '--noembed' in msg:
                    if message.embeds != []:
                        await message.edit(embed = None)
                    else:
                        return await ctx.send(embed = discord.Embed(description = f'{ctx.author.mention}, нечего удалять. Возможно, вы имели ввиду cy/edit {message.id} --delete', color = 0xff8000))
                else:
                    return await message.edit(content = msg)
            else:
                return await ctx.send(embed = discord.Embed(description = f'{message.id} не является сообщением от {self.client.user.mention}', color = 0xff0000))
        else:
            if message.embeds != []:
                old_embed = message.embeds[0]
                title = old_embed.title
                description = old_embed.description
                color = old_embed.color
            else:
                title = description = ''
                color = None
            image = thumbnail = footer = None
            embed_values = msg.split('&')
            for i in embed_values:
                if i.strip().lower().startswith('th'):
                    thumbnail = i.strip()[2:].strip()
                elif i.strip().lower().startswith('d'):
                    description = i.strip()[1:].strip()
                elif i.strip().lower().startswith('c'):
                    color = i.strip()[1:].strip()
                elif i.strip().lower().startswith('img'):
                    image = i.strip()[3:].strip()
                elif i.strip().lower().startswith('t'):
                    title = i.strip()[1:].strip()
                elif i.strip().lower().startswith('f'):
                    footer = i.strip()[1:].strip()
            if message.embeds == [] or color is None:
                color = 0x2f3136
            elif message.embeds != [] and '&c' not in msg:
                color = message.embeds[0].color
            else:
                if '#' not in color:
                    color = int('0x' + color, 16)
                else:
                    color = int('0x' + color.lstrip('#'), 16)
            emb = discord.Embed(title = title, description = description, color = color, timestamp = discord.utils.utcnow())
            emb.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar.url)
            if image:
                emb.set_image(url = image)
            if thumbnail:
                emb.set_thumbnail(url = thumbnail)
            if footer:
                emb.set_footer(text = footer)
            if message.author == self.client.user:
                if '--delete' in msg:
                    await message.delete()
                    return await ctx.send('Сообщение удалено')
                if '--clean' in msg:
                    return await message.edit(content = None, embed = emb)
                if '--noembed' in msg:
                    if message.embeds != []:
                        return await message.edit(embed = None)
                    else:
                        return await ctx.send(embed = discord.Embed(description = f'{ctx.author.mention}, нечего удалять. Возможно, вы имели ввиду cy/edit {message.id} --delete', color = 0xff8000))
                else:
                    return await message.edit(embed = emb)
            else:
                return await ctx.send(embed = discord.Embed(description = f'{message.id} не является сообщением от {self.client.user.mention}', color = 0xff8000))

    @commands.command(aliases = ['ctx'])
    async def content(self, ctx, arg, channel: discord.TextChannel = None, should_be_edit = None):
        if channel is None:
            channel = ctx.channel
        message = await channel.fetch_message(arg)
        for emb in message.embeds:
            if emb.color is not None:
                color = f' color {emb.color}'
                c = f' &c {emb.color}'
            else:
                color = c = ''
            if emb.author.name is not None:
                author = f' author {emb.author.name}'
            else:
                author = ''
            if message.content == '':
                content = ''
            else:
                content = f'content {message.content}'
            if emb.image.url is not None:
                img = f' &img {emb.image.url}'
                image = f' image {emb.image.url}'
            else:
                img = image = ''
            if emb.thumbnail.url is not None:
                th = f' &th {emb.thumbnail.url}'
                thumb = f' thumbnail {emb.thumbnail.url}'
            else:
                th = thumb = ''
            if emb.description is not None:
                d = f' &d {emb.description}'
                description = f' description {emb.description}'
            else:
                d = description = ''
            if emb.title is not None:
                t = f'&t {emb.title}'
                title = f' title {emb.title}'
            else:
                t = title = ''
            if emb.footer.text is not None:
                f = f' &f {emb.footer.text}'
                footer = f' footer {emb.footer.text}'
            else:
                f = footer = ''
        if message.author.id in botversions:
            if message.embeds == []:
                if '```' in message.content:
                    if should_be_edit == '--edit':
                        await ctx.send(f'cy/edit {message.id} {message.content}')
                    else:
                        await ctx.send(f'cy/say {message.content}')
                else:
                    if should_be_edit == '--edit':
                        await ctx.send(f'```cy/edit {message.id} {message.content}```')
                    else:
                        await ctx.send(f'```cy/say {message.content}```')
            else:
                if should_be_edit == '--edit':
                    await ctx.send(f'```cy/edit {message.id} {t}{d}{f}{th}{img}{c}```')
                else:
                    await ctx.send(f'```cy/say {t}{d}{f}{th}{img}{c}```')
        else:
            if message.embeds == []:
                if '```' in message.content:
                    await ctx.send(f'@{message.author.display_name} {message.content}')
                else:
                    await ctx.send(f'```@{message.author.display_name} {message.content}```')
            else:
                await ctx.send(f'```{content}{title}{description}{footer}{color}{author}{image}{thumb}```')

async def setup(client):
    await client.add_cog(Embeds(client))