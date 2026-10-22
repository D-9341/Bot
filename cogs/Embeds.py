import discord
from discord.ext import commands
import re

from cogs.Constants import botversions as bots, colors
from main import bot_owner_or_has_permissions

async def parse_embed(ctx: commands.Context, msg: str, old_embed: discord.Embed = None):
    pattern = re.compile(r'([a-zA-Z]+)& (.*?)(?=\s*[a-zA-Z]+&|\s*$)', re.DOTALL)
    matches = pattern.findall(msg)

    from collections import defaultdict
    values = defaultdict(list)

    for key, val in matches:
        key = key.lower()
        values[key].append(val.strip())

    title = values.get('t', [''])[0] if 't' in values else old_embed.title if old_embed else ''
    description = values.get('d', [''])[0] if 'd' in values else old_embed.description if old_embed else ''
    image = values.get('img', [None])[0]
    thumbnail = values.get('th', [None])[0]
    message = values.get('msg', [None])[0]
    footer = values.get('f', [None])[0]
    color = values.get('c', [None])[0] if 'c' in values else str(old_embed.color) if old_embed else None
    authors = values.get('a', [])
    buttons = values.get('b', [])
    
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
    if authors:
        authors = [await commands.MemberConverter().convert(ctx, author) for author in authors]
    else:
        authors = [ctx.author]
    view = discord.ui.View()
    for button in buttons:
        parts: str = button.split('|')
        label = url = None
        for part in parts:
            part = part.strip()
            if part.lower().startswith('label'):
                label = part[5:].strip()
            elif part.lower().startswith('url'):
                url = part[3:].strip().lstrip('<').rstrip('>')
        if url:
            view.add_item(discord.ui.Button(label = label, url = url, style = discord.ButtonStyle.gray))
        else:
            view.add_item(discord.ui.Button(label = label, disabled = True, style = discord.ButtonStyle.gray))

    return description, title, image, thumbnail, message, footer, color, authors, view


def _format_authors(authors: list[discord.Member]) -> tuple[str, str | None]:
    if len(authors) == 1:
        return authors[0].display_name, authors[0].avatar.url
    *others, last = authors
    names = ", ".join(a.display_name for a in others) + f" и {last.display_name}"
    icon_url = authors[0].avatar.url if len(authors) == 1 else None
    return names, icon_url

def _split_author_names(name: str) -> list[str]:
    if not name:
        return []
    return [p.strip() for p in re.split(r',\s*|\s+и\s+', name) if p.strip()]


class Embeds(commands.Cog):
    def __init__(self, client):
        self.client: commands.Bot = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Модуль Embeds загружен')

    @commands.command()
    async def say(self, ctx: commands.Context, *, msg: str):
        has_keys = re.search(r'[a-zA-Z]+&', msg)
        if not has_keys:
            return await ctx.send(msg)
        description, title, image, thumbnail, message, footer, color, authors, view = await parse_embed(ctx, msg)
        emb = discord.Embed(title = title, description = description, color = color)
        author_name, author_icon = _format_authors(authors)
        emb.set_author(name = author_name, icon_url = author_icon)
        if image:
            emb.set_image(url = image)
        if thumbnail:
            emb.set_thumbnail(url = thumbnail)
        if footer:
            emb.set_footer(text = footer)
        if message:
            return await ctx.send(f'{message}', embed = emb, view = view)
        return await ctx.send(embed = emb, view = view)

    @commands.command()
    @commands.check(bot_owner_or_has_permissions(manage_messages = True))
    async def edit(self, ctx: commands.Context, arg, *, msg: str = None):
        message = await ctx.channel.fetch_message(arg)
        has_keys = re.search(r'[a-zA-Z]+&', msg)
        if not has_keys:
            if message.author == self.client.user:
                if '--delete' in msg:
                    await message.delete()
                    return await ctx.send('Сообщение удалено')
                if '--clean' in msg:
                    return await message.edit(content = None)
                if '--noembed' in msg:
                    if message.embeds:
                        await message.edit(embed = None)
                    return await ctx.send(embed = discord.Embed(description = f'{ctx.author.mention}, нечего удалять. Возможно, вы имели ввиду cy/edit {message.id} --delete', color = colors.JDH))
                return await message.edit(content = msg)
            return await ctx.send(embed = discord.Embed(description = f'{message.jump_url} не является сообщением от {self.client.user.mention}', color = colors.ERROR))
        description, title, image, thumbnail, _, footer, color, authors, view = await parse_embed(ctx, msg, message.embeds[0])
        emb = discord.Embed(title = title, description = description, color = color, timestamp = discord.utils.utcnow())
        author_name, author_icon = _format_authors(authors)
        emb.set_author(name = author_name, icon_url = author_icon)
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
                if message.embeds:
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
                embed_data["c"] = f' c& {emb.color}'
            if emb.author.name:
                embed_data["author"] = f' author {emb.author.name}'
                embed_data["a"] = ''.join(f' a& {name}' for name in _split_author_names(emb.author.name))
            if emb.image.url:
                embed_data["img"] = f' img& {emb.image.url}'
                embed_data["image"] = f' image {emb.image.url}'
            if emb.thumbnail.url:
                embed_data["th"] = f' th& {emb.thumbnail.url}'
                embed_data["thumb"] = f' thumbnail {emb.thumbnail.url}'
            if emb.description:
                embed_data["d"] = f' d& {emb.description}'
                embed_data["description"] = f' description {emb.description}'
            if emb.title:
                embed_data["t"] = f' t& {emb.title}'
                embed_data["title"] = f' title {emb.title}'
            if emb.footer.text:
                embed_data["f"] = f' f& {emb.footer.text}'
                embed_data["footer"] = f' footer {emb.footer.text}'

        for component in message.components:
            for button in component.children:
                embed_data["b"] += f' b& label {button.label}{f' | url {button.url}' if button.url else ""}'

        if message.author.id in bots.botversions:
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