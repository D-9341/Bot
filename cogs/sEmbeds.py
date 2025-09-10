import discord
from discord import app_commands
from discord.ext import commands
from cogs.Constants import colors

botversions = [764882153812787250, 694170281270312991, 762015251264569352]

class sEmbeds(commands.Cog):

    def __init__(self, client):
        self.client: commands.Bot = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('/ - Команды Embeds синхронизированы')

    @app_commands.command(description = 'Позволяет писать от лица бота. Пропишите /help say для подробностей использования')
    @app_commands.describe(msg = 'Что вы хотите написать от лица бота')
    async def say(self, interaction: discord.Interaction, *, msg: str):
        title = ''
        description = ''
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
        if color == None:
            color = colors.DEFAULT
        else:
            color = int('0x' + color.lstrip('#'), 16)
        emb = discord.Embed(title = title, description = description, color = color)
        for i in embed_values:
            emb.set_author(name = interaction.user.display_name, icon_url = interaction.user.avatar.url)
            if image:
                emb.set_image(url = image)
            if thumbnail:
                emb.set_thumbnail(url = thumbnail)
            if footer:
                emb.set_footer(text = footer)
            if not any(keyword in msg for keyword in ['&t', '&d', '&img', '&th', '&f', '&c', '&a']):
                return await interaction.response.send_message(msg)
            else:
                if message:
                    return await interaction.response.send_message(f'{message}', embed = emb)
                else:
                    return await interaction.response.send_message(embed = emb)

    @app_commands.command(description = 'Вы можете отредактировать сообщения бота')
    @app_commands.describe(arg = 'ID сообщения, которое нужно отредактировать', msg = 'Что вы хотите изменить. Пропишите /help edit для подробностей использования')
    @app_commands.checks.has_permissions(manage_messages = True)
    @app_commands.allowed_contexts(guilds = True, dms = False)
    async def edit(self, interaction: discord.Interaction, arg: str, *, msg: str = None):
        message = await interaction.channel.fetch_message(int(arg))
        if not any(keyword in msg for keyword in ['&t', '&d', '&img', '&th', '&f', '&c', '&a']):
            if message.author == self.client.user:
                if '--delete' in msg:
                    await message.delete()
                    return await interaction.response.send_message('Сообщение удалено')
                if '--clean' in msg:
                    return await message.edit(content = None)
                if '--noembed' in msg:
                    if message.embeds != []:
                        await message.edit(embed = None)
                    else:
                        return await interaction.response.send_message(embed = discord.Embed(description = f'{interaction.user.mention}, нечего удалять. Возможно, вы имели ввиду cy/edit {message.id} --delete', color = 0xff8000))
                else:
                    return await message.edit(content = msg)
            else:
                return await interaction.response.send_message(embed = discord.Embed(description = f'{message.id} не является сообщением от {self.client.user.mention}', color = 0xff0000))
        else:
            if message.embeds != []:
                old_embed = message.embeds[0]
                title = old_embed.title
                description = old_embed.description
                color = old_embed.color
            else:
                title = description = ''
                color = None
            image = thumbnail = footer = author = None
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
                elif i.strip().lower().startswith('a'):
                    author = i.strip()[1:].strip()
                    author = await commands.MemberConverter().convert(interaction, author)
            if author is None:
                author = interaction.user
            if message.embeds == [] or color is None:
                color = colors.DEFAULT
            elif message.embeds != [] and '&c' not in msg:
                color = message.embeds[0].color
            else:
                color = int('0x' + color.lstrip('#'), 16)
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
                    return await interaction.response.send_message('Сообщение удалено')
                if '--clean' in msg:
                    return await message.edit(content = None, embed = emb)
                if '--noembed' in msg:
                    if message.embeds != []:
                        return await message.edit(embed = None)
                    return await interaction.response.send_message(embed = discord.Embed(description = f'{interaction.user.mention}, нечего удалять. Возможно, вы имели ввиду cy/edit {message.id} --delete', color = 0xff8000))
                return await message.edit(embed = emb)
            return await interaction.response.send_message(embed = discord.Embed(description = f'{message.jump_url} не является сообщением от {self.client.user.mention}', color = 0xff8000))

    @app_commands.command(description = 'Получите контент сообщения. Можно использовать не только на сообщениях бота')
    @app_commands.describe(arg = 'ID сообщения, контент которого нужно получить', channel = 'Канал, из которого нужно достать сообщение. Не указывайте, если команда выполняется в том же канале, что и сообщение')
    async def content(self, interaction: discord.Interaction, arg: str, channel: discord.TextChannel = None, should_be_edit: str = 'no'):
        if channel == None:
            channel = interaction.channel
        message = await channel.fetch_message(int(arg))
        embed_data = {
            "color": '',
            "c": '',
            "author": '',
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
            "footer": ''
        }
        for emb in message.embeds:
            if emb.color:
                embed_data["color"] = f' color {emb.color}'
                embed_data["c"] = f' &c {emb.color}'
            if emb.author.name:
                embed_data["author"] = f' author {emb.author.name}'
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
                embed_data["t"] = f'&t {emb.title}'
                embed_data["title"] = f' title {emb.title}'
            if emb.footer.text:
                embed_data["f"] = f' &f {emb.footer.text}'
                embed_data["footer"] = f' footer {emb.footer.text}'
        if message.author.id in botversions:
            command = 'edit' if should_be_edit == '--edit' else 'say'
            if message.embeds:
                await interaction.response.send_message(f'```cy/{command} {message.id if command == "edit" else ""} {embed_data["t"]}{embed_data["d"]}{embed_data["f"]}{embed_data["th"]}{embed_data["img"]}{embed_data["c"]}```')
            else:
                content_prefix = '' if '```' in message.content else '```'
                await interaction.response.send_message(f'{content_prefix}cy/{command} {message.content}{content_prefix}')
        else:
            content_prefix = '' if '```' in message.content else '```'
            if message.embeds:
                await interaction.response.send_message(f'{content_prefix}{embed_data["content"]}{embed_data["title"]}{embed_data["description"]}{embed_data["footer"]}{embed_data["color"]}{embed_data["author"]}{embed_data["image"]}{embed_data["thumb"]}{content_prefix}')
            else:
                await interaction.response.send_message(f'{content_prefix}@{message.author.display_name} {message.content}{content_prefix}')

async def setup(client):
    await client.add_cog(sEmbeds(client))
