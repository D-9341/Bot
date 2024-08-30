import asyncio
import datetime
import string
import random

import discord
from functions import translate, get_locale
from discord.ext import commands

class Mod(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Модуль Mod загружен')

    @commands.command()
    @commands.has_permissions(view_audit_log = True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def dm(self, ctx, member: discord.Member, * , text):
        locale = get_locale(ctx.author.id)
        emb = discord.Embed(description = f'{text}', color = 0x2f3136)
        emb.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar.url)
        await member.send(embed = emb)
        await ctx.send(embed = discord.Embed(description = translate(locale, 'dm'), color = 0xff8000))

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.bot_has_permissions(kick_members = True)
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, member: discord.Member, *, reason: str = None):
        locale = get_locale(ctx.author.id)
        bot = discord.utils.get(ctx.guild.members, id = self.client.user.id)
        if member.id not in self.client.owner_ids:
            if reason is None:
                reason = translate(locale, 'reason')
            if member == ctx.author:
                emb = discord.Embed(description = translate(locale, 'kick_member_is_author') , color = discord.Color.blurple())
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
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, member: discord.Member, *, reason: str = None):
        locale = get_locale(ctx.author.id)
        bot = discord.utils.get(ctx.guild.members, id = self.client.user.id)
        if member.id not in self.client.owner_ids:
            if reason is None:
                reason = translate(locale, 'reason')
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
                emb.add_field(name = 'Упрощённо забанен' if '--soft' in reason else 'Забанен', value = f'{member.mention} ({member.display_name})')
                if '--reason' in reason:
                    reason = reason.strip()[15:].strip()
                emb.add_field(name = 'По причине', value = reason)
                await ctx.send(embed = emb)
                await member.ban(reason = reason)
                if '--soft' in reason:
                    await member.unban(reason = '--softban')
        else:
            emb = discord.Embed(description = f'{translate(locale, "ban_attempt_to_ban_dev")}'.format(author_mention = ctx.author.mention), color = 0xff0000)
            await ctx.send(embed = emb)

    @commands.command()
    @commands.bot_has_permissions(manage_roles = True)
    @commands.has_permissions(manage_channels = True)
    async def give(self, ctx, member: discord.Member, role: discord.Role):
        locale = get_locale(ctx.author.id)
        bot = ctx.guild.get_member(self.client.user.id)
        if role.name == 'Muted' or role.name == 'Deafened':
            if member.id not in self.client.owner_ids:
                if member == ctx.author:
                    emb = discord.Embed(description = f'{translate(locale, "attempt_to_mute_self")}', color = 0xff0000)
                    return await ctx.send(embed = emb)
                else:
                    await member.add_roles(role)
                    emb = discord.Embed(description = f'{translate(locale, "give_mute")}'.format(author_mention = ctx.author.mention, member_mention = member.mention), color = 0x2f3136)
                    return await ctx.send(embed = emb)
            else:
                emb = discord.Embed(description = translate(locale, "give_attempt_to_mute_dev"), color = 0xff0000)
                return await ctx.send(embed = emb)
        else:
            if role > ctx.author.top_role:
                emb = discord.Embed(description = f'{translate(locale, "give_role_gt_author_top")}'.format(role_mention = role.mention), color = 0xff8000)
                await ctx.send(embed = emb)
            elif role == ctx.author.top_role:
                emb = discord.Embed(description = f'{translate(locale, "give_role_eq_author_top")}'.format(role_mention = role.mention), color = 0xff8000)
                await ctx.send(embed = emb)
            elif role > bot.top_role:
                emb = discord.Embed(description = f'{translate(locale, "give_role_gt_bot_top")}'.format(role_mention = role.mention), color = 0xff0000)
                await ctx.send(embed = emb)
            elif role == bot.top_role:
                emb = discord.Embed(description = f'{translate(locale, "give_role_eq_bot_top")}'.format(role_mention = role.mention), color = 0xff0000)
                await ctx.send(embed = emb)
            elif role.is_default():
                emb = discord.Embed(description = translate(locale, "give_everyone"), color = 0xff8000)
                await ctx.send(embed = emb)
            else:
                await member.add_roles(role)
                emb = discord.Embed(color = 0xff8000, timestamp = discord.utils.utcnow())
                emb.add_field(name = 'ВЫДАНА_РОЛЬ', value = f'{role.mention} | {role.name} | {role.id}')
                emb.add_field(name = 'ВЫДАНА:', value = member.mention, inline = False)
                emb.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar.url)
                await ctx.send(embed = emb)

    @commands.command()
    @commands.bot_has_permissions(manage_roles = True)
    @commands.has_permissions(manage_channels = True)
    async def take(self, ctx, member: discord.Member, role: discord.Role):
        locale = get_locale(ctx.author.id)
        bot = ctx.guild.get_member(self.client.user.id)
        if role.name == 'Muted' or role.name == 'Deafened':
            await member.remove_roles(role)
            emb = discord.Embed(description = f'{translate(locale, "take_mute")}'.format(author_mention = ctx.author.mention, member_mention = member.mention), color = 0xff8000)
            return await ctx.send(embed = emb)
        if role > ctx.author.top_role:
            emb = discord.Embed(description = f'{translate(locale, "take_role_gt_author_top")}'.format(role_mention = role.mention), color = 0x2f3136)
            await ctx.send(embed = emb)
        elif role == ctx.author.top_role:
            emb = discord.Embed(description = f'{translate(locale, "take_role_eq_author_top")}'.format(role_mention = role.mention), color = 0x2f3136)
            await ctx.send(embed = emb)
        elif role > bot.top_role:
            emb = discord.Embed(description = f'{translate(locale, "take_role_gt_bot_top")}'.format(role_mention = role.mention), color = 0xff0000)
            await ctx.send(embed = emb)
        elif role == bot.top_role:
            emb = discord.Embed(description = f'{translate(locale, "take_role_eq_bot_top")}'.format(role_mention = role.mention), color = 0xff0000)
            await ctx.send(embed = emb)
        elif role.is_default():
            emb = discord.Embed(description = translate(locale, "take_everyone"), color = 0xffffff)
            await ctx.send(embed = emb)
        else:
            await member.remove_roles(role)
            emb = discord.Embed(color = 0xff8000, timestamp = discord.utils.utcnow())
            emb.add_field(name = 'ЗАБРАНА_РОЛЬ', value = f'{role.mention} | {role.name} | {role.id}')
            emb.add_field(name = 'ЗАБРАНА_У:', value = member.mention, inline = False)
            emb.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar.url)
            await ctx.send(embed = emb)

    @commands.command()
    @commands.bot_has_permissions(manage_roles = True)
    @commands.has_permissions(view_audit_log = True)
    async def mute(self, ctx, member: discord.Member, *, reason = None):
        locale = get_locale(ctx.author.id)
        if reason is None:
            reason = translate(locale, 'reason')
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
                await member.add_roles(role)
                emb = discord.Embed(color = 0xff8000, timestamp = discord.utils.utcnow())
                emb.add_field(name = 'Заглушён', value = f'{member.mention}')
                emb.add_field(name = 'Причина', value = reason)
                await ctx.send(embed = emb)
        else:
            emb = discord.Embed(description = f'{translate(locale, "attempt_to_mute_dev")}'.format(author_mention = ctx.author.mention), color = 0xff0000)
            await ctx.send(embed = emb)

    @commands.command()
    @commands.bot_has_permissions(moderate_members = True)
    @commands.has_permissions(manage_channels = True)
    async def timeout(self, ctx, member: discord.Member, *, reason = None):
        locale = get_locale(ctx.author.id)
        if reason is None:
            reason = translate(locale, 'reason')
        if member.id not in self.client.owner_ids:
            if member == ctx.author:
                emb = discord.Embed(description = translate(locale, "attempt_to_mute_self"), color = discord.Color.blurple())
                await ctx.send(embed = emb)
            if ctx.author.top_role == member.top_role:
                emb = discord.Embed(description = f'{translate(locale, "timeout_member_top_eq_author_top")}'.format(author_mention = ctx.author.mention, member_mention = member.mention), color = 0xff8000)
                await ctx.send(embed = emb)
            elif ctx.author.top_role < member.top_role:
                emb = discord.Embed(description = f'{translate(locale, "timeout_member_top_gt_author_top")}', color = 0xff8000)
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

    @commands.command(aliases = ['silencio'])
    @commands.bot_has_permissions(manage_roles = True)
    @commands.has_permissions(manage_channels = True)
    async def deaf(self, ctx, member: discord.Member, *, reason = None):
        locale = get_locale(ctx.author.id)
        role = discord.utils.get(ctx.guild.roles, name = 'Deafened')
        if reason is None:
            reason = translate(locale, 'reason')
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
                await member.add_roles(role)
                emb = discord.Embed(color = 0x2f3136, timestamp = discord.utils.utcnow())
                emb.add_field(name = 'Заглушён', value = member.mention)
                emb.add_field(name = 'Причина', value = reason)
                await ctx.send(embed = emb)
        else:
            emb = discord.Embed(description = translate(locale, 'attempt_to_mute_dev'), color = 0xff0000)
            await ctx.send(embed = emb)

    @commands.command()
    @commands.bot_has_permissions(manage_roles = True)
    @commands.has_permissions(manage_channels = True)
    async def undeaf(self, ctx, member: discord.Member, *, reason = None):
        locale = get_locale(ctx.author.id)
        role = discord.utils.get(ctx.guild.roles, name = 'Deafened')
        if reason is None:
            reason = translate(locale, 'reason')
        if role:
            if role in member.roles:
                await member.remove_roles(role)
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
    @commands.has_permissions(manage_channels = True)
    async def unmute(self, ctx, member: discord.Member, *, reason = None):
        locale = get_locale(ctx.author.id)
        role = discord.utils.get(ctx.guild.roles, name = 'Muted')
        if reason is None:
            reason = translate(locale, 'reason')
        if role is not None:
            if role in member.roles:
                await member.remove_roles(role)
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
    @commands.has_permissions(administrator = True)
    async def clear(self, ctx, amount: int, members = '--everyone', *, filt = None):
        await ctx.message.delete()
        authors = {}
        if not '--silent' in members:
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
                    emb = discord.Embed(description = 'Даже будучи разработчиком бота ты не имеешь права выполнить это действие на этом сервере.', color = 0xff0000)
                    emb.set_footer(text = f'Выполнил {ctx.author.display_name}')
                    await ctx.send(embed = emb)
                    await sus.send(embed = emb)
                elif ctx.guild.id == 693929822543675455 and ctx.author.id == 338714886001524737:
                    emb = discord.Embed(description = 'Даже ты не можешь выполнить это действие на этом сервере.', color = 0xff8000)
                    await ctx.send(embed = emb)
                else:
                    random_pass = ''.join(random.choice(string.digits) for _ in range(6))
                    if ctx.author.id == sus.id:
                        await pro.send(embed = discord.Embed(description = f'{sus.mention} хочет удалить канал `{ctx.channel.name}` на сервере {ctx.guild}. Для подтверждения введите код: `{random_pass}` - у вас есть 30 секунд', color = 0xff0000))
                        try:
                            code = await self.client.wait_for('message', check = lambda message: message.author == pro, timeout = 30)
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
                    elif ctx.author.id == pro.id:
                        await sus.send(embed = discord.Embed(description = f'{pro.mention} хочет удалить канал `{ctx.channel.name}` на сервере {ctx.guild}. Для подтверждения введите код: `{random_pass}` - у вас есть 30 секунд', color = 0xff0000))
                        try:
                            code = await self.client.wait_for('message', check = lambda message: message.author == sus, timeout = 30)
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
            emb = discord.Embed(description = f'{ctx.author.mention}, при таком числе удаления сообщений ({amount}) последует большое время ожидания ответа {self.client.user.mention}', color = 0x2f3136)
            await ctx.send(f'{ctx.guild.owner.mention}', embed = emb)
        elif amount >= 250:
            if ctx.author != ctx.guild.owner:
                emb = discord.Embed(description = f'{ctx.author.mention}, операция с данным числом ({amount}) доступна только {ctx.guild.owner.mention}', color = 0x2f3136)
                await ctx.send(f'{ctx.guild.owner.mention}', embed = emb, delete_after = 15)
            else:
                emb = discord.Embed(description = f'{ctx.author.mention}, это слишком большое число для удаления сообщений ({amount}). Возможно большое время ожидания ответа {self.client.user.mention}, которое может усугубится разницей во времени между предыдущими сообщениями и сообщением содержащим команду **и повлияет не только на этот сервер!** Продолжить? (y/n)\n||Отмена через 20 секунд||', color = 0x2f3136)
                sent = await ctx.send(embed = emb)
                try:
                    msg = await self.client.wait_for('message', timeout = 20, check = lambda message: message.channel == ctx.message.channel)
                    if msg.content.lower() == 'y' and msg.author.id == ctx.guild.owner.id:
                        await msg.delete()
                        await sent.delete()
                    if '--silent' not in members:
                        emb = discord.Embed(description = 'Удаляем..', color = 0x2f3136)
                        sent = await ctx.send(embed = emb)
                    if '--bots' in members and '--users' not in members:
                        if filt:
                            cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == True and m.pinned == False and m.content.lower() == filt, before = sent if '--silent' not in members else None)
                        else:
                            cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == True and m.pinned == False, before = sent if '--silent' not in members else None)
                    if '--users' in members and '--bots' not in members:
                        if filt:
                            cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False and m.pinned == False and m.content.lower() == filt, before = sent if '--silent' not in members else None)
                        else:    
                            cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False and m.pinned == False, before = sent if '--silent' not in members else None)
                    elif ('--users' in members and '--bots' in members) or '--everyone' in members:
                        if filt:
                            cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.pinned == False and m.content.lower() == filt, before = sent if '--silent' not in members else None)
                        else:
                            cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.pinned == False, before = sent if '--silent' not in members else None)
                    elif members == '--silent':
                        await ctx.channel.purge(limit = amount, check = lambda m: m.pinned == False)
                    if '--silent' not in members:
                        try:
                            emb = discord.Embed(title = 'Результаты удаления сообщений', color = 0x2f3136)
                            emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{len(cleared)} / {amount}```')
                            if filt:
                                emb.add_field(name = 'Применён фильтр:', value = f'```{filt} ({members})```', inline = True)
                            emb.add_field(name = 'Найдены сообщения от:', value = ''.join([f"```ARM\n{author.display_name} : {amount}```" for author, amount in authors.items()]), inline = False)
                            emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c".')
                            await sent.edit(embed = emb)
                            msg = await self.client.wait_for('message', timeout = 10, check = lambda message: message.channel == ctx.message.channel and message.author == ctx.author and message.content.lower() == 'c')
                            emb.set_footer(text = None)
                            await sent.edit(embed = emb)
                        except asyncio.TimeoutError:
                            await sent.delete()
                    elif msg.content.lower() == 'n' and msg.author.id == ctx.guild.owner.id:
                        await msg.delete()
                        await sent.delete()
                        emb = discord.Embed(description = f'{ctx.guild.owner.mention} отменил запрос.', color = 0x2f3136)
                        await ctx.send(embed = emb, delete_after = 3)
                    elif msg.content.lower() == 'n' or msg.content.lower() == 'y' and msg.author.id != ctx.guild.owner.id:
                        await msg.delete()
                        await sent.delete()
                        emb = discord.Embed(description = f'{ctx.author.mention}, ты не являешься владельцем сервера.', color = 0x2f3136)
                        await ctx.send(embed = emb, delete_after = 3)
                    else:
                        await msg.delete()
                        await sent.delete()
                        emb = discord.Embed(description = f'Недопустимый ответ - {msg.content}', color = 0x2f3136)
                        await ctx.send(embed = emb, delete_after = 3)
                except asyncio.TimeoutError:
                    await sent.delete()
                    emb = discord.Embed(description = f'{ctx.author.mention}, Время вышло.', color = 0x2f3136)
                    await ctx.send(f'{ctx.guild.owner.mention}', embed = emb, delete_after = 3)
        elif amount >= 100:
            if ctx.author != ctx.guild.owner:
                emb = discord.Embed(description = f'{ctx.author.mention}, создан запрос на удаление {amount} сообщений. Мне нужен ответ создателя сервера на это действие. Продолжаем? (y/n)\n||Запрос будет отменён через 1 минуту.||', color = 0x2f3136)
                sent = await ctx.send(f'{ctx.guild.owner.mention}', embed = emb)
            else:
                emb = discord.Embed(description = f'{ctx.author.mention}, создан запрос на удаление {amount} сообщений. Продолжить? (y/n)\n||Запрос будет отменён через 10 секунд.||', color = 0x2f3136)
                sent = await ctx.send(embed = emb)
            try:
                msg = await self.client.wait_for('message', timeout = 60 if ctx.author != ctx.guild.owner else 10, check = lambda message: message.channel == ctx.message.channel)
                if msg.content.lower() == 'y' and msg.author.id == ctx.guild.owner.id:
                    await msg.delete()
                    await sent.delete()
                    if '--silent' not in members:
                        emb = discord.Embed(description = 'Удаляем..', color = 0x2f3136)
                        sent = await ctx.send(embed = emb)
                    if '--bots' in members and '--users' not in members:
                        if filt:
                            cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == True and m.pinned == False and m.content.lower() == filt, before = sent if '--silent' not in members else None)
                        else:
                            cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == True and m.pinned == False, before = sent if '--silent' not in members else None)
                    if '--users' in members and '--bots' not in members:
                        if filt:
                            cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False and m.pinned == False and m.content.lower() == filt, before = sent if '--silent' not in members else None)
                        else:    
                            cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False and m.pinned == False, before = sent if '--silent' not in members else None)
                    elif ('--users' in members and '--bots' in members) or '--everyone' in members:
                        if filt:
                            cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.pinned == False and m.content.lower() == filt, before = sent if '--silent' not in members else None)
                        else:
                            cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.pinned == False, before = sent if '--silent' not in members else None)
                    elif members == '--silent':
                        await ctx.channel.purge(limit = amount, check = lambda m: m.pinned == False)
                    if '--silent' not in members:
                        try:
                            emb = discord.Embed(title = 'Результаты удаления сообщений', color = 0x2f3136)
                            emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{len(cleared)} / {amount}```')
                            if filt:
                                emb.add_field(name = 'Применён фильтр:', value = f'```{filt} ({members})```', inline = True)
                            emb.add_field(name = 'Найдены сообщения от:', value = ''.join([f"```ARM\n{author.display_name} : {amount}```" for author, amount in authors.items()]), inline = False)
                            emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c".')
                            await sent.edit(embed = emb)
                            msg = await self.client.wait_for('message', timeout = 10, check = lambda message: message.channel == ctx.message.channel and message.author == ctx.author and message.content.lower() == 'c')
                            emb.set_footer(text = None)
                            await sent.edit(embed = emb)
                        except asyncio.TimeoutError:
                            await sent.delete()
                elif msg.content.lower() == 'n' and (msg.author.id == ctx.guild.owner.id or msg.author.id in self.client.owner_ids):
                    await msg.delete()
                    await sent.delete()
                    emb = discord.Embed(description = f'{ctx.guild.owner.mention} отменил запрос', color = 0x2f3136)
                    await ctx.send(embed = emb, delete_after = 3)
                elif msg.content.lower() == 'n' or msg.content.lower() == 'y' and msg.author.id != ctx.guild.owner.id:
                    await msg.delete()
                    await sent.delete()
                    emb = discord.Embed(description = f'{ctx.author.mention}, ты не являешься владельцем сервера', color = 0x2f3136)
                    await ctx.send(embed = emb, delete_after = 3)
                else:
                    await msg.delete()
                    await sent.delete()
                    emb = discord.Embed(description = f'Недопустимый ответ - {msg.content}', color = 0x2f3136)
                    await ctx.send(embed = emb, delete_after = 3)
            except asyncio.TimeoutError:
                    await sent.delete()
                    emb = discord.Embed(description = f'{ctx.author.mention}, Время вышло.', color = 0x2f3136)
                    await ctx.send(f'{ctx.guild.owner.mention}', embed = emb, delete_after = 3)
        elif amount >= 10:
            emb = discord.Embed(description = f'{ctx.author.mention}, создан запрос на удаление {amount} сообщений. Продолжить? (y/n)\n||Запрос будет отменён через 10 секунд||', color = 0x2f3136)
            sent = await ctx.send(embed = emb)
            try:
                msg = await self.client.wait_for('message', timeout = 10, check = lambda message: message.author == ctx.author and message.channel == ctx.message.channel)
                if msg.content.lower() == 'y':
                    await msg.delete()
                    await sent.delete()
                    if '--silent' not in members:
                        emb = discord.Embed(description = 'Удаляем..', color = 0x2f3136)
                        sent = await ctx.send(embed = emb)
                    if '--bots' in members and '--users' not in members:
                        if filt:
                            cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == True and m.pinned == False and m.content.lower() == filt, before = sent if '--silent' not in members else None)
                        else:
                            cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == True and m.pinned == False, before = sent if '--silent' not in members else None)
                    if '--users' in members and '--bots' not in members:
                        if filt:
                            cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False and m.pinned == False and m.content.lower() == filt, before = sent if '--silent' not in members else None)
                        else:    
                            cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False and m.pinned == False, before = sent if '--silent' not in members else None)
                    elif ('--users' in members and '--bots' in members) or '--everyone' in members:
                        if filt:
                            cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.pinned == False and m.content.lower() == filt, before = sent if '--silent' not in members else None)
                        else:
                            cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.pinned == False, before = sent if '--silent' not in members else None)
                    elif members == '--silent':
                        await ctx.channel.purge(limit = amount, check = lambda m: m.pinned == False)
                    if '--silent' not in members:
                        try:
                            emb = discord.Embed(title = 'Результаты удаления сообщений', color = 0x2f3136)
                            emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{len(cleared)} / {amount}```')
                            if filt:
                                emb.add_field(name = 'Применён фильтр:', value = f'```{filt} ({members})```', inline = True)
                            emb.add_field(name = 'Найдены сообщения от:', value = ''.join([f"```ARM\n{author.display_name} : {amount}```" for author, amount in authors.items()]), inline = False)
                            emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c"')
                            await sent.edit(embed = emb)
                            msg = await self.client.wait_for('message', timeout = 10, check = lambda message: message.channel == ctx.message.channel and message.author == ctx.author and message.content.lower() == 'c')
                            emb.set_footer(text = None)
                            await sent.edit(embed = emb)
                        except asyncio.TimeoutError:
                            await sent.delete()
                elif msg.content.lower() == 'n':
                    await msg.delete()
                    await sent.delete()
                    emb = discord.Embed(description = 'Отменено.', color = 0x2f3136)
                    await ctx.send(embed = emb, delete_after = 3)
                else:
                    await msg.delete()
                    await sent.delete()
                    emb = discord.Embed(description = f'Недопустимый ответ - {msg.content}', color = 0x2f3136)
                    await ctx.send(embed = emb, delete_after = 3)
            except asyncio.TimeoutError:
                await sent.delete()
                emb = discord.Embed(description = f'{ctx.author.mention}, Время вышло.', color = 0x2f3136)
                await ctx.send(embed = emb, delete_after = 3)
        elif amount == 0:
            emb = discord.Embed(description = 'Удалять 0 сообщений? Ты еблан?', color = 0x2f3136)
            await ctx.send(embed = emb, delete_after = 3)
        else:
            if '--silent' not in members:
                emb = discord.Embed(description = 'Удаляем..', color = 0x2f3136)
                sent = await ctx.send(embed = emb)
            if '--bots' in members and '--users' not in members:
                if filt:
                    cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == True and m.pinned == False and m.content.lower() == filt, before = sent if '--silent' not in members else None)
                else:
                    cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == True and m.pinned == False, before = sent if '--silent' not in members else None)
            if '--users' in members and '--bots' not in members:
                if filt:
                    cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False and m.pinned == False and m.content.lower() == filt, before = sent if '--silent' not in members else None)
                else:    
                    cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False and m.pinned == False, before = sent if '--silent' not in members else None)
            elif ('--users' in members and '--bots' in members) or '--everyone' in members:
                if filt:
                    cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.pinned == False and m.content.lower() == filt, before = sent if '--silent' not in members else None)
                else:
                    cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.pinned == False, before = sent if '--silent' not in members else None)
            elif members == '--silent':
                await ctx.channel.purge(limit = amount, check = lambda m: m.pinned == False)
            if '--silent' not in members:
                try:
                    emb = discord.Embed(title = 'Результаты удаления сообщений', color = 0x2f3136)
                    emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{len(cleared)} / {amount}```')
                    if filt:
                        emb.add_field(name = 'Применён фильтр:', value = f'```{filt} ({members})```', inline = True)
                    emb.add_field(name = 'Найдены сообщения от:', value = ''.join([f"```ARM\n{author.display_name} : {amount}```" for author, amount in authors.items()]), inline = False)
                    emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c"')
                    await sent.edit(embed = emb)
                    msg = await self.client.wait_for('message', timeout = 10, check = lambda message: message.channel == ctx.message.channel and message.author == ctx.author and message.content.lower() == 'c')
                    emb.set_footer(text = None)
                    await sent.edit(embed = emb)
                except asyncio.TimeoutError:
                    await sent.delete()

async def setup(client):
    await client.add_cog(Mod(client))