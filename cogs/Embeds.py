import discord
from discord.ext import commands
from discord.utils import get

class Embeds(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Дополнение Embeds успешно загружено.')
        
    @commands.command(aliases = ['ctx'])
    @commands.cooldown(1, 5, commands.BucketType.default)
    async def content(self, ctx, arg):
        await ctx.message.delete()
        message = await ctx.fetch_message(id = arg)
        if message.author == self.client.user:
            await ctx.send(f'```cy/say noembed "{message.content}"```')
        else:
            await ctx.send(f'```{message.content}```')

    @commands.command(aliases = ['emb_ctx'])
    @commands.cooldown(1, 5, commands.BucketType.default)
    async def emb_content(self, ctx, arg):
        await ctx.message.delete()
        message = await ctx.fetch_message(id = arg)
        for emb in message.embeds:
            if message.author == self.client.user:
                await ctx.send(f'```cy/say "" "" t& {emb.title} d& {emb.description} f& {emb.footer.text} c& {emb.colour} a& {emb.author.name} img& {emb.image.url} fu& {emb.thumbnail.url}```')
                break
            else:
                await ctx.send(f'```title {emb.title} description {emb.description} footer {emb.footer.text} color {emb.colour} author {emb.author.name} image {emb.image.url} footer img {emb.thumbnail.url}```')
                break
            
    @commands.command(aliases = ['emb_e'])
    @commands.has_permissions(mention_everyone = True)
    @commands.cooldown(1, 20, commands.BucketType.default)
    async def say_everyone(self, ctx, arg = None, text = None, t = None, d = None, fu = None, img = None, f = None, c = None, a : discord.Member = None):
        await ctx.message.delete()
        if c == None:
            c = ctx.author.color
        else:
            c = int('0x' + c, 16)
        if a == None:
            a = ctx.author
        if img == None:
            img = ('')
        if f == None:
            f = ('')
        if fu == None:
            fu = ('Cephalon Cy by сасиска#2472')
        emb = discord.Embed(title = t, description = d, colour = c)
        emb.set_author(name = a, icon_url = a.avatar_url)
        emb.set_image(url = img)
        emb.set_thumbnail(url = f)
        emb.set_footer(text = fu)
        if arg == 'noembed':
            await ctx.send('@everyone ' + text)
        elif arg != 'noembed':
            await ctx.send('@everyone', embed = emb)
    
    @commands.command(aliases = ['Say', 'SAY'])
    @commands.has_permissions(manage_channels = True)
    async def say(self, ctx, arg = None, text = None, t = None, d = None, fu = None, img = None, f = None, c = None, a : discord.Member = None, *, role: discord.Role = None):
        await ctx.message.delete()
        if c == None:
            c = ctx.author.color
        else:
            c = int('0x' + c, 16)
        if a == None:
            a = ctx.author
        if img == None:
            img = ('')
        if f == None:
            f = ('')
        if role != None:
            c = role.color
        if fu == None:
            fu = ('Cephalon Cy by сасиска#2472')
        emb = discord.Embed(title = t, description = d, colour = c)
        emb.set_author(name = a, icon_url = a.avatar_url)
        emb.set_image(url = img)
        emb.set_thumbnail(url = f)
        emb.set_footer(text = fu)
        if role is not None and arg != 'noembed':
            await ctx.send(f'{role.mention}', embed = emb)
        elif role is None and arg != 'noembed':
            await ctx.send(embed = emb)
        if arg == 'noembed':
            await ctx.send(text)

    @commands.command(aliases = ['emb_ed'])
    @commands.has_permissions(manage_channels = True)
    async def emb_edit(self, ctx, arg, t = None, d = None, fu = None, img = None, f = None, c = None, a : discord.Member = None):
        await ctx.message.delete()
        message = await ctx.fetch_message(id = arg)
        if c == None:
            c = ctx.author.color
        else:
            c = int('0x' + c, 16)
        if a == None:
            a = ctx.author
        if img == None:
            img = ('')
        if f == None:
            f = ('')
        if fu == None:
            fu = ('Cephalon Cy by сасиска#2472')
        emb = discord.Embed(title = t, description = d, colour = c)
        emb.set_author(name = a, icon_url = a.avatar_url)
        emb.set_image(url = img)
        emb.set_thumbnail(url = f)
        emb.set_footer(text = fu)
        await message.edit(embed = emb)
        await ctx.send('👌', delete_after = 1)
    
    @commands.command(aliases = ['Edit', 'EDIT'])
    @commands.has_permissions(manage_channels = True)
    async def edit(self, ctx, arg, *, text):
        await ctx.message.delete()
        message = await ctx.fetch_message(id = arg)
        await message.edit(content = text)
        await ctx.send('👌', delete_after = 1)

def setup(client):
    client.add_cog(Embeds(client))
