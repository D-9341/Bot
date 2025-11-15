import discord
from discord.ext import commands

from cogs.Constants import botversions, colors
from main import bot_owner_or_has_permissions

class Embeds(commands.Cog):
    def __init__(self, client):
        self.client: commands.Bot = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Модуль Embeds загружен')

    @commands.command()
    async def say(self, ctx: commands.Context, *, msg: str):
        view = discord.ui.View()
        title = description = ''
        image = thumbnail = message = footer = color = author = label = url = None
        embed_values = msg.split('&')
        for part in range(len(embed_values)):
            try:
                if '<@' in embed_values[part] and '>' in embed_values[part + 1]:
                    embed_values[part] = f'{embed_values[part]}&{embed_values[part + 1]}'
                    del embed_values[part + 1]
            except IndexError:
                pass
        for value in embed_values:
            if value.strip().lower().startswith('th'):
                thumbnail = value.strip()[2:].strip()
            elif value.strip().lower().startswith('b'):
                values = value.strip()[1:].strip().split('|')
                for value in values:
                    if value.strip().lower().startswith('label'):
                        label = value.strip()[5:].strip()
                    elif value.strip().lower().startswith('url'):
                        url = value.strip()[3:].strip().lstrip('<').rstrip('>')
                if url:
                    view.add_item(discord.ui.Button(label = label, url = url, style = discord.ButtonStyle.gray))
                else:
                    view.add_item(discord.ui.Button(label = label, disabled = True, style = discord.ButtonStyle.gray))
            elif value.strip().lower().startswith('d'):
                description = value.strip()[1:].strip()
            elif value.strip().lower().startswith('c'):
                color = value.strip()[1:].strip()
            elif value.strip().lower().startswith('img'):
                image = value.strip()[3:].strip()
            elif value.strip().lower().startswith('t'):
                title = value.strip()[1:].strip()
            elif value.strip().lower().startswith('msg'):
                message = value.strip()[3:].strip()
            elif value.strip().lower().startswith('f'):
                footer = value.strip()[1:].strip()
            elif value.strip().lower().startswith('a'):
                author = value.strip()[1:].strip()
                author = await commands.MemberConverter().convert(ctx, author)
        if author is None:
            author = ctx.author
        if color is None:
            color = colors.DEFAULT
        else:
            if hasattr(colors, color):
                color = getattr(colors, color)
            else:
                try:
                    color = int('0x' + color.lstrip('#'), 16)
                except ValueError:
                    color = colors.DEFAULT
        emb = discord.Embed(title = title, description = description, color = color)
        emb.set_author(name = author.display_name, icon_url = author.avatar.url)
        if image:
            emb.set_image(url = image)
        if thumbnail:
            emb.set_thumbnail(url = thumbnail)
        if footer:
            emb.set_footer(text = footer)
        if not any(keyword in msg for keyword in ['&t', '&d', '&img', '&th', '&f', '&c', '&a', '&b']):
            return await ctx.send(msg, view = view)
        if message:
            return await ctx.send(f'{message}', embed = emb, view = view)
        return await ctx.send(embed = emb, view = view)

    @commands.command()
    @commands.check(bot_owner_or_has_permissions(manage_messages = True))
    async def edit(self, ctx: commands.Context, arg, *, msg: str = None):
        message = await ctx.channel.fetch_message(arg)
        view = discord.ui.View()
        if not any(keyword in msg for keyword in ['&t', '&d', '&img', '&th', '&f', '&c', '&a', '&b']):
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
                        return await ctx.send(embed = discord.Embed(description = f'{ctx.author.mention}, нечего удалять. Возможно, вы имели ввиду cy/edit {message.id} --delete', color = colors.JDH))
                else:
                    return await message.edit(content = msg)
            else:
                return await ctx.send(embed = discord.Embed(description = f'{message.jump_url} не является сообщением от {self.client.user.mention}', color = colors.ERROR))
        else:
            if message.embeds != []:
                old_embed = message.embeds[0]
                title = old_embed.title
                description = old_embed.description
                color = old_embed.color
            else:
                title = description = ''
                color = None
            image = thumbnail = footer = author = label = url = None
            embed_values = msg.split('&')
            for part in range(len(embed_values)):
                try:
                    if '<@' in embed_values[part] and '>' in embed_values[part + 1]:
                        embed_values[part] = f'{embed_values[part]}&{embed_values[part + 1]}'
                        del embed_values[part + 1]
                except IndexError:
                    pass
            for value in embed_values:
                if value.strip().lower().startswith('th'):
                    thumbnail = value.strip()[2:].strip()
                elif value.strip().lower().startswith('b'):
                    message.components = []
                    values = value.strip()[1:].strip().split('|')
                    for value in values:
                        if value.strip().lower().startswith('label'):
                            label = value.strip()[5:].strip()
                        elif value.strip().lower().startswith('url'):
                            url = value.strip()[3:].strip().lstrip('<').rstrip('>')
                    if url:
                        view.add_item(discord.ui.Button(label = label, url = url, style = discord.ButtonStyle.gray))
                    else:
                        view.add_item(discord.ui.Button(label = label, disabled = True, style = discord.ButtonStyle.gray))
                elif value.strip().lower().startswith('d'):
                    description = value.strip()[1:].strip()
                elif value.strip().lower().startswith('c'):
                    color = value.strip()[1:].strip()
                elif value.strip().lower().startswith('img'):
                    image = value.strip()[3:].strip()
                elif value.strip().lower().startswith('t'):
                    title = value.strip()[1:].strip()
                elif value.strip().lower().startswith('f'):
                    footer = value.strip()[1:].strip()
                elif value.strip().lower().startswith('a'):
                    author = value.strip()[1:].strip()
                    author = await commands.MemberConverter().convert(ctx, author)
            if author is None:
                author = ctx.author
            if message.embeds == [] or color is None:
                color = colors.DEFAULT
            elif message.embeds != [] and '&c' not in msg:
                color = message.embeds[0].color
            else:
                if hasattr(colors, color):
                    color = getattr(colors, color)
                else:
                    try:
                        color = int('0x' + color.lstrip('#'), 16)
                    except ValueError:
                        color = colors.DEFAULT
            emb = discord.Embed(title = title, description = description, color = color, timestamp = discord.utils.utcnow())
            emb.set_author(name = author.display_name, icon_url = author.avatar.url)
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
                    return await message.edit(content = None, embed = emb, view = view)
                if '--noembed' in msg:
                    if message.embeds != []:
                        return await message.edit(embed = None, view = view)
                    return await ctx.send(embed = discord.Embed(description = f'{ctx.author.mention}, нечего удалять. Возможно, вы имели ввиду cy/edit {message.id} --delete', color = colors.JDH))
                return await message.edit(embed = emb, view = view)
            return await ctx.send(embed = discord.Embed(description = f'{message.jump_url} не является сообщением от {self.client.user.mention}', color = colors.JDH))

    @commands.command(aliases = ['ctx'])
    async def content(self, ctx: commands.Context, msg: int, channel: discord.TextChannel | str = None, option = None):
        if channel is None or channel == 'current':
            channel = ctx.channel
        message = await channel.fetch_message(msg)
        embed_data = {
            "color": '',
            "c": '',
            "author": '',
            'a': '',
            "content": f'content {message.content}' if message.content else '',
            "img": '',
            "image": '',
            "th": '',
            "thumb": '',
            "d": '',
            "description": '',
            "t": '',
            "title": '',
            "f": '',
            "footer": '',
            "b": ''
        }
        for emb in message.embeds:
            if emb.color:
                embed_data["color"] = f' color {emb.color}'
                embed_data["c"] = f' &c {emb.color}'
            if emb.author.name:
                embed_data["author"] = f' author {emb.author.name}'
                embed_data["a"] = f' &a {emb.author.name}'
            if emb.image.url:
                embed_data["img"] = f' &img {emb.image.url}'
                embed_data["image"] = f' image {emb.image.url}'
            if emb.thumbnail.url:
                embed_data["th"] = f' &th {emb.thumbnail.url}'
                embed_data["thumb"] = f' thumbnail {emb.thumbnail.url}'
            if emb.description:
                embed_data["d"] = f' &d {emb.description}'
                embed_data["description"] = f' description {emb.description}'
            if emb.title:
                embed_data["t"] = f' &t {emb.title}'
                embed_data["title"] = f' title {emb.title}'
            if emb.footer.text:
                embed_data["f"] = f' &f {emb.footer.text}'
                embed_data["footer"] = f' footer {emb.footer.text}'
        for component in message.components:
            for button in component.children:
                embed_data["b"] += f' &b label {button.label}{f' | url {button.url}' if button.url else ""}'
        if message.author.id in botversions.botversions:
            command = 'edit' if option == '--edit' else 'say'
            if message.embeds:
                await ctx.send(f'```cy/{command}{f' {message.id}' if command == "edit" else ""}{embed_data["t"]}{embed_data["d"]}{embed_data["f"]}{embed_data["th"]}{embed_data["img"]}{embed_data["c"]}{embed_data["a"]}{embed_data["b"]}```')
            else:
                content_prefix = '' if '```' in message.content else '```'
                await ctx.send(f'{content_prefix}cy/{command} {message.content}{content_prefix}')
        else:
            content_prefix = '' if '```' in message.content else '```'
            if message.embeds:
                await ctx.send(f'{content_prefix}{embed_data["content"]}{embed_data["title"]}{embed_data["description"]}{embed_data["footer"]}{embed_data["color"]}{embed_data["author"]}{embed_data["image"]}{embed_data["thumb"]}{content_prefix}')
            else:
                await ctx.send(f'{content_prefix}@{message.author.display_name} {message.content}{content_prefix}')

async def setup(client):
    await client.add_cog(Embeds(client))
