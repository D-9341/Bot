import discord
from discord.ext import commands
from discord.utils import get
import datetime

class Events(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('Дополнение Events успешно загружено.')

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        channel = self.client.get_channel(693929823030214658)
        emb = discord.Embed(description = f'Меня выгнали с сервера `{guild.name}`...', colour = discord.Color.red())
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await channel.send(embed = emb)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        channel = self.client.get_channel(693929823030214658)
        emb = discord.Embed(description = f'Меня добавили на сервер `{guild.name}`!', colour = discord.Color.green())
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await channel.send(embed = emb)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if after.channel.id == 742647888424730735:
            category = discord.utils.get(member.guild.categories, id = 742647888101769236)
            channel = await member.guild.create_voice_channel(name = f'Комната {member}', category = category)
            await member.move_to(channel)
            await channel.set_permissions(member, mute_members = True, move_members = True, manage_channels = True)
            def check(a,b,c):
                return len(channel.members) == 0
            await self.client.wait_for('voice_state_update', check = check)
            await channel.delete()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == 693931411815661608:
            await message.add_reaction('👍')
            await message.add_reaction('👎')
        elif message.channel.id == 694213387625693264:
            await message.add_reaction('👍')
            await message.add_reaction('👎')
        elif message.channel.id == 747838996729692160:
            await message.add_reaction('👍')
            await message.add_reaction('👎')
        elif message.channel.id == 707498623981715557:
            await message.add_reaction('👍')
            await message.add_reaction('👎')
        elif message.channel.id == 767848243291095090:
            await message.add_reaction('👍')
            await message.add_reaction('👎')
        channel = self.client.get_channel(714175791033876490)
        if channel is None:
            await self.client.process_commands(message)
            return
        if not message.author.bot:
            emb = discord.Embed(colour = discord.Color.orange(), timestamp = datetime.datetime.utcnow())
            emb.set_author(name = message.author, icon_url = message.author.avatar_url)
            emb.add_field(name = 'На сервере', value = message.guild)
            emb.add_field(name = 'В канале', value = f'{message.channel.mention} ({message.channel.name})')
            emb.add_field(name = 'Было написано', value = message.content)
            emb.set_footer(text = f'Cephalon Cy by сасиска#2472')
            await self.client.process_commands(message)
            await channel.send(embed = emb)
    
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        channel = self.client.get_channel(714175791033876490)
        if channel is None:
            return
        if not before.author.bot:
            emb = discord.Embed(description = f'[Сообщение]({before.jump_url}) было изменено', colour = discord.Color.orange(), timestamp = datetime.datetime.utcnow())
            emb.set_author(name = before.author, icon_url = before.author.avatar_url)
            emb.add_field(name = 'На сервере', value = before.guild)
            emb.add_field(name = 'Было', value = f'```{before.content}```')
            emb.add_field(name = 'Стало', value = f'```{after.content}```')
            emb.set_footer(text = f'Cephalon Cy by сасиска#2472')
            await channel.send(embed = emb)

def setup(client):
    client.add_cog(Events(client))
