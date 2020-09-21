import discord
from discord.ext import commands
import random

class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('Дополнение Moderation успешно загружено.')
        
    @commands.command()
    async def mute(self, ctx, member: discord.Member, time: int, reason: str = None):
        await ctx.message.delete()
        guild = ctx.guild
        if member.id != client.owner_id:
            role = discord.utils.get(guild.roles, name = 'Muted')
            if role != None:
                await member.add_roles(role)
                if reason == None:
                    reason = 'Не указана'
                emb = discord.Embed(colour = member.color)
                emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                emb.add_field(name = 'В муте', value = f'{member.mention}')
                emb.add_field(name = 'По причине', value = reason)
                emb.add_field(name = 'Время мута в минутах', value = time)
                emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
                await ctx.send(embed = emb, delete_after = time*60)
                await asyncio.sleep(time*60)
                if role != None:
                    emb = discord.Embed(colour = member.color)
                    emb.add_field(name = 'Размучен по истечению времени', value = member.mention)
                    emb.add_field(name = 'По причине', value = reason)
                    emb.add_field(name = 'Время мута в минутах составляло', value = time)
                    emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
                    await member.remove_roles(role)
                    await ctx.send(f'{member.mention}', embed = emb)
                else:
                    emb = discord.Embed(description = f'{ctx.author.mention}, Я не могу снять мут у {member.mention} из-за того, что роль Muted была удалена/отредактирована!', colour = discord.Color.orange())
                    emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
                    await ctx.send(embed = emb)
            else:
                await guild.create_role(name = 'Muted', colour = discord.Colour(0x000001))
                emb1 = discord.Embed(description = f'{ctx.author.mention}, По причине того, что я не нашёл нужную роль, была создана роль {role.mention} с цветом 0x000001.', colour = discord.Color.orange())
                emb1.set_footer(text = 'Это сообщение должно показываться только 1 раз. Иначе, роль была удалена/отредактирована')
                await ctx.send(embed = emb1)
                await asyncio.sleep(3)
                role = discord.utils.get(guild.roles, name = 'Muted')
                await member.add_roles(role)
                emb = discord.Embed(colour = member.color, timestamp = ctx.message.created_at)
                emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                emb.add_field(name = 'В муте', value = f'{member.mention}')
                emb.add_field(name = 'По причине', value = reason)
                emb.add_field(name = 'Время мута в минутах', value = time)
                emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
                await ctx.send(embed = emb, delete_after = time*60)
                await asyncio.sleep(time*60)
                if role != None:
                    emb = discord.Embed(colour = member.color, timestamp = ctx.message.created_at)
                    emb.add_field(name = 'Размучен по истечению времени', value = member.mention)
                    emb.add_field(name = 'По причине', value = reason)
                    emb.add_field(name = 'Время мута в минутах составляло', value = time)
                    emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
                    await ctx.send(f'{member.mention}', embed = emb)
                    await member.remove_roles(role)
        else:
            emb = discord.Embed(description = f'Извините, {ctx.author.mention}, но вы не можете замутить моего создателя!', colour = discord.Color.orange())
            emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
            await ctx.send(embed = emb)
        
def setup(client):
    client.add_cog(Moderation(client))
