import discord
from discord import app_commands
from discord.ext import commands

botversions = [764882153812787250, 694170281270312991, 762015251264569352]

class sEmbeds(commands.Cog):

    def __init__(self, client):
        self.client = client

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
            color = 0x2f3136
        else:
            if '#' not in color:
                color = int('0x' + color, 16)
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
            if not any(keyword in msg for keyword in ['&t', '&d', '&img', '&th', '&msg', '&f', '&c']):
                return await interaction.response.send_message(msg)
            else:
                if message:
                    return await interaction.response.send_message(f'{message}', embed = emb)
                else:
                    return await interaction.response.send_message(embed = emb)

    @app_commands.command(description = 'Вы можете отредактировать сообщения бота')
    @app_commands.describe(arg = 'ID сообщения, которое нужно отредактировать', msg = 'Что вы хотите изменить. Пропишите /help edit для подробностей использования')
    @app_commands.checks.has_permissions(manage_messages = True)
    async def edit(self, interaction: discord.Interaction, arg: str, *, msg: str = None):
        message = await interaction.channel.fetch_message(int(arg))
        if not any(keyword in msg for keyword in ['&t', '&d', '&img', '&th', '&f', '&c']):
            if message.author == self.client.user:
                if '--delete' in msg:
                    await message.delete()
                    await interaction.response.send_message('Сообщение удалено.')
                    return
                if '--clean' in msg:
                    await message.edit(content = None)
                    return
                if '--noembed' in msg:
                    if message.embeds != []:
                        await message.edit(embed = None)
                        return
                    else:
                        await interaction.response.send_message(f'{interaction.user.mention}, нечего удалять. Возможно, вы имели ввиду /edit {message.id} --delete')
                        return
                else:
                    await message.edit(content = msg)
                    return
            else:
                await interaction.response.send_message(f'{message.id} не является сообщением от {self.client.user.mention}')
                return
        else:
            if message.embeds != []:
                old_embed = message.embeds[0]
                title = old_embed.title
                description = old_embed.description
                color = old_embed.color
            else:
                title = ''
                description = ''
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
            if message.embeds == [] or color == None:
                color = 0x2f3136
            elif message.embeds != [] and '&c' not in msg:
                color = message.embeds[0].color
            else:
                if '#' not in color:
                    color = int('0x' + color, 16)
                else:
                    color = int('0x' + color.lstrip('#'), 16)
            emb = discord.Embed(title = title, description = description, color = color, timestamp = discord.utils.utcnow())
            emb.set_author(name = interaction.user.display_name, icon_url = interaction.user.avatar.url)
            if image:
                emb.set_image(url = image)
            if thumbnail:
                emb.set_thumbnail(url = thumbnail)
            if footer:
                emb.set_footer(text = footer)
            if message.author == self.client.user:
                if '--delete' in msg:
                    await message.delete()
                    await interaction.response.send_message('Сообщение удалено.')
                    return
                if '--clean' in msg:
                    await message.edit(content = None, embed = emb)
                    return
                if '--noembed' in msg:
                    if message.embeds != []:
                        await message.edit(embed = None)
                        return
                    else:
                        await interaction.response.send_message(f'{interaction.user.mention}, нечего удалять. Возможно, вы имели ввиду cy/edit {message.id} --delete')
                        return
                else:
                    await message.edit(embed = emb)
                    return
            else:
                await interaction.response.send_message(f'{message.id} не является сообщением от {self.client.user.mention}')
                return

    @app_commands.command(description = 'Получите контент сообщения. Можно использовать не только на сообщениях бота')
    @app_commands.describe(arg = 'ID сообщения, контент которого нужно получить', channel = 'Канал, из которого нужно достать сообщение. Не указывайте, если команда выполняется в том же канале, что и сообщение')
    async def content(self, interaction: discord.Interaction, arg: str, channel: discord.TextChannel = None, should_be_edit: str = 'no'):
        if channel == None:
            channel = interaction.channel
        message = await channel.fetch_message(int(arg))
        for emb in message.embeds:
            if emb.color != None:
                color = f' color {emb.color}'
                c = f' &c {emb.color}'
            else:
                color = ''
                c = ''
            if emb.author.name != None:
                author = f' author {emb.author.name}'
            else:
                author = ''
            if message.content == '':
                content = ''
            else:
                content = f'content {message.content}'
            if emb.image.url != None:
                img = f' &img {emb.image.url}'
                image = f' image {emb.image.url}'
            else:
                img = ''
                image = ''
            if emb.thumbnail.url != None:
                th = f' &th {emb.thumbnail.url}'
                thumb = f' thumbnail {emb.thumbnail.url}'
            else:
                th = ''
                thumb = ''
            if emb.description != None:
                d = f' &d {emb.description}'
                description = f' description {emb.description}'
            else:
                d = ''
                description = ''
            if emb.title != None:
                t = f'&t {emb.title}'
                title = f' title {emb.title}'
            else:
                t = ''
                title = ''
            if emb.footer.text != None:
                f = f' &f {emb.footer.text}'
                footer = f' footer {emb.footer.text}'
            else:
                f = ''
                footer = ''
        if message.author.id in botversions:
            if message.embeds == []:
                if '```' in message.content:
                    if should_be_edit == '--edit':
                        await interaction.response.send_message(f'cy/edit {message.id} {message.content}')
                    else:
                        await interaction.response.send_message(f'cy/say {message.content}')
                else:
                    if should_be_edit == '--edit':
                        await interaction.response.send_message(f'```cy/edit {message.id} {message.content}```')
                    else:
                        await interaction.response.send_message(f'```cy/say {message.content}```')
            else:
                if should_be_edit == '--edit':
                    await interaction.response.send_message(f'```cy/edit {message.id} {t}{d}{f}{th}{img}{c}```')
                else:
                    await interaction.response.send_message(f'```cy/say {t}{d}{f}{th}{img}{c}```')
        else:
            if message.embeds == []:
                if '```' in message.content:
                    await interaction.response.send_message(f'@{message.author.display_name} {message.content}')
                else:
                    await interaction.response.send_message(f'```@{message.author.display_name} {message.content}```')
            else:
                await interaction.response.send_message(f'```{content}{title}{description}{footer}{color}{author}{image}{thumb}```')

async def setup(client):
    await client.add_cog(sEmbeds(client))