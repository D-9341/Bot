import discord
from discord.ext import commands
import datetime

class Events(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('Дополнение Events успешно загружено.')

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        channel = self.client.get_channel(714175791033876490)
        emb = discord.Embed(description = f'Меня выгнали с сервера `{guild}`...', colour = discord.Color.red())
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await channel.send(embed = emb)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        channel = self.client.get_channel(714175791033876490)
        emb = discord.Embed(description = f'Меня добавили на сервер `{guild}`!', colour = discord.Color.green())
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await channel.send(embed = emb)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        message_id = payload.message_id
        if message_id == 707496056505761802:
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)

            if payload.emoji.name == 'strashilka':
                role = discord.utils.get(guild.roles, id = 693933515540135987)

            if role is not None:
                member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                if member is not None:
                    await member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        message_id = payload.message_id
        if message_id == 707496056505761802:
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)

            if payload.emoji.name == 'strashilka':
                role = discord.utils.get(guild.roles, id = 693933515540135987)

            if role is not None:
                member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                if member is not None:
                    await member.remove_roles(role)        

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.client.get_channel(693929823030214658)
        if member.bot == False:
            role = discord.utils.get(member.guild.roles, id = 693933516294979704)
            role1 = discord.utils.get(member.guild.roles, id = 693933510523879454)
            role2 = discord.utils.get(member.guild.roles, id = 693933514198089838)
            if role is not None:
                await member.add_roles(role, role1, role2)
            emb = discord.Embed(description = f'{member.mention} ({member.name}) Has entered the `{member.guild.name}`, 👋', colour = discord.Color.orange())
            emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
            await channel.send(embed = emb)
        else:
            role = discord.utils.get(member.guild.roles, id = 693933516831850527)
            role1 = discord.utils.get(member.guild.roles, id = 693933511412940800)
            if role is not None:
                await member.add_roles(role, role1)
            emb = discord.Embed(description = f'А, {member.mention} ({member.name}) - очередной ботяра? `{member.guild.name}`, зачем?', colour = discord.Color.orange())
            await channel.send(embed = emb)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.client.get_channel(693929823030214658)
        if member.bot == False:
            emb = discord.Embed(description = f'{member.mention} ({member.name}) Has exited the `{member.guild.name}`...', colour = discord.Color.red())
            emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
            await channel.send(embed = emb)
        elif member.bot != False and member.id != 694170281270312991:
            emb = discord.Embed(description = f'{member.mention} ({member.name}), ну и вали с `{member.guild.name}` ботаря, хаха!', colour = discord.Color.orange())
            emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
            await channel.send(embed = emb)
        elif member.bot != False and member.id == 694170281270312991:
            emb = discord.Embed(description = f'Ой, это я чтоли с `{member.guild.name}` вышел?', colour = discord.Color.orange())
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
            await client.wait_for('voice_state_update', check = check)
            await channel.delete()

    @commands.Cog.listener()
    async def on_message(self, message):
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
            emb.set_author(name = before.author.name, icon_url = before.author.avatar_url)
            emb.add_field(name = 'На сервере', value = message.guild)
            emb.add_field(name = 'Было', value = f'```{before.content}```')
            emb.add_field(name = 'Стало', value = f'```{after.content}```')
            emb.set_footer(text = f'Cephalon Cy by сасиска#2472')
            await channel.send(embed = emb)

def setup(client):
    client.add_cog(Events(client))
