import asyncio
import discord
import random
import json
from functions import get_plural_form, get_locale, translate
from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, client):
        self.client: commands.Bot = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Модуль Fun загружен')

    @commands.command()
    @commands.cooldown(1, 20, commands.BucketType.user)
    @commands.bot_has_permissions(manage_channels = True)
    async def roulette(self, ctx: commands.Context, player: discord.User | str = None):
        bot = discord.utils.get(ctx.guild.members, id = self.client.user.id)
        locale = get_locale(ctx.author.id)
        if player == 'leaderboard':
            with open('leaderboard/leaders.json', 'r') as file:
                data = json.load(file)
                data = sorted(data.items(), key = lambda x: x[1], reverse = True)
                return await ctx.send(embed = discord.Embed(description = f'Топ 5 лидеров по победам:\n\n{"\n".join([f"{i + 1}. {self.client.get_user(int(x[0])).mention if '\u0414\u0438\u043b\u0435\u0440' not in x[0] else x[0]} - {x[1]} {get_plural_form(x[1], ['победа', 'победы', 'побед'])}" for i, x in enumerate(data[:5])])}', color = 0xff8000))
        items_list = {
            1: f'{translate(locale, "cigarettes")}', 2: f'{translate(locale, "handsaw")}', 3: f'{translate(locale, "beer")}',
            4: f'{translate(locale, "magnifying_glass")}', 5: f'{translate(locale, "burner_phone")}', 6: f'{translate(locale, "expired_medicine")}',
            7: f'{translate(locale, "inverter")}', 8: f'{translate(locale, "adrenaline_syringe")}', 9: f'{translate(locale, "handcuffs")}',
        }
        damage = 1
        glass = False
        p1_cursed, p2_cursed = False, False
        p1_cuffed, p2_cuffed = False, False
        rounds_order = []
        p1_items, p2_items = [], []
        stop = False
        if player == ctx.author: return await ctx.send(embed = discord.Embed(description = translate(locale, "roulette_play_self"), color = 0xff0000))
        if player and player != bot:
            await ctx.send(player.mention, embed = discord.Embed(description = translate(locale, "roulette_play_invite"), color = 0xff8000))
            answer = await self.client.wait_for('message', timeout = 30, check = lambda message: message.channel == ctx.message.channel and message.author == player)
            if answer.content == 'y':
                MAX_HP = random.randint(4, 6)
                p1_hp, p2_hp = MAX_HP, MAX_HP
                channel = await ctx.guild.create_text_channel(f'{translate(locale, "roulette_session_start")}'.format(ctx_author = ctx.author.display_name, player = player.display_name))
                await ctx.send(embed = discord.Embed(description = f'{translate(locale, "roulette_go_to_other_channel")}'.format(channel_mention = channel.mention), color = 0x2f3136))
                await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_players")}'.format(ctx_author = ctx.author.mention, player = player.mention), color = 0xffffff))
                await channel.send(embed = discord.Embed(description = translate(locale, "roulette_rules_vs_user"), color = 0x2f3136))
                await asyncio.sleep(15)
                turn_order = random.randint(0, 1)
                for i in range(11):
                    if i == 10: await channel.send(embed = discord.Embed(description = translate(locale, "roulette_stalemate"), color = 0xff8000)); await asyncio.sleep(10); return await channel.delete()
                    first = True
                    p1_cuffed = False
                    p2_cuffed = False
                    if stop: await channel.send(embed = discord.Embed(description = translate(locale, "roulette_game_stopped"), color = 0xff8000)); await asyncio.sleep(10); return await channel.delete()
                    rounds_order = []
                    winner = player if p1_hp <= 0 else ctx.author
                    if p1_hp <= 0 or p2_hp <= 0:
                        await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_winner")}'.format(winner = winner.mention), color = 0xff8000))
                        with open('leaderboard/leaders.json', 'r') as file:
                            data = json.load(file)
                        data[str(winner.id)] = data.get(str(winner.id), 0) + 1
                        with open('leaderboard/leaders.json', 'w') as users_file:
                            json.dump(data, users_file, indent = 4)
                        await asyncio.sleep(10); return await channel.delete()
                    await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_round_number")}{"" if i + 1 != 5 else f"{translate(locale, "roulette_round_number_is_5")}"}'.format(i = i + 1,), color = 0xffffff))
                    if i + 1 <= 4:
                        for _ in range(2):
                            if len(p1_items) < 8:
                                p1_items.append(items_list[random.randint(1, 9)])
                            else:
                                await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_use_more_often")}'.format(player = ctx.author.mention), color=0xff0000))
                                break
                        for _ in range(2):
                            if len(p2_items) < 8:
                                p2_items.append(items_list[random.randint(1, 9)])
                            else:
                                await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_use_more_often")}'.format(player = player.mention), color=0xff0000))
                                break
                    else:
                        for _ in range(4):
                            if len(p1_items) < 8:
                                p1_items.append(items_list[random.randint(1, 9)])
                            else:
                                await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_use_more_often")}'.format(player = ctx.author.mention), color=0xff0000))
                                break
                        for _ in range(4):
                            if len(p2_items) < 8:
                                p2_items.append(items_list[random.randint(1, 9)])
                            else:
                                await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_use_more_often")}'.format(player = player.mention), color=0xff0000))
                                break
                    rounds = random.randint(2, 8)
                    while rounds > 0:
                        if p1_hp <= 2: p1_cursed = True
                        if p2_hp <= 2: p2_cursed = True
                        if p1_cuffed and turn_order == 0:
                            turn_order = 1
                            p1_cuffed = False
                        if p2_cuffed and turn_order == 1:
                            turn_order = 0
                            p2_cuffed = False
                        sawed = False
                        if p1_hp <= 0 or p2_hp <= 0:
                            break
                        if len(rounds_order) == 0:
                            for _ in range(rounds):
                                rounds_order.append(random.randint(0, 1))
                            if rounds_order.count(0) == 0: rounds_order.pop(); rounds_order.append(0)
                            if rounds_order.count(1) == 0: rounds_order.pop(); rounds_order.append(1)
                        if p1_cuffed: cuffed = ctx.author.mention
                        if p2_cuffed: cuffed = player.mention
                        if p1_cursed: cursed = ctx.author.mention
                        if p2_cursed: cursed = player.mention
                        if p1_cursed and p2_cursed: cursed = 'Никто' if locale != 'en' else 'Nobody'
                        await channel.send(embed = discord.Embed(description = f'Патронов - {len(rounds_order) if first else '?'}, боевых - {rounds_order.count(1) if first else '?'}, холостых - {rounds_order.count(0) if first else '?'}\nЗдоровье {ctx.author.mention} - {p1_hp}\nЗдоровье {player.mention} - {p2_hp}\n{f'Предметы {ctx.author.mention} ({len(p1_items)}) - {", ".join(p1_items)}' if len(p1_items) > 0 else f"У {ctx.author.mention} нет предметов"}\n{f'Предметы {player.mention} ({len(p2_items)}) - {", ".join(p2_items)}' if len(p2_items) > 0 else f"У {player.mention} нет предметов"}{f"\n__{cuffed} закован в наручники и пропускает ход__" if p1_cuffed or p2_cuffed else ""}{f'**\n{cursed} не может восстанавливать здоровье**' if p1_cursed or p2_cursed else ''}', color = 0x2f3136))
                        first = False
                        if turn_order == 0:
                            game_view = discord.ui.View()
                            game_view.add_item(discord.ui.Button(label = translate(locale, "roulette_shoot_self"), style = discord.ButtonStyle.gray, custom_id = '1'))
                            game_view.add_item(discord.ui.Button(label = translate(locale, "roulette_shoot_opponent"), style = discord.ButtonStyle.gray, custom_id = '2'))
                            if len(p1_items) > 0: game_view.add_item(discord.ui.Button(label = translate(locale, "roulette_use_item"), style = discord.ButtonStyle.gray, custom_id = '3'))
                            game_view.add_item(discord.ui.Button(label = translate(locale, "roulette_stop_game"), style = discord.ButtonStyle.red, custom_id = 'stop'))
                            await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_choose_action")}'.format(player = ctx.author.mention), color = 0xff8000), view = game_view)
                            action = await self.client.wait_for('interaction', check = lambda interaction: interaction.channel == channel and interaction.user == ctx.author)
                            await action.response.defer(ephemeral = True)
                            if action.data['custom_id'] == '1':
                                await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_shoot_self")}'.format(player = ctx.author.mention), color = 0xff8000))
                                await asyncio.sleep(3)
                                rounds -= 1
                                round = rounds_order.pop(0)
                                if round == 0:
                                    await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_shoot_self_blank")}'.format(player = player.mention), color = 0xff8000))
                                    turn_order = 0
                                elif round == 1:
                                    await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_shoot_self_live")}'.format(player = ctx.author.mention, damage = damage), color = 0xff8000))
                                    p1_hp -= damage
                                    turn_order = 1
                                damage = 1
                            elif action.data['custom_id'] == '2':
                                await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_shoot_opponent")}'.format(player1 = ctx.author.mention, player2 = player.mention), color = 0xff8000))
                                await asyncio.sleep(3)
                                rounds -= 1
                                round = rounds_order.pop(0)
                                if round == 0:
                                    await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_shoot_opponent_blank")}'.format(player = player.mention), color = 0xff8000))
                                elif round == 1:
                                    await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_shoot_opponent_live")}'.format(player = player.mention, damage = damage), color = 0xff8000))
                                    p2_hp -= damage
                                turn_order = 1
                                damage = 1
                            elif action.data['custom_id'] == '3':
                                init = [str(item) for item in p1_items]
                                items_view = discord.ui.View()
                                for i in range(len(init)):
                                    items_view.add_item(discord.ui.Button(label = init[i], style = discord.ButtonStyle.gray, custom_id = str(i + 1)))
                                await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_use_item")}'.format(player = ctx.author.mention), color = 0xff8000))
                                item = await self.client.wait_for('interaction', check = lambda interaction: interaction.channel == channel and interaction.user == ctx.author)
                                used = init[int(item.data['custom_id']) - 1]
                                if used == translate(locale, 'cigarettes'):
                                    await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_cigarettes")}'.format(player = ctx.author.mention), color = 0xff8000))
                                    if not p1_cursed: p1_hp += 1 if p1_hp < MAX_HP else 0
                                    p1_items.pop(int(item.data['custom_id']) - 1)
                                elif used == translate(locale, 'handsaw'):
                                    if sawed:
                                        await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_handsaw_used")}'.format(player = ctx.author.mention), color = 0xff0000))
                                    else:
                                        await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_handsaw")}'.format(player = ctx.author.mention), color = 0xff8000))
                                        damage += 1
                                        p1_items.pop(int(item.data['custom_id']) - 1)
                                elif used == translate(locale, 'beer'):
                                    await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_beer")}'.format(player = ctx.author.mention, shell = translate(locale, 'live_shell' if rounds_order[0] == 1 else 'blank_shell')), color = 0xff8000))
                                    rounds -= 1
                                    round = rounds_order.pop(0)
                                    p1_items.pop(int(item.data['custom_id']) - 1)
                                elif used == translate(locale, 'magnifying_glass'):
                                    await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_magnifying_glass")}'.format(player = ctx.author.mention), color = 0xff8000))
                                    await ctx.author.send(embed = discord.Embed(description = f'{translate(locale, "roulette_magnifying_glass_result")}'.format(shell = translate(locale, 'live_shell' if rounds_order[0] == 1 else 'blank_shell')), color = 0xff8000))
                                    p1_items.pop(int(item.data['custom_id']) - 1)
                                elif used == translate(locale, 'burner_phone'):
                                    number = ''.join([random.choice('1234567890') for _ in range(6)])
                                    await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_burner_phone")}'.format(player = ctx.author.mention, number = number), color = 0xff8000))
                                    p1_items.pop(int(item.data['custom_id']) - 1)
                                    if len(rounds_order) >= 3:
                                        current = random.randint(1, len(rounds_order) - 1)
                                        await ctx.author.send(embed = discord.Embed(description = f'{translate(locale, "roulette_burner_phone_result")}'.format(current = current + 1, shell = translate(locale, 'live_shell' if rounds_order[current] == 1 else 'blank_shell')), color = 0xff8000))
                                    else:
                                        await ctx.author.send(embed = discord.Embed(description = translate(locale, "roulette_burner_phone_no_result"), color = 0xff0000))
                                elif used == translate(locale, 'expired_medicine'):
                                    await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_expired_medicine")}'.format(player = ctx.author.mention), color = 0xff0000))
                                    p1_items.pop(int(item.data['custom_id']) - 1)
                                    normal = random.randint(1, 4)
                                    if normal <= 2:
                                        await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_expired_medicine_success")}'.format(player = ctx.author.mention), color = 0x00ff00))
                                        if not p1_cursed: p1_hp += 2 if p1_hp <= MAX_HP - 2 else 1 if p1_hp <= MAX_HP - 1 else 0
                                    else:
                                        await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_expired_medicine_fail")}'.format(player = ctx.author.mention), color = 0xff0000))
                                        p1_hp -= 1
                                elif used == translate(locale, 'inverter'):
                                    await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_inverter")}'.format(player = ctx.author.mention), color = 0xff8000))
                                    p1_items.pop(int(item.data['custom_id']) - 1)
                                    await channel.send(embed = discord.Embed(description = translate(locale, 'roulette_inverter_result'), color = 0xff8000))
                                    if rounds_order[0] == 0: rounds_order[0] = 1
                                    elif rounds_order[0] == 1: rounds_order[0] = 0
                                elif used == translate(locale, 'handcuffs'):
                                    if not p2_cuffed:
                                        await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_handcuffs")}'.format(player1 = ctx.author.mention, player2 = player.mention), color = 0x00ff00))
                                        p2_cuffed = True
                                        p1_items.pop(int(item.data['custom_id']) - 1)
                                    else:
                                        await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_handcuffs_used")}'.format(player = ctx.author.mention), color = 0xff0000))
                                elif used == translate(locale, 'adrenaline_syringe'):
                                    if len(p2_items) == 0: await ctx.send(embed = discord.Embed(description = translate(locale, 'roulette_syringe_no_items'), color = 0xff0000)); turn_order = 0
                                    await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_syringe")}'.format(player1 = ctx.author.mention, player2 = player.mention), color = 0xff8000))
                                    p1_items.pop(int(item.data['custom_id']) - 1)
                                    init = [str(x) for x in p2_items if x != translate(locale, 'adrenaline_syringe')]
                                    syringe_items_view = discord.ui.View()
                                    for i in range(len(init)):
                                        syringe_items_view.add_item(discord.ui.Button(label = init[i], custom_id = str(i + 1), style = discord.ButtonStyle.gray))
                                    await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_choose_opponent_item")}'.format(player = player.mention), color = 0xff8000), view = syringe_items_view)
                                    item = await self.client.wait_for('interaction', check = lambda interaction: interaction.channel == channel and interaction.user == ctx.author)
                                    used = init[int(item.data['custom_id']) - 1]
                                    if used == translate(locale, 'cigarettes'):
                                        await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_stole_cigarretes")}'.format(player = ctx.author.mention), color = 0x00ff00))
                                        if not p1_cursed: p1_hp += 1 if p1_hp < MAX_HP else 0
                                        p2_items.pop(int(item.data['custom_id']) - 1)
                                    elif used == translate(locale, 'handsaw'):
                                        if sawed:
                                            await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_handcuffs_used")}', color = 0xff0000))
                                            p1_items.insert(int(item.content), items_list[8])
                                        else:
                                            await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_stole_handsaw")}'.format(player = ctx.author.mention), color = 0x00ff00))
                                            sawed = True
                                            damage += 1
                                            p2_items.pop(int(item.data['custom_id']) - 1)
                                    elif used == translate(locale, 'beer'):
                                        await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_stole_beer")}'.format(player = ctx.author.mention, shell = translate(locale, 'live_shell' if rounds_order[0] == 1 else 'blank_shell')), color = 0xff8000))
                                        rounds -= 1
                                        round = rounds_order.pop(0)
                                        p2_items.pop(int(item.data['custom_id']) - 1)
                                    elif used == translate(locale, 'magnifying_glass'):
                                        await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_stole_magnifying_glass")}'.format(player = ctx.author.mention), color = 0xff8000))
                                        await ctx.author.send(embed = discord.Embed(description = f'{translate(locale, "roulette_magnifying_glass_result")}'.format(shell = translate(locale, 'live_shell' if rounds_order[0] == 1 else 'blank_shell')), color = 0xff0000 if rounds_order[0] == 1 else 0x00ff00))
                                        p2_items.pop(int(item.data['custom_id']) - 1)
                                    elif used == translate(locale, 'burner_phone'):
                                        number = ''.join([random.choice('1234567890') for _ in range(6)])
                                        await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_burner_phone")}'.format(player = ctx.author.mention, number = number), color = 0xff8000))
                                        p2_items.pop(int(item.data['custom_id']) - 1)
                                        if len(rounds_order) >= 3:
                                            current = random.randint(1, len(rounds_order) - 1)
                                            await ctx.author.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_burner_phone_result")}'.format(player = ctx.author.mention, shell = translate(locale, 'live_shell' if rounds_order[current] == 1 else 'blank_shell')), color = 0xff8000))
                                        else:
                                            await ctx.author.send(embed = discord.Embed(description = translate(locale, "roulette_player_burner_phone_no_result"), color = 0xff8000))
                                    elif used == translate(locale, 'expired_medicine'):
                                        await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_stole_expired_medicine")}'.format(player = ctx.author.mention), color = 0xff0000))
                                        p2_items.pop(int(item.data['custom_id']) - 1)
                                        normal = random.randint(1, 4)
                                        if normal <= 2:
                                            await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_stole_expired_medicine_success")}'.format(player = ctx.author.mention), color = 0x00ff00))
                                            if not p1_cursed: p1_hp += 2 if p1_hp <= 4 else 1 if p1_hp <= 5 else 0
                                        else:
                                            await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_stole_expired_medicine_fail")}'.format(player = ctx.author.mention), color = 0xff0000))
                                            p1_hp -= 1
                                    elif used == translate(locale, 'inverter'):
                                        await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_stole_inverter")}'.format(player = ctx.author.mention), color = 0xff8000))
                                        p2_items.pop(int(item.data['custom_id']) - 1)
                                        await channel.send(embed = discord.Embed(description = translate(locale, 'roulette_inverter_result'), color = 0xff8000))
                                        if rounds_order[0] == 0: rounds_order[0] = 1
                                        elif rounds_order[0] == 1: rounds_order[0] = 0
                                    elif used == translate(locale, 'handcuffs'):
                                        if not p2_cuffed:
                                            await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_stole_handcuffs")}'.format(player1 = ctx.author.mention, player2 = player.mention), color = 0x00ff00))
                                            p2_cuffed = True
                                            p2_items.pop(int(item.data['custom_id']) - 1)
                                        else:
                                            await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_handcuffs_used")}', color = 0xff0000))
                                    turn_order = 0
                                    await asyncio.sleep(2)
                            elif action.data['custom_id'] == 'stop': stop = True; break
                        elif turn_order == 1:
                            game_view = discord.ui.View()
                            game_view.add_item(discord.ui.Button(label = translate(locale, "roulette_shoot_self"), style = discord.ButtonStyle.gray, custom_id = '1'))
                            game_view.add_item(discord.ui.Button(label = translate(locale, "roulette_shoot_opponent"), style = discord.ButtonStyle.gray, custom_id = '2'))
                            if len(p1_items) > 0: game_view.add_item(discord.ui.Button(label = translate(locale, "roulette_use_item"), style = discord.ButtonStyle.gray, custom_id = '3'))
                            game_view.add_item(discord.ui.Button(label = translate(locale, "roulette_stop_game"), style = discord.ButtonStyle.red, custom_id = 'stop'))
                            await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_choose_action")}'.format(player = player.mention), color = 0xff8000), view = game_view)
                            action = await self.client.wait_for('interaction', check = lambda interaction: interaction.channel == channel and interaction.user == player)
                            await action.response.defer(ephemeral = True)
                            if action.data['custom_id'] == '1':
                                await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_shoot_self")}'.format(player = player.mention), color = 0xff8000))
                                rounds -= 1
                                round = rounds_order.pop(0)
                                if rounds_order[0] == 0:
                                    await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_shoot_self_blank")}'.format(player = ctx.author.mention), color = 0xff8000))
                                    turn_order = 1
                                elif rounds_order[0] == 1:
                                    await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_shoot_self_live")}'.format(player = player.mention, damage = damage), color = 0xff8000))
                                    p2_hp -= damage
                                    turn_order = 0
                                damage = 1
                            elif action.data['custom_id'] == '2':
                                await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_shoot_opponent")}'.format(player1 = player.mention, player2 = ctx.author.mention), color = 0xff8000))
                                rounds -= 1
                                round = rounds_order.pop(0)
                                if round == 0:
                                    await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_shoot_opponent_blank")}'.format(player = ctx.author.mention), color = 0xff8000))
                                elif round == 1:
                                    await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_shoot_opponent_live")}'.format(player = ctx.author.mention, damage = damage), color = 0xff8000))
                                    p1_hp -= damage
                                damage = 1
                                turn_order = 0
                            elif action.data['custom_id'] == '3':
                                init = [str(x) for x in p2_items]
                                await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_choose_item")}'.format(player = player.mention), color = 0xff8000))
                                item = await self.client.wait_for('interaction', check = lambda interaction: interaction.channel == channel and interaction.user == player)
                                used = init[int(item.data['custom_id']) - 1]
                                if used == translate(locale, 'cigarettes'):
                                    await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_cigarettes")}'.format(player = player.mention), color = 0xff8000))
                                    if not p2_cursed: p2_hp += 1 if p2_hp < MAX_HP else 0
                                    p2_items.pop(int(item.data['custom_id']) - 1)
                                elif used == translate(locale, 'handsaw'):
                                    if sawed:
                                        await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_handsaw_used")}'.format(player = player.mention), color = 0xff0000))
                                    else:
                                        await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_handsaw")}'.format(player = player.mention), color = 0xff8000))
                                        damage += 1
                                        p2_items.pop(int(item.data['custom_id']) - 1)
                                elif used == translate(locale, 'beer'):
                                    await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_beer")}'.format(player = player.mention, shell = translate(locale, 'live_shell' if rounds_order[0] == 1 else 'blank_shell')), color = 0xff8000))
                                    rounds -= 1
                                    round = rounds_order.pop(0)
                                    p2_items.pop(int(item.data['custom_id']) - 1)
                                elif used == translate(locale, 'magnifying_glass'):
                                    await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_magnifying_glass")}'.format(player = player.mention), color = 0xff8000))
                                    await player.send(embed = discord.Embed(description = f'{translate(locale, "roulette_magnifying_glass_result")}'.format(shell = translate(locale, 'live_shell' if rounds_order[0] == 1 else 'blank_shell')), color = 0xff8000))
                                    p2_items.pop(int(item.data['custom_id']) - 1)
                                elif used == translate(locale, 'burner_phone'):
                                    number = ''.join([random.choice('1234567890') for _ in range(6)])
                                    await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_burner_phone")}'.format(player = player.mention, number = number), color = 0xff8000))
                                    p2_items.pop(int(item.data['custom_id']) - 1)
                                    if len(rounds_order) >= 3:
                                        current = random.randint(1, len(rounds_order) - 1)
                                        await player.send(embed = discord.Embed(description = f'{translate(locale, "roulette_burner_phone_result")}'.format(current = current + 1, shell = translate(locale, 'live_shell' if rounds_order[current] == 1 else 'blank_shell')), color = 0xff8000))
                                    else:
                                        await player.send(embed = discord.Embed(description = translate(locale, "roulette_burner_phone_no_result"), color = 0xff0000))
                                elif used == translate(locale, 'expired_medicine'):
                                    await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_expired_medicine")}'.format(player = player.mention), color = 0xff0000))
                                    p2_items.pop(int(item.data['custom_id']) - 1)
                                    normal = random.randint(1, 4)
                                    if normal <= 2:
                                        await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_expired_medicine_success")}'.format(player = player.mention), color = 0x00ff00))
                                        if not p2_cursed: p2_hp += 2 if p2_hp <= MAX_HP - 2 else 1 if p2_hp <= MAX_HP - 1 else 0
                                    else:
                                        await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_expired_medicine_fail")}'.format(player = player.mention), color = 0xff0000))
                                        p2_hp -= 1
                                elif used == translate(locale, 'inverter'):
                                    await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_inverter")}'.format(player = player.mention), color = 0xff8000))
                                    p2_items.pop(int(item.data['custom_id']) - 1)
                                    await channel.send(embed = discord.Embed(description = translate(locale, 'roulette_inverter_result'), color = 0xff8000))
                                    if rounds_order[0] == 0: rounds_order[0] = 1
                                    elif rounds_order[0] == 1: rounds_order[0] = 0
                                elif used == translate(locale, 'handcuffs'):
                                    if not p1_cuffed:
                                        await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_handcuffs")}'.format(player1 = player.mention, player2 = ctx.author.mention), color = 0xff8000))
                                        p1_cuffed = True
                                        p2_items.pop(int(item.data['custom_id']) - 1)
                                    else:
                                        await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_handcuffs_used")}'.format(player = player.mention), color = 0xff0000))
                                elif used == translate(locale, 'adrenaline_syringe'):
                                    if len(p1_items) == 0: await channel.send(embed = discord.Embed(description = translate(locale, "roulette_syringe_no_items"), color = 0xff0000)); turn_order = 1
                                    else:
                                        await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_syringe")}'.format(player1 = player.mention, player2 = ctx.author.mention), color = 0xff8000))
                                        p2_items.pop(int(item.data['custom_id']) - 1)
                                        init = [str(x) for x in p1_items if x != translate(locale, 'adrenaline_syringe')]
                                        syringe_items_view = discord.ui.View()
                                        await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_choose_opponent_item")}'.format(player = ctx.author.mention), color = 0xff8000), view = syringe_items_view)
                                        item = await self.client.wait_for('message', check = lambda message: message.channel == channel and message.author == player and message.content.lower() in ([str(x) for x in range(1, len(p1_items) + 1)]))
                                        used = init[int(item.data['custom_id']) - 1]
                                        if used == translate(locale, 'cigarettes'):
                                            await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_stole_cigarettes")}'.format(player = player.mention), color = 0x00ff00))
                                            if not p2_cursed: p2_hp += 1 if p2_hp < MAX_HP else 0
                                            p1_items.pop(int(item.data['custom_id']) - 1)
                                        elif used == translate(locale, 'handsaw'):
                                            if sawed:
                                                await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_handsaw_used")}'.format(player = player.mention), color = 0xff0000))
                                                p2_items.insert(int(item.content), items_list[8])
                                            else:
                                                await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_handsaw")}'.format(player = player.mention), color = 0x00ff00))
                                                sawed = True
                                                damage += 1
                                                p1_items.pop(int(item.data['custom_id']) - 1)
                                        elif used == translate(locale, 'beer'):
                                            await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_stole_beer")}'.format(player = player.mention, shell = translate(locale, 'live_shell' if rounds_order[0] == 1 else 'blank_shell')), color = 0xff8000))
                                            rounds -= 1
                                            round = rounds_order.pop(0)
                                            p1_items.pop(int(item.data['custom_id']) - 1)
                                        elif used == translate(locale, 'magnifying_glass'):
                                            await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_stole_magnifying_glass")}'.format(player = player.mention), color = 0xff8000))
                                            await player.send(embed = discord.Embed(description = f'{translate(locale, "roulette_magnifying_glass_result")}'.format(shell = translate(locale, 'live_shell' if rounds_order[0] == 1 else 'blank_shell')), color = 0xff0000 if rounds_order[0] == 1 else 0x00ff00))
                                            p1_items.pop(int(item.data['custom_id']) - 1)
                                        elif used == translate(locale, 'burner_phone'):
                                            number = ''.join([random.choice('1234567890') for _ in range(6)])
                                            await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_burner_phone")}'.format(player = player.mention, number = number), color = 0xff8000))
                                            p1_items.pop(int(item.data['custom_id']) - 1)
                                            if len(rounds_order) >= 3:
                                                current = random.randint(1, len(rounds_order) - 1)
                                                await player.send(embed = discord.Embed(description = f'{translate(locale, "roulette_burner_phone_result")}'.format(current = current + 1, shell = translate(locale, 'live_shell' if rounds_order[current] == 1 else 'blank_shell')), color = 0xff8000))
                                            else:
                                                await player.send(embed = discord.Embed(description = translate(locale, "roulette_burner_phone_no_result"), color = 0xff0000))
                                        elif used == translate(locale, 'expired_medicine'):
                                            await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_stole_expired_medicine")}'.format(player = player.mention), color = 0xff0000))
                                            p1_items.pop(int(item.data['custom_id']) - 1)
                                            normal = random.randint(1, 4)
                                            if normal <= 2:
                                                await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_expired_medicine_success")}'.format(player = player.mention), color = 0x00ff00))
                                                if not p2_cursed: p2_hp += 2 if p2_hp <= MAX_HP - 2 else 1 if p2_hp <= MAX_HP - 1 else 0
                                            else:
                                                await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_expired_medicine_fail")}'.format(player = player.mention), color = 0xff0000))
                                                p2_hp -= 1
                                        elif used == translate(locale, 'inverter'):
                                            await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_inverter")}'.format(player = player.mention), color = 0xff8000))
                                            p1_items.pop(int(item.data['custom_id']) - 1)
                                            await channel.send(embed = discord.Embed(description = translate(locale, 'roulette_inverter_result'), color = 0xff8000))
                                            if rounds_order[0] == 0: rounds_order[0] = 1
                                            elif rounds_order[0] == 1: rounds_order[0] = 0
                                        elif used == translate(locale, 'handcuffs'):
                                            if not p1_cuffed:
                                                await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_handcuffs")}'.format(player1 = player.mention, player2 = ctx.author.mention), color = 0xff8000))
                                                p1_cuffed = True
                                                p1_items.pop(int(item.data['custom_id']) - 1)
                                            else:
                                                await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_player_handcuffs_used")}'.format(player = player.mention), color = 0xff0000))
                                await asyncio.sleep(1)
                                turn_order = 1
                            elif action.data['custom_id'] == 'stop': stop = True; break
            elif answer.content == 'n':
                await ctx.send(embed = discord.Embed(description = translate(locale, "roulette_play_cancel"), color = 0x2f3136))
        elif player is None or player == bot:
            p1_hp, p2_hp = 6, 6
            channel = await ctx.guild.create_text_channel(f'{translate(locale, 'roulette_session_start')}'.format(ctx_author = ctx.author.display_name, player = player.display_name if player else translate(locale, 'roulette_dealer')))
            await ctx.send(embed = discord.Embed(description = f'{translate(locale, 'roulette_go_to_other_channel')}'.format(channel_mention = channel.mention), color = 0x2f3136))
            await channel.send(embed = discord.Embed(description = translate(locale, "roulette_vs_bot"), color = 0xff8000))
            await channel.send(embed = discord.Embed(description = translate(locale, "roulette_rules_vs_bot"), color = 0x2f3136))
            await asyncio.sleep(15)
            for i in range(11):
                if i == 10: await channel.send(embed = discord.Embed(description = translate(locale, "roulette_stalemate"), color = 0xff8000)); await asyncio.sleep(10); return await channel.delete()
                first = True
                p1_cuffed = False
                p2_cuffed = False
                if stop: await channel.send(embed = discord.Embed(description = translate(locale, "roulette_game_stopped"), color = 0xff8000)); await asyncio.sleep(10); return await channel.delete()
                turn_order = 0
                rounds_order = []
                winner = translate(locale, "roulette_dealer") if p1_hp <= 0 else ctx.author.mention
                if p1_hp <= 0 or p2_hp <= 0:
                    await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_winner")}'.format(winner = winner), color = 0x00ff00 if winner == ctx.author.mention else 0xff0000))
                    with open('leaderboard/leaders.json', 'r') as file:
                        data = json.load(file)
                    if winner != translate(locale, "roulette_dealer"):
                        if str(ctx.author.id) not in data:
                            data[str(ctx.author.id)] = 1
                        else:
                            data[str(ctx.author.id)] += 1
                    else:
                        if '\u0414\u0438\u043b\u0435\u0440' not in data:
                            data['\u0414\u0438\u043b\u0435\u0440'] = 1
                        else:
                            data['\u0414\u0438\u043b\u0435\u0440'] += 1
                    with open('leaderboard/leaders.json', 'w') as users_file:
                        json.dump(data, users_file, indent = 4)
                    await asyncio.sleep(10); return await channel.delete()
                await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_round_number")}'.format(i = i + 1) if i + 1 != 5 else f'{translate(locale, "roulette_round_number_is_5")}'.format(i = i + 1), color = 0xffffff))
                if i + 1 < 5:
                    if len(p1_items) < 7:
                        p1_items.append(items_list[random.randint(1, 9)])
                        p1_items.append(items_list[random.randint(1, 9)])
                    elif len(p1_items) == 7:
                        p1_items.append(items_list[random.randint(1, 9)])
                    elif len(p1_items) == 8:
                        await channel.send(embed = discord.Embed(description = translate(locale, "roulette_no_space"), color = 0xff0000))
                    if len(p2_items) < 7:
                        p2_items.append(items_list[random.randint(1, 9)])
                        p2_items.append(items_list[random.randint(1, 9)])
                    elif len(p2_items) == 7:
                        p2_items.append(items_list[random.randint(1, 9)])
                    elif len(p2_items) == 8: pass
                else:
                    j = 4
                    h = 4
                    while j > 0 and len(p1_items) < 8:
                        p1_items.append(items_list[random.randint(1, 9)])
                        j -= 1
                    if len(p1_items) == 8:
                        await channel.send(embed = discord.Embed(description = translate(locale, "roulette_no_space"), color = 0xff0000))
                    while h > 0 and len(p2_items) < 8:
                        p2_items.append(items_list[random.randint(1, 9)])
                        h -= 1
                rounds = random.randint(2, 8)
                while rounds > 0:
                    if p1_hp <= 2: p1_cursed = True
                    if p2_hp <= 2: p2_cursed = True
                    if p1_cuffed and turn_order == 0:
                        turn_order = 1
                        p1_cuffed = False
                    if p2_cuffed and turn_order == 1:
                        turn_order = 0
                        p2_cuffed = False
                    sawed = False
                    if p1_hp <= 0 or p2_hp <= 0:
                        break
                    if len(rounds_order) == 0:
                        for _ in range(rounds):
                            rounds_order.append(random.randint(0, 1))
                        if rounds_order.count(0) == 0: rounds_order.pop(); rounds_order.append(0)
                        if rounds_order.count(1) == 0: rounds_order.pop(); rounds_order.append(1)
                    if p1_cuffed: cuffed = 'Человек' if locale != 'en' else 'Player'
                    if p2_cuffed: cuffed = 'Дилер' if locale != 'en' else 'Dealer'
                    if p1_cursed: cursed = 'Человек' if locale != 'en' else 'Player'
                    if p2_cursed: cursed = 'Дилер' if locale != 'en' else 'Dealer'
                    if p1_cursed and p2_cursed: cursed = 'Никто' if locale != 'en' else 'Nobody'
                    await channel.send(embed = discord.Embed(description = f'Патронов - {len(rounds_order) if first else "?"}, боевых - {rounds_order.count(1) if first else '?'}, холостых - {rounds_order.count(0) if first else '?'}\nВаше здоровье - {p1_hp}\nЗдоровье врага - {p2_hp}\n{f'Ваши предметы ({len(p1_items)}) - {", ".join(p1_items)}' if len(p1_items) > 0 else "У вас нет предметов"}\n{f'Предметы противника ({len(p2_items)}) - {", ".join(p2_items)}' if len(p2_items) > 0 else "У противника нет предметов"}{f"\n__{cuffed} закован в наручники и пропускает ход__" if p1_cuffed or p2_cuffed else ""}{f'\n**{cursed} не может восстанавливать здоровье**' if p1_cursed or p2_cursed else ''}', color = 0x2f3136))
                    first = False
                    if turn_order == 0:
                        game_view = discord.ui.View()
                        game_view.add_item(discord.ui.Button(label = translate(locale, "roulette_shoot_self"), style = discord.ButtonStyle.gray, custom_id = '1'))
                        game_view.add_item(discord.ui.Button(label = translate(locale, "roulette_shoot_opponent"), style = discord.ButtonStyle.gray, custom_id = '2'))
                        if len(p1_items) > 0: game_view.add_item(discord.ui.Button(label = translate(locale, "roulette_use_item"), style = discord.ButtonStyle.gray, custom_id = '3'))
                        game_view.add_item(discord.ui.Button(label = translate(locale, "roulette_stop_game"), style = discord.ButtonStyle.red, custom_id = 'stop'))
                        await channel.send(embed = discord.Embed(description = translate(locale, "roulette_choose_action"), color = 0xff8000), view = game_view)
                        action = await self.client.wait_for('interaction', check = lambda interaction: interaction.user == ctx.author)
                        await action.response.defer(ephemeral = True)
                        if action.data['custom_id'] == '1':
                            await action.followup.send(embed = discord.Embed(description = translate(locale, "roulette_chose_self"), color = 0xff0000))
                            await asyncio.sleep(3)
                            current_round = rounds_order.pop(0)
                            rounds -= 1
                            if current_round == 0:
                                await channel.send(embed = discord.Embed(description = translate(locale, "roulette_shoot_self_blank"), color = 0x00ff00))
                                turn_order = 0
                            else:
                                await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_shoot_self_live")}'.format(damage = damage), color = 0xff0000))
                                p1_hp -= damage
                                turn_order = 1
                            await asyncio.sleep(1)
                            damage = 1
                        elif action.data['custom_id'] == '2':
                            await action.followup.send(embed = discord.Embed(description = translate(locale, "roulette_chose_opponent"), color = 0xff8000))
                            await asyncio.sleep(3)
                            current_round = rounds_order.pop(0)
                            rounds -= 1
                            if current_round == 0:
                                await channel.send(embed = discord.Embed(description = translate(locale, "roulette_shoot_opponent_blank"), color = 0xff0000))
                            else:
                                await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_shoot_opponent_live")}'.format(damage = damage), color = 0x00ff00))
                                p2_hp -= damage
                            damage = 1
                            await asyncio.sleep(1)
                            turn_order = 1
                        elif action.data['custom_id'] == '3':
                            init = [str(x) for x in p1_items]
                            items_view = discord.ui.View()
                            for i in range(len(init)):
                                items_view.add_item(discord.ui.Button(label = init[i], style = discord.ButtonStyle.gray, custom_id = str(i + 1)))
                            await action.followup.send(embed = discord.Embed(description = f'{translate(locale, "roulette_chose_item")}', color = 0xff8000), view = items_view)
                            item = await self.client.wait_for('interaction', check = lambda interaction: interaction.user == ctx.author)
                            await item.response.defer(ephemeral = True)
                            used = init[int(item.data['custom_id']) - 1]
                            if used == translate(locale, 'cigarettes'):
                                await channel.send(embed = discord.Embed(description = translate(locale, "roulette_cigarettes"), color = 0x00ff00))
                                if not p1_cursed: p1_hp += 1 if p1_hp < 6 else 0
                                p1_items.pop(int(item.data['custom_id']) - 1)
                            elif used == translate(locale, 'handsaw'):
                                if sawed:
                                    await channel.send(embed = discord.Embed(description = translate(locale, "roulette_handsaw_used"), color = 0xff0000))
                                else:
                                    await channel.send(embed = discord.Embed(description = translate(locale, "roulette_handsaw"), color = 0x00ff00))
                                    sawed = True
                                    damage += 1
                                    p1_items.pop(int(item.data['custom_id']) - 1)
                            elif used == translate(locale, 'beer'):
                                await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_beer")}'.format(shell = translate(locale, 'live_shell' if rounds_order[0] == 1 else 'blank_shell')), color = 0xff8000))
                                rounds -= 1
                                round = rounds_order.pop(0)
                                p1_items.pop(int(item.data['custom_id']) - 1)
                            elif used == translate(locale, 'magnifying_glass'):
                                await channel.send(embed = discord.Embed(description = translate(locale, "roulette_magnifying_glass_use"), color = 0xff8000))
                                await asyncio.sleep(3)
                                await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_magnifying_glass_result")}'.format(shell = translate(locale, 'live_shell' if rounds_order[0] == 1 else 'blank_shell')), color = 0xff0000 if rounds_order[0] == 1 else 0x00ff00))
                                p1_items.pop(int(item.data['custom_id']) - 1)
                            elif used == translate(locale, 'burner_phone'):
                                number = ''.join([random.choice('1234567890') for _ in range(6)])
                                await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_burner_phone_use")}'.format(number = number), color = 0xff8000))
                                await asyncio.sleep(3)
                                p1_items.pop(int(item.data['custom_id']) - 1)
                                if len(rounds_order) >= 3:
                                    current = random.randint(1, len(rounds_order) - 1)
                                    await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_burner_phone_result")}'.format(current = current + 1, shell = translate(locale, 'live_shell' if rounds_order[current] == 1 else 'blank_shell')), color = 0xff8000))
                                else:
                                    await channel.send(embed = discord.Embed(description = translate(locale, "roulette_burner_phone_no_result"), color = 0xff8000))
                            elif used == translate(locale, 'expired_medicine'):
                                await channel.send(embed = discord.Embed(description = translate(locale, "roulette_expired_medicine_use"), color = 0xff0000))
                                await asyncio.sleep(3)
                                p1_items.pop(int(item.data['custom_id']) - 1)
                                normal = random.randint(1, 4)
                                if normal <= 2:
                                    await channel.send(embed = discord.Embed(description = translate(locale, "roulette_expired_medicine_success"), color = 0x00ff00))
                                    if not p1_cursed: p1_hp += 2 if p1_hp <= 4 else 1 if p1_hp <= 5 else 0
                                else:
                                    await channel.send(embed = discord.Embed(description = translate(locale, "roulette_expired_medicine_fail"), color = 0xff0000))
                                    p1_hp -= 1
                            elif used == translate(locale, 'inverter'):
                                await channel.send(embed = discord.Embed(description = translate(locale, "roulette_inverter_use"), color = 0xff8000))
                                await asyncio.sleep(3)
                                p1_items.pop(int(item.data['custom_id']) - 1)
                                await channel.send(embed = discord.Embed(description = translate(locale, "roulette_inverter_result"), color = 0xff8000))
                                if rounds_order[0] == 0: rounds_order[0] = 1
                                elif rounds_order[0] == 1: rounds_order[0] = 0
                            elif used == translate(locale, 'handcuffs'):
                                if not p2_cuffed:
                                    await channel.send(embed = discord.Embed(description = translate(locale, "roulette_handcuffs_use"), color = 0x00ff00))
                                    await asyncio.sleep(3)
                                    p2_cuffed = True
                                    p1_items.pop(int(item.data['custom_id']) - 1)
                                else:
                                    await channel.send(embed = discord.Embed(description = translate(locale, "roulette_handcuffs_already_used"), color = 0xff0000))
                            elif used == translate(locale, 'adrenaline_syringe'):
                                if len(p1_items) == 0: await channel.send(embed = discord.Embed(description = translate(locale, "roulette_adrenaline_syringe_no_items"), color = 0xff0000)); turn_order = 0
                                else:
                                    await channel.send(embed = discord.Embed(description = translate(locale, "roulette_syringe_use"), color = 0x00ff00))
                                    await asyncio.sleep(3)
                                    p1_items.pop(int(item.data['custom_id']) - 1)
                                    init = [str(x) for x in p2_items if x != translate(locale, 'adrenaline_syringe')]
                                    syringe_items_view = discord.ui.View()
                                    for i in range(len(init)):
                                        syringe_items_view.add_item(discord.ui.Button(label = init[i], style = discord.ButtonStyle.gray, custom_id = str(i + 1)))
                                    await channel.send(embed = discord.Embed(description = translate(locale, "roulette_choose_opponent_item"), color = 0xff8000), view = syringe_items_view)
                                    item = await self.client.wait_for('interaction', check = lambda interaction: interaction.channel == channel and interaction.user == ctx.author)
                                    await item.response.defer(ephemeral = True)
                                    used = init[int(item.data['custom_id']) - 1]
                                    if used == translate(locale, 'cigarettes'):
                                        await channel.send(embed = discord.Embed(description = translate(locale, 'roulette_cigarettes_stolen'), color = 0x00ff00))
                                        if not p1_cursed: p1_hp += 1 if p1_hp < 6 else 0
                                        p2_items.pop(int(item.data['custom_id']) - 1)
                                    elif used == translate(locale, 'handsaw'):
                                        if sawed:
                                            await channel.send(embed = discord.Embed(description = translate(locale, 'roulette_handsaw_used'), color = 0xff0000))
                                            p1_items.insert(int(item.data['custom_id']), items_list[8])
                                        else:
                                            await channel.send(embed = discord.Embed(description = translate(locale, 'roulette_handsaw_stolen'), color = 0x00ff00))
                                            sawed = True
                                            damage += 1
                                            p2_items.pop(int(item.data['custom_id']) - 1)
                                    elif used == translate(locale, 'beer'):
                                        round = rounds_order.pop(0)
                                        await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_beer_stolen")}'.format(shell = translate(locale, 'live_shell' if round == 1 else 'blank_shell')), color = 0xff8000))
                                        rounds -= 1
                                        p2_items.pop(int(item.data['custom_id']) - 1)
                                    elif used == translate(locale, 'magnifying_glass'):
                                        await channel.send(embed = discord.Embed(description = translate(locale, 'roulette_magnifying_glass_stolen'), color = 0xff8000))
                                        await asyncio.sleep(3)
                                        await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_magnifying_glass_result")}'.format(shell = translate(locale, 'live_shell' if rounds_order[0] == 1 else 'blank_shell')), color = 0xff0000 if rounds_order[0] == 1 else 0x00ff00))
                                        p2_items.pop(int(item.data['custom_id']) - 1)
                                    elif used == translate(locale, 'burner_phone'):
                                        number = ''.join([random.choice('1234567890') for _ in range(6)])
                                        await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_burner_phone_use")}'.format(number = number), color = 0xff8000))
                                        await asyncio.sleep(3)
                                        p2_items.pop(int(item.data['custom_id']) - 1)
                                        if len(rounds_order) >= 3:
                                            current = random.randint(1, len(rounds_order) - 1)
                                            await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_burner_phone_result")}'.format(current = current + 1, shell = translate(locale, 'live_shell' if rounds_order[current] == 1 else 'blank_shell')), color = 0xff8000))
                                        else:
                                            await channel.send(embed = discord.Embed(description = translate(locale, 'roulette_burner_phone_no_result'), color = 0xff0000))
                                    elif used == translate(locale, 'expired_medicine'):
                                        await channel.send(embed = discord.Embed(description = translate(locale, 'roulette_expired_medicine_stolen'), color = 0xff0000))
                                        await asyncio.sleep(3)
                                        p2_items.pop(int(item.data['custom_id']) - 1)
                                        normal = random.randint(1, 4)
                                        if normal <= 2:
                                            await channel.send(embed = discord.Embed(description = translate(locale, 'roulette_expired_medicine_success'), color = 0x00ff00))
                                            if not p1_cursed: p1_hp += 2 if p1_hp <= 4 else 1 if p1_hp <= 5 else 0
                                        else:
                                            await channel.send(embed = discord.Embed(description = translate(locale, 'roulette_expired_medicine_fail'), color = 0xff0000))
                                            p1_hp -= 1
                                    elif used == translate(locale, 'inverter'):
                                        await channel.send(embed = discord.Embed(description = translate(locale, "roulette_inverter_stolen"), color = 0xff8000))
                                        await asyncio.sleep(3)
                                        p2_items.pop(int(item.data['custom_id']) - 1)
                                        await channel.send(embed = discord.Embed(description = translate(locale, "roulette_inverter_result"), color = 0xff8000))
                                        if rounds_order[0] == 0: rounds_order[0] = 1
                                        elif rounds_order[0] == 1: rounds_order[0] = 0
                                    elif used == translate(locale, 'handcuffs'):
                                        if not p2_cuffed:
                                            await channel.send(embed = discord.Embed(description = translate(locale, 'roulette_handcuffs_stolen'), color = 0x00ff00))
                                            await asyncio.sleep(3)
                                            p2_cuffed = True
                                            p2_items.pop(int(item.data['custom_id']) - 1)
                                        else:
                                            await channel.send(embed = discord.Embed(description = translate(locale, 'roulette_handcuffs_already_used'), color = 0xff0000))
                            await asyncio.sleep(1)
                            turn_order = 0
                        elif action.data['custom_id'] == 'stop': stop = True; break
                    elif turn_order == 1: # TODO: бот должен иметь более развитый интеллект, зависящий от обстоятельств, а не рандома, который позволит ему чаще использовать предметы и принимать правильные решения
                        glass = False     # Сейчас бот имеет версию ИИ 0.5
                        if not p2_items:
                            if rounds_order.count(1) > rounds_order.count(0):
                                action = 3
                            elif rounds_order.count(1) < rounds_order.count(0):
                                action = 2
                            else:
                                action = random.randint(1, 4)
                            if action <= 2:
                                await channel.send(embed = discord.Embed(description = translate(locale, "roulette_dealer_shoot_self"), color = 0xff8000))
                                await asyncio.sleep(3)
                                rounds -= 1
                                round = rounds_order.pop(0)
                                if round == 0:
                                    await channel.send(embed = discord.Embed(description = translate(locale, "roulette_dealer_shoot_self_blank"), color = 0xff0000))
                                    turn_order = 1
                                elif round == 1:
                                    await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_dealer_shoot_self_live")}'.format(damage = damage), color = 0x00ff00))
                                    p2_hp -= damage
                                    turn_order = 0
                                damage = 1
                            elif action >= 3:
                                await channel.send(embed = discord.Embed(description = translate(locale, "roulette_dealer_shoot_opponent"), color = 0xff0000))
                                await asyncio.sleep(3)
                                rounds -= 1
                                round = rounds_order.pop(0)
                                if round == 0:
                                    await channel.send(embed = discord.Embed(description = translate(locale, "roulette_dealer_shoot_opponent_blank"), color = 0x00ff00))
                                elif round == 1:
                                    await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_dealer_shoot_opponent_live")}'.format(damage = damage), color = 0xff0000))
                                    p1_hp -= damage
                                damage = 1
                                turn_order = 0
                        else:
                            if rounds_order.count(1) > rounds_order.count(0):
                                action = 3
                            elif rounds_order.count(1) < rounds_order.count(0):
                                action = 2
                            else:
                                action = random.randint(1, 4)
                            if len(rounds_order) >= 4 and translate(locale, 'beer') in p2_items:
                                p2_items.pop(p2_items.index(translate(locale, 'beer')))
                                round = rounds_order.pop(0)
                                await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_dealer_used_beer")}'.format(shell = translate(locale, "live_shell" if round == 1 else "blank_shell")), color = 0xff8000))
                                await asyncio.sleep(3)
                                rounds -= 1
                            elif translate(locale, 'inverter') in p2_items and rounds_order[0] == 0 and len(rounds_order) == 1:
                                p2_items.pop(p2_items.index(translate(locale, 'inverter')))
                                await channel.send(embed = discord.Embed(description = translate(locale, 'roulette_dealer_used_inverter'), color = 0xff8000))
                                await asyncio.sleep(3)
                                await channel.send(embed = discord.Embed(description = translate(locale, 'roulette_inverter_result'), color = 0xff8000))
                                if rounds_order[0] == 0: rounds_order[0] = 1
                                elif rounds_order[0] == 1: rounds_order[0] = 0
                                action = 3
                            elif translate(locale, 'handcuffs') in p2_items and rounds_order.count(1) > 0 and not p1_cuffed:
                                p2_items.pop(p2_items.index(translate(locale, 'handcuffs')))
                                await channel.send(embed = discord.Embed(description = translate(locale, 'roulette_dealer_used_handcuffs'), color = 0xff0000))
                                await asyncio.sleep(3)
                                p1_cuffed = True
                            elif translate(locale, 'cigarettes') in p2_items and p2_hp < 6:
                                p2_items.pop(p2_items.index(translate(locale, 'cigarettes')))
                                await channel.send(embed = discord.Embed(description = translate(locale, 'roulette_dealer_used_cigarettes'), color = 0xff8000))
                                await asyncio.sleep(3)
                                if not p2_cursed: p2_hp += 1
                            elif translate(locale, 'magnifying_glass') in p2_items and (rounds_order.count(1) > 0 and len(rounds_order) > 1):
                                p2_items.pop(p2_items.index(translate(locale, 'magnifying_glass')))
                                await channel.send(embed = discord.Embed(description = translate(locale, 'roulette_dealer_used_magnifying_glass'), color = 0xff0000))
                                await asyncio.sleep(3)
                                glass = True
                                if rounds_order[0] == 0:
                                    action = 1
                                    if translate(locale, 'inverter') in p2_items:
                                        p2_items.pop(p2_items.index(translate(locale, 'inverter')))
                                        await channel.send(embed = discord.Embed(description = translate(locale, 'roulette_dealer_used_inverter'), color = 0xff8000))
                                        await asyncio.sleep(3)
                                        await channel.send(embed = discord.Embed(description = translate(locale, 'roulette_inverter_result'), color = 0xff8000))
                                        if rounds_order[0] == 0: rounds_order[0] = 1
                                        elif rounds_order[0] == 1: rounds_order[0] = 0
                                        if translate(locale, 'handsaw') in p2_items and not sawed:
                                            p2_items.pop(p2_items.index(translate(locale, 'handsaw')))
                                            damage += 1
                                            await channel.send(embed = discord.Embed(description = translate(locale, 'roulette_dealer_used_handsaw'), color = 0xff0000))
                                        action = 3
                                    elif translate(locale, 'adrenaline_syringe') in p2_items and translate(locale, 'inverter') in p1_items:
                                        p2_items.pop(p2_items.index(translate(locale, 'adrenaline_syringe')))
                                        await channel.send(embed = discord.Embed(description = translate(locale, 'roulette_dealer_used_syringe'), color = 0xff8000))
                                        await asyncio.sleep(3)
                                        p1_items.pop(p1_items.index(translate(locale, 'inverter')))
                                        await channel.send(embed = discord.Embed(description = translate(locale, 'roulette_dealer_stole_inverter'), color = 0xff8000))
                                        await asyncio.sleep(3)
                                        await channel.send(embed = discord.Embed(description = translate(locale, 'roulette_inverter_result'), color = 0xff8000))
                                        await asyncio.sleep(1)
                                        if rounds_order[0] == 0: rounds_order[0] = 1
                                        elif rounds_order[0] == 1: rounds_order[0] = 0
                                        if translate(locale, 'handsaw') in p2_items and not sawed:
                                            p2_items.pop(p2_items.index(translate(locale, 'handsaw')))
                                            damage += 1
                                            await channel.send(embed = discord.Embed(description = translate(locale, 'roulette_dealer_used_handsaw'), color = 0xff0000))
                                        action = 3
                                    else:
                                        if action <= 2:
                                            await channel.send(embed = discord.Embed(description = translate(locale, 'roulette_dealer_shoot_self'), color = 0xff8000))
                                            await asyncio.sleep(3)
                                            rounds -= 1
                                            round = rounds_order.pop(0)
                                            if round == 0:
                                                await channel.send(embed = discord.Embed(description = translate(locale, 'roulette_dealer_shoot_self_blank'), color = 0xff0000))
                                                turn_order = 1
                                            elif round == 1:
                                                await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_dealer_shoot_self_live")}'.format(damage = damage), color = 0x00ff00))
                                                p2_hp -= damage
                                                turn_order = 0
                                            damage = 1
                                        elif action >= 3:
                                            await channel.send(embed = discord.Embed(description = translate(locale, 'roulette_dealer_shoot_opponent'), color = 0xff0000))
                                            await asyncio.sleep(3)
                                            rounds -= 1
                                            round = rounds_order.pop(0)
                                            if round == 0:
                                                await channel.send(embed = discord.Embed(description = translate(locale, 'roulette_dealer_shoot_opponent_blank'), color = 0x00ff00))
                                            elif round == 1:
                                                await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_dealer_shoot_opponent_live")}'.format(damage = damage), color = 0xff0000))
                                                p1_hp -= damage
                                            damage = 1
                                            turn_order = 0
                                else:
                                    if translate(locale, 'handsaw') in p2_items and not sawed:
                                        p2_items.pop(p2_items.index(translate(locale, 'handsaw')))
                                        damage += 1
                                        await channel.send(embed = discord.Embed(description = translate(locale, 'roulette_dealer_used_handsaw'), color = 0xff0000))
                                        await asyncio.sleep(1)
                                    elif translate(locale, 'adrenaline_syringe') in p2_items and translate(locale, 'handsaw') in p1_items and not sawed:
                                        p2_items.pop(p2_items.index(translate(locale, 'adrenaline_syringe')))
                                        await channel.send(embed = discord.Embed(description = translate(locale, 'roulette_dealer_used_syringe'), color = 0xff8000))
                                        await asyncio.sleep(3)
                                        await channel.send(embed = discord.Embed(description = translate(locale, 'roulette_dealer_stole_handsaw'), color = 0xff0000))
                                        p1_items.pop(p1_items.index(translate(locale, 'handsaw')))
                                        damage += 1
                                        await asyncio.sleep(1)
                                    await channel.send(embed = discord.Embed(description = translate(locale, 'roulette_dealer_shoot_opponent'), color = 0xff0000))
                                    await asyncio.sleep(3)
                                    await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_dealer_shoot_opponent_live")}'.format(damage = damage), color = 0xff0000))
                                    rounds -= 1
                                    rounds_order.pop(0)
                                    p1_hp -= damage
                                    damage = 1
                                    turn_order = 0
                            elif translate(locale, 'expired_medicine') in p2_items and 1 < p2_hp < 6:
                                p2_items.pop(p2_items.index(translate(locale, 'expired_medicine')))
                                await channel.send(embed = discord.Embed(description = translate(locale, 'roulette_dealer_used_expired_medicine'), color = 0xff8000))
                                await asyncio.sleep(3)
                                normal = random.randint(1, 4)
                                if normal <= 2:
                                    await channel.send(embed = discord.Embed(description = translate(locale, 'roulette_dealer_expired_medicine_success'), color = 0xff0000))
                                    if not p2_cursed: p2_hp += 2 if p2_hp <= 4 else 1 if p2_hp <= 5 else 0
                                else:
                                    await channel.send(embed = discord.Embed(description = translate(locale, 'roulette_dealer_expired_medicine_fail'), color = 0x00ff00))
                                    p2_hp -= 1
                                await asyncio.sleep(1)
                            elif translate(locale, 'handsaw') in p2_items and rounds_order.count(1) > rounds_order.count(0):
                                p2_items.pop(p2_items.index(translate(locale, 'handsaw')))
                                await channel.send(embed = discord.Embed(description = translate(locale, 'roulette_dealer_used_handsaw'), color = 0xff0000))
                                await asyncio.sleep(3)
                                damage += 1
                                action = 3
                            elif translate(locale, 'adrenaline_syringe') in p2_items and p1_items:
                                p2_items.pop(p2_items.index(translate(locale, 'adrenaline_syringe')))
                                if p2_hp < 6 and translate(locale, 'cigarettes') in p1_items:
                                    p1_items.pop(p1_items.index(translate(locale, 'cigarettes')))
                                    await channel.send(embed = discord.Embed(description = translate(locale, 'roulette_dealer_stole_cigarettes'), color = 0xff0000))
                                    await asyncio.sleep(3)
                                    p2_hp += 1
                                elif 1 < p2_hp < 6 and translate(locale, 'expired_medicine') in p1_items:
                                    p1_items.pop(p1_items.index(translate(locale, 'expired_medicine')))
                                    await channel.send(embed = discord.Embed(description = translate(locale, 'roulette_dealer_stole_expired_medicine'), color = 0xff0000))
                                    await asyncio.sleep(3)
                                    normal = random.randint(1, 4)
                                    if normal <= 2:
                                        await channel.send(embed = discord.Embed(description = translate(locale, 'roulette_dealer_expired_medicine_success'), color = 0x00ff00))
                                        if not p2_cursed: p2_hp += 2 if p2_hp <= 4 else 1 if p2_hp <= 5 else 0
                                    else:
                                        await channel.send(embed = discord.Embed(description = translate(locale, 'roulette_dealer_expired_medicine_fail'), color = 0xff0000))
                                        p2_hp -= 1
                                    await asyncio.sleep(1)
                                elif translate(locale, 'magnifying_glass') in p1_items and (rounds_order.count(1) > 0 and len(rounds_order) > 1):
                                    p1_items.pop(p1_items.index(translate(locale, 'magnifying_glass')))
                                    await channel.send(embed = discord.Embed(description = translate(locale, 'roulette_dealer_used_magnifying_glass'), color = 0xff0000))
                                    await asyncio.sleep(3)
                                    if rounds_order[0] == 0:
                                        action = 1
                                        if translate(locale, 'inverter') in p2_items:
                                            p2_items.pop(p2_items.index(translate(locale, 'inverter')))
                                            await channel.send(embed = discord.Embed(description = translate(locale, 'roulette_dealer_used_inverter'), color = 0xff8000))
                                            await asyncio.sleep(3)
                                            await channel.send(embed = discord.Embed(description = translate(locale, 'roulette_inverter_result'), color = 0xff8000))
                                            if rounds_order[0] == 0: rounds_order[0] = 1
                                            elif rounds_order[0] == 1: rounds_order[0] = 0
                                            if translate(locale, 'handsaw') in p2_items and not sawed:
                                                p2_items.pop(p2_items.index(translate(locale, 'handsaw')))
                                                damage += 1
                                                await channel.send(embed = discord.Embed(description = translate(locale, 'roulette_dealer_used_handsaw'), color = 0xff0000))
                                            action = 3
                                        elif translate(locale, 'adrenaline_syringe') in p2_items and translate(locale, 'inverter') in p1_items:
                                            p2_items.pop(p2_items.index(translate(locale, 'adrenaline_syringe')))
                                            await channel.send(embed = discord.Embed(description = translate(locale, 'roulette_dealer_used_syringe'), color = 0xff8000))
                                            await asyncio.sleep(3)
                                            p1_items.pop(p1_items.index(translate(locale, 'inverter')))
                                            await channel.send(embed = discord.Embed(description = translate(locale, 'roulette_dealer_stole_inverter'), color = 0xff8000))
                                            await asyncio.sleep(3)
                                            await channel.send(embed = discord.Embed(description = translate(locale, 'roulette_inverter_result'), color = 0xff8000))
                                            await asyncio.sleep(1)
                                            if rounds_order[0] == 0: rounds_order[0] = 1
                                            elif rounds_order[0] == 1: rounds_order[0] = 0
                                            if translate(locale, 'handsaw') in p2_items and not sawed:
                                                p2_items.pop(p2_items.index(translate(locale, 'handsaw')))
                                                damage += 1
                                                await channel.send(embed = discord.Embed(description = translate(locale, 'roulette_dealer_used_handsaw'), color = 0xff0000))
                                            action = 3
                                        else:
                                            if action <= 2:
                                                await channel.send(embed = discord.Embed(description = translate(locale, 'roulette_dealer_shoot_self'), color = 0xff8000))
                                                await asyncio.sleep(3)
                                                rounds -= 1
                                                round = rounds_order.pop(0)
                                                if round == 0:
                                                    await channel.send(embed = discord.Embed(description = translate(locale, 'roulette_dealer_shoot_self_blank'), color = 0xff0000))
                                                    turn_order = 1
                                                elif round == 1:
                                                    await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_dealer_shoot_self_live")}'.format(damage = damage), color = 0x00ff00))
                                                    p2_hp -= damage
                                                    turn_order = 0
                                                damage = 1
                                            elif action >= 3:
                                                await channel.send(embed = discord.Embed(description = translate(locale, 'roulette_dealer_shoot_opponent'), color = 0xff0000))
                                                await asyncio.sleep(3)
                                                rounds -= 1
                                                round = rounds_order.pop(0)
                                                if round == 0:
                                                    await channel.send(embed = discord.Embed(description = translate(locale, 'roulette_dealer_shoot_opponent_blank'), color = 0x00ff00))
                                                elif round == 1:
                                                    await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_dealer_shoot_opponent_live")}'.format(damage = damage), color = 0xff0000))
                                                    p1_hp -= damage
                                                damage = 1
                                                turn_order = 0
                                    else:
                                        if translate(locale, 'handsaw') in p2_items and not sawed:
                                            p2_items.pop(p2_items.index(translate(locale, 'handsaw')))
                                            damage += 1
                                            await channel.send(embed = discord.Embed(description = translate(locale, 'roulette_dealer_used_handsaw'), color = 0xff0000))
                                            await asyncio.sleep(1)
                                        elif translate(locale, 'adrenaline_syringe') in p2_items and translate(locale, 'handsaw') in p1_items and not sawed:
                                            p2_items.pop(p2_items.index(translate(locale, 'adrenaline_syringe')))
                                            await channel.send(embed = discord.Embed(description = translate(locale, 'roulette_dealer_used_syringe'), color = 0xff8000))
                                            await asyncio.sleep(3)
                                            await channel.send(embed = discord.Embed(description = translate(locale, 'roulette_dealer_stole_handsaw'), color = 0xff0000))
                                            p1_items.pop(p1_items.index(translate(locale, 'handsaw')))
                                            damage += 1
                                            await asyncio.sleep(1)
                                        await channel.send(embed = discord.Embed(description = translate(locale, 'roulette_dealer_shoot_opponent'), color = 0xff0000))
                                        await asyncio.sleep(3)
                                        await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_dealer_shoot_opponent_live")}'.format(damage = damage), color = 0xff0000))
                                        rounds -= 1
                                        rounds_order.pop(0)
                                        p1_hp -= damage
                                        damage = 1
                                        turn_order = 0
                                elif translate(locale, 'handcuffs') in p1_items:
                                    p1_items.pop(p1_items.index(translate(locale, 'handcuffs')))
                                    await channel.send(embed = discord.Embed(description = translate(locale, 'roulette_dealer_stole_handcuffs'), color = 0xff0000))
                                    await asyncio.sleep(3)
                                    p1_cuffed = True
                                else:
                                    p2_items.append(items_list[8])
                                    action = 3
                            if action <= 2 and not glass:
                                await channel.send(embed = discord.Embed(description = translate(locale, 'roulette_dealer_shoot_self'), color = 0xff8000))
                                await asyncio.sleep(3)
                                rounds -= 1
                                round = rounds_order.pop(0)
                                if round == 0:
                                    await channel.send(embed = discord.Embed(description = translate(locale, 'roulette_dealer_shoot_self_blank'), color = 0xff0000))
                                    turn_order = 1
                                elif round == 1:
                                    await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_dealer_shoot_self_live")}'.format(damage = damage), color = 0x00ff00))
                                    p2_hp -= damage
                                    turn_order = 0
                                damage = 1
                            elif action >= 3 and not glass:
                                await channel.send(embed = discord.Embed(description = translate(locale, 'roulette_dealer_shoot_opponent'), color = 0xff0000))
                                await asyncio.sleep(3)
                                rounds -= 1
                                round = rounds_order.pop(0)
                                if round == 0:
                                    await channel.send(embed = discord.Embed(description = translate(locale, 'roulette_dealer_shoot_opponent_blank'), color = 0x00ff00))
                                elif round == 1:
                                    await channel.send(embed = discord.Embed(description = f'{translate(locale, "roulette_dealer_shoot_opponent_live")}'.format(damage = damage), color = 0xff0000))
                                    p1_hp -= damage
                                damage = 1
                                turn_order = 0

    @commands.command()
    @commands.cooldown(1, 15, commands.BucketType.user)
    @commands.bot_has_permissions(manage_messages = True)
    async def dotersbrain(self, ctx: commands.Context):
        words = ['чё', 'а', 'да', 'нет', 'ок']
        answers = {'чё': 'хуй через плечо', 'а': 'хуй на', 'да': 'пизда', 'нет': 'пидора ответ', 'ок': 'хуй намок'}
        await ctx.send(f'{ctx.author.mention}, через 5 секунд появится одно из слов ({", ".join(words)}), на которое вам нужно будет правильно ответить. На размышление 5 секунд')
        await asyncio.sleep(5)
        sent = await ctx.send(random.choice(words))
        try:
            msg = await self.client.wait_for('message', timeout = 5, check = lambda message: message.author == ctx.author and message.channel == ctx.message.channel)
            if msg.content.lower() == answers[sent.content]:
                await ctx.send('Поздравляю, у вас 3 стадия рака!')
            else:
                await ctx.send('Вы совершенно здоровый человек! ||попробуйте cy/help dotersbrain||')
        except asyncio.TimeoutError:
            await ctx.send(f'{ctx.author.mention}, слишком медленно.')
        await sent.delete()

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def aghanim(self, ctx: commands.Context):
        rand = random.randint(1, 40)
        if rand >= 15:
            await ctx.send(embed = discord.Embed(description = f'Ого! Твой аганим длиной аж {rand} см!', color = 0xff8000))
        else:
            await ctx.send(embed = discord.Embed(description = f'Длина твоего аганима {rand} см, лошара', color = 0xff8000))

async def setup(client):
    await client.add_cog(Fun(client))
