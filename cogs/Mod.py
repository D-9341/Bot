import re
import discord
from discord.ext import commands
import datetime
import asyncio

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

class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('Дополнение Moderation успешно загружено.')
        
    @commands.command()
    @commands.has_permissions(view_audit_log = True)
    @commands.cooldown(1, 5, commands.BucketType.default)
    async def dm(self, ctx, member: discord.Member, *, arg):
        await ctx.message.delete()
        emb = discord.Embed(description = f'{arg}', colour = member.color)
        emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await member.send(embed = emb)

    @commands.command(aliases = ['Kick', 'KICK'])
    @commands.cooldown(1, 10, commands.BucketType.default)
    @commands.has_permissions(kick_members = True)
    async def kick(ctx, member: discord.Member, *, reason: str = None):
        await ctx.message.delete()
        if ctx.guild.id not in guilds:
            emb = discord.Embed(description = f'Сервер `{ctx.guild}` не имеет активных подписок. Купить можно по [Ссылке](https://www.patreon.com/cephaloncy) Преимущества: пинг не более 25ms, больший аптайм, защита от несанкционированного добавления на сервера.', colour = discord.Color.red())
            await ctx.send(embed = emb)
        else:
            if member.id != 338714886001524737:
                if reason == None:
                    reason = 'Не указана.'
                if ctx.author.top_role == member.top_role:
                    await ctx.send(f'{ctx.author.mention}, ваша высшая роль равна высшей роли {member.mention}. Отклонено')
                else:
                    emb = discord.Embed(colour = member.color)
                    emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                    emb.add_field(name = 'Был кикнут', value = member.mention)
                    emb.add_field(name = 'По причине', value = reason)
                    await ctx.send(embed = emb)
                    await member.kick(reason = reason)
            else:
                emb = discord.Embed(description = f'Извините, {ctx.author.mention}, но вы не можете кикнуть моего создателя!', colour = discord.Color.red())
                await ctx.send(embed = emb)

    @commands.command(aliases = ['Ban', 'BAN'])
    @commands.cooldown(1, 10, commands.BucketType.default)
    @commands.has_permissions(ban_members = True)
    async def ban(ctx, member: discord.Member, *, reason = None):
        await ctx.message.delete()
        if ctx.guild.id not in guilds:
            emb = discord.Embed(description = f'Сервер `{ctx.guild}` не имеет активных подписок. Купить можно по [Ссылке](https://www.patreon.com/cephaloncy) Преимущества: пинг не более 25ms, больший аптайм, защита от несанкционированного добавления на сервера.', colour = discord.Color.red())
            await ctx.send(embed = emb)
        else:
            if member.id != 338714886001524737:
                if reason == None:
                    reason = 'Не указана.'
                if ctx.author.top_role == member.top_role:
                    await ctx.send(f'{ctx.author.mention}, ваша высшая роль равна высшей роли {member.mention}. Отклонено')
                else:
                    emb = discord.Embed(colour = member.color)
                    emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                    emb.add_field(name = 'Был кикнут', value = member.mention)
                    emb.add_field(name = 'По причине', value = reason)
                    await ctx.send(embed = emb)
                    await member.ban(reason = reason)
            else:
                emb = discord.Embed(description = f'Извините, {ctx.author.mention}, но вы не можете забанить моего создателя!', colour = discord.Color.red())
                await ctx.send(embed = emb)

    @commands.command(aliases = ['Give', 'GIVE'])
    @commands.has_permissions(manage_channels = True)
    async def give(self, ctx, member: discord.Member, *, role: discord.Role):
        await ctx.message.delete()
        if role != None:
            if role > member.top_role and ctx.message.author.id != 338714886001524737:
                await ctx.send('Вы не можете выдать эту роль, так как она имеет более высокий ранг, чем ваша высшая роль.')
            elif role == ctx.author.top_role and ctx.message.author.id != 338714886001524737:
                await ctx.send('Вы не можете выдать эту роль кому-либо, так как она равна вашей высшей роли.')
            elif role.is_default():
                await ctx.send('Выдавать everyone? Всё с башкой хорошо?')
            else:
                await member.add_roles(role)
                channel = self.client.get_channel(714175791033876490)
                emb = discord.Embed(colour = member.color, timestamp = ctx.message.created_at)
                emb.add_field(name = 'Была выдана роль', value = f'{role.mention} | {role.name} | ID {role.id}')
                emb.add_field(name = 'Выдана:', value = member.mention)
                emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
                await channel.send(embed = emb)
        else:
            emb = discord.Embed(description = f'{ctx.author.mention}, я не могу найти {role.mention} в списке ролей.', colour = member.color, timestamp = ctx.message.created_at)
            emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
            await ctx.send(embed = emb)
            
    @commands.command(aliases = ['Take', 'TAKE'])
    @commands.has_permissions(manage_channels = True)
    async def take(self, ctx, member: discord.Member, *, role: discord.Role):
        await ctx.message.delete()
        if role != None:
            if role > ctx.author.top_role and ctx.message.author.id != 338714886001524737:
                await ctx.send('Вы не можете забрать эту роль, так как она имеет более высокий ранг, чем ваша высшая роль.')
            elif role == ctx.author.top_role and ctx.message.author.id != 338714886001524737:
                await ctx.send('Вы не можете забрать эту роль у кого-либо, так как она равна вашей высшей роли.')
            elif role.is_default():
                await ctx.send('Забирать everyone? Всё с башкой хорошо?')
            else:
                await member.add_roles(role)
                channel = self.client.get_channel(714175791033876490)
                emb = discord.Embed(colour = member.color, timestamp = ctx.message.created_at)
                emb.add_field(name = 'Была забрана роль', value = f'{role.mention} | {role.name} | ID {role.id}')
                emb.add_field(name = 'Забрана:', value = member.mention)
                emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
                await channel.send(embed = emb)
        else:
            emb = discord.Embed(description = f'{ctx.author.mention}, я не могу найти {role.mention} в списке ролей.', colour = member.color, timestamp = ctx.message.created_at)
            emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
            await ctx.send(embed = emb)
            
    @commands.command(aliases = ['Mute', 'MUTE'])
    @commands.has_permissions(manage_channels = True)
    async def mute(self, ctx, member: discord.Member, time: TimeConverter, *, reason: str = None):
        await ctx.message.delete()
        if member.id != 338714886001524737:
            role = discord.utils.get(ctx.guild.roles, name = 'Muted')
            if role != None:
                await member.add_roles(role)
                if reason == None:
                    reason = 'Не указана'
                emb = discord.Embed(colour = member.color, timestamp = ctx.message.created_at)
                emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                emb.add_field(name = 'В муте', value = f'{member.mention}')
                emb.add_field(name = 'По причине', value = reason)
                emb.add_field(name = 'Время мута', value = f'{time}s')
                emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
                await ctx.send(embed = emb, delete_after = time)
                await asyncio.sleep(time)
                if role != None:
                    if role in member.roles:
                        emb = discord.Embed(colour = member.color, timestamp = ctx.message.created_at)
                        emb.add_field(name = 'Размучен по истечению времени', value = member.mention)
                        emb.add_field(name = 'Был в муте по причине', value = reason)
                        emb.add_field(name = 'Время мута составляло', value = f'{time}s')
                        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
                        await member.remove_roles(role)
                        await ctx.send(f'{member.mention}', embed = emb)
                    else:
                        emb = discord.Embed(description = f'Снятие мута для {member.mention} не требуется. Роли Muted не обнаружено в списке ролей участника.', colour = discord.Color.red())
                        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
                        await ctx.send(embed = emb)
                else:
                    emb = discord.Embed(description = f'{ctx.author.mention}, Я не могу снять мут у {member.mention} из-за того, что роль Muted была удалена/отредактирована!', colour = discord.Color.orange(), timestamp = ctx.message.created_at)
                    emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
                    await ctx.send(embed = emb)
            else:
                await ctx.guild.create_role(name = 'Muted', colour = discord.Colour(0x000001))
                role = discord.utils.get(ctx.guild.roles, name = 'Muted')
                emb1 = discord.Embed(description = f'{ctx.author.mention}, По причине того, что я не нашёл нужную роль, была создана роль {role.name} с цветом {role.colour}.', colour = discord.Color.orange(), timestamp = ctx.message.created_at)
                emb1.set_footer(text = 'Это сообщение должно показываться только 1 раз. Иначе, роль была удалена/отредактирована')
                await ctx.send(embed = emb1)
                await asyncio.sleep(3)
                role = discord.utils.get(ctx.guild.roles, name = 'Muted')
                await member.add_roles(role)
                emb = discord.Embed(colour = member.color, timestamp = ctx.message.created_at)
                emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                emb.add_field(name = 'В муте', value = f'{member.mention}')
                emb.add_field(name = 'По причине', value = reason)
                emb.add_field(name = 'Время мута', value = f'{time}s')
                emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
                await ctx.send(embed = emb, delete_after = time)
                await asyncio.sleep(time)
                if role != None:
                    if role in member.roles:
                        emb = discord.Embed(colour = member.color, timestamp = ctx.message.created_at)
                        emb.add_field(name = 'Размучен по истечению времени', value = member.mention)
                        emb.add_field(name = 'По причине', value = reason)
                        emb.add_field(name = 'Время мута составляло', value = f'{time}s')
                        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
                        await ctx.send(f'{member.mention}', embed = emb)
                        await member.remove_roles(role)
                    else:
                        emb = discord.Embed(description = f'Снятие мута для {member.mention} не требуется. Роли Muted не обнаружено в списке ролей участника.', colour = discord.Color.red())
                        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
                        await ctx.send(embed = emb)
        else:
            emb = discord.Embed(description = f'Извините, {ctx.author.mention}, но вы не можете замутить моего создателя!', colour = discord.Color.orange())
            emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
            await ctx.send(embed = emb)
        
    @commands.command(aliases = ['Unmute', 'UNMUTE'])
    @commands.has_permissions(manage_channels = True)
    async def unmute(self, ctx, member: discord.Member, *, reason = None):
        await ctx.message.delete()
        role = discord.utils.get(ctx.guild.roles, name = 'Muted')
        if role != None:
            if role in member.roles:
                await member.remove_roles(role)
                if reason == None:
                    reason = 'Не указана.'
                emb = discord.Embed(title = f'Принудительное снятие мута у {member}', colour = member.color, timestamp = ctx.message.created_at)
                emb.add_field(name = 'Снял мут', value = ctx.author.mention)
                emb.add_field(name = 'По причине', value = reason)
                emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
                await ctx.send(embed = emb)
            else:
                emb = discord.Embed(description = 'Снятие мута не требуется. Роли Muted не обнаружено в списке ролей участника.')
                emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
                await ctx.send(embed = emb)
                
        else:
            emb = discord.Embed(description = f'{ctx.author.mention}, Я не могу снять мут у {member.mention} из-за того, что роль Muted была удалена/отредактирована!', colour = discord.Color.orange(), timestamp = ctx.message.created_at)
            emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
            await ctx.send(embed = emb)

    @commands.command(aliases = ['Clear', 'CLEAR'])
    @commands.cooldown(1, 10, commands.BucketType.default)
    @commands.has_permissions(administrator = True)
    async def clear(self, ctx, amount : int, confirm : str = None):
        await ctx.message.delete()
        if amount == 0:
            emb = discord.Embed(description = 'Удалять 0 сообщений? Ты еблан?', colour = discord.Color.red())
            emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
            await ctx.send(embed = emb, delete_after = 3)
        elif amount == 1:
            emb = discord.Embed(description = f'удалено {amount} сообщение', colour = discord.Color.orange())
            emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
            await ctx.channel.purge(limit = amount)
            await ctx.send(embed = emb, delete_after = 1)
        elif amount == 2:
            emb = discord.Embed(description = f'удалено {amount} сообщения', colour = discord.Color.orange())
            emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
            await ctx.channel.purge(limit = amount)
            await ctx.send(embed = emb, delete_after = 1)
        elif amount == 3:
            emb = discord.Embed(description = f'удалено {amount} сообщения', colour = discord.Color.orange())
            emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
            await ctx.channel.purge(limit = amount)
            await ctx.send(embed = emb, delete_after = 1)
        elif amount == 4:
            emb = discord.Embed(description = f'удалено {amount} сообщения', colour = discord.Color.orange())
            emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
            await ctx.channel.purge(limit = amount)
            await ctx.send(embed = emb, delete_after = 1)
        elif amount >= 10:
            if confirm == 'confirm':
                await ctx.send(f'Через 3 секунды будет удалено {amount} сообщений')
                await asyncio.sleep(3)
                await ctx.channel.purge(limit = amount + 1)
                await ctx.send(f'удалено {amount} сообщений', delete_after = 2)
            if confirm == None:
                emb = discord.Embed(description = f'{ctx.author.mention}, для выполнения этой команды мне нужно ваше подтвеждение! (чувствительно к регистру)', colour = discord.Color.orange())
                emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
                await ctx.send(embed = emb)
        else:
            emb = discord.Embed(description = f'удалено {amount} сообщений', colour = discord.Color.orange())
            emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
            await ctx.channel.purge(limit = amount)
            await ctx.send(embed = emb, delete_after = 1)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.message.delete()
            emb = discord.Embed(description = f'{ctx.author.mention}, команда в кд, потерпи чутка!', colour = discord.Color.orange())
            emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
            await ctx.send(embed = emb)

def setup(client):
    client.add_cog(Moderation(client))
