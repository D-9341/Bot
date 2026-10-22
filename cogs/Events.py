import random
from datetime import timedelta

import discord
from discord.ext import commands
from contextlib import closing

from cogs.Constants import colors
from cogs.Logging import LOGS
from functions import get_plural_form, connect_db, get_locale

class Events(commands.Cog):
    def __init__(self, client):
        self.client: commands.Bot = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Модуль Events загружен')

    @commands.Cog.listener()
    async def on_guild_role_update(self, before: discord.Role, after: discord.Role):
        if before.name == 'Muted':
            role = before.guild.get_role(after.id)
            await role.edit(name = 'Muted', color = colors.BLACK, reason = 'Нельзя изменять эту роль')
        if before.name == 'Deafened':
            role = before.guild.get_role(after.id)
            await role.edit(name = 'Deafened', color = colors.BLACK, reason = 'Нельзя изменять эту роль')

    @commands.Cog.listener()
    async def on_command_completion(self, ctx: commands.Context):
        channel = self.client.get_channel(714175791033876490)
        emb = discord.Embed(title = 'ВЫПОЛНЕНИЕ_КОМАНДЫ', color = colors.JDH)
        emb.add_field(name = 'НАЗВАНИЕ', value = f'```{ctx.command.name}```')
        emb.add_field(name = 'ИСПОЛНИТЕЛЬ', value = f'{ctx.author.mention} ({ctx.author})')
        emb.add_field(name = 'СЕРВЕР', value = ctx.guild.name if ctx.guild else "ЛС", inline = False)
        emb.add_field(name = 'КАНАЛ', value = f'{ctx.channel.name} ({ctx.channel.mention})' if ctx.guild else "Недоступно в ЛС", inline = False)
        await channel.send(embed = emb)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        user = 'БОТ' if member.bot else 'УЧАСТНИК'
        channel = self.client.get_channel(714175791033876490)
        emb = discord.Embed(title = rf'{user}\_ЗАШЁЛ\_НА_СЕРВЕР', color = colors.JDH, timestamp = discord.utils.utcnow())
        emb.add_field(name = f'{user}', value = member)
        emb.add_field(name = 'УПОМИНАНИЕ', value = member.mention)
        emb.add_field(name = 'СЕРВЕР', value = member.guild.name)
        emb.set_footer(text = f'ID: {member.id}')
        await channel.send(embed = emb)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        user = 'БОТ' if member.bot else 'УЧАСТНИК'
        channel = self.client.get_channel(714175791033876490)
        emb = discord.Embed(title = rf'{user}\_ВЫШЕЛ\_С_СЕРВЕРА', color = colors.JDH, timestamp = discord.utils.utcnow())
        emb.add_field(name = f'{user}', value = member)
        emb.add_field(name = 'УПОМИНАНИЕ', value = member.mention)
        emb.add_field(name = 'СЕРВЕР', value = member.guild.name)
        emb.set_footer(text = f'ID: {member.id}')
        await channel.send(embed = emb)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        channel = self.client.get_channel(714175791033876490)
        emb = discord.Embed(title = r'ВЫХОД\_С_СЕРВЕРА', color = colors.JDH, timestamp = discord.utils.utcnow())
        emb.add_field(name = 'СЕРВЕР', value = guild.name)
        emb.set_footer(text = f'ID: {guild.id}')
        await channel.send(embed = emb)

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        channel = self.client.get_channel(714175791033876490)
        emb = discord.Embed(title = r'ДОБАВЛЕНИЕ\_НА_СЕРВЕР', color = colors.JDH, timestamp = discord.utils.utcnow())
        emb.add_field(name = 'СЕРВЕР', value = guild.name)
        emb.set_footer(text = f'ID: {guild.id}')
        await channel.send(embed = emb)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, _: discord.VoiceState, after: discord.VoiceState):
        role = discord.utils.get(member.guild.roles, name = 'Deafened')
        if role in member.roles:
            await member.edit(mute = True, reason = 'Заглушён командой deaf')
        if after.channel.name == 'Создать канал':
            with closing(connect_db('voice_channels')) as conn, conn.cursor() as cur:
                cur.execute(f"SELECT name FROM channels WHERE user_id = {member.id}")
                voice_channel = cur.fetchone()
                await after.channel.edit(user_limit = 1)
                bitrate_map = {
                    0: 96000,
                    1: 128000,
                    2: 256000,
                }
                bitrate = bitrate_map.get(member.guild.premium_tier, 384000)
                if not voice_channel:
                    room = 'чё' if member.bot else f'Канал {member.display_name}'
                else:
                    room = voice_channel[0]
                channel = await member.guild.create_voice_channel(name = room, category = after.channel.category, bitrate = bitrate)
                await member.move_to(channel)
                await channel.set_permissions(member, mute_members = True, move_members = True, manage_channels = True)
                def check(a, b, c): return len(channel.members) == 0
                await self.client.wait_for('voice_state_update', check = check)
                if not member.bot:
                    cur.execute("INSERT INTO channels (user_id, name) VALUES (%s, %s) ON CONFLICT (user_id) DO UPDATE SET name = %s", (member.id, channel.name, channel.name))
                    conn.commit()
                    LOGS.write(f'[DB] {(discord.utils.utcnow() + timedelta(hours = 3)).strftime('%d.%m.%Y %H:%M:%S')} Запись в БД voice_channels: {member.id} ({member.display_name}): {channel.name}\n')
                    LOGS.flush()
                await channel.delete()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.id == 417012231406878720:
            if 'во лох' in message.content.lower():
                return await message.channel.send('сам лох')
        if message.author.bot is False:
            with closing(connect_db()) as conn, conn.cursor() as cur:
                cur.execute("INSERT INTO users (user_id, locale) VALUES (%s, %s) ON CONFLICT (user_id) DO NOTHING", (message.author.id, 'ru'))
                conn.commit()
        if message.content.startswith(f'<@{self.client.user.id}>') and len(message.content) == len(f'<@{self.client.user.id}>') and message.author.id not in self.client.owner_ids:
            await message.channel.send(f'чё звал {message.author.mention} ||`cy/`||')
        if message.channel.id == 1345125935636283504 and not message.author.bot:
            role = discord.utils.get(message.guild.roles, id = 1314332101512007741)
            sent = await message.channel.send(role.mention)
            await sent.delete()
        if message.channel.id == 1041417879788208169:
            if message.author.bot is True and message.author.id != 694170281270312991:
                role = discord.utils.get(message.guild.roles, id = 1078051320088510644)
                sent = await message.channel.send(role.mention)
                await sent.delete()
                channel = self.client.get_channel(714175791033876490)
                emb = discord.Embed(title = r'ОПОВЕЩЕНИЕ\_ОБ_ОБНОВЛЕНИИ', color = colors.JDH, timestamp = discord.utils.utcnow())
                emb.add_field(name = 'ОПОВЕЩЕНЫ', value = 'РАЗРАБОТЧИКИ')
                await channel.send(embed = emb)
        if message.channel.id == 1552798719701688402:
            if message.author.bot is True and message.author.id != 694170281270312991:
                if 'RU:' not in message.content: return
                role = discord.utils.get(message.guild.roles, id = 1552798725926162443)
                sent = await message.channel.send(role.mention)
                await sent.delete()
                channel = self.client.get_channel(714175791033876490)
                emb = discord.Embed(title = r'ОПОВЕЩЕНИЕ\_ОБ_ОБНОВЛЕНИИ', color = colors.JDH, timestamp = discord.utils.utcnow())
                emb.add_field(name = 'ОПОВЕЩЕНЫ', value = role.mention)
                await channel.send(embed = emb)
        if message.channel.id == 750372413102883028:
            if message.author.bot is True and message.author.id != 694170281270312991:
                role = discord.utils.get(message.guild.roles, id = 750368477671325728)
                sent = await message.channel.send(role.mention)
                await sent.delete()
                channel = self.client.get_channel(714175791033876490)
                emb = discord.Embed(title = r'ОПОВЕЩЕНИЕ\_ОБ_ОБНОВЛЕНИИ', color = colors.JDH, timestamp = discord.utils.utcnow())
                emb.add_field(name = 'ОПОВЕЩЕНЫ', value = role.mention)
                await channel.send(embed = emb)
        if message.channel.id == 750368033578680361:
            if message.author.bot is True and message.author.id != 694170281270312991:
                role = discord.utils.get(message.guild.roles, id = 750366804689420319)
                sent = await message.channel.send(role.mention)
                await sent.delete()
                channel = self.client.get_channel(714175791033876490)
                emb = discord.Embed(title = r'ОПОВЕЩЕНИЕ\_ОБ_ОБНОВЛЕНИИ', color = colors.JDH, timestamp = discord.utils.utcnow())
                emb.add_field(name = 'ОПОВЕЩЕНЫ', value = role.mention)
                await channel.send(embed = emb)
        if message.channel.id == 750363498290348123:
            if message.author.bot is True and message.author.id != 694170281270312991:
                role = discord.utils.get(message.guild.roles, id = 750363797226782802)
                sent = await message.channel.send(role.mention)
                await sent.delete()
                channel = self.client.get_channel(714175791033876490)
                emb = discord.Embed(title = r'ОПОВЕЩЕНИЕ\_ОБ_ОБНОВЛЕНИИ', color = colors.JDH, timestamp = discord.utils.utcnow())
                emb.add_field(name = 'ОПОВЕЩЕНЫ', value = role.mention)
                await channel.send(embed = emb)
        if message.channel.id == 750373602460827730:
            if message.author.bot is True and message.author.id != 694170281270312991:
                role = discord.utils.get(message.guild.roles, id = 750373687479238787)
                sent = await message.channel.send(role.mention)
                await sent.delete()
                channel = self.client.get_channel(714175791033876490)
                emb = discord.Embed(title = r'ОПОВЕЩЕНИЕ\_ОБ_ОБНОВЛЕНИИ', color = colors.JDH, timestamp = discord.utils.utcnow())
                emb.add_field(name = 'ОПОВЕЩЕНЫ', value = role.mention)
                await channel.send(embed = emb)
        if message.channel.id == 707498623981715557:
            await message.add_reaction('👍')
            await message.add_reaction('👎')

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.DisabledCommand):
            await ctx.send(embed = discord.Embed(description = f'{ctx.author.mention}, команда `{ctx.command.name}` отключена', color = colors.JDH))
        elif isinstance(error, discord.NotFound):
            await ctx.send(embed = discord.Embed(description = f'{ctx.author.mention}, переданный объект не найден', color = colors.JDH))
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send(embed = discord.Embed(description = f'{ctx.author.mention}, команда `{ctx.command.name}` недоступна в ЛС', color = colors.JDH))
        elif isinstance(error, commands.NotOwner):
            await ctx.send(embed = discord.Embed(description = f'{ctx.author.mention}, это действие может совершить только один из создателей бота', color = colors.JDH))
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send(embed = discord.Embed(description = f'{ctx.author.mention}, у **меня** недостаточно прав на выполнение команды `{ctx.command.name}`, напишите cy/help `{ctx.command.name}` для просмотра необходимых прав\n||Выдача прав администратора решит эту проблему||', color = colors.ERROR))
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(embed = discord.Embed(description = f'{ctx.author.mention}, у вас недостаточно прав на выполнение команды `{ctx.command.name}`. Напишите cy/help `{ctx.command.name}` для просмотра необходимых прав', color = colors.JDH))
        elif isinstance(error, commands.CommandOnCooldown):
            seconds = round(error.retry_after)
            choises = ['Ещё не время.', 'Я не готов.', 'Ещё нет.', 'Ещё. Не. Время.', 'Я. Не. Готов.', 'Ещё. Нет.', 'ЕЩЁ НЕ ВРЕМЯ!', 'Я НЕ ГОТОВ!', 'ЕЩЁ НЕТ!']
            rand = random.choice(choises)
            await ctx.send(embed = discord.Embed(description = f'{rand} Команда `{ctx.command.name}` будет доступна через {seconds} {get_plural_form(seconds, ["секунду", "секунды", "секунд"])}!', color = colors.ERROR))
        elif isinstance(error, commands.MissingRequiredArgument):
            ctx.command.reset_cooldown(ctx)
            if ctx.command.name == 'clear':
                await self.client.get_command('help')(ctx, 'clear', get_locale(ctx.author.id))
            elif ctx.command.name == 'say':
                await ctx.send(embed = discord.Embed(description = '```apache\ncy/say [обычный текст] [&t title текст] [&d description текст] [&th ссылка на картинку справа] [&img ссылка на картинку снизу] [&f footer текст] [&c цвет в HEX коде] [&msg сообщение над эмбедом] [&b label текст | url ссылка]\ncy/say &t Заголовок &d Описание\ncy/say [текст]\ncy/say &b label FunClub P-sune | url https://discord.gg/rDR4SSt\nВсе аргументы являются необязательными, но если отправить пустую команду - ответом будет это сообщение\n\n[] - опционально```', color = colors.JDH))
            elif ctx.command.name == 'edit':
                await self.client.get_command('help')(ctx, 'edit', get_locale(ctx.author.id))
            elif ctx.command.name == 'ban':
                await self.client.get_command('help')(ctx, 'ban', get_locale(ctx.author.id))
            else:
                emb = discord.Embed(description = f'{ctx.author.mention}, предоставлено недостаточно аргументов для `{ctx.command.name}`. Попробуйте cy/help `{ctx.command.name}`', color = colors.JDH)
                emb.set_footer(text = 'Счётчик перезарядки сброшен')
                await ctx.send(embed = emb)
        elif isinstance(error, commands.MemberNotFound):
            ctx.command.reset_cooldown(ctx)
            emb = discord.Embed(description = f'{ctx.author.mention}, участник не найден', color = colors.JDH)
            emb.set_footer(text = 'Счётчик перезарядки сброшен')
            await ctx.send(embed = emb)
        elif isinstance(error, commands.BadArgument):
            ctx.command.reset_cooldown(ctx)
            emb = discord.Embed(description = f'{ctx.author.mention}, предоставлен неверный аргумент для `{ctx.command.name}`. Попробуйте cy/help `{ctx.command.name}`', color = colors.JDH)
            emb.set_footer(text = 'Счётчик перезарядки сброшен')
            await ctx.send(embed = emb)

async def setup(client):
    await client.add_cog(Events(client))
