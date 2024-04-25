import asyncio
import discord
import random
from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Модуль Fun загружен')

    @commands.command()
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def roulette(self, ctx, player: discord.User = None):
        items_list = {1: 'Сигаретка', 2: 'Ножовка по металлу', 3: 'Пиво', 4: 'Лупа'}
        turn_order = random.randint(0, 1)
        rounds_order = []
        p1_items = []
        p2_items = []
        stop = False
        p1_cuffed, p2_cuffed = False, False
        p1_hp, p2_hp = 4, 4
        if player:
            await ctx.send('Вы были приглашены поиграть в русскую рулетку! Для принятия напишите `y` ||для отказа напишите `n`||')
        else:
            await ctx.send(embed = discord.Embed(description = 'Игра против ИИ', color = 0xff8000))
        await ctx.send(embed = discord.Embed(description = 'В магазин вставляется случайное количество патронов от 2 до 8. Патрон может быть боевым или холостым. Количество как боевых, так и холостых патронов абсолютно случайно, но не равно нулю. Игра заканчивается в тот момент, когда здоровье одного из игроков будет равно нулю. Максимальное количество раундов - 10. При выстреле в себя холостым оппонент пропустит ход. Использование предмета считается дополнительным действием. На каждый ход у вас 30 секунд. Так как вы играете с ботом, первым в раунде всегда ходит человек', color = 0x2f3136))
        await asyncio.sleep(15) # Перед каждым раундом вы получаете случайные предметы в размере двух штук, максимум 8 предметов.
        for i in range(10):
            if stop: return await ctx.send(embed = discord.Embed(description = 'Игра была остановлена игроком', color = 0xff8000))
            turn_order = 0
            rounds_order = []
            winner = 'бот' if p1_hp <= 0 else 'человек'
            if p1_hp <= 0 or p2_hp <= 0:
                await ctx.send(embed = discord.Embed(description = f'Игра окончена. Победил {winner}', color = 0x00ff00 if winner == 'человек' else 0xff0000)); break
            await ctx.send(embed = discord.Embed(description = f'Раунд номер {i + 1}', color = 0xffffff))
            if len(p1_items) < 7:
                p1_items.append(items_list[random.randint(1, 4)])
                p1_items.append(items_list[random.randint(1, 4)])
            elif len(p1_items) == 7:
                p1_items.append(items_list[random.randint(1, 4)])
            elif len(p1_items) == 8:
                await ctx.send(embed = discord.Embed(description = 'Предметы не были добавлены, так как у вас их 8. Используйте предметы чаще', color = 0xff0000))
            if len(p2_items) < 7:
                p2_items.append(items_list[random.randint(1, 4)])
                p2_items.append(items_list[random.randint(1, 4)])
            elif len(p2_items) == 7:
                p2_items.append(items_list[random.randint(1, 4)])
            elif len(p2_items) == 8: pass
            rounds = random.randint(2, 8)
            for _ in range(rounds):
                if p1_cuffed: turn_order = 1; p1_cuffed = False
                if p2_cuffed: turn_order = 0; p2_cuffed = False
                if p1_hp <= 0 or p2_hp <= 0:
                    break
                if len(rounds_order) == 0:
                    for _ in range(rounds):
                        rounds_order.append(random.randint(0, 1))
                        if rounds_order.count(0) == 0: rounds_order.pop(); rounds_order.append(0) 
                        if rounds_order.count(1) == 0: rounds_order.pop(); rounds_order.append(1)
                damage = 1
                await ctx.send(embed = discord.Embed(description = f'Патронов - {len(rounds_order)}, боевых - {rounds_order.count(1)}, холостых - {rounds_order.count(0)}\nВаше здоровье - {p1_hp}\nЗдоровье врага - {p2_hp}', color = 0x2f3136)) # \nВаши предметы - {", ".join(p1_items)}\nПредметы противника - {", ".join(p2_items)}
                if turn_order == 0:
                    await ctx.send(embed = discord.Embed(description = 'Выберите действие: 1 - выстрелить в себя, 2 - выстрелить в оппонента', color = 0xff8000)) # , 3 - использовать предмет
                    action = await self.client.wait_for('message', timeout = 30, check = lambda message: message.channel == ctx.message.channel and message.author == ctx.author and message.content.lower() == '1' or message.content.lower() == '2' or message.content.lower() == 'stop')
                    if action.content == '1':
                        await ctx.send(embed = discord.Embed(description = 'Вы выбрали выстрелить в себя...', color = 0xff0000))
                        await asyncio.sleep(3)
                        if rounds_order[0] == 0:
                            rounds_order.pop(0)
                            await ctx.send(embed = discord.Embed(description = 'Холостой, противник пропускает ход', color = 0x00ff00))
                            turn_order = 0
                        elif rounds_order[0] == 1:
                            await ctx.send(embed = discord.Embed(description = f'Это был боевой.. вы теряете здоровье в размере {damage}', color = 0xff0000))
                            rounds_order.pop(0)
                            p1_hp -= damage
                            turn_order = 1
                    elif action.content == '2':
                        await ctx.send(embed = discord.Embed(description = 'Вы выбрали выстрелить в противника', color = 0xff8000))
                        await asyncio.sleep(3)
                        if rounds_order[0] == 0:
                            rounds_order.pop(0)
                            await ctx.send(embed = discord.Embed(description = 'Холостой, перенос хода', color = 0xff0000))
                            turn_order = 1
                        elif rounds_order[0] == 1:
                            await ctx.send(embed = discord.Embed(description = f'Это был боевой, противник теряет {damage} здоровья', color = 0x00ff00))
                            rounds_order.pop(0)
                            p2_hp -= damage
                            turn_order = 1
                    #elif action.content == '3':
                    #    init = []
                    #    for i in range(len(p1_items)):
                    #        init.append(f'{i + 1} - {p1_items[i]}')
                    #    item = int(input(f'Выберите предмет из инвентаря: {", ".join(init)} '))
                    #    item = init[item - 1]
                    elif action.content.lower() == 'stop': stop = True; break
                elif turn_order == 1:
                    action = random.randint(1, 4)
                    if rounds_order.count(1) == 0: action = 1
                    if rounds_order.count(0) == 0: action = 3
                    if action <= 2:
                        await ctx.send(embed = discord.Embed(description = 'Оппонент решил выстрелить в себя...', color = 0xff8000))
                        await asyncio.sleep(3)
                        if rounds_order[0] == 0:
                            await ctx.send(embed = discord.Embed(description = 'Холостой, вы пропускаете ход', color = 0xff0000))
                            rounds_order.pop(0)
                            turn_order = 1
                        elif rounds_order[0] == 1:
                            await ctx.send(embed = discord.Embed(description = f'Это был боевой.. противник теряет здоровье в размере {damage}', color = 0x00ff00))
                            rounds_order.pop(0)
                            p2_hp -= damage
                            turn_order = 0
                    elif action >= 3:
                        await ctx.send(embed = discord.Embed(description = 'Противник стреляет в вас', color = 0xff0000))
                        await asyncio.sleep(3)
                        if rounds_order[0] == 0:
                            await ctx.send(embed = discord.Embed(description = 'Холостой, перенос хода', color = 0x00ff00))
                            rounds_order.pop(0)
                            turn_order = 0
                        elif rounds_order[0] == 1:
                            await ctx.send(embed = discord.Embed(description = f'Это был боевой, вы теряете {damage} здоровья', color = 0xff0000))
                            rounds_order.pop(0)
                            p1_hp -= damage
                            turn_order = 0

    @commands.command()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def dotersbrain(self, ctx):
        sent1 = await ctx.send(f'{ctx.author.mention}, через 5 секунд появится одно из слов (чё, а, да, нет, ок), на которое вам нужно будет правильно ответить. На размышление 4 секунды.')
        await asyncio.sleep(5)
        words = ['чё', 'а', 'да', 'нет', 'ок']
        rand = random.choice(words)
        sent = await ctx.send(rand)
        try:
            msg = await self.client.wait_for('message', timeout = 4, check = lambda message: message.author == ctx.author and message.channel == ctx.message.channel)
            if msg.content.lower() == 'хуй через плечо' and sent.content == 'чё':
                await ctx.send(content = 'Поздравляю, у вас 3 стадия рака!')
                await sent1.delete()
                await sent.delete()
            elif sent.content == 'а' and msg.content.lower() == 'хуй на':
                await ctx.send(content = 'Поздравляю, у вас 3 стадия рака!')
                await sent1.delete()
                await sent.delete()
            elif sent.content == 'да' and msg.content.lower() == 'пизда':
                await ctx.send(content = 'Поздравляю, у вас 3 стадия рака!')
                await sent1.delete()
                await sent.delete()
            elif sent.content == 'нет' and msg.content.lower() == 'пидора ответ':
                await ctx.send(content = 'Поздравляю, у вас 3 стадия рака!')
                await sent1.delete()
                await sent.delete()
            elif sent.content == 'ок' and msg.content.lower() == 'хуй намок':
                await ctx.send(content = 'Поздравляю, у вас 3 стадия рака!')
                await sent1.delete()
                await sent.delete()
            else:
                await ctx.send('Вы совершенно здоровый человек! ||попробуйте cy/help dotersbrain||')
                await sent1.delete()
                await sent.delete()
        except asyncio.TimeoutError:
            await ctx.send(f'{ctx.author.mention}, слишком медленно.')
            await sent.delete()

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def aghanim(self, ctx):
        rand = random.randint(1, 40)
        if rand >= 15:
            await ctx.send(embed = discord.Embed(description = f'Ого! Твой аганим длиной аж {rand} см!', color = 0xff8000))
        else:
            await ctx.send(embed = discord.Embed(description = f'Длина твоего аганима {rand} см, лошара', color = 0xff8000))

    @commands.command()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def sanya(self, ctx):
        await ctx.send(embed = discord.Embed().set_image(url = 'https://cdn.discordapp.com/attachments/685176670344183836/1076601210485866546/76923ec8de0a6ca5.png'))

    @commands.command()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def ball(self, ctx):
        await ctx.send(embed = discord.Embed().set_image(url ="https://cdn.discordapp.com/attachments/1064581563603488911/1070381595137163427/rn_image_picker_lib_temp_63aafe99-1b5a-4811-9ad4-5be217ced37f.jpg"))

async def setup(client):
    await client.add_cog(Fun(client))