import discord
from discord.ext import commands
import asyncio

class Misc(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('Дополнение Misc успешно загружено.')

    @commands.command(aliases = ['Guild', 'GUILD'])
    @commands.cooldown(1, 5, commands.BucketType.default)
    async def guild(self, ctx, guild: discord.Guild = None):
        if guild == None:
            guild = ctx.guild
        await ctx.message.delete()
        emb = discord.Embed(title = f'Информация о {guild}', colour = discord.Color.orange(), timestamp = ctx.message.created_at)
        emb.add_field(name = 'ID сервера', value = guild.id)
        emb.add_field(name = 'Уровень сервера', value = guild.premium_tier)
        emb.add_field(name = 'Люди, бустящие сервер', value = guild.premium_subscribers)
        emb.add_field(name = 'Владелец сервера', value = guild.owner.mention, inline = False)
        emb.add_field(name = 'Количество человек на сервере', value = guild.member_count)
        emb.add_field(name = 'Дата создания сервера', value = guild.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline = False)
        emb.set_thumbnail(url = guild.icon_url)
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb)
    
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.default)
    async def role(self, ctx, *, role: discord.Role):
        await ctx.message.delete()
        if role.mentionable == False:
            role.mentionable = 'Нет'
        elif role.mentionable == True:
            role.mentionable = 'Да'
        if role.managed == False:
            role.managed = 'Нет'
        elif role.managed == True:
            role.managed = 'Да'
        if role.hoist == False:
            role.hoist = 'Нет'
        elif role.hoist == True:
            role.hoist = 'Да'
        emb = discord.Embed(title = role.name, colour = role.colour)
        emb.add_field(name = 'ID', value = role.id)
        emb.add_field(name = 'Цвет', value = role.color)
        emb.add_field(name = 'Упоминается?', value = role.mentionable)
        emb.add_field(name = 'Управляется интеграцией?', value = role.managed)
        emb.add_field(name = 'Позиция в списке', value = role.position)
        emb.add_field(name = 'Создана', value = role.created_at.strftime("%A, %#d %B %Y, %I:%M %p UTC"), inline = False)
        emb.add_field(name = 'Показывает участников отдельно?', value = role.hoist)
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb)
    
    @commands.command(aliases = ['Avatar', 'AVATAR'])
    @commands.cooldown(1, 5, commands.BucketType.default)
    async def avatar(self, ctx, member: discord.Member = None):
        await ctx.message.delete()
        if member == None:
            member = ctx.author
        emb = discord.Embed(description = f'[Прямая ссылка]({member.avatar_url})', colour = member.color)
        emb.set_author(name = member)
        emb.set_image(url = member.avatar_url)
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb)
    
    @commands.command(aliases = ['me', 'Me', 'ME', 'About', 'ABOUT'])
    @commands.cooldown(1, 5, commands.BucketType.default)
    async def about(self, ctx, member: discord.Member = None):
        await ctx.message.delete()
        if member == None:
            member = ctx.author
        if member.nick == None:
            member.nick = 'Не указан'
        if member.bot == False:
            bot = 'Неа'
        elif member.bot == True:
            bot = 'Ага'
        emb = discord.Embed(title = f'Информация о {member}', colour = member.color, timestamp = ctx.message.created_at)
        emb.add_field(name = 'ID', value = member.id)
        emb.add_field(name = 'Создан', value = member.created_at.strftime("%A, %#d %B %Y, %I:%M %p UTC"), inline = False)
        emb.add_field(name = 'Вошёл', value = member.joined_at.strftime("%A, %#d %B %Y, %I:%M %p UTC"), inline = False)
        emb.add_field(name = 'Упоминание', value = member.mention)
        emb.add_field(name = 'Имя', value = member.name)
        emb.add_field(name = 'Никнейм', value = member.nick)
        emb.add_field(name = 'Статус', value = member.status)
        emb.add_field(name = f'Роли [{len(member.roles)-1}]', value=' '.join([role.mention for role in member.roles[1:]]), inline = False)
        emb.add_field(name = 'Высшая Роль', value = member.top_role.mention, inline = False)
        emb.add_field(name = 'Бот?', value = bot)
        emb.set_thumbnail(url = member.avatar_url)
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb)
        
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.default)
    async def remind(self, ctx, time: int, *, arg):
        await ctx.message.delete()
        emb = discord.Embed(colour = ctx.author.color, timestamp = ctx.message.created_at)
        emb.add_field(name = 'Напомню через', value = f'{time} минут(у, ы)')
        emb.add_field(name = 'О чём напомню?', value = arg)
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb, delete_after = time * 60)
        await asyncio.sleep(time * 60)
        emb = discord.Embed(title = 'Напоминание', colour = ctx.author.color)
        emb.add_field(name = 'Напомнил через', value = f'{time} минут(у, ы)')
        emb.add_field(name = 'Напоминаю о', value = arg)
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(f'{ctx.author.mention}', embed = emb) 

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.message.delete()
            emb = discord.Embed(description = f'{ctx.author.mention}, команда в кд, потерпи чутка!', colour = discord.Color.orange())
            emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
            await ctx.send(embed = emb)

def setup(client):
    client.add_cog(Misc(client))
