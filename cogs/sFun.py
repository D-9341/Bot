import asyncio
import discord
import random
from discord import app_commands
from discord.ext import commands

class sFun(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('/ - Команды Fun синхронизированы')

    @app_commands.command(description = 'Проверьте себя на мозг дотера!')
    async def dotersbrain(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'{interaction.user.mention}, через 5 секунд появится одно из слов (чё, а, да, нет, ок), на которое вам нужно будет правильно ответить. На размышление 4 секунды.')
        await asyncio.sleep(5)
        words = ['чё', 'а', 'да', 'нет', 'ок']
        rand = random.choice(words)
        sent = await interaction.followup.send(content = rand)
        try:
            msg = await self.client.wait_for('message', timeout = 4, check = lambda message: message.author == interaction.user and message.channel == interaction.channel)
            if msg.content.lower() == 'хуй через плечо' and sent.content == 'чё':
                await interaction.followup.send(content = 'Поздравляю, у вас 3 стадия рака!')
                await sent.delete()
            elif sent.content == 'а' and msg.content.lower() == 'хуй на':
                await interaction.followup.send(content = 'Поздравляю, у вас 3 стадия рака!')
                await sent.delete()
            elif sent.content == 'да' and msg.content.lower() == 'пизда':
                await interaction.followup.send(content = 'Поздравляю, у вас 3 стадия рака!')
                await sent.delete()
            elif sent.content == 'нет' and msg.content.lower() == 'пидора ответ':
                await interaction.followup.send(content = 'Поздравляю, у вас 3 стадия рака!')
                await sent.delete()
            elif sent.content == 'ок' and msg.content.lower() == 'хуй намок':
                await interaction.followup.send(content = 'Поздравляю, у вас 3 стадия рака!')
                await sent.delete()
            else:
                await interaction.followup.send(content = 'Вы совершенно здоровый человек! ||попробуйте /help dotersbrain||')
                await sent.delete()
        except asyncio.TimeoutError:
            await interaction.followup.send(f'{interaction.user.mention}, Слишком медленно.')
            await sent.delete()

    @app_commands.command(description = 'Измерь длину своего аганима!')
    async def aghanim(self, interaction: discord.Interaction):
        rand = random.randint(1, 40)
        if rand >= 15:
            await interaction.response.send_message(embed = discord.Embed(description = f'Ого! Твой аганим длиной аж {rand} см!', color = 0xff8000))
        else:
            await interaction.response.send_message(embed = discord.Embed(description = f'Длина твоего аганима {rand} см, лошара', color = 0xff8000))
    
    @app_commands.command(description = 'Саня')
    async def sanya(self, interaction: discord.Interaction):
        await interaction.response.send_message(embed = discord.Embed().set_image(url = 'https://cdn.discordapp.com/attachments/685176670344183836/1076601210485866546/76923ec8de0a6ca5.png'))

    @app_commands.command(description = 'Яйца')
    async def ball(self, interaction: discord.Interaction):
        await interaction.response.send_message(embed = discord.Embed().set_image(url ="https://cdn.discordapp.com/attachments/1064581563603488911/1070381595137163427/rn_image_picker_lib_temp_63aafe99-1b5a-4811-9ad4-5be217ced37f.jpg"))

async def setup(client):
    await client.add_cog(sFun(client))
