import random
from datetime import timedelta

import discord
import psycopg2
from discord.ext import commands

from cogs.Constants import colors
from cogs.Logging import LOGS
from functions import get_plural_form
from main import PASSWORD

def rearm(command: commands.Command, message: discord.Message):
    if command._buckets.valid:
        bucket = command._buckets.get_bucket(message)
        bucket._tokens = min(bucket.rate, bucket._tokens + 1)

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
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        role = discord.utils.get(member.guild.roles, name = 'Deafened')
        if after.channel.name == 'Создать канал':
            conn = psycopg2.connect(host = "localhost", database = "voice_channels", user = "postgres", password = PASSWORD, port = 5432)
            cur = conn.cursor()
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
                room = 'чё' if member.bot is True else f'Канал {member.display_name}'
            else:
                room = voice_channel[0]
            channel = await member.guild.create_voice_channel(name = room, category = after.channel.category, bitrate = bitrate)
            await member.move_to(channel)
            await channel.set_permissions(member, mute_members = True, move_members = True, manage_channels = True)
            def check(a, b, c): return len(channel.members) == 0
            await self.client.wait_for('voice_state_update', check = check)
            cur.execute("INSERT INTO channels (user_id, name) VALUES (%s, %s) ON CONFLICT (user_id) DO UPDATE SET name = %s", (member.id, channel.name, channel.name))
            conn.commit()
            LOGS.write(f'[DB] {(discord.utils.utcnow() + timedelta(hours = 3)).strftime('%d.%m.%Y %H:%M:%S')} Запись в БД voice_channels: {member.id} ({member.display_name}): {channel.name}\n')
            LOGS.flush()
            conn.close()
            await channel.delete()
        if role in member.roles:
            await member.edit(mute = True, reason = 'Заглушён командой deaf')

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.id == 417012231406878720:
            if 'во лох' in message.content.lower():
                return await message.channel.send('сам лох')
        if message.author.bot is False:
            conn = psycopg2.connect(
                host = "localhost",
                database = "locales",
                user = "postgres",
                password = PASSWORD,
                port = 5432
            )
            cur = conn.cursor()
            cur.execute("INSERT INTO users (user_id, locale) VALUES (%s, %s) ON CONFLICT (user_id) DO NOTHING", (message.author.id, 'ru'))
            conn.commit()
            conn.close()
        if message.content.startswith(f'<@{self.client.user.id}>') and len(message.content) == len(f'<@{self.client.user.id}>') and message.author.id not in self.client.owner_ids:
            await message.channel.send(f'чё звал {message.author.mention} ||`cy/`||')
        # if message.channel.id == 1345125935636283504 and not message.author.bot:
        #     role = discord.utils.get(message.guild.roles, id = 1314332101512007741)
        #     sent = await message.channel.send(role.mention)
        #     await sent.delete()
        if message.channel.id == 1041417879788208169:
            if message.author.bot is True and message.author.id != 694170281270312991:
                role = discord.utils.get(message.guild.roles, id = 1078051320088510644)
                sent = await message.channel.send(role.mention)
                await sent.delete()
                channel = self.client.get_channel(714175791033876490)
                emb = discord.Embed(title = r'ОПОВЕЩЕНИЕ\_ОБ_ОБНОВЛЕНИИ', color = colors.JDH, timestamp = discord.utils.utcnow())
                emb.add_field(name = 'ОПОВЕЩЕНЫ', value = 'РАЗРАБОТЧИКИ')
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
            rearm(ctx.command, ctx.message)
            if ctx.command.name == 'clear':
                await ctx.send('```apache\ncy/clear <количество> [диапазон] [фильтр]\ncy/clear 10\ncy/clear 50 --everyone хыха\ncy/clear 30 --bots\ncy/clear 15 --users\ncy/clear 5 --silent\ncy/clear 200 "--silent --everyone"\n\n--everyone удалит сообщения от всех\n--bots удалит сообщения только от ботов\n--users удалит сообщения только от людей\n--silent не покажет результаты удаления сообщений. Учтите, что если нужно будет подтверждение удаления - оно будет показано\nПри указании фильтра необходимо писать именно то, что написано в сообщении - команда чувствительна к регистру\n\nПри указании диапазона не будет удалено столько сообщений, сколько было указано, будет удалено столько, сколько будет найдено в пределах заданного количества сообщений\nДопустим cy/clear 10 --bots\nЕсли сообщения от ботов и людей чередуются, будет удалено лишь то кол-во сообщений от ботов, что было найдено в указанном пределе 10. Это сделано намеренно, но может быть изменено в будущем\n\nСообщения старше 2 недель будут удалены не сразу - лимит discord API\nПри удалении более 100 сообщений нужно подтверждение владельца сервера.\nТолько владелец сервера может удалять от 250 сообщений за раз.\nНе более 300 за раз!\n\n[] - опционально, <> - обязательно, / - или\nНеобходимы разрешения - права администратора\nБоту необходимы разрешения - управлять сообщениями```')
            elif ctx.command.name == 'say':
                await ctx.send('```apache\ncy/say [обычный текст] [&t title текст] [&d description текст] [&th ссылка на картинку справа] [&img ссылка на картинку снизу] [&f footer текст] [&c цвет в HEX коде] [&msg сообщение над эмбедом] [&b label текст | url ссылка]\ncy/say &t Заголовок &d Описание\ncy/say [текст]\ncy/say &b label FunClub P-sune | url https://discord.gg/rDR4SSt\nВсе аргументы являются необязательными, но если отправить пустую команду - ответом будет это сообщение\n\n[] - опционально```')
            elif ctx.command.name == 'edit':
                await ctx.send('```apache\ncy/edit <ID> [обычный текст] [&t title текст] [&d description текст] [&f footer текст] [&c цвет в HEX коде] [&th ссылка на картинку справа] [&img ссылка на картинку снизу] [&b label текст | url ссылка]\ncy/edit <ID> [текст]\ncy/edit <ID> --clean\ncy/edit <ID> --noembed\ncy/edit <ID> --delete\n\n--clean удалит контент над эмбедом\n--noembed удалит эмбед\n--delete удалит сообщение\n\nИспользование --clean и --noembed одновременно невозможно\nЕсли у сообщения есть эмбед и в команде нет агрументов, автоматически будет заменён &msg\nЗаголовок, описание и цвет будут взяты со старого эмбеда, если таковой имеется и эти аргументы не были указаны\nДля очистки какого-либо поля укажите аргумент и оставьте его пустым:\ncy/edit <ID> &d\nЭто опустошит описание\n\n[] - опционально, <> - обязательно\nНеобходимы разрешения - управлять сообщениями```')
            elif ctx.command.name == 'ban':
                await ctx.send('```apache\ncy/ban <@пинг/имя/ID> [причина/--soft --reason]\ncy/ban 185476724627210241 --soft --reason лошара\ncy/ban @сасиска чмо\ncy/ban @крипочек --soft\n\nПри использовании --soft обязательно указывать --reason __после__ него, однако можно не использовать --reason\ncy/ban adamant --soft --reason упырь\n\n[] - опционально, <> - обязательно, / - или\nНеобходимы разрешения - банить участников```')
            else:
                emb = discord.Embed(description = f'{ctx.author.mention}, предоставлено недостаточно аргументов для `{ctx.command.name}`. Попробуйте cy/help `{ctx.command.name}`', color = colors.JDH)
                emb.set_footer(text = 'Счётчик перезарядки сброшен')
                await ctx.send(embed = emb)
        elif isinstance(error, commands.MemberNotFound):
            rearm(ctx.command, ctx.message)
            emb = discord.Embed(description = f'{ctx.author.mention}, участник не найден', color = colors.JDH)
            emb.set_footer(text = 'Счётчик перезарядки сброшен')
            await ctx.send(embed = emb)
        elif isinstance(error, commands.BadArgument):
            rearm(ctx.command, ctx.message)
            emb = discord.Embed(description = f'{ctx.author.mention}, предоставлен неверный аргумент для `{ctx.command.name}`. Попробуйте cy/help `{ctx.command.name}`', color = colors.JDH)
            emb.set_footer(text = 'Счётчик перезарядки сброшен')
            await ctx.send(embed = emb)

async def setup(client):
    await client.add_cog(Events(client))
