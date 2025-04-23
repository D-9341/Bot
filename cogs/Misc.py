import random

import discord
from datetime import timedelta
from discord.ext import commands

class Misc(commands.Cog):
    def __init__(self, client):
        self.client: commands.Bot = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Модуль Misc загружен')

    @commands.command()
    async def roll(self, ctx: commands.Context, first: str | int = None, second: int = None):
        if not first and not second:
            rand = random.randint(0, 100)
            if rand == 42:
                await ctx.send(embed = discord.Embed(description = f'{ctx.author.display_name} получает случайное число (0-100)\n`100`', color = 0xff8000))
            else:
                rand1 = random.randint(0, 9)
                rand2 = random.randint(0, 9)
                await ctx.send(embed = discord.Embed(description = f'{ctx.author.display_name} получает случайное число (0-100)\n`0{rand1}{rand2}`', color = 0xff8000))
        if first and not second:
            if '-' in first:
                [first, second] = first.split('-')
                first, second = int(first), int(second)
                if first > second:
                    return await ctx.send(embed = discord.Embed(description = f'{ctx.author.display_name} получает случайное число ({first}-{first})\n`{first}`', color = 0xff8000))
                rand = random.randint(first, second)
                await ctx.send(embed = discord.Embed(description = f'{ctx.author.display_name} получает случайное число ({first}-{second})\n`{rand}`', color = 0xff8000))
            if first == 'adamant':
                await ctx.send(embed = discord.Embed(description = f'{ctx.author.display_name} получает случайное число \n`5 6 4 7 0 -9 9 2 π √2 Ω א`', color = 0xff8000))
            if 'd' in first:
                [dice_amount, dice_edges] = first.split('d')
                dice_amount, dice_edges = int(dice_amount), int(dice_edges)
                if dice_amount == 1 and dice_edges == 2:
                    return await self.coinflip(ctx)
                if ctx.author.id not in self.client.owner_ids:
                    if dice_amount > 20:
                        return await ctx.send(embed = discord.Embed(description = 'Нельзя бросить больше 20 дайсов', color = 0xff0000))
                    if dice_edges > 20:
                        return await ctx.send(embed = discord.Embed(description = 'Вы не можете кинуть дайс с большим количеством граней, чем 20', color = 0xff8000))
                if dice_amount > 1:
                    results = ''
                    result = 0
                    for i in range(1, dice_amount + 1):
                        rand = random.randint(1, dice_edges)
                        results += f'{i}. `{rand}`\n'
                        result += rand
                    results += f'В сумме - ||{result}||'
                else:
                    res = random.randint(1, dice_edges)
                    total = ''
                    if res == 1 and dice_edges == 20:
                        total = ', критический провал'
                    if res == 20:
                        total = ', критический успех!'
                    return await ctx.send(embed = discord.Embed(description = f'Получено случайное число: `{res}`{total}', color = 0xff8000))
                await ctx.send(embed = discord.Embed(description = results, color = 0xff8000))
            else:
                first = int(first)
                rand = random.randint(0, first)
                await ctx.send(embed = discord.Embed(description = f'{ctx.author.display_name} получает случайное число (0-{first})\n`{rand:>02}`', color=0xff8000))
        if (first and second) or (first == 0 and second):
            first = int(first)
            if first > second:
                return await ctx.send(embed = discord.Embed(description = f'{ctx.author.display_name} получает случайное число ({first}-{first})\n`{first}`', color = 0xff8000))
            rand = random.randint(first, second)
            await ctx.send(embed = discord.Embed(description = f'{ctx.author.display_name} получает случайное число ({first}-{second})\n`{rand}`', color = 0xff8000))

    @commands.command(aliases = ['c', 'coin'])
    async def coinflip(self, ctx: commands.Context):
        coin = random.choice(['ОРЁЛ', 'РЕШКА'])
        await ctx.send(embed = discord.Embed(description = f'{ctx.author.mention} подбрасывает монетку: {coin}', color = 0xff8000))

    @commands.command()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def someone(self, ctx: commands.Context, *, text):
        member = random.choice(ctx.channel.members)
        emb = discord.Embed(description = f'{text}', color =  0x2f3136, timestamp = discord.utils.utcnow())
        emb.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar.url)
        return await ctx.send(f'@someone ||{member.mention}||', embed = emb)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def rolemembers(self, ctx: commands.Context, role: discord.Role):
        emb = discord.Embed(color = 0xff8000)
        if len(role.members) != 0:
            emb.add_field(name = f'Участники с ролью {role} ({len(role.members)})', value = ', '.join([member.mention for member in role.members]))
        else:
            emb.description = f'Роли {role.name} нет ни у кого.'
        await ctx.send(embed = emb)

    @commands.command(aliases = ['guild'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def serverinfo(self, ctx: commands.Context):
        guild = ctx.guild
        emb = discord.Embed(color = 0x2f3136, timestamp = discord.utils.utcnow())
        emb.set_author(name = guild, icon_url = guild.icon.url if guild.icon else None)
        emb.add_field(name = 'ID сервера', value = guild.id)
        emb.add_field(name = 'Владелец', value = guild.owner.mention)
        emb.add_field(name = 'Участников', value = f'{guild.member_count}\n**Из них ботов:** {len(list(filter(lambda m: m.bot, guild.members)))}\n**Из них людей:** {len(list(filter(lambda m: not m.bot, guild.members)))}')
        emb.add_field(name = 'Каналов', value = f'Текстовых {len(guild.text_channels)} | Голосовых {len(guild.voice_channels)}')
        roles = ', '.join([role.name for role in guild.roles[1:]][::-1])
        if len(roles) > 1:
            emb.add_field(name = f'Роли ({len(guild.roles)-1})', value = roles, inline = False)
        d = (guild.created_at + timedelta(hours = 3)).strftime('%d.%m.%Y %H:%M:%S GMT +3')
        emb.add_field(name = 'Дата создания сервера', value = f'{d}', inline = False)
        emb.set_thumbnail(url = guild.icon.url if guild.icon else None)
        await ctx.send(embed = emb)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def roleinfo(self, ctx: commands.Context, role: discord.Role):
        is_mentionable = 'Да' if role.mentionable else 'Нет'
        is_managed = 'Да' if role.managed else 'Нет'
        is_hoisted = 'Да' if role.hoist else 'Нет'
        emb = discord.Embed(title = role.name, color = 0x2f3136)
        emb.add_field(name = 'ID', value = role.id)
        emb.add_field(name = 'Цвет', value = role.color)
        emb.add_field(name = 'Упоминается?', value = is_mentionable)
        emb.add_field(name = 'Управляется интеграцией?', value = is_managed)
        emb.add_field(name = 'Позиция в списке', value = role.position)
        d = (role.created_at + timedelta(hours = 3)).strftime('%d.%m.%Y %H:%M:%S GMT +3')
        emb.add_field(name = 'Создана', value = f'{d}', inline = False)
        emb.add_field(name = 'Показывает участников отдельно?', value = is_hoisted)
        await ctx.send(embed = emb)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def avatar(self, ctx: commands.Context, member: discord.User = None):
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
    async def about(self, ctx: commands.Context, member: discord.Member = None):
        target = member if member else ctx.author
        is_bot = 'Да' if target.bot else 'Нет'
        emb = discord.Embed(color = 0x2f3136, timestamp = discord.utils.utcnow())
        emb.set_author(name = target.display_name if target.id != 694170281270312991 else 'Это я!', icon_url = target.avatar.url)
        emb.add_field(name = 'ID', value = target.id)
        created_at = (target.created_at + timedelta(hours = 3)).strftime('%d.%m.%Y %H:%M:%S GMT +3')
        emb.add_field(name = 'Создан', value = created_at, inline = False)
        if ctx.guild:
            joined_at = (target.joined_at + timedelta(hours = 3)).strftime('%d.%m.%Y %H:%M:%S GMT +3')
            emb.add_field(name = 'Вошёл', value = joined_at, inline = False)
        emb.add_field(name = 'Упоминание', value = target.mention)
        emb.add_field(name = 'Глобальное имя', value = target.name)
        if target.nick:
            emb.add_field(name = 'Никнейм', value = target.nick)
        status_map = {
            discord.Status.online: 'В сети',
            discord.Status.dnd: 'Не беспокоить',
            discord.Status.idle: 'Не активен',
            discord.Status.offline: 'Не в сети'
        }
        emb.add_field(name = 'Статус', value = status_map.get(target.status, 'Неизвестно'))
        emb.add_field(name = 'Бот?', value = is_bot)
        if ctx.guild:
            roles = ', '.join([role.name for role in target.roles[1:]])
            if len(roles) > 1:
                emb.add_field(name = f'Роли ({len(target.roles)-1})', value = roles, inline = False)
                emb.add_field(name = 'Высшая роль', value = target.top_role.name)
        emb.set_thumbnail(url = target.avatar.url)
        await ctx.send(embed = emb)

async def setup(client):
    await client.add_cog(Misc(client))
