import asyncio
import os
import random

import disnake
from disnake.ext import commands
from pymongo import MongoClient

passw = os.environ.get('passw')
cluster = MongoClient(f"mongodb+srv://cephalon:{passw}@locale.ttokw.mongodb.net/Locale?retryWrites=true&w=majority")
collection = cluster.Locale.locale

friends = [351071668241956865, 417362845303439360]

class sFun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Группа Slash-команд Fun загружена')

    @commands.slash_command(name = 'dotersbrain', description = 'Здесь вы можете проверить себя на наличие мозга дотера.')
    async def _dotersbrain(self, inter):
        sent1 = await inter.response.send_message(f'{inter.author.mention}, через 5 секунд появится одно из слов (чё, а, да, нет, ок), на которое вам нужно будет правильно ответить. На размышление 4 секунды.')
        await asyncio.sleep(5)
        words = ['чё', 'а', 'да', 'нет', 'ок']
        rand = random.choice(words)
        sent = await inter.response.send_message(rand)
        try:
            msg = await self.client.wait_for('message', timeout = 4, check = lambda message: message.author == inter.author and message.channel == inter.channel)
            if msg.content.lower() == 'хуй через плечо' and sent.content == 'чё':
                await inter.response.send_message(f'Поздравляю, у вас 3 стадия рака!')
                await sent1.delete()
                await sent.delete()
            elif sent.content == 'а' and msg.content.lower() == 'хуй на':
                await inter.response.send_message(f'Поздравляю, у вас 3 стадия рака!')
                await sent1.delete()
                await sent.delete()
            elif sent.content == 'да' and msg.content.lower() == 'пизда':
                await inter.response.send_message(f'Поздравляю, у вас 3 стадия рака!')
                await sent1.delete()
                await sent.delete()
            elif sent.content == 'нет' and msg.content.lower() == 'пидора ответ':
                await inter.response.send_message(f'Поздравляю, у вас 3 стадия рака!')
                await sent1.delete()
                await sent.delete()
            elif sent.content == 'ок' and msg.content.lower() == 'хуй намок':
                await inter.response.send_message(f'Поздравляю, у вас 3 стадия рака!')
                await sent1.delete()
                await sent.delete()
            else:
                await inter.response.send_message('Вы совершенно здоровый человек! ||попробуйте cy/help dotersbrain||')
                await sent1.delete()
                await sent.delete()
        except asyncio.TimeoutError:
            await inter.response.send_message(f'{inter.author.mention}, Слишком медленно.')
            await sent1.delete()
            await sent.delete()

    @commands.slash_command(name = 'niggers', description = 'Осуждаем!')
    async def _niggers(self, inter):
        rlocale = rlocale = collection.find_one({"_id": inter.author.id})["locale"]
        if rlocale == 'ru':
            emb = disnake.Embed(description = '[осуждающее видео](https://www.youtube.com/watch?v=167apVK8Suw)', colour = disnake.Color.orange())
            await inter.response.send_message(embed = emb)
        if rlocale == 'gnida':
            emb = disnake.Embed(description = '[негры пидарасы, и извинятся за это не буду](https://www.youtube.com/watch?v=167apVK8Suw)', colour = disnake.Color.orange())
            await inter.response.send_message(embed = emb)

    @commands.slash_command(name = 'ayebalbec', description = 'Я не ангел и не бес, просто..')
    async def balbec(self, inter):
        emb = disnake.Embed(colour = inter.author.color)
        emb.set_author(name = inter.author, icon_url = inter.author.avatar_url)
        emb.set_image(url = 'https://sun9-61.userapi.com/tja5cuQthduwgxq2yMigLiUxfYq_5fqiA6cJWg/sZOkbPajoSY.jpg')
        await inter.response.send_message(embed = emb)

    @commands.slash_command(name = 'rp', description = 'Ультимативный гайд по рп отыгровке')
    async def _rp(self, inter):
        emb = disnake.Embed(description = '[Ныа](https://www.youtube.com/watch?v=idmTSW9mfYI)', colour = disnake.Color.orange())
        await inter.response.send_message(embed = emb)

    @commands.slash_command(name = 'rap', description = '.rap')
    async def _rap(self, inter):
        emb = disnake.Embed(colour = inter.author.color)
        emb.set_author(name = inter.author, icon_url = inter.author.avatar_url)
        emb.set_image(url = 'https://thumbs.gfycat.com/MessyCarefreeHousefly-size_restricted.gif')
        await inter.response.send_message(embed = emb)

    @commands.slash_command(name = 'zatka', description = 'Форма заявки для Набор кадров')
    async def _zatka(self, inter):
        emb = disnake.Embed(title = 'Форма заявки для Набор кадров', colour = inter.author.color)
        emb.set_author(name = inter.author, icon_url = inter.author.avatar_url)
        emb.add_field(name = '(1). ZATKA в STEAM.  ZATKA_KING#8406 в Discord.', value = 'возраст 14+  часовой пояс IL +0.', inline = False)
        emb.add_field(name = '(2). Интересующая управление:', value = 'Discord', inline = False)
        emb.add_field(name = '(3). Опыт администрирования:', value = 'Есть.', inline = False)
        emb.add_field(name = 'творческие:', value = 'Есть.', inline = False)
        emb.add_field(name = 'технические навыки:', value = 'Нет.', inline = False)
        emb.add_field(name = '(4). Сколько часов готовы уделять работе', value = '[ 15+ в неделю ]', inline = False)
        emb.add_field(name = 'в какое время дня свободны', value = '16:00 до 22:00+', inline = False)
        await inter.response.send_message(embed = emb)

def setup(client):
    client.add_cog(sFun(client))
