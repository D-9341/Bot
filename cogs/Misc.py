import discord
from discord.ext import commands
import datetime
import asyncio
import re

time_regex = re.compile("(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {'h': 3600, 's': 1, 'm': 60, 'd': 86400}

class TimeConverter(commands.Converter):
    async def convert(self, ctx, argument):
        args = argument.lower()
        time = 0
        matches = re.findall(time_regex, args)
        for key, value in matches:
            try:
                time += time_dict[value] * float(key)
            except KeyError:
                raise commands.BadArgument(f'{value} не является правильным аргументом! Правильные: h|m|s|d')
            except ValueError:
                raise commands.BadArgument(f'{key} не число!')
        return time

class Misc(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('Дополнение Misc успешно загружено.')

    @commands.command(aliases = ['Guild', 'GUILD'])
    @commands.cooldown(1, 5, commands.BucketType.default)
    async def guild(self, ctx):
        await ctx.message.delete()
        guild = ctx.guild
        emb = discord.Embed(colour = discord.Color.orange(), timestamp = ctx.message.created_at)
        emb.set_author(name = guild, icon_url = guild.icon_url)
        emb.add_field(name = 'ID сервера', value = guild.id)
        emb.add_field(name = 'Голосовой регион', value = guild.region)
        emb.add_field(name = 'Участников', value = guild.member_count)
        emb.add_field(name = 'Каналов', value = f'Текстовых {len(guild.text_channels)} | Голосовых {len(guild.voice_channels)}')
        limit = len(guild.roles)
        if limit > 21:
            emb.add_field(name = 'Роли', value = f'Слишком много для отрисовки ({len(guild.roles)-1}) [лимит 20]', inline = False)
        elif limit == 21:
            emb.add_field(name = f'Роли ({len(guild.roles)-1}) [лимит достигнут]', value = ', '.join([role.mention for role in guild.roles[1:]]), inline = False)
        elif limit == 20:
            emb.add_field(name = f'Роли ({len(guild.roles)-1}) [1 до лимита]', value = ', '.join([role.mention for role in guild.roles[1:]]), inline = False)
        elif limit == 19:
            emb.add_field(name = f'Роли ({len(guild.roles)-1}) [2 до лимита]', value = ', '.join([role.mention for role in guild.roles[1:]]), inline = False)
        elif limit == 18:
            emb.add_field(name = f'Роли ({len(guild.roles)-1}) [3 до лимита]', value = ', '.join([role.mention for role in guild.roles[1:]]), inline = False)
        else:
            emb.add_field(name = f'Роли ({len(guild.roles)-1})', value = ', '.join([role.mention for role in guild.roles[1:]]), inline = False)
        now = datetime.datetime.today()
        then = guild.created_at
        delta = now - then
        d = guild.created_at.strftime('%d/%m/%Y %H:%M:%S UTC')
        emb.add_field(name = 'Дата создания сервера', value = f'{delta.days} дней назад. ({d})', inline = False)
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        emb.set_thumbnail(url = guild.icon_url)
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
        now = datetime.datetime.today()
        then = role.created_at
        delta = now - then
        d = role.created_at.strftime('%d/%m/%Y %H:%M:%S UTC')
        emb.add_field(name = 'Создана', value = f'{delta.days} дня(ей) назад. ({d})', inline = False)
        emb.add_field(name = 'Показывает участников отдельно?', value = role.hoist)
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb)
    
    @commands.command(aliases = ['Avatar', 'AVATAR'])
    @commands.cooldown(1, 5, commands.BucketType.default)
    async def avatar(self, ctx, *, member: discord.Member = None):
        await ctx.message.delete()
        if member == None:
            member = ctx.author
        av = 'png'
        av1 = 'webp'
        av2 = 'jpg'
        emb = discord.Embed(colour = member.color)
        emb.add_field(name = '.png', value = f'[Ссылка]({member.avatar_url_as(format = av)})')
        emb.add_field(name = '.webp', value = f'[Ссылка]({member.avatar_url_as(format = av1)})')
        emb.add_field(name = '.jpg', value = f'[Ссылка]({member.avatar_url_as(format = av2)})')
        emb.set_image(url = member.avatar_url)
        emb.set_author(name = member)
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb)
    
    @commands.command(aliases = ['me', 'Me', 'ME', 'About', 'ABOUT'])
    @commands.cooldown(1, 5, commands.BucketType.default)
    async def about(self, ctx, *, member: discord.Member = None):
        await ctx.message.delete()
        if member == None:
            member = ctx.author
        if member.nick == None:
            member.nick = 'Не указан'
        if member.bot == False:
            bot = 'Неа'
        elif member.bot == True:
            bot = 'Ага'
        emb = discord.Embed(colour = member.color, timestamp = ctx.message.created_at)
        emb.set_author(name = member)
        emb.add_field(name = 'ID', value = member.id)
        now = datetime.datetime.today()
        then = member.created_at
        delta = now - then
        d = member.created_at.strftime('%d/%m/%Y %H:%M:%S UTC')
        then1 = member.joined_at
        delta1 = now - then1
        d1 = member.joined_at.strftime('%d/%m/%Y %H:%M:%S UTC')
        emb.add_field(name = 'Создан', value = f'{delta.days} дня(ей) назад. ({d})', inline = False)
        emb.add_field(name = 'Вошёл', value = f'{delta1.days} дня(ей) назад. ({d1})', inline = False)
        emb.add_field(name = 'Упоминание', value = member.mention)
        emb.add_field(name = 'Raw имя', value = member.name)
        emb.add_field(name = 'Никнейм', value = member.nick)
        limit = len(member.roles)
        if limit > 21:
            emb.add_field(name = 'Роли', value = f'Слишком много для отрисовки ({len(member.roles)-1}) [лимит 20]', inline = False)
        elif limit == 21:
            emb.add_field(name = f'Роли ({len(member.roles)-1}) [лимит достигнут]', value = ', '.join([role.mention for role in member.roles[1:]]), inline = False)
        elif limit == 20:
            emb.add_field(name = f'Роли ({len(member.roles)-1}) [1 до лимита]', value = ', '.join([role.mention for role in member.roles[1:]]), inline = False)
        elif limit == 19:
            emb.add_field(name = f'Роли ({len(member.roles)-1}) [2 до лимита]', value = ', '.join([role.mention for role in member.roles[1:]]), inline = False)
        elif limit == 18:
            emb.add_field(name = f'Роли ({len(member.roles)-1}) [3 до лимита]', value = ', '.join([role.mention for role in member.roles[1:]]), inline = False)
        else:
            emb.add_field(name = f'Роли ({len(member.roles)-1})', value = ', '.join([role.mention for role in member.roles[1:]]), inline = False)
        emb.add_field(name = 'Высшая Роль', value = member.top_role.mention, inline = False)
        emb.add_field(name = 'Бот?', value = bot)
        emb.set_thumbnail(url = member.avatar_url)
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb)
        
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.default)
    async def remind(self, ctx, time: TimeConverter, *, arg):
        await ctx.message.delete()
        emb = discord.Embed(colour = ctx.author.color, timestamp = ctx.message.created_at)
        emb.add_field(name = 'Напомню через', value = f'{time}s')
        emb.add_field(name = 'О чём напомню?', value = arg)
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb, delete_after = time)
        await asyncio.sleep(time)
        emb = discord.Embed(colour = ctx.author.color, timestamp = ctx.message.created_at)
        emb.add_field(name = 'Напомнил через', value = f'{time}s')
        emb.add_field(name = 'Напоминаю о', value = arg)
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(f'{ctx.author.mention}', embed = emb) 

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.message.delete()
            emb = discord.Embed(description = f'{ctx.author.mention}, команда в кд, потерпи чутка!', colour = discord.Color.orange())
            await ctx.send(embed = emb)

def setup(client):
    client.add_cog(Misc(client))
