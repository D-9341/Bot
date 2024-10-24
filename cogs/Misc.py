import random

import discord
from discord.ext import commands

class Slapper(commands.Converter):
    async def convert(self, ctx, argument):
        mention = random.choice(ctx.channel.members)
        emb = discord.Embed(description = f'{argument}', color =  0x2f3136, timestamp = discord.utils.utcnow())
        emb.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar.url)
        return await ctx.send(f'@someone ||{mention.mention}||', embed = emb)

    async def error(self, ctx, error):
        """
        it is used as a placeholder
        """
        await ctx.send(error)

class Misc(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Модуль Misc загружен')

    @commands.command()
    async def roll(self, ctx, first: str | int = None, second: int = None):
        if not first and not second:
            rand = random.randint(0, 100)
            if rand == 42:
                await ctx.send(embed = discord.Embed(description = f'{ctx.author.display_name} получает случайное число (0-100)\n`100`', color = 0xff8000))
            else:
                rand1 = random.randint(0, 9)
                rand2 = random.randint(0, 9)
                await ctx.send(embed = discord.Embed(description = f'{ctx.author.display_name} получает случайное число (0-100)\n`0{rand1}{rand2}`', color = 0xff8000))
        if first and not second:
            if first == 'adamant':
                await ctx.send(embed = discord.Embed(description = f'{ctx.author.display_name} получает случайное число \n`5 6 4 7 0 -9 9 2 π √2 Ω א`', color = 0xff8000))
            if 'd' in first:
                [dice_amount, dice_edges] = first.split('d')
                dice_amount, dice_edges = int(dice_amount), int(dice_edges)
                if dice_amount > 20:
                    return await ctx.send(embed = discord.Embed(description = 'Нельзя бросить больше 20 дайсов', color = 0xff0000))
                if dice_edges > 20:
                    return await ctx.send(embed = discord.Embed(description = 'Вы не можете кинуть дайс с большим количеством граней, чем 20', color = 0xff8000))
                if dice_amount > 1:
                    attempts = ''
                    result = 0
                    for i in range(1, dice_amount + 1):
                        rand = random.randint(1, dice_edges)
                        attempts += f'{i}. `{rand}`\n'
                        result += rand
                    attempts += f'В сумме - ||{result}||'
                else:
                    res = random.randint(1, dice_edges)
                    total = ''
                    if res == 1 and dice_edges == 20:
                        total = ', критический провал'
                    if res == 20:
                        total = ', критический успех!'
                    return await ctx.send(embed = discord.Embed(description = f'Получено случайное число: `{res}`{total}', color = 0xff8000))
                await ctx.send(embed = discord.Embed(description = attempts, color = 0xff8000))
            else:
                first = int(first)
                rand = random.randint(0, first)
                if first < 10:
                    await ctx.send(embed = discord.Embed(description = f'{ctx.author.display_name} получает случайное число (0-{first})\n`0{rand}`', color = 0xff8000))
                else:
                    await ctx.send(embed = discord.Embed(description = f'{ctx.author.display_name} получает случайное число (0-{first})\n`{rand}`', color = 0xff8000))
        if (first and second) or (first == 0 and second):
            first = int(first)
            if first > second:
                rand = random.randint(first, first)
                return await ctx.send(embed = discord.Embed(description = f'{ctx.author.display_name} получает случайное число ({first}-{first})\n`{rand}`', color = 0xff8000))
            rand = random.randint(first, second)
            await ctx.send(embed = discord.Embed(description = f'{ctx.author.display_name} получает случайное число ({first}-{second})\n`{rand}`', color = 0xff8000))

    @commands.command(aliases = ['c', 'coin'])
    async def coinflip(self, ctx):
        coin = random.choice(['ОРЁЛ', 'РЕШКА'])
        await ctx.send(embed = discord.Embed(description = f'{ctx.author.mention} подбрасывает монетку: {coin}', color = 0xff8000))

    @commands.command()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def someone(self, ctx, *, text: Slapper):
        await ctx.send(embed = text)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def rolemembers(self, ctx, role: discord.Role):
        emb = discord.Embed(color = 0xff8000)
        if len(role.members) != 0:
            emb.add_field(name = f'Участники с ролью {role} ({len(role.members)})', value = ', '.join([member.mention for member in role.members]))
        else:
            emb.description = f'Роли {role.name} нет ни у кого.'
        await ctx.send(embed = emb)

    @commands.command(aliases = ['guild'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def serverinfo(self, ctx):
        guild = ctx.guild
        emb = discord.Embed(color = 0x2f3136, timestamp = discord.utils.utcnow())
        emb.set_author(name = guild, icon_url = guild.icon.url if guild.icon else 'https://cdn.discordapp.com/attachments/685176670344183836/1076601210485866546/76923ec8de0a6ca5.png')
        emb.add_field(name = 'ID сервера', value = guild.id)
        emb.add_field(name = 'Владелец', value = guild.owner.mention)
        emb.add_field(name = 'Участников', value = f'{guild.member_count}\n**Из них ботов:** {len(list(filter(lambda m: m.bot, guild.members)))}\n**Из них людей:** {len(list(filter(lambda m: not m.bot, guild.members)))}')
        emb.add_field(name = 'Каналов', value = f'Текстовых {len(guild.text_channels)} | Голосовых {len(guild.voice_channels)}')
        roles = ', '.join([role.name for role in guild.roles[1:]])
        if len(roles) > 1:
            emb.add_field(name = f'Роли ({len(guild.roles)-1})', value = roles, inline = False)
        d = guild.created_at.strftime('%d.%m.%Y %H:%M:%S GMT')
        emb.add_field(name = 'Дата создания сервера', value = f'{d}', inline = False)
        emb.set_thumbnail(url = guild.icon.url if guild.icon else 'https://cdn.discordapp.com/attachments/685176670344183836/1076601210485866546/76923ec8de0a6ca5.png')
        await ctx.send(embed = emb)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def roleinfo(self, ctx, role: discord.Role):
        is_mentionable = 'Да' if role.mentionable else 'Нет'
        is_managed = 'Да' if role.managed else 'Нет'
        is_hoisted = 'Да' if role.hoist else 'Нет'
        emb = discord.Embed(title = role.name, color = 0x2f3136)
        emb.add_field(name = 'ID', value = role.id)
        emb.add_field(name = 'Цвет', value = role.color)
        emb.add_field(name = 'Упоминается?', value = is_mentionable)
        emb.add_field(name = 'Управляется интеграцией?', value = is_managed)
        emb.add_field(name = 'Позиция в списке', value = role.position)
        d = role.created_at.strftime('%d.%m.%Y %H:%M:%S GMT')
        emb.add_field(name = 'Создана', value = f'{d}', inline = False)
        emb.add_field(name = 'Показывает участников отдельно?', value = is_hoisted)
        await ctx.send(embed = emb)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def avatar(self, ctx, member: discord.User = None):
        member = member if member else ctx.author
        emb = discord.Embed(color = 0x2f3136)
        if not member.avatar.is_animated():
            emb.set_image(url = member.avatar.with_format('png'))
        else:
            emb.set_image(url = member.avatar.url)
        emb.set_author(name = member.display_name)
        await ctx.send(embed = emb)

    @commands.command(aliases = ['me'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def about(self, ctx, member: discord.Member = None):
        target = member if member else ctx.author
        is_bot = 'Да' if target.bot else 'Нет'
        embed = discord.Embed(color = 0x2f3136, timestamp = discord.utils.utcnow())
        embed.set_author(name = target.display_name)
        embed.add_field(name = 'ID', value = target.id)
        if ctx.guild:
            created_at = target.created_at.strftime('%d.%m.%Y %H:%M:%S GMT')
            joined_at = target.joined_at.strftime('%d.%m.%Y %H:%M:%S GMT')
            embed.add_field(name = 'Создан', value = created_at, inline = False)
            embed.add_field(name = 'Вошёл', value = joined_at, inline = False)
        embed.add_field(name = 'Упоминание', value = target.mention)
        embed.add_field(name = 'Глобальное имя', value = target.name)
        if target.nick:
            embed.add_field(name = 'Никнейм', value = target.nick)
        status_map = {
            discord.Status.online: 'В сети',
            discord.Status.dnd: 'Не беспокоить',
            discord.Status.idle: 'Не активен',
            discord.Status.offline: 'Не в сети',
        }
        status = status_map.get(target.status, 'Неизвестно')
        embed.add_field(name = 'Статус', value = status)
        if ctx.guild:
            roles = ', '.join([role.name for role in target.roles[1:]])
        embed.add_field(name = 'Бот?', value = is_bot)
        if len(target.roles) > 1 and ctx.guild:
            embed.add_field(name = f'Роли ({len(target.roles)-1})', value = roles, inline = False)
            embed.add_field(name = 'Высшая роль', value = target.top_role.mention, inline = False)
        embed.set_thumbnail(url = target.avatar.url)
        await ctx.send(embed = embed)

async def setup(client):
    await client.add_cog(Misc(client))
