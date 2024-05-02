import asyncio
import discord
import random
import json
from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Модуль Fun загружен')

    @commands.command()
    @commands.cooldown(1, 20, commands.BucketType.user)
    @commands.bot_has_permissions(manage_channels = True)
    async def roulette(self, ctx, player: discord.User | str = None):
        if player == 'leaderboard':
            with open('leaderboard/leaders.json', 'r') as file:
                data = json.load(file)
                data = sorted(data.items(), key = lambda x: x[1], reverse = True)
                return await ctx.send(embed = discord.Embed(description = f'Топ 10 лидеров:\n\n{"\n".join([f"{i + 1}. {self.client.get_user(int(x[0])).mention} - {x[1]} побед(а)" for i, x in enumerate(data[:10])])}', color = 0xff8000))
        items_list = {1: 'Сигарета', 2: 'Ножовка по металлу', 3: 'Пиво', 4: 'Лупа', 5: 'Старый телефон', 6: 'Подозрительные таблетки', 7: 'Странная кассета', 8: 'Шприц адреналина', 9: 'Наручники'}
        damage = 1
        current = 0
        glass = False
        p1_cuffed = False
        p2_cuffed = False
        rounds_order = []
        p1_items, p2_items = [], []
        stop = False
        p1_hp, p2_hp = 4, 4
        if player == ctx.author: return await ctx.send(embed = discord.Embed(description = 'Вы не можете играть с собой', color = 0xff0000))
        if player:
            await ctx.send(player.mention, embed = discord.Embed(description = 'Вы были приглашены поиграть в русскую рулетку! Для принятия напишите `y`, у вас есть 30 секунд ||для отказа напишите `n`||', color = 0xff8000))
            answer = await self.client.wait_for('message', timeout = 30, check = lambda message: message.channel == ctx.message.channel and message.author == player)
            if answer.content == 'y':
                channel = await ctx.guild.create_text_channel(f'Сессия игры в рулетку {ctx.author.display_name} vs {player.display_name}')
                await ctx.send(embed = discord.Embed(description = f'Давайте перейдём в другой канал: {channel.mention}', color = 0x2f3136))
                await channel.send(embed = discord.Embed(description = f'{ctx.author.mention} vs {player.mention}', color = 0xffffff))
                await channel.send(embed = discord.Embed(description = 'В магазин вставляется случайное количество патронов от 2 до 8.\nПатрон может быть боевым или холостым.\nПеред каждым раундом вы получаете случайные предметы в размере двух штук, максимум 8 предметов.\nИспользование предмета считается дополнительным действием и не влияет на порядок ходов.\nВы __не можете__ отменить использование предмета.\nКоличество как боевых, так и холостых патронов абсолютно случайно, но не равно нулю.\nИгра заканчивается в тот момент, когда здоровье одного из игроков будет равно нулю.\nМаксимальное количество раундов - 10.\nПри выстреле в себя холостым противник пропустит ход.\nПорядок ходов будет решён подбрасыванием монетки', color = 0x2f3136))
                await asyncio.sleep(10)
                for i in range(11):
                    if i == 10: await channel.send(embed = discord.Embed(description = 'Игра окончена ничьёй, канал удалиться через 10 секунд', color = 0xff8000)); await asyncio.sleep(10); return await channel.delete()
                    first = True
                    if stop: return await channel.send(embed = discord.Embed(description = 'Игра была остановлена игроком', color = 0xff8000))
                    turn_order = random.randint(0, 1)
                    rounds_order = []
                    winner = player if p1_hp <= 0 else ctx.author
                    if p1_hp <= 0 or p2_hp <= 0:
                        await channel.send(embed = discord.Embed(description = f'Игра окончена. Победил {winner.mention}, канал удалиться через 10 секунд', color = 0xff8000))
                        with open('leaderboard/leaders.json', 'r') as file:
                            data = json.load(file)
                        if str(winner.id) not in data:
                            data[str(winner.id)] = 1
                            with open('leaderboard/leaders.json', 'w') as users_file:
                                json.dump(data, users_file, indent = 4)
                        else:
                            data[str(winner.id)] += 1
                            with open('leaderboard/leaders.json', 'w') as users_file:
                                json.dump(data, users_file, indent = 4)
                        await asyncio.sleep(10); return await channel.delete()
                    await channel.send(embed = discord.Embed(description = f'Раунд номер {i + 1}', color = 0xffffff))
                    if len(p1_items) < 7:
                        p1_items.append(items_list[random.randint(1, 9)])
                        p1_items.append(items_list[random.randint(1, 9)])
                    elif len(p1_items) == 7:
                        p1_items.append(items_list[random.randint(1, 9)])
                    elif len(p1_items) == 8:
                        await channel.send(embed = discord.Embed(description = f'{ctx.author.mention} предметы не были добавлены, так как у вас их 8. Используйте предметы чаще', color = 0xff0000))
                    if len(p2_items) < 7:
                        p2_items.append(items_list[random.randint(1, 9)])
                        p2_items.append(items_list[random.randint(1, 9)])
                    elif len(p2_items) == 7:
                        p2_items.append(items_list[random.randint(1, 9)])
                    elif len(p2_items) == 8:
                        await channel.send(embed = discord.Embed(description = f'{player.mention} предметы не были добавлены, так как у вас их 8. Используйте предметы чаще', color = 0xff0000))
                    rounds = random.randint(2, 8)
                    while rounds > 0:
                        if p1_cuffed and turn_order == 0:
                            turn_order = 1
                            p1_cuffed = False
                        if p2_cuffed and turn_order == 1:
                            turn_order = 0
                            p2_cuffed = False
                        sawed = False
                        live_rounds = []
                        if p1_hp <= 0 or p2_hp <= 0:
                            break
                        if len(rounds_order) == 0:
                            for _ in range(rounds):
                                rounds_order.append(random.randint(0, 1))
                            if rounds_order.count(0) == 0: rounds_order.pop(); rounds_order.append(0) 
                            if rounds_order.count(1) == 0: rounds_order.pop(); rounds_order.append(1)
                        if p1_cuffed: cuffed = ctx.author.mention
                        if p2_cuffed: cuffed = player.mention
                        await channel.send(embed = discord.Embed(description = f'Патронов - {len(rounds_order)}, боевых - {rounds_order.count(1) if first else '?'}, холостых - {rounds_order.count(0) if first else '?'}\nЗдоровье {ctx.author.mention} - {p1_hp}\nЗдоровье {player.mention} - {p2_hp}\nПредметы {ctx.author.mention} - {", ".join(p1_items)}\nПредметы {player.mention} - {", ".join(p2_items)}\n{f"__{cuffed} закован в наручники и пропускает ход__" if p1_cuffed or p2_cuffed else ""}', color = 0x2f3136))
                        first = False
                        if turn_order == 0:
                            await channel.send(embed = discord.Embed(description = f'{ctx.author.mention}, выберите действие: 1 - выстрелить в себя, 2 - выстрелить в противника{"" if len(p1_items) == 0 else ", 3 - использовать предмет"}', color = 0xff8000))
                            to_listen = ['1', '2', '3', 'stop'] if len(p1_items) > 0 else ['1', '2', 'stop']
                            action = await self.client.wait_for('message', check = lambda message: message.channel == channel and message.author == ctx.author and message.content.lower() in to_listen)
                            if action.content == '1':
                                await channel.send(embed = discord.Embed(description = f'{ctx.author.mention} решил выстрелить в себя...', color = 0xff8000))
                                await asyncio.sleep(3)
                                if rounds_order[0] == 0:
                                    rounds_order.pop(0)
                                    await channel.send(embed = discord.Embed(description = f'Холостой, {player.mention} пропускает ход', color = 0xff8000))
                                    rounds -= 1
                                    damage = 1
                                    turn_order = 0
                                elif rounds_order[0] == 1:
                                    await channel.send(embed = discord.Embed(description = f'Это был боевой.. {ctx.author.mention} теряет здоровье в размере {damage}', color = 0xff8000))
                                    rounds -= 1
                                    p1_hp -= damage
                                    rounds_order.pop(0)
                                    damage = 1
                                    turn_order = 1
                            elif action.content == '2':
                                await channel.send(embed = discord.Embed(description = f'{ctx.author.mention} выбрал выстрелить в {player.mention}', color = 0xff8000))
                                await asyncio.sleep(3)
                                if rounds_order[0] == 0:
                                    rounds_order.pop(0)
                                    await channel.send(embed = discord.Embed(description = f'Холостой, ход переходит {player.mention}', color = 0xff8000))
                                    rounds -= 1
                                    damage = 1
                                    turn_order = 1
                                elif rounds_order[0] == 1:
                                    await channel.send(embed = discord.Embed(description = f'Это был боевой, {player.mention} теряет {damage} здоровья', color = 0xff8000))
                                    rounds -= 1
                                    p2_hp -= damage
                                    rounds_order.pop(0)
                                    damage = 1
                                    turn_order = 1
                            elif action.content == '3':
                                init = []
                                for i in range(len(p1_items)):
                                    init.append(f'{i + 1} - {p1_items[i]}')
                                await channel.send(embed = discord.Embed(description = f'{ctx.author.mention}, выберите предмет из инвентаря: {", ".join(init)}', color = 0xff8000))
                                item = await self.client.wait_for('message', check = lambda message: message.channel == channel and message.author == ctx.author and message.content.lower() in ['1', '2', '3', '4', '5', '6', '7', '8'])
                                used = init[int(item.content) - 1]
                                if 'Сигарета' in used:
                                    await channel.send(embed = discord.Embed(description = f'{ctx.author.mention} использовал сигарету, здоровье {ctx.author.mention} увеличено на 1', color = 0xff8000))
                                    p1_hp += 1
                                    p1_items.pop(int(item.content) - 1)
                                    turn_order = 0
                                elif 'Ножовка' in used:
                                    if sawed:
                                        await channel.send(embed = discord.Embed(description = f'{ctx.author.mention}, вы уже использовали ножовку', color = 0xff0000))
                                        await asyncio.sleep(1)
                                        turn_order = 0
                                    else:
                                        await channel.send(embed = discord.Embed(description = f'{ctx.author.mention} использовал ножовку по металлу, следующий выстрел {ctx.author.mention} нанесёт в 2 раза больше урона', color = 0xff8000))
                                        damage *= 2
                                        p1_items.pop(int(item.content) - 1)
                                        turn_order = 0
                                elif 'Пиво' in used:
                                    await channel.send(embed = discord.Embed(description = f'{ctx.author.mention} использовал пиво, текущий патрон извлечён из патронника, это был {'холостой' if rounds_order[0] == 0 else 'боевой'}', color = 0xff8000))
                                    rounds -= 1
                                    rounds_order = rounds_order[1:]
                                    p1_items.pop(int(item.content) - 1)
                                    turn_order = 0
                                elif 'Лупа' in used:
                                    await channel.send(embed = discord.Embed(description = f'{ctx.author.mention} использовал лупу...', color = 0xff8000))
                                    await asyncio.sleep(3)
                                    await ctx.author.send(embed = discord.Embed(description = f'Сейчас в патроннике: {'холостой' if rounds_order[0] == 0 else 'боевой'}', color = 0xff8000))
                                    p1_items.pop(int(item.content) - 1)
                                    turn_order = 0
                                elif 'Старый' in used:
                                    number = "".join([''.join([random.choice('1234567890') for _ in range(6)])])
                                    await channel.send(embed = discord.Embed(description = f'{ctx.author.mention} звонит на {number}...', color = 0xff8000))
                                    await asyncio.sleep(3)
                                    p1_items.pop(int(item.content) - 1)
                                    if rounds_order.count(1) > 0:
                                        for i in range(0, len(rounds_order)):
                                            if rounds_order[i] == 1:
                                                live_rounds.append(i)
                                        await ctx.author.send(embed = discord.Embed(description = f'...{(random.choice(live_rounds)) + 1} патрон боевой...', color = 0xff8000))
                                        await asyncio.sleep(1)
                                        turn_order = 0
                                    else:
                                        await ctx.author.send(embed = discord.Embed(description = '$%#&^!@*'))
                                        await asyncio.sleep(1)
                                        turn_order = 0
                                elif 'таблетки' in used:
                                    await channel.send(embed = discord.Embed(description = f'{ctx.author.mention} использовал таблетки...', color = 0xff0000))
                                    await asyncio.sleep(3)
                                    p1_items.pop(int(item.content) - 1)
                                    normal = random.randint(1, 4)
                                    if normal <= 2:
                                        await channel.send(embed = discord.Embed(description = f'{ctx.author.mention} восстанавливает 2 здоровья...', color = 0x00ff00))
                                        p1_hp += 2
                                        await asyncio.sleep(1)
                                        turn_order = 0
                                    else:
                                        await channel.send(embed = discord.Embed(description = f'...{ctx.author.mention} теряет 1 здоровье...', color = 0xff0000))
                                        p1_hp -= 1
                                        await asyncio.sleep(1)
                                        turn_order = 0
                                elif 'Странная' in used:
                                    await channel.send(embed = discord.Embed(description = f'{ctx.author.mention} использовал странную кассету...', color = 0xff8000))
                                    await asyncio.sleep(3)
                                    p1_items.pop(int(item.content) - 1)
                                    await channel.send(embed = discord.Embed(description = 'Тип патрона в патроннике изменён', color = 0xff8000))
                                    await asyncio.sleep(1)
                                    if rounds_order[0] == 0: rounds_order[0] = 1; turn_order = 0
                                    elif rounds_order[0] == 1: rounds_order[0] = 0; turn_order = 0
                                elif 'Наручники' in used:
                                    if not p2_cuffed:
                                        await channel.send(embed = discord.Embed(description = f'{ctx.author.mention} использовал наручники, {player.mention} пропустит следующий ход', color = 0x00ff00))
                                        await asyncio.sleep(3)
                                        p2_cuffed = True
                                        p1_items.pop(int(item.content) - 1)
                                        turn_order = 0
                                    else:
                                        await channel.send(embed = discord.Embed(description = f'{ctx.author.mention}, вы уже использовали наручники', color = 0xff0000))
                                        await asyncio.sleep(1)
                                        turn_order = 0
                                elif 'Шприц' in used:
                                    await channel.send(embed = discord.Embed(description = f'{ctx.author.mention} использовал шприц адреналина, теперь он может выбрать предмет {player.mention}', color = 0xff8000))
                                    await asyncio.sleep(3)
                                    p1_items.pop(int(item.content) - 1)
                                    init = []
                                    for i in range(len(p2_items)):
                                            init.append(f'{i + 1} - {p2_items[i]}')
                                    await channel.send(embed = discord.Embed(description = f'Выберите предмет из инвентаря {player.mention}: {", ".join(init)}', color = 0xff8000))
                                    item = await self.client.wait_for('message', check = lambda message: message.channel == channel and message.author == ctx.author and message.content.lower() in ['1', '2', '3', '4', '5', '6', '7', '8'])
                                    used = init[int(item.content) - 1]
                                    if 'Сигарета' in used:
                                        await channel.send(embed = discord.Embed(description = f'{ctx.author.mention} украл сигарету, здоровье увеличено на 1', color = 0x00ff00))
                                        p1_hp += 1
                                        p2_items.pop(int(item.content) - 1)
                                        await asyncio.sleep(1)
                                        turn_order = 0
                                    elif 'Ножовка' in used:
                                        if sawed:
                                            await channel.send(embed = discord.Embed(description = f'{ctx.author.mention}, вы уже использовали ножовку', color = 0xff0000))
                                            await asyncio.sleep(1)
                                            p1_items.insert(int(item.content), items_list[8])
                                            turn_order = 0
                                        else:
                                            await channel.send(embed = discord.Embed(description = f'{ctx.author.mention} украл ножовку по металлу, следующий его выстрел нанесёт в 2 раза больше урона', color = 0x00ff00))
                                            sawed = True
                                            damage *= 2
                                            p2_items.pop(int(item.content) - 1)
                                            await asyncio.sleep(1)
                                            turn_order = 0
                                    elif 'Пиво' in used:
                                        await channel.send(embed = discord.Embed(description = f'{ctx.author.mention} украл пиво, текущий патрон извлечён из патронника, это был {'холостой' if rounds_order[0] == 0 else 'боевой'}', color = 0xff8000))
                                        rounds -= 1
                                        rounds_order = rounds_order[1:]
                                        p2_items.pop(int(item.content) - 1)
                                        await asyncio.sleep(1)
                                        turn_order = 0
                                    elif 'Лупа' in used:
                                        await channel.send(embed = discord.Embed(description = f'{ctx.author.mention} украл лупу...', color = 0xff8000))
                                        await asyncio.sleep(3)
                                        await ctx.author.send(embed = discord.Embed(description = f'Сейчас в патроннике: {'холостой' if rounds_order[0] == 0 else 'боевой'}', color = 0xff0000 if rounds_order[0] == 1 else 0x00ff00))
                                        p2_items.pop(int(item.content) - 1)
                                        await asyncio.sleep(1)
                                        turn_order = 0
                                    elif 'Старый' in used:
                                        number = "".join([''.join([random.choice('1234567890') for _ in range(6)])])
                                        await channel.send(embed = discord.Embed(description = f'{ctx.author.mention} звонит на {number}...', color = 0xff8000))
                                        await asyncio.sleep(3)
                                        p2_items.pop(int(item.content) - 1)
                                        if rounds_order.count(1) > 0:
                                            for i in range(0, len(rounds_order)):
                                               if rounds_order[i] == 1:
                                                   live_rounds.append(i)
                                            await ctx.author.send(embed = discord.Embed(description = f'...{(random.choice(live_rounds)) + 1} патрон боевой...', color = 0xff8000))
                                            await asyncio.sleep(1)
                                            turn_order = 0
                                        else:
                                            await ctx.author.send(embed = discord.Embed(description = '$%#&^!@*'))
                                            await asyncio.sleep(1)
                                            turn_order = 0
                                    elif 'таблетки' in used:
                                        await channel.send(embed = discord.Embed(description = f'{ctx.author.mention} украл таблетки...', color = 0xff0000))
                                        await asyncio.sleep(3)
                                        p2_items.pop(int(item.content) - 1)
                                        normal = random.randint(1, 4)
                                        if normal <= 2:
                                            await channel.send(embed = discord.Embed(description = f'{ctx.author.mention} восстанавливает 2 здоровья...', color = 0x00ff00))
                                            p1_hp += 2
                                            await asyncio.sleep(1)
                                            turn_order = 0
                                        else:
                                            await channel.send(embed = discord.Embed(description = f'...{ctx.author.mention} теряет 1 здоровье...', color = 0xff0000))
                                            p1_hp -= 1
                                            await asyncio.sleep(1)
                                            turn_order = 0
                                    elif 'Странная' in used:
                                        await channel.send(embed = discord.Embed(description = f'{ctx.author.mention} украл странную кассету...', color = 0xff8000))
                                        await asyncio.sleep(3)
                                        p2_items.pop(int(item.content) - 1)
                                        await channel.send(embed = discord.Embed(description = 'Тип патрона в патроннике изменён', color = 0xff8000))
                                        await asyncio.sleep(1)
                                        if rounds_order[0] == 0: rounds_order[0] = 1; turn_order = 0
                                        elif rounds_order[0] == 1: rounds_order[0] = 0; turn_order = 0
                                    elif 'Наручники' in used:
                                        if not p2_cuffed:
                                            await channel.send(embed = discord.Embed(description = f'{ctx.author.mention} украл наручники, {player.mention} пропустит следующий ход', color = 0x00ff00))
                                            await asyncio.sleep(3)
                                            p2_cuffed = True
                                            p2_items.pop(int(item.content) - 1)
                                            turn_order = 0
                                        else:
                                            await channel.send(embed = discord.Embed(description = f'{ctx.author.mention}, вы уже использовали наручники', color = 0xff0000))
                                            await asyncio.sleep(1)
                                            turn_order = 0
                                    elif 'Шприц' in used:
                                        await channel.send(embed = discord.Embed(description = f'{ctx.author.mention} попытался украсть ещё один шприц', color = 0xff0000))
                                        await asyncio.sleep(1)
                                        p1_items.insert(int(item.content), items_list[8])
                                        turn_order = 0
                            elif action.content.lower() == 'stop': stop = True; break
                        elif turn_order == 1:
                            await channel.send(embed = discord.Embed(description = f'{player.mention}, выберите действие: 1 - выстрелить в себя, 2 - выстрелить в противника{"" if len(p2_items) == 0 else ", 3 - использовать предмет"}', color = 0xff8000))
                            to_listen = ['1', '2', '3', 'stop'] if len(p2_items) > 0 else ['1', '2', 'stop']
                            action = await self.client.wait_for('message', check = lambda message: message.channel == channel and message.author == player and message.content.lower() in to_listen)
                            if action.content == '1':
                                await channel.send(embed = discord.Embed(description = f'{player.mention} решил выстрелить в себя...', color = 0xff8000))
                                await asyncio.sleep(3)
                                if rounds_order[0] == 0:
                                    await channel.send(embed = discord.Embed(description = f'Холостой, {ctx.author.mention} пропускает ход', color = 0xff8000))
                                    rounds -= 1
                                    damage = 1
                                    rounds_order.pop(0)
                                    turn_order = 1
                                elif rounds_order[0] == 1:
                                    await channel.send(embed = discord.Embed(description = f'Это был боевой.. {player.mention} теряет здоровье в размере {damage}', color = 0xff8000))
                                    rounds -= 1
                                    rounds_order.pop(0)
                                    p2_hp -= damage
                                    damage = 1
                                    turn_order = 0
                            elif action.content == '2':
                                await channel.send(embed = discord.Embed(description = f'{player.mention} стреляет в {ctx.author.mention}', color = 0xff8000))
                                await asyncio.sleep(3)
                                if rounds_order[0] == 0:
                                    await channel.send(embed = discord.Embed(description = f'Холостой, ход переходит {ctx.author.mention}', color = 0xff8000))
                                    rounds -= 1
                                    damage = 1
                                    rounds_order.pop(0)
                                    turn_order = 0
                                elif rounds_order[0] == 1:
                                    await channel.send(embed = discord.Embed(description = f'Это был боевой, {ctx.author.mention} теряет {damage} здоровья', color = 0xff8000))
                                    rounds -= 1
                                    rounds_order.pop(0)
                                    p1_hp -= damage
                                    damage = 1
                                    turn_order = 0
                            elif action.content == '3':
                                init = []
                                for i in range(len(p2_items)):
                                    init.append(f'{i + 1} - {p2_items[i]}')
                                await channel.send(embed = discord.Embed(description = f'{player.mention}, выберите предмет из инвентаря: {", ".join(init)}', color = 0xff8000))
                                item = await self.client.wait_for('message', check = lambda message: message.channel == channel and message.author == player and message.content.lower() in ['1', '2', '3', '4', '5', '6', '7', '8'])
                                used = init[int(item.content) - 1]
                                if 'Сигарета' in used:
                                    await channel.send(embed = discord.Embed(description = f'{player.mention} использовал сигарету, его здоровье увеличено на 1', color = 0xff8000))
                                    p2_hp += 1
                                    p2_items.pop(int(item.content) - 1)
                                    turn_order = 1
                                elif 'Ножовка' in used:
                                    if sawed:
                                        await channel.send(embed = discord.Embed(description = f'{player.mention}, вы уже использовали ножовку', color = 0xff0000))
                                        await asyncio.sleep(1)
                                        turn_order = 1
                                    else:
                                        await channel.send(embed = discord.Embed(description = f'{player.mention} использовал ножовку по металлу, следующий его выстрел нанесёт в 2 раза больше урона', color = 0xff8000))
                                        damage *= 2
                                        p2_items.pop(int(item.content) - 1)
                                        turn_order = 1
                                elif 'Пиво' in used:
                                    await channel.send(embed = discord.Embed(description = f'{player.mention} использовал пиво, текущий патрон извлечён из патронника, это был {'холостой' if rounds_order[0] == 0 else 'боевой'}', color = 0xff8000))
                                    rounds -= 1
                                    rounds_order = rounds_order[1:]
                                    p2_items.pop(int(item.content) - 1)
                                    turn_order = 1
                                elif 'Лупа' in used:
                                    await channel.send(embed = discord.Embed(description = f'{player.mention} использует лупу...', color = 0xff8000))
                                    await asyncio.sleep(3)
                                    await player.send(embed = discord.Embed(description = f'Сейчас в патроннике: {'холостой' if rounds_order[0] == 0 else 'боевой'}', color = 0xff8000))
                                    p2_items.pop(int(item.content) - 1)
                                    turn_order = 1
                                elif 'Старый' in used:
                                    number = "".join([''.join([random.choice('1234567890') for _ in range(6)])])
                                    await channel.send(embed = discord.Embed(description = f'{player.mention} звонит на {number}...', color = 0xff8000))
                                    await asyncio.sleep(3)
                                    p2_items.pop(int(item.content) - 1)
                                    if rounds_order.count(1) > 0:
                                        for i in range(0, len(rounds_order)):
                                            if rounds_order[i] == 1:
                                                live_rounds.append(i)
                                        await player.send(embed = discord.Embed(description = f'...{(random.choice(live_rounds)) + 1} патрон боевой...', color = 0xff8000))
                                        await asyncio.sleep(1)
                                        turn_order = 1
                                    else:
                                        await player.send(embed = discord.Embed(description = '$%#&^!@*'))
                                        await asyncio.sleep(1)
                                        turn_order = 1
                                elif 'таблетки' in used:
                                    await channel.send(embed = discord.Embed(description = f'{player.mention} использовал таблетки...', color = 0xff0000))
                                    await asyncio.sleep(3)
                                    p2_items.pop(int(item.content) - 1)
                                    normal = random.randint(1, 4)
                                    if normal <= 2:
                                        await channel.send(embed = discord.Embed(description = f'{player.mention} восстанавливает 2 здоровья...', color = 0x00ff00))
                                        p2_hp += 2
                                        await asyncio.sleep(1)
                                        turn_order = 1
                                    else:
                                        await channel.send(embed = discord.Embed(description = f'...{player.mention} теряет 1 здоровье...', color = 0xff0000))
                                        p2_hp -= 1
                                        await asyncio.sleep(1)
                                        turn_order = 1
                                elif 'Странная' in used:
                                    await channel.send(embed = discord.Embed(description = f'{player.mention} использовал странную кассету...', color = 0xff8000))
                                    await asyncio.sleep(3)
                                    p2_items.pop(int(item.content) - 1)
                                    await channel.send(embed = discord.Embed(description = 'Тип патрона в патроннике изменён', color = 0xff8000))
                                    await asyncio.sleep(1)
                                    if rounds_order[0] == 0: rounds_order[0] = 1; turn_order = 1
                                    elif rounds_order[0] == 1: rounds_order[0] = 0; turn_order = 1
                                elif 'Наручники' in used:
                                    if not p1_cuffed:
                                        await channel.send(embed = discord.Embed(description = f'{player.mention} использовал наручники, {ctx.author.mention} пропустит следующий ход', color = 0xff8000))
                                        await asyncio.sleep(3)
                                        p1_cuffed = True
                                        p2_items.pop(int(item.content) - 1)
                                        turn_order = 1
                                    else:
                                        await channel.send(embed = discord.Embed(description = f'{player.mention}, вы уже использовали наручники', color = 0xff0000))
                                        await asyncio.sleep(1)
                                        turn_order = 1
                                elif 'Шприц' in used:
                                    if len(p1_items) == 0: await channel.send(embed = discord.Embed(description = 'В инвентаре противника нет предметов', color = 0xff0000)); turn_order = 0
                                    else:
                                        await channel.send(embed = discord.Embed(description = f'{player.mention} использовал шприц адреналина, теперь он может выбрать предмет {ctx.author.mention}', color = 0xff8000))
                                        await asyncio.sleep(3)
                                        p2_items.pop(int(item.content) - 1)
                                        init = []
                                        for i in range(len(p1_items)):
                                            init.append(f'{i + 1} - {p1_items[i]}')
                                        await channel.send(embed = discord.Embed(description = f'Выберите предмет из инвентаря {ctx.author.mention}: {", ".join(init)}', color = 0xff8000))
                                        item = await self.client.wait_for('message', check = lambda message: message.channel == channel and message.author == player and message.content.lower() in ['1', '2', '3', '4', '5', '6', '7', '8'])
                                        used = init[int(item.content) - 1]
                                        if 'Сигарета' in used:
                                            await channel.send(embed = discord.Embed(description = f'{player.mention} украл сигарету {ctx.author.mention}, ваше здоровье увеличено на 1', color = 0x00ff00))
                                            p2_hp += 1
                                            p1_items.pop(int(item.content) - 1)
                                            await asyncio.sleep(1)
                                            turn_order = 1
                                        elif 'Ножовка' in used:
                                            if sawed:
                                                await channel.send(embed = discord.Embed(description = f'{player.mention}, вы уже использовали ножовку', color = 0xff0000))
                                                await asyncio.sleep(1)
                                                p2_items.insert(int(item.content), items_list[8])
                                                turn_order = 1
                                            else:
                                                await channel.send(embed = discord.Embed(description = f'{player.mention} украл ножовку по металлу, следующий его выстрел нанесёт в 2 раза больше урона', color = 0x00ff00))
                                                sawed = True
                                                damage *= 2
                                                p1_items.pop(int(item.content) - 1)
                                                await asyncio.sleep(1)
                                                turn_order = 1
                                        elif 'Пиво' in used:
                                            await channel.send(embed = discord.Embed(description = f'{player.mention} украл пиво, текущий патрон извлечён из патронника, это был {'холостой' if rounds_order[0] == 0 else 'боевой'}', color = 0xff8000))
                                            rounds -= 1
                                            rounds_order = rounds_order[1:]
                                            p1_items.pop(int(item.content) - 1)
                                            await asyncio.sleep(1)
                                            turn_order = 1
                                        elif 'Лупа' in used:
                                            await channel.send(embed = discord.Embed(description = f'{player.mention} украл лупу...', color = 0xff8000))
                                            await asyncio.sleep(3)
                                            await player.send(embed = discord.Embed(description = f'Сейчас в патроннике: {'холостой' if rounds_order[0] == 0 else 'боевой'}', color = 0xff0000 if rounds_order[0] == 1 else 0x00ff00))
                                            p1_items.pop(int(item.content) - 1)
                                            await asyncio.sleep(1)
                                            turn_order = 1
                                        elif 'Старый' in used:
                                            number = "".join([''.join([random.choice('1234567890') for _ in range(6)])])
                                            await channel.send(embed = discord.Embed(description = f'{player.mention} звонит на {number}...', color = 0xff8000))
                                            await asyncio.sleep(3)
                                            p1_items.pop(int(item.content) - 1)
                                            if rounds_order.count(1) > 0:
                                                for i in range(0, len(rounds_order)):
                                                    if rounds_order[i] == 1:
                                                        live_rounds.append(i)
                                                await player.send(embed = discord.Embed(description = f'...{(random.choice(live_rounds)) + 1} патрон боевой...', color = 0xff8000))
                                                await asyncio.sleep(1)
                                                turn_order = 1
                                            else:
                                                await player.send(embed = discord.Embed(description = '$%#&^!@*'))
                                                await asyncio.sleep(1)
                                                turn_order = 1
                                        elif 'таблетки' in used:
                                            await channel.send(embed = discord.Embed(description = f'{player.mention} украл таблетки...', color = 0xff0000))
                                            await asyncio.sleep(3)
                                            p1_items.pop(int(item.content) - 1)
                                            normal = random.randint(1, 4)
                                            if normal <= 2:
                                                await channel.send(embed = discord.Embed(description = f'{player.mention} восстанавливает 2 здоровья...', color = 0x00ff00))
                                                p2_hp += 2
                                                await asyncio.sleep(1)
                                                turn_order = 1
                                            else:
                                                await channel.send(embed = discord.Embed(description = f'...{player.mention} теряет 1 здоровье...', color = 0xff0000))
                                                p2_hp -= 1
                                                await asyncio.sleep(1)
                                                turn_order = 1
                                        elif 'Странная' in used:
                                            await channel.send(embed = discord.Embed(description = f'{player.mention} украл странную кассету...', color = 0xff8000))
                                            await asyncio.sleep(3)
                                            p1_items.pop(int(item.content) - 1)
                                            await channel.send(embed = discord.Embed(description = 'Тип патрона в патроннике изменён', color = 0xff8000))
                                            await asyncio.sleep(1)
                                            if rounds_order[0] == 0: rounds_order[0] = 1; turn_order = 1
                                            elif rounds_order[0] == 1: rounds_order[0] = 0; turn_order = 1
                                        elif 'Наручники' in used:
                                            if not p1_cuffed:
                                                await channel.send(embed = discord.Embed(description = f'{player.mention} украл наручники, {ctx.author.mention} пропустит следующий ход', color = 0xff8000))
                                                await asyncio.sleep(3)
                                                p1_cuffed = True
                                                p1_items.pop(int(item.content) - 1)
                                                turn_order = 1
                                            else:
                                                await channel.send(embed = discord.Embed(description = f'{player.mention}, вы уже использовали наручники', color = 0xff0000))
                                                await asyncio.sleep(1)
                                                turn_order = 1
                                        elif 'Шприц' in used:
                                            await channel.send(embed = discord.Embed(description = f'{player.mention} попытался украсть ещё один шприц', color = 0xff0000))
                                            p2_items.insert(int(item.content), items_list[8])
                                            await asyncio.sleep(1)
                                            turn_order = 1
                            elif action.content.lower() == 'stop': stop = True; break
            elif answer.content == 'n':
                await ctx.send(embed = discord.Embed(description = 'Ну ок', color = 0x2f3136))
        elif player is None:
            channel = await ctx.guild.create_text_channel(f'Сессия игры в рулетку {ctx.author.display_name} vs {self.client.user.name}')
            await ctx.send(embed = discord.Embed(description = f'Давайте перейдём в другой канал: {channel.mention}', color = 0x2f3136))
            await channel.send(embed = discord.Embed(description = 'Игра против ИИ', color = 0xff8000))
            await channel.send(embed = discord.Embed(description = 'В магазин вставляется случайное количество патронов от 2 до 8.\nПатрон может быть боевым или холостым.\nПеред каждым раундом вы получаете случайные предметы в размере двух штук, максимум 8 предметов.\nИспользование предмета считается дополнительным действием и не влияет на порядок ходов.\nВы __не можете__ отменить использование предмета.\nКоличество как боевых, так и холостых патронов абсолютно случайно, но не равно нулю.\nИгра заканчивается в тот момент, когда здоровье одного из игроков будет равно нулю.\nМаксимальное количество раундов - 10.\nПри выстреле в себя холостым противник пропустит ход.\nТак как вы играете с ботом, первым в раунде всегда ходит человек', color = 0x2f3136))
            await asyncio.sleep(10)
            for i in range(11):
                if i == 10: await channel.send(embed = discord.Embed(description = 'Игра окончена ничьёй, канал удалиться через 10 секунд', color = 0xff8000)); await asyncio.sleep(10); return await channel.delete()
                first = True
                if stop: return await channel.send(embed = discord.Embed(description = 'Игра была остановлена игроком', color = 0xff8000))
                turn_order = 0
                rounds_order = []
                winner = 'бот' if p1_hp <= 0 else 'человек'
                if p1_hp <= 0 or p2_hp <= 0:
                    await channel.send(embed = discord.Embed(description = f'Игра окончена. Победил {winner}, канал будет удалён через 10 секунд', color = 0x00ff00 if winner == 'человек' else 0xff0000))
                    if winner == 'человек':
                        with open('leaderboard/leaders.json', 'r') as file:
                            data = json.load(file)
                        if str(ctx.author.id) not in data:
                            data[str(ctx.author.id)] = 1
                            with open('leaderboard/leaders.json', 'w') as users_file:
                                json.dump(data, users_file, indent = 4)
                        else:
                            data[str(ctx.author.id)] += 1
                            with open('leaderboard/leaders.json', 'w') as users_file:
                                json.dump(data, users_file, indent = 4)
                        await asyncio.sleep(10); return await channel.delete()
                await channel.send(embed = discord.Embed(description = f'Раунд номер {i + 1}', color = 0xffffff))
                if len(p1_items) < 7:
                    p1_items.append(items_list[random.randint(1, 9)])
                    p1_items.append(items_list[random.randint(1, 9)])
                elif len(p1_items) == 7:
                    p1_items.append(items_list[random.randint(1, 9)])
                elif len(p1_items) == 8:
                    await channel.send(embed = discord.Embed(description = 'Предметы не были добавлены, так как у вас их 8. Используйте предметы чаще', color = 0xff0000))
                if len(p2_items) < 7:
                    p2_items.append(items_list[random.randint(1, 9)])
                    p2_items.append(items_list[random.randint(1, 9)])
                elif len(p2_items) == 7:
                    p2_items.append(items_list[random.randint(1, 9)])
                elif len(p2_items) == 8: pass
                rounds = random.randint(2, 8)
                while rounds > 0:
                    if p1_cuffed and turn_order == 0:
                        turn_order = 1
                        p1_cuffed = False
                    if p2_cuffed and turn_order == 1:
                        turn_order = 0
                        p2_cuffed = False
                    sawed = False
                    live_rounds = []
                    if p1_hp <= 0 or p2_hp <= 0:
                        break
                    if len(rounds_order) == 0:
                        for _ in range(rounds):
                            rounds_order.append(random.randint(0, 1))
                        if rounds_order.count(0) == 0: rounds_order.pop(); rounds_order.append(0) 
                        if rounds_order.count(1) == 0: rounds_order.pop(); rounds_order.append(1)
                    if p1_cuffed: cuffed = 'Человек'
                    if p2_cuffed: cuffed = 'Бот'
                    await channel.send(embed = discord.Embed(description = f'Патронов - {len(rounds_order)}, боевых - {rounds_order.count(1) if first else '?'}, холостых - {rounds_order.count(0) if first else '?'}\nВаше здоровье - {p1_hp}\nЗдоровье врага - {p2_hp}\nВаши предметы - {", ".join(p1_items)}\nПредметы противника - {", ".join(p2_items)}\n{f"__{cuffed} закован в наручники и пропускает ход__" if p1_cuffed or p2_cuffed else ""}', color = 0x2f3136))
                    first = False
                    if turn_order == 0:
                        await channel.send(embed = discord.Embed(description = f'Выберите действие: 1 - выстрелить в себя, 2 - выстрелить в противника{"" if len(p1_items) == 0 else ", 3 - использовать предмет"}', color = 0xff8000))
                        to_listen = ['1', '2', '3', 'stop'] if len(p1_items) > 0 else ['1', '2', 'stop']
                        action = await self.client.wait_for('message', check = lambda message: message.channel == channel and message.author == ctx.author and message.content.lower() in to_listen)
                        if action.content == '1':
                            await channel.send(embed = discord.Embed(description = 'Вы выбрали выстрелить в себя...', color = 0xff0000))
                            await asyncio.sleep(3)
                            if rounds_order[0] == 0:
                                rounds_order.pop(0)
                                await channel.send(embed = discord.Embed(description = 'Холостой, противник пропускает ход', color = 0x00ff00))
                                rounds -= 1
                                damage = 1
                                await asyncio.sleep(1)
                                turn_order = 0
                            elif rounds_order[0] == 1:
                                await channel.send(embed = discord.Embed(description = f'Это был боевой.. вы теряете здоровье в размере {damage}', color = 0xff0000))
                                rounds -= 1
                                p1_hp -= damage
                                rounds_order.pop(0)
                                damage = 1
                                await asyncio.sleep(1)
                                turn_order = 1
                        elif action.content == '2':
                            await channel.send(embed = discord.Embed(description = 'Вы выбрали выстрелить в противника', color = 0xff8000))
                            await asyncio.sleep(3)
                            if rounds_order[0] == 0:
                                rounds_order.pop(0)
                                await channel.send(embed = discord.Embed(description = 'Холостой, перенос хода', color = 0xff0000))
                                rounds -= 1
                                damage = 1
                                await asyncio.sleep(1)
                                turn_order = 1
                            elif rounds_order[0] == 1:
                                await channel.send(embed = discord.Embed(description = f'Это был боевой, противник теряет {damage} здоровья', color = 0x00ff00))
                                rounds -= 1
                                p2_hp -= damage
                                rounds_order.pop(0)
                                damage = 1
                                await asyncio.sleep(1)
                                turn_order = 1
                        elif action.content == '3':
                            init = []
                            for i in range(len(p1_items)):
                                init.append(f'{i + 1} - {p1_items[i]}')
                            await channel.send(embed = discord.Embed(description = f'Выберите предмет из инвентаря: {", ".join(init)}', color = 0xff8000))
                            item = await self.client.wait_for('message', check = lambda message: message.channel == channel and message.author == ctx.author and message.content.lower() in ['1', '2', '3', '4', '5', '6', '7', '8'])
                            used = init[int(item.content) - 1]
                            if 'Сигарета' in used:
                                await channel.send(embed = discord.Embed(description = 'Вы использовали сигарету, ваше здоровье увеличено на 1', color = 0x00ff00))
                                p1_hp += 1
                                p1_items.pop(int(item.content) - 1)
                                await asyncio.sleep(1)
                                turn_order = 0
                            elif 'Ножовка' in used:
                                if sawed:
                                    await channel.send(embed = discord.Embed(description = 'Вы уже использовали ножовку', color = 0xff0000))
                                    await asyncio.sleep(1)
                                    turn_order = 0
                                else:
                                    await channel.send(embed = discord.Embed(description = 'Вы использовали ножовку по металлу, следующий ваш выстрел нанесёт в 2 раза больше урона', color = 0x00ff00))
                                    sawed = True
                                    damage *= 2
                                    p1_items.pop(int(item.content) - 1)
                                    await asyncio.sleep(1)
                                    turn_order = 0
                            elif 'Пиво' in used:
                                await channel.send(embed = discord.Embed(description = f'Вы использовали пиво, текущий патрон извлечён из патронника, это был {'холостой' if rounds_order[0] == 0 else 'боевой'}', color = 0xff8000))
                                rounds -= 1
                                rounds_order = rounds_order[1:]
                                p1_items.pop(int(item.content) - 1)
                                await asyncio.sleep(1)
                                turn_order = 0
                            elif 'Лупа' in used:
                                await channel.send(embed = discord.Embed(description = 'Вы использовали лупу...', color = 0xff8000))
                                await asyncio.sleep(3)
                                await channel.send(embed = discord.Embed(description = f'Сейчас в патроннике: {'холостой' if rounds_order[0] == 0 else 'боевой'}', color = 0xff0000 if rounds_order[0] == 1 else 0x00ff00))
                                p1_items.pop(int(item.content) - 1)
                                await asyncio.sleep(1)
                                turn_order = 0
                            elif 'Старый' in used:
                                number = "".join([''.join([random.choice('1234567890') for _ in range(6)])])
                                await channel.send(embed = discord.Embed(description = f'Звоним на {number}...', color = 0xff8000))
                                await asyncio.sleep(3)
                                p1_items.pop(int(item.content) - 1)
                                if rounds_order.count(1) > 0:
                                    for i in range(0, len(rounds_order)):
                                        if rounds_order[i] == 1:
                                            live_rounds.append(i)
                                    await channel.send(embed = discord.Embed(description = f'...{(random.choice(live_rounds)) + 1} патрон боевой...', color = 0xff8000))
                                    await asyncio.sleep(1)
                                    turn_order = 0
                                else:
                                    await channel.send(embed = discord.Embed(description = '$%#&^!@*'))
                                    await asyncio.sleep(1)
                                    turn_order = 0
                            elif 'таблетки' in used:
                                await channel.send(embed = discord.Embed(description = f'Вы использовали таблетки...', color = 0xff0000))
                                await asyncio.sleep(3)
                                p1_items.pop(int(item.content) - 1)
                                normal = random.randint(1, 4)
                                if normal <= 2:
                                    await channel.send(embed = discord.Embed(description = 'Вы восстанавливаете 2 здоровья...', color = 0x00ff00))
                                    p1_hp += 2
                                    await asyncio.sleep(1)
                                    turn_order = 0
                                else:
                                    await channel.send(embed = discord.Embed(description = '...Вы теряете 1 здоровье...', color = 0xff0000))
                                    p1_hp -= 1
                                    await asyncio.sleep(1)
                                    turn_order = 0
                            elif 'Странная' in used:
                                await channel.send(embed = discord.Embed(description = 'Вы использовали странную кассету...', color = 0xff8000))
                                await asyncio.sleep(3)
                                p1_items.pop(int(item.content) - 1)
                                await channel.send(embed = discord.Embed(description = 'Тип патрона в патроннике изменён', color = 0xff8000))
                                await asyncio.sleep(1)
                                if rounds_order[0] == 0: rounds_order[0] = 1; turn_order = 0
                                elif rounds_order[0] == 1: rounds_order[0] = 0; turn_order = 0
                            elif 'Наручники' in used:
                                if not p2_cuffed:
                                    await channel.send(embed = discord.Embed(description = 'Вы использовали наручники, противник пропустит следующий ход', color = 0x00ff00))
                                    await asyncio.sleep(3)
                                    p2_cuffed = True
                                    p1_items.pop(int(item.content) - 1)
                                    turn_order = 0
                                else:
                                    await channel.send(embed = discord.Embed(description = f'Вы уже использовали наручники', color = 0xff0000))
                                    await asyncio.sleep(1)
                                    turn_order = 0
                            elif 'Шприц' in used:
                                if len(p1_items) == 0: await channel.send(embed = discord.Embed(description = 'В инвентаре противника нет предметов', color = 0xff0000)); turn_order = 0
                                else:
                                    await channel.send(embed = discord.Embed(description = 'Вы использовали шприц адреналина, теперь вы можете выбрать один предмет противника', color = 0x00ff00))
                                    await asyncio.sleep(3)
                                    p1_items.pop(int(item.content) - 1)
                                    init = []
                                    for i in range(len(p2_items)):
                                        init.append(f'{i + 1} - {p2_items[i]}')
                                    await channel.send(embed = discord.Embed(description = f'Выберите предмет из инвентаря противника: {", ".join(init)}', color = 0xff8000))
                                    item = await self.client.wait_for('message', check = lambda message: message.channel == channel and message.author == ctx.author and message.content.lower() in ['1', '2', '3', '4', '5', '6', '7', '8'])
                                    used = init[int(item.content) - 1]
                                    if 'Сигарета' in used:
                                        await channel.send(embed = discord.Embed(description = 'Вы украли сигарету противника, ваше здоровье увеличено на 1', color = 0x00ff00))
                                        p1_hp += 1
                                        p2_items.pop(int(item.content) - 1)
                                        await asyncio.sleep(1)
                                        turn_order = 0
                                    elif 'Ножовка' in used:
                                        if sawed:
                                            await channel.send(embed = discord.Embed(description = 'Вы уже использовали ножовку', color = 0xff0000))
                                            await asyncio.sleep(1)
                                            p1_items.insert(int(item.content), items_list[8])
                                            turn_order = 0
                                        else:
                                            await channel.send(embed = discord.Embed(description = 'Вы украли ножовку по металлу, следующий ваш выстрел нанесёт в 2 раза больше урона', color = 0x00ff00))
                                            sawed = True
                                            damage *= 2
                                            p2_items.pop(int(item.content) - 1)
                                            await asyncio.sleep(1)
                                            turn_order = 0
                                    elif 'Пиво' in used:
                                        await channel.send(embed = discord.Embed(description = f'Вы украли пиво, текущий патрон извлечён из патронника, это был {'холостой' if rounds_order[0] == 0 else 'боевой'}', color = 0xff8000))
                                        rounds -= 1
                                        rounds_order = rounds_order[1:]
                                        p2_items.pop(int(item.content) - 1)
                                        await asyncio.sleep(1)
                                        turn_order = 0
                                    elif 'Лупа' in used:
                                        await channel.send(embed = discord.Embed(description = 'Вы украли лупу...', color = 0xff8000))
                                        await asyncio.sleep(3)
                                        await channel.send(embed = discord.Embed(description = f'Сейчас в патроннике: {'холостой' if rounds_order[0] == 0 else 'боевой'}', color = 0xff0000 if rounds_order[0] == 1 else 0x00ff00))
                                        p2_items.pop(int(item.content) - 1)
                                        await asyncio.sleep(1)
                                        turn_order = 0
                                    elif 'Старый' in used:
                                        number = "".join([''.join([random.choice('1234567890') for _ in range(6)])])
                                        await channel.send(embed = discord.Embed(description = f'Звоним на {number}...', color = 0xff8000))
                                        await asyncio.sleep(3)
                                        p2_items.pop(int(item.content) - 1)
                                        if rounds_order.count(1) > 0:
                                            for i in range(0, len(rounds_order)):
                                                if rounds_order[i] == 1:
                                                    live_rounds.append(i)
                                            await channel.send(embed = discord.Embed(description = f'...{(random.choice(live_rounds)) + 1} патрон боевой...', color = 0xff8000))
                                            await asyncio.sleep(1)
                                            turn_order = 0
                                        else:
                                            await channel.send(embed = discord.Embed(description = '$%#&^!@*'))
                                            await asyncio.sleep(1)
                                            turn_order = 0
                                    elif 'таблетки' in used:
                                        await channel.send(embed = discord.Embed(description = f'Вы украли таблетки...', color = 0xff0000))
                                        await asyncio.sleep(3)
                                        p2_items.pop(int(item.content) - 1)
                                        normal = random.randint(1, 4)
                                        if normal <= 2:
                                            await channel.send(embed = discord.Embed(description = 'Вы восстанавливаете 2 здоровья...', color = 0x00ff00))
                                            p1_hp += 2
                                            await asyncio.sleep(1)
                                            turn_order = 0
                                        else:
                                            await channel.send(embed = discord.Embed(description = '...Вы теряете 1 здоровье...', color = 0xff0000))
                                            p1_hp -= 1
                                            await asyncio.sleep(1)
                                            turn_order = 0
                                    elif 'Странная' in used:
                                        await channel.send(embed = discord.Embed(description = 'Вы украли странную кассету...', color = 0xff8000))
                                        await asyncio.sleep(3)
                                        p2_items.pop(int(item.content) - 1)
                                        await channel.send(embed = discord.Embed(description = 'Тип патрона в патроннике изменён', color = 0xff8000))
                                        await asyncio.sleep(1)
                                        if rounds_order[0] == 0: rounds_order[0] = 1; turn_order = 0
                                        elif rounds_order[0] == 1: rounds_order[0] = 0; turn_order = 0
                                    elif 'Наручники' in used:
                                        if not p2_cuffed:
                                            await channel.send(embed = discord.Embed(description = 'Вы украли наручники, противник пропустит следующий ход', color = 0x00ff00))
                                            await asyncio.sleep(3)
                                            p2_cuffed = True
                                            p2_items.pop(int(item.content) - 1)
                                            turn_order = 0
                                        else:
                                            await channel.send(embed = discord.Embed(description = f'Вы уже использовали наручники', color = 0xff0000))
                                            await asyncio.sleep(1)
                                            turn_order = 0
                                    elif 'Шприц' in used:
                                        await channel.send(embed = discord.Embed(description = 'Вы не можете украсть ещё один шприц', color = 0xff0000))
                                        p1_items.insert(int(item.content), items_list[8])
                                        await asyncio.sleep(1)
                                        turn_order = 0
                        elif action.content.lower() == 'stop': stop = True; break
                    elif turn_order == 1:
                        if not glass:
                            action = random.randint(1, 6)
                        else:
                            action = 1 if current == 0 else 3
                            glass = False
                        if rounds_order.count(1) == 0: action = 1
                        if rounds_order.count(0) == 0: action = 3
                        if len(p2_items) == 0: action = random.randint(1, 4)
                        if action <= 2:
                            await channel.send(embed = discord.Embed(description = 'Противник решил выстрелить в себя...', color = 0xff8000))
                            await asyncio.sleep(3)
                            if rounds_order[0] == 0:
                                await channel.send(embed = discord.Embed(description = 'Холостой, вы пропускаете ход', color = 0xff0000))
                                rounds -= 1
                                damage = 1
                                rounds_order.pop(0)
                                turn_order = 1
                            elif rounds_order[0] == 1:
                                await channel.send(embed = discord.Embed(description = f'Это был боевой.. противник теряет здоровье в размере {damage}', color = 0x00ff00))
                                rounds -= 1
                                rounds_order.pop(0)
                                p2_hp -= damage
                                damage = 1
                                turn_order = 0
                        elif action >= 3 and action <= 4:
                            await channel.send(embed = discord.Embed(description = 'Противник стреляет в вас', color = 0xff0000))
                            await asyncio.sleep(3)
                            if rounds_order[0] == 0:
                                await channel.send(embed = discord.Embed(description = 'Холостой, перенос хода', color = 0x00ff00))
                                rounds -= 1
                                damage = 1
                                rounds_order.pop(0)
                                turn_order = 0
                            elif rounds_order[0] == 1:
                                await channel.send(embed = discord.Embed(description = f'Это был боевой, вы теряете {damage} здоровья', color = 0xff0000))
                                rounds -= 1
                                rounds_order.pop(0)
                                p1_hp -= damage
                                damage = 1
                                turn_order = 0
                        elif action >= 5:
                            await channel.send(embed = discord.Embed(description = 'Противник выбирает предмет..', color = 0xff0000))
                            await asyncio.sleep(3)
                            item = random.randint(0, len(p2_items) - 1)
                            used = p2_items[item]
                            if 'Сигарета' in used:
                                await channel.send(embed = discord.Embed(description = 'Противник использовал сигарету, его здоровье увеличено на 1', color = 0xff0000))
                                p2_hp += 1
                                p2_items.pop(item)
                                turn_order = 1
                            elif 'Ножовка' in used:
                                await channel.send(embed = discord.Embed(description = 'Противник использовал ножовку по металлу, следующий его выстрел нанесёт в 2 раза больше урона', color = 0xff0000))
                                damage *= 2
                                p2_items.pop(item)
                                turn_order = 1
                            elif 'Пиво' in used:
                                await channel.send(embed = discord.Embed(description = f'Противник использовал пиво, текущий патрон извлечён из патронника, это был {'холостой' if rounds_order[0] == 0 else 'боевой'}', color = 0xff8000))
                                rounds -= 1
                                rounds_order = rounds_order[1:]
                                p2_items.pop(item)
                                turn_order = 1
                            elif 'Лупа' in used:
                                await channel.send(embed = discord.Embed(description = 'Противник использует лупу...', color = 0xff8000))
                                await asyncio.sleep(3)
                                glass = True
                                if rounds_order[0] == 0: current = 0
                                if rounds_order[0] == 1: current = 1
                                p2_items.pop(item)
                                turn_order = 1
                            elif 'Старый' in used:
                                number = "".join([''.join([random.choice('1234567890') for _ in range(6)])])
                                await channel.send(embed = discord.Embed(description = f'Противник звонит на {number}...', color = 0xff8000))
                                await asyncio.sleep(3)
                                p2_items.pop(item)
                                if rounds_order.count(1) > 0:
                                    turn_order = 1
                                else:
                                    turn_order = 1
                            elif 'таблетки' in used:
                                await channel.send(embed = discord.Embed(description = f'Противник использовал таблетки...', color = 0xff0000))
                                await asyncio.sleep(3)
                                p2_items.pop(item)
                                normal = random.randint(1, 4)
                                if normal <= 2:
                                    await channel.send(embed = discord.Embed(description = 'Противник восстанавливает 2 здоровья...', color = 0x00ff00))
                                    p2_hp += 2
                                    await asyncio.sleep(1)
                                    turn_order = 1
                                else:
                                    await channel.send(embed = discord.Embed(description = '...Противник теряет 1 здоровье...', color = 0xff0000))
                                    p2_hp -= 1
                                    await asyncio.sleep(1)
                                    turn_order = 1
                            elif 'Странная' in used:
                                await channel.send(embed = discord.Embed(description = 'Противник использовал странную кассету...', color = 0xff8000))
                                await asyncio.sleep(3)
                                p2_items.pop(item)
                                await channel.send(embed = discord.Embed(description = 'Тип патрона в патроннике изменён', color = 0xff8000))
                                await asyncio.sleep(1)
                                if rounds_order[0] == 0: rounds_order[0] = 1; turn_order = 1
                                elif rounds_order[0] == 1: rounds_order[0] = 0; turn_order = 1
                            elif 'Наручники' in used:
                                await channel.send(embed = discord.Embed(description = 'Противник использовал наручники, вы пропустите следующий ход', color = 0xff0000))
                                await asyncio.sleep(3)
                                p1_cuffed = True
                                p2_items.pop(item)
                                turn_order = 0
                            elif 'Шприц' in used:
                                await channel.send(embed = discord.Embed(description = 'Противник использовал шприц адреналина...', color = 0xff0000))
                                await asyncio.sleep(3)
                                p2_items.pop(item)
                                if len(p1_items) != 0:
                                    used = p1_items[item]
                                    if 'Сигарета' in used:
                                        await channel.send(embed = discord.Embed(description = 'Противник украл вашу сигарету, его здоровье увеличено на 1', color = 0xff0000))
                                        p2_hp += 1
                                        p1_items.pop(item)
                                        turn_order = 1
                                    elif 'Ножовка' in used:
                                        await channel.send(embed = discord.Embed(description = 'Противник украл вашу ножовку по металлу, следующий его выстрел нанесёт в 2 раза больше урона', color = 0xff0000))
                                        damage *= 2
                                        p1_items.pop(item)
                                        turn_order = 1
                                    elif 'Пиво' in used:
                                        await channel.send(embed = discord.Embed(description = f'Противник украл ваше пиво, текущий патрон извлечён из патронника, это был {'холостой' if rounds_order[0] == 0 else 'боевой'}', color = 0xff8000))
                                        rounds -= 1
                                        rounds_order = rounds_order[1:]
                                        p1_items.pop(item)
                                        turn_order = 1
                                    elif 'Лупа' in used:
                                        await channel.send(embed = discord.Embed(description = 'Противник украл вашу лупу...', color = 0xff8000))
                                        await asyncio.sleep(3)
                                        glass = True
                                        if rounds_order[0] == 0: current = 0
                                        if rounds_order[0] == 1: current = 1
                                        p1_items.pop(item)
                                        turn_order = 1
                                    elif 'Старый' in used:
                                        number = "".join([''.join([random.choice('1234567890') for _ in range(6)])])
                                        await channel.send(embed = discord.Embed(description = f'Противник звонит на {number}...', color = 0xff8000))
                                        await asyncio.sleep(3)
                                        p1_items.pop(item)
                                        if rounds_order.count(1) > 0:
                                            turn_order = 1
                                        else:
                                            turn_order = 1
                                    elif 'таблетки' in used:
                                        await channel.send(embed = discord.Embed(description = f'Противник украл ваши таблетки...', color = 0xff0000))
                                        await asyncio.sleep(3)
                                        p1_items.pop(item)
                                        normal = random.randint(1, 4)
                                        if normal <= 2:
                                            await channel.send(embed = discord.Embed(description = 'Противник восстанавливает 2 здоровья...', color = 0x00ff00))
                                            p2_hp += 2
                                            await asyncio.sleep(1)
                                            turn_order = 1
                                        else:
                                            await channel.send(embed = discord.Embed(description = '...Противник теряет 1 здоровье...', color = 0xff0000))
                                            p2_hp -= 1
                                            await asyncio.sleep(1)
                                            turn_order = 1
                                    elif 'Странная' in used:
                                        await channel.send(embed = discord.Embed(description = 'Противник украл вашу странную кассету...', color = 0xff8000))
                                        await asyncio.sleep(3)
                                        p1_items.pop(item)
                                        await channel.send(embed = discord.Embed(description = 'Тип патрона в патроннике изменён', color = 0xff8000))
                                        await asyncio.sleep(1)
                                        if rounds_order[0] == 0: rounds_order[0] = 1; turn_order = 1
                                        elif rounds_order[0] == 1: rounds_order[0] = 0; turn_order = 1
                                    elif 'Наручники' in used:
                                        await channel.send(embed = discord.Embed(description = 'Противник украл наручники, вы пропустите следующий ход', color = 0xff0000))
                                        await asyncio.sleep(3)
                                        p1_cuffed = True
                                        p2_items.pop(item)
                                        turn_order = 0
                                    elif 'Шприц' in used:
                                        await channel.send(embed = discord.Embed(description = 'Он попытался украсть шприц', color = 0xff0000))
                                        p2_items.insert(item, items_list[8])
                                        await asyncio.sleep(1)
                                        turn_order = 1
                                else:
                                    await channel.send(embed = discord.Embed(description = 'Но у вас нет предметов, ухахаха', color = 0x00ff00))
                                    p2_items.insert(item, items_list[8])
                                    await asyncio.sleep(1)
                                    turn_order = 1

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