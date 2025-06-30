import asyncio
import datetime
import string
import random

import discord
from discord.ext import commands

from functions import translate, get_locale, parse_members, get_plural_form
from main import bot_owner_or_has_permissions

class CancelButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label = 'Отменить', style = discord.ButtonStyle.red, custom_id = 'cancel')

class ConfirmButton(discord.ui.Button):
    def __init__(self, style = discord.ButtonStyle.green):
        super().__init__(label = 'Да', style = style, custom_id = 'yes')

class DenyButton(discord.ui.Button):
    def __init__(self, style = discord.ButtonStyle.red):
        super().__init__(label = 'Нет', style = style, custom_id = 'no')

class Mod(commands.Cog):
    def __init__(self, client):
        self.client: commands.Bot = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Модуль Mod загружен')

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.check(bot_owner_or_has_permissions(view_audit_log = True))
    async def dm(self, ctx: commands.Context, member: discord.Member, * , text):
        locale = get_locale(ctx.author.id)
        emb = discord.Embed(description = f'{text}', color = 0x2f3136)
        emb.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar.url)
        await member.send(embed = emb)
        await ctx.send(embed = discord.Embed(description = translate(locale, 'dm'), color = 0xff8000))

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.bot_has_permissions(kick_members = True)
    @commands.check(bot_owner_or_has_permissions(kick_members = True))
    async def kick(self, ctx: commands.Context, member: discord.Member, *, reason = None):
        locale = get_locale(ctx.author.id)
        bot = discord.utils.get(ctx.guild.members, id = self.client.user.id)
        if member.id not in self.client.owner_ids:
            if reason is None:
                reason = f'{translate(locale, 'reason')}'.format(sentence = 'кик с этого сервера')
            if member == ctx.author:
                emb = discord.Embed(description = translate(locale, 'kick_member_is_author'), color = discord.Color.blurple())
                return await ctx.send(embed = emb)
            if ctx.author.top_role == member.top_role:
                emb = discord.Embed(description = f'{translate(locale, "kick_member_top_eq_author")}'.format(author_mention = ctx.author.mention, member_mention = member.mention), color = 0xff8000)
                await ctx.send(embed = emb)
            elif member.top_role > ctx.author.top_role:
                emb = discord.Embed(description = f'{translate(locale, "kick_member_top_gt_author")}'.format(author_mention = ctx.author.mention, member_mention = member.mention), color = 0xff8000)
                await ctx.send(embed = emb)
            elif member.top_role == bot.top_role:
                emb = discord.Embed(description = f'{translate(locale, "kick_member_top_eq_bot")}'.format(author_mention = ctx.author.mention, member_mention = member.mention), color = 0xff0000)
                await ctx.send(embed = emb)
            elif member.top_role > bot.top_role:
                emb = discord.Embed(description = f'{translate(locale, "kick_member_top_gt_bot")}'.format(author_mention = ctx.author.mention, member_mention = member.mention), color = 0xff0000)
                await ctx.send(embed = emb)
            else:
                emb = discord.Embed(color = 0xff8000)
                emb.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar.url)
                emb.add_field(name = 'Был кикнут', value = member.mention)
                emb.add_field(name = 'По причине', value = reason)
                await ctx.send(embed = emb)
                await member.kick(reason = reason)
        else:
            emb = discord.Embed(description = f'{translate(locale, "kick_attempt_to_kick_dev")}'.format(author_mention = ctx.author.mention), color = 0xff0000)
            await ctx.send(embed = emb)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.bot_has_permissions(ban_members = True)
    @commands.check(bot_owner_or_has_permissions(ban_members = True))
    async def ban(self, ctx: commands.Context, member: discord.Member, *, reason = None):
        locale = get_locale(ctx.author.id)
        bot = discord.utils.get(ctx.guild.members, id = self.client.user.id)
        if member.id not in self.client.owner_ids:
            if reason is None:
                reason = f'{translate(locale, 'reason')}'.format(sentence = 'бан на этом сервере')
            if member == ctx.author:
                emb = discord.Embed(description = f'{translate(locale, "ban_member_is_author")}', color = discord.Color.blurple())
                return await ctx.send(embed = emb)
            if ctx.author.top_role == member.top_role:
                emb = discord.Embed(description = f'{translate(locale, "ban_member_top_eq_author")}'.format(author_mention = ctx.author.mention, member_mention = member.mention), color = 0xff8000)
                await ctx.send(embed = emb)
            elif member.top_role > ctx.author.top_role:
                emb = discord.Embed(description = f'{translate(locale, "ban_member_top_gt_author")}'.format(author_mention = ctx.author.mention, member_mention = member.mention), color = 0xff8000)
                await ctx.send(embed = emb)
            elif member.top_role == bot.top_role:
                emb = discord.Embed(description = f'{translate(locale, "ban_member_top_eq_bot")}'.format(author_mention = ctx.author.mention, member_mention = member.mention), color = 0xff0000)
                await ctx.send(embed = emb)
            elif member.top_role > bot.top_role:
                emb = discord.Embed(description = f'{translate(locale, "ban_member_top_gt_bot")}'.format(author_mention = ctx.author.mention, member_mention = member.mention), color = 0xff0000)
                await ctx.send(embed = emb)
            else:
                emb = discord.Embed(color = 0xff8000)
                emb.set_author(name = ctx.author, icon_url = ctx.author.avatar.url)
                is_softban = '--soft' in reason
                ban_reason = reason.replace('--reason', '').strip() if '--reason' in reason else reason
                emb.add_field(name = 'Упрощённо забанен' if is_softban else 'Забанен', value = f'{member.mention} ({member.display_name})')
                emb.add_field(name = 'По причине', value = ban_reason)
                await ctx.send(embed = emb)
                await member.ban(reason = ban_reason)
                if is_softban:
                    await member.unban(reason = '--softban')
        else:
            emb = discord.Embed(description = f'{translate(locale, "ban_attempt_to_ban_dev")}'.format(author_mention = ctx.author.mention), color = 0xff0000)
            await ctx.send(embed = emb)

    @commands.command()
    @commands.bot_has_permissions(manage_roles = True)
    @commands.check(bot_owner_or_has_permissions(manage_roles = True))
    async def give(self, ctx: commands.Context, member: discord.Member, roles: commands.Greedy[discord.Role]):
        locale = get_locale(ctx.author.id)
        bot = ctx.guild.get_member(self.client.user.id)
        added_roles = []
        for role in roles:
            if role.name in {'Muted', 'Deafened'}:
                if member.id in self.client.owner_ids:
                    await ctx.send(embed = discord.Embed(description = translate(locale, "give_attempt_to_mute_dev"), color = 0xff0000))
                if member == ctx.author:
                    await ctx.send(embed = discord.Embed(description = translate(locale, "attempt_to_mute_self"), color = 0xff0000))
                await member.add_roles(role)
                await ctx.send(embed = discord.Embed(description = translate(locale, "give_mute").format(author_mention = ctx.author.mention, member_mention = member.mention), color = 0x2f3136))
            if role > ctx.author.top_role:
                await ctx.send(embed = discord.Embed(description = f'{translate(locale, "give_role_gt_author_top")}'.format(role_mention = role.mention), color = 0xff8000))
            if role == ctx.author.top_role:
                await ctx.send(embed = discord.Embed(description = f'{translate(locale, "give_role_eq_author_top")}'.format(role_mention = role.mention), color = 0xff8000))
            if role > bot.top_role:
                await ctx.send(embed = discord.Embed(description = f'{translate(locale, "give_role_gt_bot_top")}'.format(role_mention = role.mention), color = 0xff0000))
            if role == bot.top_role:
                await ctx.send(embed = discord.Embed(description = f'{translate(locale, "give_role_eq_bot_top")}'.format(role_mention = role.mention), color = 0xff0000))
            if role.is_default():
                await ctx.send(embed = discord.Embed(description = translate(locale, "give_everyone"), color = 0xff8000))
            else:
                added_roles.append(role)
        for role in added_roles:
            await member.add_roles(role)
        if not added_roles:
            await ctx.send(embed = discord.Embed(description = 'Никакие роли не были выданы', color = 0xff8000))
        else:
            await ctx.send(embed = discord.Embed(description = f'{', '.join(role.mention for role in added_roles)} {'была выдана' if len(added_roles) == 1 else 'были выданы'} {member.mention}', color = 0xff8000))

    @commands.command()
    @commands.bot_has_permissions(manage_roles = True)
    @commands.check(bot_owner_or_has_permissions(manage_roles = True))
    async def take(self, ctx: commands.Context, member: discord.Member, roles: commands.Greedy[discord.Role]):
        locale = get_locale(ctx.author.id)
        bot = ctx.guild.get_member(self.client.user.id)
        removed_roles = []
        for role in roles:
            if role.name in {'Muted', 'Deafened'}:
                if member.id in self.client.owner_ids:
                    await ctx.send(embed = discord.Embed(description = translate(locale, "take_attempt_to_mute_dev"), color = 0xff0000))
                if member == ctx.author:
                    await ctx.send(embed = discord.Embed(description = translate(locale, "attempt_to_mute_self"), color = 0xff0000))
                await member.add_roles(role)
                await ctx.send(embed = discord.Embed(description = translate(locale, "take_mute").format(author_mention = ctx.author.mention, member_mention = member.mention), color = 0x2f3136))
            if role > ctx.author.top_role:
                await ctx.send(embed = discord.Embed(description = f'{translate(locale, "take_role_gt_author_top")}'.format(role_mention = role.mention), color = 0xff8000))
            if role == ctx.author.top_role:
                await ctx.send(embed = discord.Embed(description = f'{translate(locale, "take_role_eq_author_top")}'.format(role_mention = role.mention), color = 0xff8000))
            if role > bot.top_role:
                await ctx.send(embed = discord.Embed(description = f'{translate(locale, "take_role_gt_bot_top")}'.format(role_mention = role.mention), color = 0xff0000))
            if role == bot.top_role:
                await ctx.send(embed = discord.Embed(description = f'{translate(locale, "take_role_eq_bot_top")}'.format(role_mention = role.mention), color = 0xff0000))
            if role.is_default():
                await ctx.send(embed = discord.Embed(description = translate(locale, "take_everyone"), color = 0xff8000))
            else:
                removed_roles.append(role)
        for role in removed_roles:
            await member.remove_roles(role)
        if not removed_roles:
            await ctx.send(embed = discord.Embed(description = 'Никакие роли не были забраны', color = 0xff8000))
        else:
            await ctx.send(embed = discord.Embed(description = f'{", ".join(role.mention for role in removed_roles)} {"была забрана" if len(removed_roles) == 1 else "были забраны"} у {member.mention}', color = 0xff8000))

    @commands.command()
    @commands.bot_has_permissions(manage_roles = True)
    @commands.check(bot_owner_or_has_permissions(view_audit_log = True))
    async def mute(self, ctx: commands.Context, member: discord.Member, *, reason = None):
        locale = get_locale(ctx.author.id)
        if reason is None:
            reason = f'{translate(locale, 'reason')}'.format(sentence = 'забор у тебя права писать в чат')
        role = discord.utils.get(ctx.guild.roles, name = 'Muted')
        if role in member.roles:
            emb = discord.Embed(description = translate(locale, "mute_member_has_role"), color = 0x2f3136)
            return await ctx.send(embed = emb)
        if member == ctx.author:
            emb = discord.Embed(description = translate(locale, "attempt_to_mute_self"), color = discord.Color.blurple())
            return await ctx.send(embed = emb)
        if member.id not in self.client.owner_ids:
            if ctx.author.top_role == member.top_role:
                emb = discord.Embed(description = f'{translate(locale, "mute_member_top_eq_author_top")}'.format(author_mention = ctx.author.mention, member_mention = member.mention), color = 0xff8000)
                await ctx.send(embed = emb)
            elif ctx.author.top_role < member.top_role:
                emb = discord.Embed(description = f'{translate(locale, "mute_member_top_gt_author_top")}'.format(author_mention = ctx.author.mention, member_mention = member.mention), color = 0xff8000)
                await ctx.send(embed = emb)
            else:
                if not role:
                    role = await ctx.guild.create_role(name = 'Muted', color = 0x000001, reason = 'Создано автоматически командой mute')
                await member.add_roles(role, reason = reason)
                emb = discord.Embed(color = 0xff8000, timestamp = discord.utils.utcnow())
                emb.add_field(name = 'Заглушён', value = f'{member.mention}')
                emb.add_field(name = 'Причина', value = reason)
                await ctx.send(embed = emb)
        else:
            emb = discord.Embed(description = f'{translate(locale, "attempt_to_mute_dev")}'.format(author_mention = ctx.author.mention), color = 0xff0000)
            await ctx.send(embed = emb)

    @commands.command()
    @commands.bot_has_permissions(moderate_members = True)
    @commands.check(bot_owner_or_has_permissions(manage_roles = True))
    async def timeout(self, ctx: commands.Context, member: discord.Member, *, reason = None):
        locale = get_locale(ctx.author.id)
        if reason is None:
            reason = f'{translate(locale, 'reason')}'.format(sentence = 'забор у тебя права писать в чат и говорить в голосовом канале')
        if member.id not in self.client.owner_ids:
            if member == ctx.author:
                emb = discord.Embed(description = translate(locale, "attempt_to_mute_self"), color = discord.Color.blurple())
                await ctx.send(embed = emb)
            if ctx.author.top_role == member.top_role:
                emb = discord.Embed(description = f'{translate(locale, "timeout_member_top_eq_author_top")}'.format(author_mention = ctx.author.mention, member_mention = member.mention), color = 0xff8000)
                await ctx.send(embed = emb)
            elif ctx.author.top_role < member.top_role:
                emb = discord.Embed(description = f'{translate(locale, "timeout_member_top_gt_author_top")}'.format(author_mention = ctx.author.mention, member_mention = member.mention), color = 0xff8000)
                await ctx.send(embed = emb)
            else:
                await member.timeout(datetime.timedelta(hours = 1), reason = reason)
                emb = discord.Embed(title = f'Тайм-аут участника {member.display_name}', color = 0xff8000, timestamp = discord.utils.utcnow())
                emb.add_field(name = 'Причина', value = reason)
                emb.add_field(name = 'Время тайм-аута', value = '1 час')
                await ctx.send(embed = emb)
        else:
            emb = discord.Embed(description = f'{translate(locale, "attempt_to_mute_dev")}'.format(author_mention = ctx.author.mention), color = 0xff0000)
            await ctx.send(embed = emb)

    @commands.command()
    @commands.bot_has_permissions(manage_roles = True)
    @commands.check(bot_owner_or_has_permissions(manage_roles = True))
    async def deaf(self, ctx: commands.Context, member: discord.Member, *, reason = None):
        locale = get_locale(ctx.author.id)
        role = discord.utils.get(ctx.guild.roles, name = 'Deafened')
        if reason is None:
            reason = f'{translate(locale, 'reason')}'.format(sentence = 'забор у тебя права говорить в голосовом канале')
        if role in member.roles:
                emb = discord.Embed(description = translate(locale, "deaf_member_has_role"), color = 0x2f3136)
                return await ctx.send(embed = emb)
        if member.id not in self.client.owner_ids:
            if member == ctx.author:
                emb = discord.Embed(description = translate(locale, "attempt_to_mute_self"), color = discord.Color.blurple())
                await ctx.send(embed = emb)
            if ctx.author.top_role == member.top_role:
                emb = discord.Embed(description = f'{translate(locale, "deaf_member_top_eq_author_top")}'.format(author_mention = ctx.author.mention, member_mention = member.mention), color = 0xff8000)
                await ctx.send(embed = emb)
            elif ctx.author.top_role < member.top_role:
                emb = discord.Embed(description = f'{translate(locale, "deaf_member_top_gt_author_top")}'.format(author_mention = ctx.author.mention, member_mention = member.mention), color = 0xff8000)
                await ctx.send(embed = emb)
            else:
                if not role:
                    role = await ctx.guild.create_role(name = 'Deafened', color = 0x000001, reason = 'Создано автоматически командой deaf')
                await member.add_roles(role, reason = reason)
                emb = discord.Embed(color = 0x2f3136, timestamp = discord.utils.utcnow())
                emb.add_field(name = 'Заглушён', value = member.mention)
                emb.add_field(name = 'Причина', value = reason)
                await ctx.send(embed = emb)
        else:
            emb = discord.Embed(description = translate(locale, 'attempt_to_mute_dev'), color = 0xff0000)
            await ctx.send(embed = emb)

    @commands.command()
    @commands.bot_has_permissions(manage_roles = True)
    @commands.check(bot_owner_or_has_permissions(manage_roles = True))
    async def undeaf(self, ctx: commands.Context, member: discord.Member, *, reason = None):
        locale = get_locale(ctx.author.id)
        role = discord.utils.get(ctx.guild.roles, name = 'Deafened')
        if reason is None:
            reason = f'{translate(locale, 'reason')}'.format(sentence = 'помилование и восстановление права говорить в голосовом канале')
        if role:
            if role in member.roles:
                await member.remove_roles(role, reason = reason)
                emb = discord.Embed(title = f'{translate(locale, "undeaf_success")}'.format(member = member), color = 0xff8000, timestamp = discord.utils.utcnow())
                emb.add_field(name = 'Снял заглушение', value = ctx.author.mention)
                emb.add_field(name = 'Причина', value = reason)
                await ctx.send(embed = emb)
            else:
                emb = discord.Embed(description = translate(locale, 'undeaf_member_has_no_role'), color = 0xff8000)
                await ctx.send(embed = emb)
        else:
            emb = discord.Embed(description = f'{translate(locale, "undeaf_no_role")}'.format(author_mention = ctx.author.mention, member_mention = member.mention), color = 0xff8000, timestamp = discord.utils.utcnow())
            await ctx.send(embed = emb)

    @commands.command()
    @commands.bot_has_permissions(manage_roles = True)
    @commands.check(bot_owner_or_has_permissions(manage_roles = True))
    async def unmute(self, ctx: commands.Context, member: discord.Member, *, reason = None):
        locale = get_locale(ctx.author.id)
        role = discord.utils.get(ctx.guild.roles, name = 'Muted')
        if reason is None:
            reason = f'{translate(locale, 'reason')}'.format(sentence = 'помилование и восстановление права писать в чат')
        if role is not None:
            if role in member.roles:
                await member.remove_roles(role, reason = reason)
                emb = discord.Embed(title = f'{translate(locale, "unmute_success")}'.format(member = member), color = 0xff8000, timestamp = discord.utils.utcnow())
                emb.add_field(name = 'Снял заглушение', value = ctx.author.mention)
                emb.add_field(name = 'По причине', value = reason)
                await ctx.send(embed = emb)
            else:
                emb = discord.Embed(description = translate(locale, 'unmute_member_has_no_role'), color = 0xff8000)
                await ctx.send(embed = emb)
        else:
            emb = discord.Embed(description = f'{translate(locale, "unmute_no_role")}'.format(author_mention = ctx.author.mention), color = 0xff8000, timestamp = discord.utils.utcnow())
            await ctx.send(embed = emb)

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.user)
    @commands.bot_has_permissions(manage_messages = True)
    @commands.check(bot_owner_or_has_permissions(administrator = True))
    async def clear(self, ctx: commands.Context, amount: int, members = '--everyone', *, filt = None):
        await ctx.message.delete()
        if members == 'self':
            if ctx.author.id not in self.client.owner_ids:
                raise commands.NotOwner()
            cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.author.id == self.client.user.id)
            return await ctx.send(embed = discord.Embed(description = f'Удалено {len(cleared)} {get_plural_form(len(cleared), ["сообщение", "сообщения", "сообщений"])} бота', color = 0xff8000))
        args = parse_members(members)
        check_func = lambda m: m.pinned is False and ((not args.bots or m.author.bot) and (not args.users or not m.author.bot) or args.everyone) and (not filt or m.content.lower() == filt)
        authors = {}
        if not args.silent:
            async for message in ctx.channel.history(limit = amount):
                if message.author not in authors:
                    authors[message.author] = 1
                else:
                    authors[message.author] += 1
        if amount == 2472:
            sus = self.client.get_user(338714886001524737)
            pro = self.client.get_user(417012231406878720)
            if ctx.author.id in self.client.owner_ids:
                if ctx.guild.id == 693929822543675455 and ctx.author.id != 338714886001524737:
                    emb = discord.Embed(description = 'Даже будучи разработчиком бота ты не имеешь права выполнить это действие на этом сервере', color = 0xff0000)
                    emb.set_footer(text = f'Выполнил {ctx.author.display_name}')
                    await ctx.send(embed = emb)
                    await sus.send(embed = emb)
                elif ctx.guild.id == 693929822543675455 and ctx.author.id == 338714886001524737:
                    emb = discord.Embed(description = 'Даже ты не можешь выполнить это действие на этом сервере', color = 0xff8000)
                    await ctx.send(embed = emb)
                else:
                    random_pass = ''.join(random.choice(string.digits) for _ in range(6))
                    member = sus if ctx.author.id == 417012231406878720 else pro
                    await member.send(embed = discord.Embed(description = f'{ctx.author.mention} хочет удалить канал `{ctx.channel.name}` на сервере {ctx.guild}. Для подтверждения введите код: `{random_pass}` - у вас есть 30 секунд', color = 0xff0000))
                    try:
                        code = await self.client.wait_for('message', check = lambda message: message.author == member, timeout = 30)
                        if code.content == random_pass:
                            await ctx.channel.delete()
                            emb = discord.Embed(description = f'Канал `{ctx.channel.name}` на сервере {ctx.guild} удалён', color = 0xff0000)
                            emb.set_footer(text = f'Выполнил: {ctx.author.display_name}')
                            await sus.send(embed = emb)
                            await pro.send(embed = emb)
                        else:
                            emb = discord.Embed(description = 'Код подтверждения неверный', color = 0xff0000)
                            await sus.send(embed = emb)
                            await pro.send(embed = emb)
                    except asyncio.TimeoutError:
                        await sus.send(embed = discord.Embed(description = 'Время вышло', color = 0xff0000))
                        await pro.send(embed = discord.Embed(description = 'Время вышло', color = 0xff0000))
            else:
                raise commands.NotOwner()
        elif amount >= 300:
            emb = discord.Embed(description = f'{ctx.author.mention}, при таком числе удаления сообщений `{amount}` последует большое время ожидания ответа {self.client.user.mention}', color = 0x2f3136)
            await ctx.send(f'{ctx.guild.owner.mention}', embed = emb)
        elif amount >= 250:
            if ctx.author != ctx.guild.owner:
                emb = discord.Embed(description = f'{ctx.author.mention}, операция с данным числом `{amount}` доступна только {ctx.guild.owner.mention}', color = 0x2f3136)
                await ctx.send(f'{ctx.guild.owner.mention}', embed = emb)
            else:
                emb = discord.Embed(description = f'{ctx.author.mention}, это слишком большое число для удаления сообщений (`{amount}`). Возможно большое время ожидания ответа {self.client.user.mention}, которое может усугубится разницей во времени между предыдущими сообщениями и сообщением содержащим команду **и повлияет не только на этот сервер!** Продолжить? (y/n)\n||Отмена через 20 секунд||', color = 0x2f3136)
                view = discord.ui.View()
                view.add_item(ConfirmButton(discord.ButtonStyle.red))
                view.add_item(DenyButton(discord.ButtonStyle.green))
                sent = await ctx.send(embed = emb, view = view)
                try:
                    interaction = await self.client.wait_for('interaction', timeout = 20, check = lambda i: i.channel == ctx.message.channel)
                    if interaction.data['custom_id'] == 'yes' and interaction.user.id == ctx.guild.owner.id:
                        await interaction.response.defer()
                        await sent.delete()
                        if not args.silent:
                            emb = discord.Embed(description = 'Удаляем..', color = 0x2f3136)
                            sent = await ctx.send(embed = emb)
                        cleared = await ctx.channel.purge(limit = amount, check = check_func, before = sent if not args.silent else None)
                        if not args.silent:
                            view = discord.ui.View()
                            view.add_item(CancelButton())
                            try:
                                emb = discord.Embed(title = 'Результаты удаления сообщений', color = 0x2f3136)
                                emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{len(cleared)} / {amount}```')
                                if filt:
                                    args_list = []
                                    if args.bots or args.everyone:
                                        args_list.append('боты')
                                    if args.users or args.everyone:
                                        args_list.append('пользователи')
                                    emb.add_field(name = 'Применён фильтр:', value = f'```{filt} ({", ".join(args_list) if len(args_list) != 2 else 'каждое сообщение'})```', inline = True)
                                emb.add_field(name = 'Найдены сообщения от:', value = ''.join([f"```ARM\n{author.display_name}: {amount}```" for author, amount in authors.items()]), inline = False)
                                emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены нажмите на кнопку "Отменить"')
                                await sent.edit(embed = emb, view = view)
                                await self.client.wait_for('interaction', timeout = 10, check = lambda i: i.channel == ctx.message.channel and i.user == ctx.author and i.data['custom_id'] == 'cancel')
                                emb.set_footer(text = None)
                                await sent.edit(embed = emb, view = None)
                            except asyncio.TimeoutError:
                                await sent.delete()
                    elif interaction.data['custom_id'] == 'no' and (interaction.user.id == ctx.guild.owner.id or interaction.user.id in self.client.owner_ids):
                        await interaction.response.defer()
                        await sent.delete()
                        emb = discord.Embed(description = f'{ctx.guild.owner.mention} отменил операцию', color = 0x2f3136)
                        await ctx.send(embed = emb)
                    elif interaction.data['custom_id'] == 'yes' or interaction.data['custom_id'] == 'no' and interaction.user.id != ctx.guild.owner.id:
                        await interaction.response.defer()
                        await sent.delete()
                        emb = discord.Embed(description = f'{ctx.author.mention}, ты не являешься владельцем сервера', color = 0x2f3136)
                        await ctx.send(embed = emb)
                except asyncio.TimeoutError:
                    await sent.delete()
                    emb = discord.Embed(description = f'{ctx.author.mention}, время вышло', color = 0x2f3136)
                    await ctx.send(f'{ctx.guild.owner.mention}', embed = emb)
        elif amount >= 100:
            emb = discord.Embed(description = f'{ctx.author.mention}, для удаления `{amount}` сообщений нужно подтверждение. {'Мне нужен ответ создателя сервера на это действие. ' if ctx.author != ctx.guild.owner else ''}Продолжить?\n||Запрос будет отменён через {'1 минуту' if ctx.author != ctx.guild.owner else '10 секунд'}||', color = 0x2f3136)
            view = discord.ui.View()
            view.add_item(ConfirmButton())
            view.add_item(DenyButton())
            sent = await ctx.send(f'{ctx.guild.owner.mention}' if ctx.author != ctx.guild.owner else None, embed = emb, view = view)
            try:
                interaction = await self.client.wait_for('interaction', timeout = 60 if ctx.author != ctx.guild.owner else 10, check = lambda i: i.channel == ctx.message.channel)
                if interaction.data['custom_id'] == 'yes' and interaction.user.id == ctx.guild.owner.id:
                    await interaction.response.defer()
                    await sent.delete()
                    if not args.silent:
                        emb = discord.Embed(description = 'Удаляем..', color = 0x2f3136)
                        sent = await ctx.send(embed = emb)
                    cleared = await ctx.channel.purge(limit = amount, check = check_func, before = sent if not args.silent else None)
                    if not args.silent:
                        view = discord.ui.View()
                        view.add_item(CancelButton())
                        try:
                            emb = discord.Embed(title = 'Результаты удаления сообщений', color = 0x2f3136)
                            emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{len(cleared)} / {amount}```')
                            if filt:
                                args_list = []
                                if args.bots or args.everyone:
                                    args_list.append('боты')
                                if args.users or args.everyone:
                                    args_list.append('пользователи')
                                emb.add_field(name = 'Применён фильтр:', value = f'```{filt} ({", ".join(args_list) if len(args_list) != 2 else 'каждое сообщение'})```', inline = True)
                            emb.add_field(name = 'Найдены сообщения от:', value = ''.join([f"```ARM\n{author.display_name}: {amount}```" for author, amount in authors.items()]), inline = False)
                            emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены нажмите на кнопку "Отменить"')
                            await sent.edit(embed = emb, view = view)
                            await self.client.wait_for('interaction', timeout = 10, check = lambda i: i.channel == ctx.message.channel and i.user == ctx.author and i.data['custom_id'] == 'cancel')
                            emb.set_footer(text = None)
                            await sent.edit(embed = emb, view = None)
                        except asyncio.TimeoutError:
                            await sent.delete()
                elif interaction.data['custom_id'] == 'no' and (interaction.user.id == ctx.guild.owner.id or interaction.user.id in self.client.owner_ids):
                    await interaction.response.defer()
                    await sent.delete()
                    emb = discord.Embed(description = f'{ctx.guild.owner.mention} отменил операцию', color = 0x2f3136)
                    await ctx.send(embed = emb)
                elif interaction.data['custom_id'] == 'yes' or interaction.data['custom_id'] == 'no' and interaction.user.id != ctx.guild.owner.id:
                    await interaction.response.defer()
                    await sent.delete()
                    emb = discord.Embed(description = f'{ctx.author.mention}, ты не являешься владельцем сервера', color = 0x2f3136)
                    await ctx.send(embed = emb)
            except asyncio.TimeoutError:
                    await sent.delete()
                    emb = discord.Embed(description = f'{ctx.author.mention}, время вышло', color = 0x2f3136)
                    await ctx.send(f'{ctx.guild.owner.mention}', embed = emb)
        elif amount >= 10:
            emb = discord.Embed(description = f'{ctx.author.mention}, для удаления `{amount}` сообщений нужно подтверждение. Продолжить?', color = 0x2f3136)
            view = discord.ui.View()
            view.add_item(ConfirmButton())
            view.add_item(DenyButton())
            sent = await ctx.send(embed = emb, view = view)
            try:
                interaction = await self.client.wait_for('interaction', timeout = 10, check = lambda i: i.user == ctx.author and i.channel == ctx.channel)
                if interaction.data['custom_id'] == 'yes':
                    await interaction.response.defer()
                    await sent.delete()
                    if not args.silent:
                        emb = discord.Embed(description = 'Удаляем..', color = 0x2f3136)
                        sent = await ctx.send(embed = emb)
                    cleared = await ctx.channel.purge(limit = amount, check = check_func, before = sent if not args.silent else None)
                    if not args.silent:
                        emb = discord.Embed(title = 'Результаты удаления сообщений', color = 0x2f3136)
                        emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{len(cleared)} / {amount}```')
                        if filt:
                            args_list = []
                            if args.bots or args.everyone:
                                args_list.append('боты')
                            if args.users or args.everyone:
                                args_list.append('пользователи')
                            emb.add_field(name = 'Применён фильтр:', value = f'```{filt} ({", ".join(args_list) if len(args_list) != 2 else 'каждое сообщение'})```', inline = True)
                        emb.add_field(name = 'Найдены сообщения от:', value = ''.join([f"```ARM\n{author.display_name}: {amount}```" for author, amount in authors.items()]), inline = False)
                        emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены нажмите на кнопку "Отменить"')
                        view = discord.ui.View()
                        view.add_item(CancelButton())
                        await sent.edit(embed = emb, view = view)
                        try:
                            interaction = await self.client.wait_for('interaction', timeout = 10, check = lambda i: i.user == ctx.author and i.channel == ctx.channel and i.data['custom_id'] == 'cancel')
                            await interaction.response.defer()
                            emb.set_footer(text = None)
                            await sent.edit(embed = emb, view = None)
                        except asyncio.TimeoutError:
                            await sent.delete()
                elif interaction.data['custom_id'] == 'no':
                    await interaction.response.defer()
                    await sent.delete()
                    emb = discord.Embed(description = f'{ctx.guild.owner.mention} отменил операцию', color = 0x2f3136)
                    await ctx.send(embed = emb)
            except asyncio.TimeoutError:
                await sent.delete()
                emb = discord.Embed(description = f'{ctx.author.mention}, время вышло', color = 0x2f3136)
                await ctx.send(embed = emb)
        elif amount == 0:
            emb = discord.Embed(description = 'Удалять 0 сообщений? Ты еблан?', color = 0x2f3136)
            await ctx.send(embed = emb)
        else:
            if not args.silent:
                emb = discord.Embed(description = 'Удаляем..', color = 0x2f3136)
                sent = await ctx.send(embed = emb)
            cleared = await ctx.channel.purge(limit = amount, check = check_func, before = sent if not args.silent else None)
            if not args.silent:
                view = discord.ui.View()
                view.add_item(CancelButton())
                try:
                    emb = discord.Embed(title = 'Результаты удаления сообщений', color = 0x2f3136)
                    emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{len(cleared)} / {amount}```')
                    if filt:
                        args_list = []
                        if args.bots or args.everyone:
                            args_list.append('боты')
                        if args.users or args.everyone:
                            args_list.append('пользователи')
                        emb.add_field(name = 'Применён фильтр:', value = f'```{filt} ({", ".join(args_list) if len(args_list) != 2 else 'каждое сообщение'})```', inline = True)
                    emb.add_field(name = 'Найдены сообщения от:', value = ''.join([f"```ARM\n{author.display_name}: {amount}```" for author, amount in authors.items()]), inline = False)
                    emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены нажмите на кнопку "Отменить"')
                    await sent.edit(embed = emb, view = view)
                    await self.client.wait_for('interaction', timeout = 10, check = lambda i: i.channel == ctx.message.channel and i.user == ctx.author and i.data['custom_id'] == 'cancel')
                    emb.set_footer(text = None)
                    await sent.edit(embed = emb, view = None)
                except asyncio.TimeoutError:
                    await sent.delete()

async def setup(client):
    await client.add_cog(Mod(client))
