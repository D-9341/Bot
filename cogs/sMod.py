import datetime

import discord
from functions import translate, get_locale
from discord import app_commands
from discord.ext import commands

class sMod(commands.Cog):
    def __init__(self, client):
        self.client: commands.Bot = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('/ - Команды Mod синхронизированы')

    @app_commands.command(description = 'Пишет участнику в лс сообщение')
    @app_commands.describe(member = 'Участник', text = 'Текст сообщения')
    @app_commands.checks.has_permissions(view_audit_log = True)
    async def dm(self, interaction: discord.Interaction, member: discord.Member, * , text: str):
        locale = get_locale(interaction.user.id)
        emb = discord.Embed(description = f'{text}', color = 0x2f3136)
        emb.set_author(name = interaction.user, icon_url = interaction.user.avatar.url)
        await member.send(embed = emb)
        await interaction.response.send_message(embed = discord.Embed(description = translate(locale, 'dm')))

    @app_commands.command(description = 'Выгоняет участника')
    @app_commands.describe(member = 'Участник', reason = 'Причина')
    @app_commands.checks.has_permissions(kick_members = True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, *, reason: str = None):
        locale = get_locale(interaction.user.id)
        bot = discord.utils.get(interaction.guild.members, id = self.client.user.id)
        if member.id not in self.client.owner_ids:
            if reason is None:
                reason = translate(locale, 'reason')
            if member == interaction.user:
                emb = discord.Embed(description = translate(locale, 'kick_member_is_author') , color = discord.Color.blurple())
                return await interaction.send(embed = emb)
            if interaction.user.top_role == member.top_role:
                emb = discord.Embed(description = f'{translate(locale, "kick_member_top_eq_author")}'.format(author_mention = interaction.user.mention, member_mention = member.mention), color = 0xff8000)
                await interaction.send(embed = emb)
            elif member.top_role > interaction.user.top_role:
                emb = discord.Embed(description = f'{translate(locale, "kick_member_top_gt_author")}'.format(author_mention = interaction.user.mention, member_mention = member.mention), color = 0xff8000)
                await interaction.send(embed = emb)
            elif member.top_role == bot.top_role:
                emb = discord.Embed(description = f'{translate(locale, "kick_member_top_eq_bot")}'.format(author_mention = interaction.user.mention, member_mention = member.mention), color = 0xff0000)
                await interaction.send(embed = emb)
            elif member.top_role > bot.top_role:
                emb = discord.Embed(description = f'{translate(locale, "kick_member_top_gt_bot")}'.format(author_mention = interaction.user.mention, member_mention = member.mention), color = 0xff0000)
                await interaction.send(embed = emb)
            else:
                emb = discord.Embed(color = 0xff8000)
                emb.set_author(name = interaction.user.display_name, icon_url = interaction.user.avatar.url)
                emb.add_field(name = 'Был кикнут', value = member.mention)
                emb.add_field(name = 'По причине', value = reason)
                await interaction.send(embed = emb)
                await member.kick(reason = reason)
        else:
            emb = discord.Embed(description = f'{translate(locale, "kick_attempt_to_kick_dev")}'.format(author_mention = interaction.user.mention), color = 0xff0000)
            await interaction.send(embed = emb)

    @app_commands.command(description = 'Блокирует участника')
    @app_commands.describe(member = 'Участник', reason = 'Причина')
    @app_commands.checks.has_permissions(ban_members = True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, *, reason: str = None):
        locale = get_locale(interaction.user.id)
        bot = discord.utils.get(interaction.guild.members, id = self.client.user.id)
        if member.id not in self.client.owner_ids:
            if reason is None:
                reason = translate(locale, 'reason')
            if member == interaction.user:
                emb = discord.Embed(description = f'{translate(locale, "ban_member_is_author")}', color = discord.Color.blurple())
                return await interaction.send(embed = emb)
            if interaction.user.top_role == member.top_role:
                emb = discord.Embed(description = f'{translate(locale, "ban_member_top_eq_author")}'.format(author_mention = interaction.user.mention, member_mention = member.mention), color = 0xff8000)
                await interaction.send(embed = emb)
            elif member.top_role > interaction.user.top_role:
                emb = discord.Embed(description = f'{translate(locale, "ban_member_top_gt_author")}'.format(author_mention = interaction.user.mention, member_mention = member.mention), color = 0xff8000)
                await interaction.send(embed = emb)
            elif member.top_role == bot.top_role:
                emb = discord.Embed(description = f'{translate(locale, "ban_member_top_eq_bot")}'.format(author_mention = interaction.user.mention, member_mention = member.mention), color = 0xff0000)
                await interaction.send(embed = emb)
            elif member.top_role > bot.top_role:
                emb = discord.Embed(description = f'{translate(locale, "ban_member_top_gt_bot")}'.format(author_mention = interaction.user.mention, member_mention = member.mention), color = 0xff0000)
                await interaction.send(embed = emb)
            else:
                emb = discord.Embed(color = 0xff8000)
                emb.set_author(name = interaction.user, icon_url = interaction.user.avatar.url)
                emb.add_field(name = 'Упрощённо забанен' if '--soft' in reason else 'Забанен', value = f'{member.mention} ({member.display_name})')
                if '--reason' in reason:
                    reason = reason.strip()[15:].strip()
                emb.add_field(name = 'По причине', value = reason)
                await interaction.send(embed = emb)
                await member.ban(reason = reason)
                if '--soft' in reason:
                    await member.unban(reason = '--softban')
        else:
            emb = discord.Embed(description = f'{translate(locale, "ban_attempt_to_ban_dev")}'.format(author_mention = interaction.user.mention), color = 0xff0000)
            await interaction.send(embed = emb)

    @app_commands.command(description = 'Выдаёт участнику роль')
    @app_commands.describe(member = 'Участник', role = 'Роль')
    @app_commands.checks.has_permissions(manage_channels = True)
    async def give(self, interaction: discord.Interaction, member: discord.Member, role: discord.Role):
        locale = get_locale(interaction.user.id)
        bot = interaction.guild.get_member(self.client.user.id)
        if role.name == 'Muted' or role.name == 'Deafened':
            if member.id not in self.client.owner_ids:
                if member == interaction.user:
                    emb = discord.Embed(description = f'{translate(locale, "attempt_to_mute_self")}', color = 0xff0000)
                    return await interaction.send(embed = emb)
                else:
                    await member.add_roles(role)
                    emb = discord.Embed(description = f'{translate(locale, "give_mute")}'.format(author_mention = interaction.user.mention, member_mention = member.mention), color = 0x2f3136)
                    return await interaction.send(embed = emb)
            else:
                emb = discord.Embed(description = translate(locale, "give_attempt_to_mute_dev"), color = 0xff0000)
                return await interaction.send(embed = emb)
        else:
            if role > interaction.user.top_role:
                emb = discord.Embed(description = f'{translate(locale, "give_role_gt_author_top")}'.format(role_mention = role.mention), color = 0xff8000)
                await interaction.send(embed = emb)
            elif role == interaction.user.top_role:
                emb = discord.Embed(description = f'{translate(locale, "give_role_eq_author_top")}'.format(role_mention = role.mention), color = 0xff8000)
                await interaction.send(embed = emb)
            elif role > bot.top_role:
                emb = discord.Embed(description = f'{translate(locale, "give_role_gt_bot_top")}'.format(role_mention = role.mention), color = 0xff0000)
                await interaction.send(embed = emb)
            elif role == bot.top_role:
                emb = discord.Embed(description = f'{translate(locale, "give_role_eq_bot_top")}'.format(role_mention = role.mention), color = 0xff0000)
                await interaction.send(embed = emb)
            elif role.is_default():
                emb = discord.Embed(description = translate(locale, "give_everyone"), color = 0xff8000)
                await interaction.send(embed = emb)
            else:
                await member.add_roles(role)
                emb = discord.Embed(color = 0xff8000, timestamp = discord.utils.utcnow())
                emb.add_field(name = 'ВЫДАНА_РОЛЬ', value = f'{role.mention} | {role.name} | {role.id}')
                emb.add_field(name = 'ВЫДАНА:', value = member.mention, inline = False)
                emb.set_author(name = interaction.user.display_name, icon_url = interaction.user.avatar.url)
                await interaction.send(embed = emb)

    @app_commands.command(description = 'Забирает роль у участника')
    @app_commands.describe(member = 'Участник', role = 'Роль')
    @app_commands.checks.has_permissions(manage_channels = True)
    async def take(self, interaction: discord.Interaction, member: discord.Member, role: discord.Role):
        locale = get_locale(interaction.user.id)
        bot = interaction.guild.get_member(self.client.user.id)
        if role.name == 'Muted' or role.name == 'Deafened':
            await member.remove_roles(role)
            emb = discord.Embed(description = f'{translate(locale, "take_mute")}'.format(author_mention = interaction.user.mention, member_mention = member.mention), color = 0xff8000)
            return await interaction.send(embed = emb)
        if role > interaction.user.top_role:
            emb = discord.Embed(description = f'{translate(locale, "take_role_gt_author_top")}'.format(role_mention = role.mention), color = 0x2f3136)
            await interaction.send(embed = emb)
        elif role == interaction.user.top_role:
            emb = discord.Embed(description = f'{translate(locale, "take_role_eq_author_top")}'.format(role_mention = role.mention), color = 0x2f3136)
            await interaction.send(embed = emb)
        elif role > bot.top_role:
            emb = discord.Embed(description = f'{translate(locale, "take_role_gt_bot_top")}'.format(role_mention = role.mention), color = 0xff0000)
            await interaction.send(embed = emb)
        elif role == bot.top_role:
            emb = discord.Embed(description = f'{translate(locale, "take_role_eq_bot_top")}'.format(role_mention = role.mention), color = 0xff0000)
            await interaction.send(embed = emb)
        elif role.is_default():
            emb = discord.Embed(description = translate(locale, "take_everyone"), color = 0xffffff)
            await interaction.send(embed = emb)
        else:
            await member.remove_roles(role)
            emb = discord.Embed(color = 0xff8000, timestamp = discord.utils.utcnow())
            emb.add_field(name = 'ЗАБРАНА_РОЛЬ', value = f'{role.mention} | {role.name} | {role.id}')
            emb.add_field(name = 'ЗАБРАНА_У:', value = member.mention, inline = False)
            emb.set_author(name = interaction.user.display_name, icon_url = interaction.user.avatar.url)
            await interaction.send(embed = emb)

    @app_commands.command(description = 'Заглушение участника')
    @app_commands.describe(member = 'Участник', reason = 'Причина')
    @app_commands.checks.has_permissions(view_audit_log = True)
    async def mute(self, interaction: discord.Interaction, member: discord.Member, *, reason: str = None):
        locale = get_locale(interaction.user.id)
        if reason is None:
            reason = translate(locale, 'reason')
        role = discord.utils.get(interaction.guild.roles, name = 'Muted')
        if role in member.roles:
            emb = discord.Embed(description = translate(locale, "mute_member_has_role"), color = 0x2f3136)
            return await interaction.send(embed = emb)
        if member == interaction.user:
            emb = discord.Embed(description = translate(locale, "attempt_to_mute_self"), color = discord.Color.blurple())
            return await interaction.send(embed = emb)
        if member.id not in self.client.owner_ids:
            if interaction.user.top_role == member.top_role:
                emb = discord.Embed(description = f'{translate(locale, "mute_member_top_eq_author_top")}'.format(author_mention = interaction.user.mention, member_mention = member.mention), color = 0xff8000)
                await interaction.send(embed = emb)
            elif interaction.user.top_role < member.top_role:
                emb = discord.Embed(description = f'{translate(locale, "mute_member_top_gt_author_top")}'.format(author_mention = interaction.user.mention, member_mention = member.mention), color = 0xff8000)
                await interaction.send(embed = emb)
            else:
                if not role:
                    role = await interaction.guild.create_role(name = 'Muted', color = 0x000001, reason = 'Создано автоматически командой mute')
                await member.add_roles(role)
                emb = discord.Embed(color = 0xff8000, timestamp = discord.utils.utcnow())
                emb.add_field(name = 'Заглушён', value = f'{member.mention}')
                emb.add_field(name = 'Причина', value = reason)
                await interaction.send(embed = emb)
        else:
            emb = discord.Embed(description = f'{translate(locale, "attempt_to_mute_dev")}'.format(author_mention = interaction.user.mention), color = 0xff0000)
            await interaction.send(embed = emb)

    @app_commands.command(description = 'Отправляет подумать участника о своём поведении')
    @app_commands.describe(member = 'Участник', reason = 'Причина')
    @app_commands.checks.has_permissions(manage_channels = True)
    async def timeout(self, interaction: discord.Interaction, member: discord.Member, *, reason: str = None):
        locale = get_locale(interaction.user.id)
        if reason is None:
            reason = translate(locale, 'reason')
        if member.id not in self.client.owner_ids:
            if member == interaction.user:
                emb = discord.Embed(description = translate(locale, "attempt_to_mute_self"), color = discord.Color.blurple())
                await interaction.send(embed = emb)
            if interaction.user.top_role == member.top_role:
                emb = discord.Embed(description = f'{translate(locale, "timeout_member_top_eq_author_top")}'.format(author_mention = interaction.user.mention, member_mention = member.mention), color = 0xff8000)
                await interaction.send(embed = emb)
            elif interaction.user.top_role < member.top_role:
                emb = discord.Embed(description = f'{translate(locale, "timeout_member_top_gt_author_top")}', color = 0xff8000)
                await interaction.send(embed = emb)
            else:
                await member.timeout(datetime.timedelta(hours = 1), reason = reason)
                emb = discord.Embed(title = f'Тайм-аут участника {member.display_name}', color = 0xff8000, timestamp = discord.utils.utcnow())
                emb.add_field(name = 'Причина', value = reason)
                emb.add_field(name = 'Время тайм-аута', value = '1 час')
                await interaction.send(embed = emb)
        else:
            emb = discord.Embed(description = f'{translate(locale, "attempt_to_mute_dev")}'.format(author_mention = interaction.user.mention), color = 0xff0000)
            await interaction.send(embed = emb)

    @app_commands.command(description = 'Отключает человеку микрофон в голосовых каналах')
    @app_commands.describe(member = 'Участник', reason = 'Причина')
    @app_commands.checks.has_permissions(manage_channels = True)
    async def deaf(self, interaction: discord.Interaction, member: discord.Member, *, reason: str = None):
        locale = get_locale(interaction.user.id)
        role = discord.utils.get(interaction.guild.roles, name = 'Deafened')
        if reason is None:
            reason = translate(locale, 'reason')
        if role in member.roles:
                emb = discord.Embed(description = translate(locale, "deaf_member_has_role"), color = 0x2f3136)
                return await interaction.send(embed = emb)
        if member.id not in self.client.owner_ids:
            if member == interaction.user:
                emb = discord.Embed(description = translate(locale, "attempt_to_mute_self"), color = discord.Color.blurple())
                await interaction.send(embed = emb)
            if interaction.user.top_role == member.top_role:
                emb = discord.Embed(description = f'{translate(locale, "deaf_member_top_eq_author_top")}'.format(author_mention = interaction.user.mention, member_mention = member.mention), color = 0xff8000)
                await interaction.send(embed = emb)
            elif interaction.user.top_role < member.top_role:
                emb = discord.Embed(description = f'{translate(locale, "deaf_member_top_gt_author_top")}'.format(author_mention = interaction.user.mention, member_mention = member.mention), color = 0xff8000)
                await interaction.send(embed = emb)
            else:
                if not role:
                    role = await interaction.guild.create_role(name = 'Deafened', color = 0x000001, reason = 'Создано автоматически командой deaf')
                await member.add_roles(role)
                emb = discord.Embed(color = 0x2f3136, timestamp = discord.utils.utcnow())
                emb.add_field(name = 'Заглушён', value = member.mention)
                emb.add_field(name = 'Причина', value = reason)
                await interaction.send(embed = emb)
        else:
            emb = discord.Embed(description = translate(locale, 'attempt_to_mute_dev'), color = 0xff0000)
            await interaction.send(embed = emb)
    
    @app_commands.command(description = 'Отменяет отключение микрофона')
    @app_commands.describe(member = 'Участник', reason = 'Причина')
    @app_commands.checks.has_permissions(manage_channels = True)
    async def undeaf(self, interaction: discord.Interaction, member: discord.Member, *, reason: str = None):
        locale = get_locale(interaction.user.id)
        role = discord.utils.get(interaction.guild.roles, name = 'Deafened')
        if reason is None:
            reason = translate(locale, 'reason')
        if role:
            if role in member.roles:
                await member.remove_roles(role)
                emb = discord.Embed(title = f'{translate(locale, "undeaf_success")}'.format(member = member), color = 0xff8000, timestamp = discord.utils.utcnow())
                emb.add_field(name = 'Снял заглушение', value = interaction.user.mention)
                emb.add_field(name = 'Причина', value = reason)
                await interaction.send(embed = emb)
            else:
                emb = discord.Embed(description = translate(locale, 'undeaf_member_has_no_role'), color = 0xff8000)
                await interaction.send(embed = emb)
        else:
            emb = discord.Embed(description = f'{translate(locale, "undeaf_no_role")}'.format(author_mention = interaction.user.mention, member_mention = member.mention), color = 0xff8000, timestamp = discord.utils.utcnow())
            await interaction.send(embed = emb)

    @app_commands.command(description = 'Разглушает участника')
    @app_commands.describe(member = 'Участник', reason = 'Причина')
    @app_commands.checks.has_permissions(manage_channels = True)
    async def unmute(self, interaction: discord.Interaction, member: discord.Member, *, reason: str = None):
        locale = get_locale(interaction.user.id)
        role = discord.utils.get(interaction.guild.roles, name = 'Muted')
        if reason is None:
            reason = translate(locale, 'reason')
        if role is not None:
            if role in member.roles:
                await member.remove_roles(role)
                emb = discord.Embed(title = f'{translate(locale, "unmute_success")}'.format(member = member), color = 0xff8000, timestamp = discord.utils.utcnow())
                emb.add_field(name = 'Снял заглушение', value = interaction.user.mention)
                emb.add_field(name = 'По причине', value = reason)
                await interaction.send(embed = emb)
            else:
                emb = discord.Embed(description = translate(locale, 'unmute_member_has_no_role'), color = 0xff8000)
                await interaction.send(embed = emb)
        else:
            emb = discord.Embed(description = f'{translate(locale, "unmute_no_role")}'.format(author_mention = interaction.user.mention), color = 0xff8000, timestamp = discord.utils.utcnow())
            await interaction.send(embed = emb) 

async def setup(client):
    await client.add_cog(sMod(client))
