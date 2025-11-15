import asyncio
import json
import random
from datetime import timedelta
from typing import cast

import discord
from discord.ext import commands

from cogs.Constants import colors
from cogs.Logging import LOGS
from functions import get_locale, get_plural_form, translate, connect_db

class RouletteSettings:
    def get_user_settings(self, user_id: int) -> tuple:
        conn = connect_db('roulette_settings')
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM user_settings WHERE user_id = %s", (user_id,))
                return cur.fetchone()
        finally:
            conn.close()

    def save(self, user_id: int, settings_data: dict) -> None:
        conn = connect_db('roulette_settings')
        try:
            with conn.cursor() as cur:
                cur.execute("""
                        INSERT INTO user_settings
                            (hp, curse, min_shells, max_shells, difficulty, items, user_id)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (user_id) DO UPDATE SET
                            hp = EXCLUDED.hp,
                            curse = EXCLUDED.curse,
                            min_shells = EXCLUDED.min_shells,
                            max_shells = EXCLUDED.max_shells,
                            difficulty = EXCLUDED.difficulty,
                            items = EXCLUDED.items
                """, (
                    settings_data['hp'],
                    settings_data['curse'],
                    settings_data['min_shells'],
                    settings_data['max_shells'],
                    settings_data['difficulty'],
                    json.dumps(settings_data['items']),
                    user_id
                ))
                conn.commit()
        finally:
            conn.close()

class SettingsPresets:
    PRESETS = {
        'default': {
            'hp': 6,
            'curse': True,
            'min_shells': 2,
            'max_shells': 8,
            'difficulty': 1,
            'items': {
                'cigarettes': True, 'handsaw': True, 'beer': True,
                'magnifying_glass': True, 'handcuffs': True, 'burner_phone': True,
                'expired_medicine': True, 'inverter': True, 'adrenaline_syringe': True,
                'linken_sphere': True, 'jammer': True, 'remote': True
            }
        },
        'classic': {
            'hp': 6,
            'curse': False,
            'min_shells': 2,
            'max_shells': 8,
            'difficulty': 1,
            'items': {
                'cigarettes': True, 'handsaw': True, 'beer': True,
                'magnifying_glass': True, 'handcuffs': True, 'burner_phone': False,
                'expired_medicine': False, 'inverter': False, 'adrenaline_syringe': False,
                'linken_sphere': False, 'jammer': True, 'remote': True
            }
        },
        'hard': {
            'hp': 5,
            'curse': True,
            'min_shells': 4,
            'max_shells': 8,
            'difficulty': 2,
            'items': {
                'cigarettes': True, 'handsaw': True, 'beer': True,
                'magnifying_glass': True, 'handcuffs': True, 'burner_phone': False,
                'expired_medicine': False, 'inverter': False, 'adrenaline_syringe': False,
                'linken_sphere': False, 'jammer': True, 'remote': False
            }
        },
        'very_hard': {
            'hp': 5,
            'curse': True,
            'min_shells': 6,
            'max_shells': 10,
            'difficulty': 2,
            'items': {
                'cigarettes': False, 'handsaw': True, 'beer': False,
                'magnifying_glass': False, 'handcuffs': True, 'burner_phone': True,
                'expired_medicine': True, 'inverter': False, 'adrenaline_syringe': False,
                'linken_sphere': False, 'jammer': True, 'remote': False
            }
        },
        'revengeance': {
            'hp': 4,
            'curse': True,
            'min_shells': 8,
            'max_shells': 10,
            'difficulty': 3,
            'items': {
                'cigarettes': False, 'handsaw': False, 'beer': False,
                'magnifying_glass': False, 'handcuffs': False, 'burner_phone': False,
                'expired_medicine': False, 'inverter': False, 'adrenaline_syringe': False,
                'linken_sphere': False, 'jammer': False, 'remote': False
            }
        }
    }
    
    @classmethod
    def get_preset(cls, preset_id: str) -> dict:
        return cls.PRESETS.get(preset_id)

class PresetsView(discord.ui.View):
    def __init__(self, locale: str):
        self.locale = locale
        super().__init__(timeout = 60)
        presets = [
            (translate(locale, 'settings_preset_default'), 'default', discord.ButtonStyle.gray),
            (translate(locale, 'settings_preset_classic'), 'classic', discord.ButtonStyle.blurple),
            (translate(locale, 'settings_preset_hard'), 'hard', discord.ButtonStyle.gray),
            (translate(locale, 'settings_preset_very_hard'), 'very_hard', discord.ButtonStyle.red),
            (translate(locale, 'settings_preset_revengeance'), 'revengeance', discord.ButtonStyle.red),
            (translate(locale, 'settings_preset_custom'), 'custom', discord.ButtonStyle.gray)
        ]

        for label, custom_id, style in presets:
            self.add_item(discord.ui.Button(label = label, custom_id = custom_id, style = style))

class HPSelector(discord.ui.View):
    def __init__(self):
        super().__init__()
        hp_options = [
            ('4', '4', discord.ButtonStyle.red),
            ('5', '5', discord.ButtonStyle.gray),
            ('6', '6', discord.ButtonStyle.gray)
        ]

        for label, custom_id, style in hp_options:
            self.add_item(discord.ui.Button(label = label, custom_id = custom_id, style = style))

class CurseSelector(discord.ui.View):
    def __init__(self, selected_hp: int):
        super().__init__()
        yes_style = discord.ButtonStyle.red if selected_hp == 4 else discord.ButtonStyle.gray
        self.add_item(discord.ui.Button(label = 'Да', custom_id = 'cursed', style = yes_style))
        self.add_item(discord.ui.Button(label = 'Нет', custom_id = 'blessed', style = discord.ButtonStyle.gray))

class MinShellSelector(discord.ui.View):
    def __init__(self):
        super().__init__()
        for i in range(2, 9):
            style = discord.ButtonStyle.red if i in [6, 7, 8] else discord.ButtonStyle.gray
            self.add_item(discord.ui.Button(label = str(i), custom_id = str(i), style = style))

class MaxShellSelector(discord.ui.View):
    def __init__(self, min_shells: int):
        super().__init__()
        for i in range(4, 11):
            disabled = i < min_shells
            style = discord.ButtonStyle.red if i in [4, 5, 6] else discord.ButtonStyle.gray
            self.add_item(discord.ui.Button(label = str(i), custom_id = str(i), style = style, disabled = disabled))

class DifficultySelector(discord.ui.View):
    def __init__(self, locale: str):
        self.locale = locale
        super().__init__()
        difficulties = [
            (translate(locale, 'settings_passive'), '0', discord.ButtonStyle.gray),
            (translate(locale, 'settings_normal'), '1', discord.ButtonStyle.gray),
            (translate(locale, 'settings_hard'), '2', discord.ButtonStyle.gray),
            (translate(locale, 'settings_very_hard'), '3', discord.ButtonStyle.red),
            (translate(locale, 'settings_revengeance'), '4', discord.ButtonStyle.red)
        ]
        
        for label, custom_id, style in difficulties:
            self.add_item(discord.ui.Button(label = label, custom_id = custom_id, style = style))

class ItemsSelector(discord.ui.View):
    def __init__(self, locale: str, current_items: dict[str, bool]):
        super().__init__()
        items = [
            ('cigarettes', 'cigarettes'),
            ('handsaw', 'handsaw'),
            ('beer', 'beer'),
            ('magnifying_glass', 'magnifying_glass'),
            ('handcuffs', 'handcuffs'),
            ('burner_phone', 'burner_phone'),
            ('expired_medicine', 'expired_medicine'),
            ('inverter', 'inverter'),
            ('adrenaline_syringe', 'adrenaline_syringe'),
            ('linken_sphere', 'linken_sphere'),
            ('jammer', 'jammer'),
            ('remote', 'remote')
        ]
        
        for i, (item_key, custom_id) in enumerate(items):
            row = i // 5
            label = translate(locale, item_key)
            style = discord.ButtonStyle.green if current_items.get(custom_id, True) else discord.ButtonStyle.red
            self.add_item(discord.ui.Button(label = label, custom_id = custom_id, style = style, row = row))
        self.add_item(discord.ui.Button(label = translate(locale, 'settings_items_all'), custom_id = 'all', style = discord.ButtonStyle.green, row = 4))
        self.add_item(discord.ui.Button(label = translate(locale, 'settings_items_none'), custom_id = 'none', style = discord.ButtonStyle.red, row = 4))
        self.add_item(discord.ui.Button(label = translate(locale, 'settings_items_done'), custom_id = 'done', style = discord.ButtonStyle.blurple, row = 4))

class BuildEmbed:
    @staticmethod
    def build_settings_embed(locale: str, data: tuple[int, bool, int, int, int, dict[str, bool]]) -> discord.Embed:
        difficulties = {0: translate(locale, 'settings_passive'),
                        1: translate(locale, 'settings_normal'),
                        2: translate(locale, 'settings_hard'),
                        3: translate(locale, 'settings_very_hard'),
                        4: translate(locale, 'settings_revengeance')}
        difficulty = difficulties.get(data[-2], translate(locale, 'settings_passive'))
        enabled_items = [translate(locale, item) for item, value in data[-1].items() if value]
        health, healing_disabled, min_ammo, max_ammo = data[1], data[2], data[3], data[4]
        embed = discord.Embed(title = 'Ваши настройки', color = colors.JDH)
        embed.add_field(name = 'Здоровье', value = f'`{health} HP`', inline = True)        
        embed.add_field(name = 'Патроны', value = f'`{min_ammo}-{max_ammo}`', inline = True)
        embed.add_field(name = 'Исцеление при здоровье <= 2', value = f'`{translate(locale, 'settings_curse_yes')}`' if not healing_disabled else f'`{translate(locale, 'settings_curse_no')}`', inline = True)
        embed.add_field(name = 'Сложность ИИ бота', value = difficulty, inline = True)
        embed.add_field(name = 'Предметы', value = str(len(enabled_items)), inline = True)
        if enabled_items:
            embed.add_field(name = 'Список предметов', value = '\n'.join(f'• {item}' for item in enabled_items), inline = False)
        return embed

    @staticmethod
    def build_presets_embed() -> discord.Embed:
        embed = discord.Embed(title = 'Настройка Русской Рулетки', description = 'Выберите пресет: эти настройки будут установлены как для одиночной игры, так и для игры против людей\nУровни сложности бота:\n**Пассивный** - бот не использует предметы, не знает порядок патронов, действует абсолютно случайно. Победа с этим режимом бота не засчитывается\n**Обычная** - бот использует 1 предмет за ход, знает последний патрон, действует соответствующим образом\n**Сложная** - бот использует 2 предмета за ход, знает последние 2 патрона, действует соответствующим образом\n**Очень сложная** - бот использует 3 предмета за ход, знает последние 3 патрона, не ошибётся при выборе того, в кого выстрелить\n**Возмездие** - практически непобедим. Использует до 4 предметов за ход, знает порядок патронов, планирует действия. **~~Использует~~ Будет использовать алгоритмическое принятие решений для просчёта ходов**', color = colors.JDH)
        presets_info = {
            'Стандарт': '6 здоровья, минимум 2 патрона, максимум 8 патронов, нет исцеления при здоровье <= 2, все предметы включены в игру, сложность бота - обычная',
            'Классика': '6 здоровья, минимум 2 патрона, максимум 8 патронов, исцеление при здоровье <= 2, включено в игру: сигареты, ножовка по металлу, пиво, лупа, наручники, сложность бота - обычная',
            'Сложно': '5 здоровья, минимум 4 патрона, максимум 8 патронов, нет исцеления при здоровье <= 2, включено в игру: сигареты, ножовка по металлу, пиво, лупа, наручники, сложность бота - сложная',
            'Очень сложно': '4 здоровья, минимум 6 патронов, максимум 10 патронов, нет исцеления при здоровье <= 2, включено в игру: ножовка по металлу, одноразовый телефон, наручники, просроченные таблетки, сложность бота - очень сложная',
            'Возмездие': '4 здоровья, минимум 8 патронов, максимум 10 патронов, **~~нет исцеления при здоровье <= 2~~ вам это не потребуется**, предметы отключены, сложность бота - возмездие',
            'Свои настройки': 'Вы можете ввести свои значения вручную'
        }
        for name, value in presets_info.items():
            embed.add_field(name = name, value = value, inline = False)
        return embed

class InteractionWaiter:
    def __init__(self, client, ctx):
        self.client: commands.Bot = client
        self.ctx: commands.Context = ctx

    async def wait_for_interaction(self) -> discord.Interaction:
        return await self.client.wait_for('interaction', check = lambda interaction: interaction.channel == self.ctx.channel and interaction.user == self.ctx.author)

class CustomSettings:
    def __init__(self, database: RouletteSettings, inter: InteractionWaiter):
        self.db = database
        self.interaction = inter

    async def handle_settings(self, ctx: commands.Context, locale: str, data: tuple, sent: discord.Message):
        current_items = data[-1] if data else {
            'cigarettes': True, 'handsaw': True, 'beer': True,
            'magnifying_glass': True, 'handcuffs': True, 'burner_phone': True,
            'expired_medicine': True, 'inverter': True, 'adrenaline_syringe': True,
            'linken_sphere': True, 'jammer': True, 'remote': True
        }
        hp = await self._select_hp(locale, sent)
        curse = await self._select_curse(locale, hp, sent)
        min_shells = await self._select_min_shells(locale, sent)
        max_shells = await self._select_max_shells(locale, min_shells, sent)
        difficulty = await self._select_difficulty(locale, sent)
        items = await self._select_items(locale, current_items, sent)
        settings_data = {
            'hp': hp,
            'curse': curse,
            'min_shells': min_shells,
            'max_shells': max_shells,
            'difficulty': difficulty,
            'items': items
        }
        self.db.save(ctx.author.id, settings_data)
        return settings_data
    
    async def _select_hp(self, locale: str, sent: discord.Message) -> int:
        view = HPSelector()
        await sent.edit(embed = discord.Embed(description = translate(locale, 'settings_select_hp'), color = colors.JDH), view = view)
        interaction = await self.interaction.wait_for_interaction()
        await interaction.response.defer()
        return int(interaction.data['custom_id'])
    
    async def _select_curse(self, locale: str, hp: int, sent: discord.Message) -> int:
        view = CurseSelector(hp)
        await sent.edit(embed = discord.Embed(description = translate(locale, 'settings_select_curse'), color = colors.JDH), view = view)
        interaction = await self.interaction.wait_for_interaction()
        await interaction.response.defer()
        return interaction.data['custom_id'] == 'cursed'

    async def _select_min_shells(self, locale: str, sent: discord.Message) -> int:
        view = MinShellSelector()
        await sent.edit(embed = discord.Embed(description = translate(locale, 'settings_select_min_shells'), color = colors.JDH), view = view)
        interaction = await self.interaction.wait_for_interaction()
        await interaction.response.defer()
        return int(interaction.data['custom_id'])
    
    async def _select_max_shells(self, locale: str, min_shells: int, sent: discord.Message) -> int:
        view = MaxShellSelector(min_shells)
        await sent.edit(embed = discord.Embed(description = translate(locale, 'settings_select_max_shells'), color = colors.JDH), view = view)
        interaction = await self.interaction.wait_for_interaction()
        await interaction.response.defer()
        return int(interaction.data['custom_id'])
    
    async def _select_difficulty(self, locale: str, sent: discord.Message) -> int:
        view = DifficultySelector(locale)
        await sent.edit(embed = discord.Embed(description = translate(locale, 'settings_select_difficulty'), color = colors.JDH), view = view)
        interaction = await self.interaction.wait_for_interaction()
        await interaction.response.defer()
        return int(interaction.data['custom_id'])
    
    async def _select_items(self, locale: str, current_items: dict[str, bool], sent: discord.Message) -> dict[str, bool]:
        view = ItemsSelector(locale, current_items)
        await sent.edit(embed = discord.Embed(description = translate(locale, 'settings_select_items'), color = colors.JDH), view = view)
        items = current_items.copy()
        while True:
            interaction = await self.interaction.wait_for_interaction()
            await interaction.response.defer()
            custom_id = interaction.data['custom_id']
            if custom_id == 'done':
                break
            if custom_id == 'all':
                items = {key: True for key in items.keys()}
            elif custom_id == 'none':
                items = {key: False for key in items.keys()}
            else:
                items[custom_id] = not items[custom_id]
            view = ItemsSelector(locale, items)
            await sent.edit(view = view)
        return items

class ApplySettings:
    def __init__(self, client):
        self.db = RouletteSettings()
        self.client: commands.Bot = client

    async def handle_settings_command(self, ctx: commands.Context, action: str = 'edit'):
        locale = get_locale(ctx.author.id)
        if action == 'check':
            return await self._handle_check_action(ctx, locale)
        return await self._handle_edit_action(ctx, locale)
    
    async def _handle_check_action(self, ctx: commands.Context, locale: str):
        data = self.db.get_user_settings(ctx.author.id)
        if not data:
            return await ctx.send(embed = discord.Embed(description = 'Вы ещё не редактировали настройки', color = colors.ERROR))
        embed = BuildEmbed.build_settings_embed(locale, data)
        return await ctx.send(embed = embed)
    
    async def _handle_edit_action(self, ctx: commands.Context, locale: str):
        interaction = InteractionWaiter(self.client, ctx)
        data = self.db.get_user_settings(ctx.author.id)
        embed = BuildEmbed.build_presets_embed()
        view = PresetsView(locale)
        sent = await ctx.send(embed = embed, view = view)
        preset_interaction = await interaction.wait_for_interaction()
        await preset_interaction.response.defer()
        preset_id = preset_interaction.data['custom_id']
        if preset_id == 'custom':
            custom_handler = CustomSettings(self.db, interaction)
            await custom_handler.handle_settings(ctx, locale, data, sent)
        else:
            preset_data = SettingsPresets.get_preset(preset_id)
            if preset_data:
                self.db.save(ctx.author.id, preset_data)
        self._log_settings_change(ctx, preset_id)
        await sent.edit(embed = discord.Embed(description = 'Настройки сохранены', color = colors.JDH), view = None)

    def _log_settings_change(self, ctx: commands.Context, preset_id: str):
        timestamp = (discord.utils.utcnow() + timedelta(hours = 3)).strftime('%d.%m.%Y %H:%M:%S')
        log_message = f'[DB] {timestamp} Запись в БД roulette_settings: {ctx.author.id} ({ctx.author.display_name}): {preset_id}\n'
        LOGS.write(log_message)
        LOGS.flush()

class GameState:
    def __init__(self, settings: tuple, players: list[discord.User], locale: str):
        self.settings = settings
        self.players = players
        self.locale = locale
        self.MAX_HP = settings[1]
        self.difficulty = settings[-2]
        
        self.hp = {player: self.MAX_HP for player in players}
        self.items = {player: [] for player in players}
        self.cursed = {player: False for player in players}
        self.cuffed = {player: False for player in players}
        self.linkened = {player: False for player in players}
        
        self.rounds_order = []
        self.current_round = 0
        self.turn_order = 0
        self.current_player_index = 0
        self.damage = 1
        self.sawed = False
        self.stop = False
        self.glass = False
        self.items_accumulator = 0
        
        self.items_pool = self._get_items_pool()

    def _get_items_pool(self) -> str:
        items_list = [
            translate(self.locale, "cigarettes"), translate(self.locale, "handsaw"), 
            translate(self.locale, "beer"), translate(self.locale, "magnifying_glass"),
            translate(self.locale, "burner_phone"), translate(self.locale, "expired_medicine"),
            translate(self.locale, "inverter"), translate(self.locale, "adrenaline_syringe"),
            translate(self.locale, "linken_sphere")
        ]

        if len(self.players) <= 2:
            items_list.extend([
                translate(self.locale, "handcuffs"), 
            ])
        else:
            items_list.extend([
                translate(self.locale, "jammer"),
                translate(self.locale, "remote")
            ])

        enabled_items = []
        for item_key, enabled in self.settings[-1].items():
            if enabled:
                item_name = translate(self.locale, item_key)
                if item_name in items_list:
                    enabled_items.append(item_name)
        
        return enabled_items

    def get_current_player(self) -> discord.User:
        return self.players[self.current_player_index]

    def get_next_player(self) -> discord.User:
        if self.turn_order == 0:
            next_index = (self.current_player_index + 1) % len(self.players)
        else:
            next_index = (self.current_player_index - 1) % len(self.players)
        return self.players[next_index]

    def advance_turn(self):
        if self.turn_order == 0:
            self.current_player_index = (self.current_player_index + 1) % len(self.players)
        else:
            self.current_player_index = (self.current_player_index - 1) % len(self.players)
    
    def reverse_turn_order(self):
        self.turn_order = 1 if self.turn_order == 0 else 0

    def is_game_over(self) -> bool:
        alive_players = [player for player, hp in self.hp.items() if hp > 0]
        return len(alive_players) <= 1

    def get_winner(self) -> discord.User:
        alive_players = [player for player, hp in self.hp.items() if hp > 0]
        return alive_players[0] if len(alive_players) == 1 else None

class RouletteGame:
    def __init__(self, client: commands.Bot, ctx: commands.Context, settings: tuple, 
                players: discord.User, locale: str):
        self.client = client
        self.ctx = ctx
        self.game_state = GameState(settings, players, locale)
        self.channel = None

    async def start_game(self):
        player_names = [cast(discord.User, player).display_name for player in self.game_state.players]
        channel_name = translate(self.game_state.locale, 'roulette_session_start', players = "-".join(player_names))
        self.channel = await self.ctx.guild.create_text_channel(channel_name[:100])
        await self.ctx.send(embed = discord.Embed(description = translate(self.game_state.locale, 'roulette_go_to_other_channel', channel_mention = self.channel.mention), color = colors.DEFAULT))
        await self.channel.send(embed = discord.Embed(description = translate(self.game_state.locale, "roulette_rules_vs_user"), color = colors.DEFAULT))
        await asyncio.sleep(5)
        await self._game_loop()

    async def _game_loop(self):
        for round_num in range(1, 12):
            if self.game_state.stop or self.game_state.is_game_over():
                break
            if round_num == 11:
                break
            await self._start_round(round_num)
        await self._end_game()

    async def _start_round(self, round_num: int):
        round_text = (
            translate(self.game_state.locale, 'roulette_round_number', i = round_num)
            if round_num != 5 
            else translate(self.game_state.locale, 'roulette_round_number_is_5', i = round_num)
        )
        await self.channel.send(embed = discord.Embed(description = round_text, color = colors.WHITE))
        await self._distribute_items(round_num)
        rounds_count = random.randint(
            self.game_state.settings[3], 
            self.game_state.settings[4]
        )
        self.game_state.rounds_order = [random.randint(0, 1) for _ in range(rounds_count)]
        if self.game_state.rounds_order.count(0) == 0:
            self.game_state.rounds_order[-1] = 0
        if self.game_state.rounds_order.count(1) == 0:
            self.game_state.rounds_order[-1] = 1
        await self._round_turns()

    async def _distribute_items(self, round_num: int):
        items_per_round = 2 if round_num < 5 else 4
        for player in self.game_state.players:
            if self.game_state.hp[player] > 0:
                for _ in range(items_per_round):
                    if len(self.game_state.items[player]) < 8 and self.game_state.items_pool:
                        new_item = random.choice(self.game_state.items_pool)
                        self.game_state.items[player].append(new_item)
                    elif len(self.game_state.items[player]) >= 8:
                        await self.channel.send(embed = discord.Embed(description = translate(self.game_state.locale, 'roulette_use_more_often', player = player.mention), color = colors.ERROR))
                        break

    async def _round_turns(self):
        first_turn = True
        while (self.game_state.rounds_order and 
                not self.game_state.stop and 
                not self.game_state.is_game_over()):
            current_player = self.game_state.get_current_player()
            if self.game_state.hp[current_player] <= 0:
                self.game_state.advance_turn()
            await self._update_player_states()
            await self._display_game_state(first_turn)
            if await self._handle_skip_conditions(current_player):
                continue
            if first_turn:
                first_turn = False
            if current_player.bot:
                await self._handle_bot_turn(current_player)
            else:
                await self._handle_player_turn(current_player)
            if self.game_state.is_game_over():
                break

    def draw_table(self, players: list, turn_order: int):
        if turn_order == 0:
            indicator = ':arrows_counterclockwise:'
        else:
            indicator = ':arrows_clockwise:'
        to_draw = f"""
        ᅠᅠᅠᅠᅠᅠ{players[0]}

        {players[1]}ᅠᅠᅠᅠ{indicator}ᅠᅠᅠᅠ{players[3] if len(players) > 2 else 'Никого...'}

        ᅠᅠᅠᅠᅠᅠ{players[2] if len(players) > 3 else 'Никого...'}
        """
        return to_draw

    async def _handle_skip_conditions(self, player: discord.User) -> bool:
        if self.game_state.cuffed[player]:
            await self.channel.send(embed = discord.Embed(description = translate(self.game_state.locale, 'roulette_cuffed_skip', player = player.mention), color = colors.ERROR))
            self.game_state.cuffed[player] = False
            self.game_state.advance_turn()
            return True
        return False

    async def _update_player_states(self):
        for player in self.game_state.players:
            if (self.game_state.hp[player] <= 2 and 
                self.game_state.settings[2]):
                self.game_state.cursed[player] = True

    async def _display_game_state(self, first_turn: bool):
        players_info = []
        for player in self.game_state.players:
            player_info = (
                f"{player.mention}: {self.game_state.hp[player]} HP"
                f"{' 💀' if self.game_state.cursed[player] else ''}"
                f"{' 🛡️' if self.game_state.linkened[player] else ''}"
                f"{' 🔒' if self.game_state.cuffed[player] else ''}"
            )
            players_info.append(player_info)

        items_info = []
        for player in self.game_state.players:
            items_info.append(translate(self.game_state.locale, 'roulette_items', player = player.mention, count = len(self.game_state.items[player]), items = ', '.join(self.game_state.items[player]) if self.game_state.items[player] else translate(self.game_state.locale, 'roulette_no_items')))

        embed = discord.Embed(title = translate(self.game_state.locale, "roulette_game_state"), description = (
                f"**{translate(self.game_state.locale, 'roulette_players')}**\n" +
                "\n".join(players_info) +
                f"\n\n**{translate(self.game_state.locale, 'roulette_rounds')}:** " +
                f"{len(self.game_state.rounds_order) if first_turn else '?'}, " +
                f"{translate(self.game_state.locale, 'live_shells')} - {self.game_state.rounds_order.count(1) if first_turn else '?'}, " +
                f"{translate(self.game_state.locale, 'blank_shells')} - {self.game_state.rounds_order.count(0) if first_turn else '?'}" +
                (f"\n\n**{translate(self.game_state.locale, 'roulette_players_items')}**\n{"\n".join(items_info)}" if self.game_state.items_pool else f'\n\n**{translate(self.game_state.locale, "roulette_items_disabled")}**')
            ), color = colors.DEFAULT)

        await self.channel.send(embed = embed)

    async def _handle_player_turn(self, player: discord.User):
        if self.game_state.hp[player] < 1:
            return self.game_state.advance_turn()
        table = self.draw_table([player.display_name for player in self.game_state.players], self.game_state.turn_order)
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label = translate(self.game_state.locale, "roulette_shoot_self"), style = discord.ButtonStyle.gray if not self.game_state.sawed else discord.ButtonStyle.red, custom_id = 'shoot_self'))
        view.add_item(discord.ui.Button(label = translate(self.game_state.locale, "roulette_shoot_opponent"), style = discord.ButtonStyle.gray if not self.game_state.sawed else discord.ButtonStyle.green, custom_id = 'shoot_opponent'))
        if self.game_state.items[player]:
            view.add_item(discord.ui.Button(label = translate(self.game_state.locale, "roulette_use_item"), style = discord.ButtonStyle.gray, custom_id = 'use_item'))
        if player.id in self.client.owner_ids:
            view.add_item(discord.ui.Button(label = translate(self.game_state.locale, "roulette_stop_game"), style = discord.ButtonStyle.red, custom_id = 'stop'))
        await self.channel.send(embed = discord.Embed(description = f"{table}\n{translate(self.game_state.locale, 'roulette_choose_action', player = player.mention)}", color = colors.JDH), view = view)
        try:
            interaction = await self.client.wait_for('interaction', timeout = 60, check = lambda i: i.user == player and i.channel == self.channel)
            await interaction.response.defer()
            if interaction.data['custom_id'] == 'shoot_self':
                await self._handle_shoot_self(player)
            elif interaction.data['custom_id'] == 'shoot_opponent':
                await self._handle_shoot_opponent(player)
            elif interaction.data['custom_id'] == 'use_item':
                await self._handle_use_item(player)
            elif interaction.data['custom_id'] == 'stop':
                self.game_state.stop = True
        except asyncio.TimeoutError:
            await self.channel.send(embed = discord.Embed(description = translate(self.game_state.locale, 'roulette_timeout', player = player.mention), color = colors.ERROR))
            self.game_state.advance_turn()

    async def _handle_shoot_self(self, player: discord.User):
        await self.channel.send(embed = discord.Embed(description = translate(self.game_state.locale, 'roulette_chose_self', player = player.mention), color = colors.JDH))
        await asyncio.sleep(2)
        round_type = self.game_state.rounds_order.pop(0)
        if round_type == 0:
            await self.channel.send(embed = discord.Embed(description = translate(self.game_state.locale, "roulette_shoot_blank", player = player.mention), color = colors.SUCCESS))
        else:
            self.game_state.hp[player] -= self.game_state.damage
            await self.channel.send(embed = discord.Embed(description = translate(self.game_state.locale, 'roulette_shoot_live', player = player.mention, damage = self.game_state.damage), color = colors.ERROR))
            self.game_state.advance_turn()
        self.game_state.damage = 1
        self.game_state.sawed = False

    async def _handle_shoot_opponent(self, player: discord.User):
        if len(self.game_state.players) > 2:
            target = await self._select_target(player)
            if not target:
                return
        else:
            target = self.game_state.get_next_player()
        await self.channel.send(embed = discord.Embed(description = translate(self.game_state.locale, 'roulette_chose_opponent', player = player.mention, target = target.mention), color = colors.JDH))
        await asyncio.sleep(2)
        round_type = self.game_state.rounds_order.pop(0)
        if round_type == 0:
            await self.channel.send(embed = discord.Embed(description = translate(self.game_state.locale, "roulette_shoot_opponent_blank"), color = colors.ERROR))
        else:
            self.game_state.hp[target] -= self.game_state.damage
            await self.channel.send(embed = discord.Embed(description = translate(self.game_state.locale, 'roulette_shoot_live', player = target.mention, damage = self.game_state.damage), color = colors.SUCCESS))
        self.game_state.advance_turn()
        self.game_state.damage = 1
        self.game_state.sawed = False

    async def _select_target(self, player: discord.User) -> discord.User:
        possible_targets = [
            p for p in self.game_state.players 
            if p != player and self.game_state.hp[p] > 0
        ]
        
        if not possible_targets:
            return None
            
        if len(possible_targets) == 1:
            return possible_targets[0]
        
        if player.bot:
            return random.choice(possible_targets)

        view = discord.ui.View()
        for target in possible_targets:
            view.add_item(discord.ui.Button(label = target.display_name, style = discord.ButtonStyle.gray, custom_id = str(target.id)))
            
        await self.channel.send(embed = discord.Embed(description = translate(self.game_state.locale, 'roulette_select_target', player = player.mention), color = colors.JDH), view = view)
        
        try:
            interaction = await self.client.wait_for('interaction', timeout = 30, check = lambda i: i.user == player and i.channel == self.channel)
            await interaction.response.defer()
            target_id = int(interaction.data['custom_id'])
            return discord.utils.get(self.game_state.players, id = target_id)
            
        except asyncio.TimeoutError:
            target = random.choice(possible_targets)
            await self.channel.send(embed = discord.Embed(description = translate(self.game_state.locale, "roulette_target_timeout", player = player.mention, target = target.mention), color = colors.ERROR))
            return discord.utils.get(self.game_state.players, id = target.id)

    async def _handle_use_item(self, player: discord.User):
        items = self.game_state.items[player]

        view = discord.ui.View()
        for i, item in enumerate(items):
            view.add_item(discord.ui.Button(label = item, style = discord.ButtonStyle.gray, custom_id = str(i)))

        await self.channel.send(embed = discord.Embed(description = translate(self.game_state.locale, 'roulette_choose_item', player = player.mention), color = colors.JDH), view = view)

        try:
            interaction = await self.client.wait_for('interaction', timeout = 30, check = lambda i: i.user == player and i.channel == self.channel)
            await interaction.response.defer()
            item_index = int(interaction.data['custom_id'])
            selected_item = items[item_index]
            await self._use_item(player, selected_item, item_index, interaction)

        except asyncio.TimeoutError:
            await self.channel.send(embed = discord.Embed(description = translate(self.game_state.locale, "roulette_item_timeout"), color = colors.ERROR))

    async def _use_item(self, player: discord.User, item: str, item_index: int, follow_up: discord.Interaction = None):          
        self.game_state.items[player].pop(item_index)
        if item == translate(self.game_state.locale, "cigarettes"):
            await self._use_cigarettes(player)
        elif item == translate(self.game_state.locale, "handsaw"):
            await self._use_handsaw(player)
        elif item == translate(self.game_state.locale, "beer"):
            await self._use_beer(player)
        elif item == translate(self.game_state.locale, "magnifying_glass"):
            await self._use_magnifying_glass(player, follow_up)
        elif item == translate(self.game_state.locale, "burner_phone"):
            await self._use_burner_phone(player, follow_up)
        elif item == translate(self.game_state.locale, "expired_medicine"):
            await self._use_expired_medicine(player)
        elif item == translate(self.game_state.locale, "inverter"):
            await self._use_inverter(player)
        elif item == translate(self.game_state.locale, "adrenaline_syringe"):
            await self._use_adrenaline_syringe(player)
        elif item == translate(self.game_state.locale, "handcuffs"):
            await self._use_handcuffs(player)
        elif item == translate(self.game_state.locale, "linken_sphere"):
            await self._use_linken_sphere(player)
        elif item == translate(self.game_state.locale, "jammer"):
            await self._use_jammer(player)
        elif item == translate(self.game_state.locale, "remote"):
            await self._use_remote(player)

    async def _check_linken_protection(self, player: discord.User, item: str) -> bool:
        blocked_items = [
            translate(self.game_state.locale, "handcuffs"),
            translate(self.game_state.locale, "adrenaline_syringe"),
            translate(self.game_state.locale, "jammer")
        ]

        if item in blocked_items:
            if self.game_state.linkened[player] and self.game_state.hp[player] > 0:
                await self.channel.send(embed = discord.Embed(description = translate(self.game_state.locale, 'roulette_linken_triggered', player = player.mention, item = item), color = colors.ERROR))
                self.game_state.linkened[player] = False
                return True
        return False

    async def _use_cigarettes(self, player: discord.User, stolen: bool = False):
        if not self.game_state.cursed[player]:
            heal_amount = 1 if self.game_state.hp[player] < self.game_state.MAX_HP else 0
            self.game_state.hp[player] += heal_amount
        if not stolen:
            await self.channel.send(embed = discord.Embed(description = translate(self.game_state.locale, 'roulette_player_cigarettes', player = player.mention), color = colors.SUCCESS))

    async def _use_handsaw(self, player: discord.User, stolen: bool = False):
        if not self.game_state.sawed:
            self.game_state.damage += 1
            self.game_state.sawed = True
            if not stolen:
                await self.channel.send(embed = discord.Embed(description = translate(self.game_state.locale, 'roulette_player_handsaw', player = player.mention), color = colors.SUCCESS))
        else:
            await self.channel.send(embed = discord.Embed(description = translate(self.game_state.locale, "roulette_player_handsaw_used"), color = colors.ERROR))
            if stolen:
                self.game_state.items[player].append(translate(self.game_state.locale, 'adrenaline_syringe'))

    async def _use_beer(self, player: discord.User, stolen: bool = False):
        if self.game_state.rounds_order:
            round_type = self.game_state.rounds_order.pop(0)
            shell_type = (
                translate(self.game_state.locale, "live_shell") 
                if round_type == 1 
                else translate(self.game_state.locale, "blank_shell")
            )
            if not stolen:
                await self.channel.send(embed = discord.Embed(description = translate(self.game_state.locale, 'roulette_player_beer', player = player.mention, shell = shell_type), color = colors.JDH))

    async def _use_magnifying_glass(self, player: discord.User, follow_up: discord.Interaction = False, stolen: bool = False):
        if self.game_state.rounds_order:
            round_type = self.game_state.rounds_order[0]
            shell_type = (
                translate(self.game_state.locale, "live_shell") 
                if round_type == 1 
                else translate(self.game_state.locale, "blank_shell")
            )
            if player.bot:
                if not stolen:
                    await self.channel.send(embed = discord.Embed(description = translate(self.game_state.locale, 'roulette_dealer_used_magnifying_glass'), color = colors.JDH))
                await asyncio.sleep(2)
                return round_type
            if not stolen:
                await self.channel.send(embed = discord.Embed(description = translate(self.game_state.locale, 'roulette_magnifying_glass_use', player = player.mention), color = colors.JDH))
            await asyncio.sleep(2)
            await follow_up.followup.send(embed = discord.Embed(description = translate(self.game_state.locale, 'roulette_magnifying_glass_result', shell = shell_type), color = colors.JDH), ephemeral = True)

    async def _use_burner_phone(self, player: discord.User, follow_up: discord.Interaction = False, stolen: bool = False):
        phone_number = ''.join(random.choices('0123456789', k = 6))
        await self.channel.send(embed = discord.Embed(description = translate(self.game_state.locale, 'roulette_player_burner_phone', player = player.mention, number = phone_number), color = colors.JDH))
        if player.bot:
            return
        if len(self.game_state.rounds_order) >= 3:
            future_index = random.randint(1, len(self.game_state.rounds_order) - 1)
            future_round = self.game_state.rounds_order[future_index]
            shell_type = (
                translate(self.game_state.locale, "live_shell") 
                if future_round == 1 
                else translate(self.game_state.locale, "blank_shell")
            )
            await follow_up.followup.send(embed = discord.Embed(description = translate(self.game_state.locale, 'roulette_burner_phone_result', current = future_index + 1, shell = shell_type), color = colors.JDH), ephemeral = True)
        else:
            await follow_up.followup.send(embed = discord.Embed(description = translate(self.game_state.locale, "roulette_burner_phone_no_result"), color = colors.ERROR), ephemeral = True)

    async def _use_expired_medicine(self, player: discord.User, stolen: bool = False):
        if not stolen:
            await self.channel.send(embed = discord.Embed(description = translate(self.game_state.locale, 'roulette_player_expired_medicine', player = player.mention), color = colors.ERROR))
        await asyncio.sleep(2)
        success = random.random() < 0.5
        if success:
            if not self.game_state.cursed[player]:
                heal_amount = min(2, self.game_state.MAX_HP - self.game_state.hp[player])
                self.game_state.hp[player] += heal_amount
            await self.channel.send(embed = discord.Embed(description = translate(self.game_state.locale, "roulette_player_expired_medicine_success", player = player.mention), color = colors.SUCCESS))
        else:
            self.game_state.hp[player] -= 1
            await self.channel.send(embed = discord.Embed(description = translate(self.game_state.locale, "roulette_player_expired_medicine_fail", player = player.mention), color = colors.ERROR))

    async def _use_inverter(self, player: discord.User, stolen: bool = False):
        if self.game_state.rounds_order:
            self.game_state.rounds_order[0] = 1 if self.game_state.rounds_order[0] == 0 else 0
            if not stolen:
                await self.channel.send(embed = discord.Embed(description = translate(self.game_state.locale, 'roulette_player_inverter', player = player.mention), color = colors.JDH))
            await asyncio.sleep(2)
            await self.channel.send(embed = discord.Embed(description = translate(self.game_state.locale, "roulette_inverter_result"), color = colors.JDH))

    async def _use_adrenaline_syringe(self, player: discord.User):
        possible_targets = [
            p for p in self.game_state.players 
            if p != player and self.game_state.hp[p] > 0 and self.game_state.items[p] and
            not all(item == translate(self.game_state.locale, "adrenaline_syringe") for item in self.game_state.items[p])
        ]
        
        if not possible_targets:
            return await self.channel.send(embed = discord.Embed(description = translate(self.game_state.locale, "roulette_syringe_all_items"), color = colors.ERROR))

        target = await self._select_syringe_target(player, possible_targets)

        if await self._check_linken_protection(target, translate(self.game_state.locale, "adrenaline_syringe")):
            return await self.channel.send(embed = discord.Embed(description = translate(self.game_state.locale, "roulette_used_linken_sphere", target = target.mention, item = translate(self.game_state.locale, "adrenaline_syringe")), color = colors.ERROR))

        stealable_items = [
            item for item in self.game_state.items[target] 
            if item != translate(self.game_state.locale, "adrenaline_syringe")
        ]

        if not target:
            return
        await self.channel.send(embed = discord.Embed(description = translate(self.game_state.locale, 'roulette_player_syringe', player = player.mention, target = target.mention), color = colors.JDH))

        if not stealable_items:
            return await self.channel.send(embed = discord.Embed(description = translate(self.game_state.locale, "roulette_syringe_no_stealable"), color = colors.ERROR))

        stolen_item = await self._select_item_to_steal(player, stealable_items)
        if not stolen_item:
            return

        await self.channel.send(embed = discord.Embed(description = translate(self.game_state.locale, 'roulette_stole_item', player = player.mention, target = target.mention, item = stolen_item), color = colors.SUCCESS))

        self.game_state.items[target].remove(stolen_item)
        if stolen_item == translate(self.game_state.locale, 'cigarettes'):
            await self._use_cigarettes(player)
        elif stolen_item == translate(self.game_state.locale, 'burner_phone'):
            await self._use_burner_phone(player)
        elif stolen_item == translate(self.game_state.locale, 'expired_medicine'):
            await self._use_expired_medicine(player)
        elif stolen_item == translate(self.game_state.locale, 'inverter'):
            await self._use_inverter(player)
        elif stolen_item == translate(self.game_state.locale, 'handsaw'):
            await self._use_handsaw(player)
        elif stolen_item == translate(self.game_state.locale, 'magnifying_glass'):
            await self._use_magnifying_glass(player)
        elif stolen_item == translate(self.game_state.locale, 'linken_sphere'):
            await self._use_linken_sphere(player)
        elif stolen_item == translate(self.game_state.locale, 'jammer'):
            await self._use_jammer(player)
        elif stolen_item == translate(self.game_state.locale, 'remote'):
            await self._use_remote(player)
        elif stolen_item == translate(self.game_state.locale, 'handcuffs'):
            await self._use_handcuffs(player)
        elif stolen_item == translate(self.game_state.locale, 'beer'):
            await self._use_beer(player)
        
    async def _select_syringe_target(self, player: discord.User, possible_targets: list[discord.User]) -> discord.User:
        if len(possible_targets) == 1:
            return possible_targets[0]
            
        if player.bot:
            return random.choice(possible_targets)

        view = discord.ui.View()
        for target in possible_targets:
            view.add_item(discord.ui.Button(label = target.display_name, style = discord.ButtonStyle.gray, custom_id = str(target.id)))
            
        await self.channel.send(embed = discord.Embed(description = translate(self.game_state.locale, 'roulette_select_opponent'), color = colors.JDH), view = view)
        
        try:
            interaction = await self.client.wait_for('interaction', timeout = 30, check = lambda i: i.user == player and i.channel == self.channel)
            await interaction.response.defer()
            
            target_id = int(interaction.data['custom_id'])
            return discord.utils.get(possible_targets, id = target_id)
            
        except asyncio.TimeoutError:
            await self.channel.send(embed = discord.Embed(description = translate(self.game_state.locale, "roulette_syringe_timeout"), color = colors.ERROR))
            return random.choice(possible_targets)

    async def _select_item_to_steal(self, player: discord.User, items: str) -> str:
        if player.bot:
            return random.choice(items)

        view = discord.ui.View()
        for i, item in enumerate(items):
            view.add_item(discord.ui.Button(label = item, style = discord.ButtonStyle.gray, custom_id = str(i)))
            
        await self.channel.send(embed = discord.Embed(description = translate(self.game_state.locale, 'roulette_choose_opponent_item'), color = colors.JDH), view = view)
        
        try:
            interaction = await self.client.wait_for('interaction', timeout = 30, check = lambda i: i.user == player and i.channel == self.channel)
            await interaction.response.defer()
            item_index = int(interaction.data['custom_id'])
            return items[item_index]
            
        except asyncio.TimeoutError:
            await self.channel.send(embed = discord.Embed(description = translate(self.game_state.locale, "roulette_steal_timeout"), color = colors.ERROR))
            return random.choice(items)

    async def _use_handcuffs(self, player: discord.User):
        if len(self.game_state.players) == 2:
            target = self.game_state.get_next_player()
            if await self._check_linken_protection(target, translate(self.game_state.locale, "handcuffs")):
                return await self.channel.send(embed = discord.Embed(description = translate(self.game_state.locale, "roulette_used_linken_sphere", target = target.mention, item = translate(self.game_state.locale, "handcuffs")), color = colors.ERROR))
            self.game_state.cuffed[target] = True
            await self.channel.send(embed = discord.Embed(description = translate(self.game_state.locale, 'roulette_player_handcuffs', player = player.mention, target = target.mention), color = colors.SUCCESS))
        else:
            await self.channel.send(embed = discord.Embed(description = translate(self.game_state.locale, "roulette_handcuffs_not_available"), color = colors.ERROR))

    async def _use_linken_sphere(self, player: discord.User):
        if not self.game_state.linkened[player]:
            self.game_state.linkened[player] = True
            await self.channel.send(embed = discord.Embed(description = translate(self.game_state.locale, 'roulette_player_linken_sphere', player = player.mention), color = colors.SUCCESS))
        else:
            await self.channel.send(embed = discord.Embed(description = translate(self.game_state.locale, "roulette_linken_sphere_already_used"), color = colors.ERROR))

    async def _use_jammer(self, player: discord.User):
        if len(self.game_state.players) > 2:
            possible_targets = [
                p for p in self.game_state.players 
                if p != player and self.game_state.hp[p] > 0
            ]
            if not possible_targets:
                return await self.channel.send(embed = discord.Embed(description = translate(self.game_state.locale, "roulette_jammer_no_targets"), color = colors.ERROR))
            target = await self._select_jammer_target(player, possible_targets)
            if await self._check_linken_protection(target, translate(self.game_state.locale, "jammer")):
                return await self.channel.send(embed = discord.Embed(description = translate(self.game_state.locale, "roulette_used_linken_sphere", target = target.mention, item = translate(self.game_state.locale, "jammer")), color = colors.ERROR))
            if not target:
                return
            self.game_state.cuffed[target] = True
            await self.channel.send(embed = discord.Embed(description = translate(self.game_state.locale, 'roulette_used_jammer', player = player.mention, target = target.mention), color = colors.SUCCESS))
        else:
            await self.channel.send(embed = discord.Embed(description = translate(self.game_state.locale, "roulette_jammer_not_available"), color = colors.ERROR))

    async def _select_jammer_target(self, player: discord.User, possible_targets: list[discord.User]) -> discord.User:
        if len(possible_targets) == 1:
            return possible_targets[0]
        if player.bot:
            return random.choice(possible_targets)
        view = discord.ui.View()
        for target in possible_targets:
            view.add_item(discord.ui.Button(label = target.display_name, style = discord.ButtonStyle.gray, custom_id = str(target.id)))
        await self.channel.send(embed = discord.Embed(description = translate(self.game_state.locale, 'roulette_select_target', player = player.mention), color = colors.JDH), view = view)
        try:
            interaction = await self.client.wait_for('interaction', timeout = 30, check = lambda i: i.user == player and i.channel == self.channel)
            await interaction.response.defer()
            target_id = int(interaction.data['custom_id'])
            return discord.utils.get(possible_targets, id = target_id)
        except asyncio.TimeoutError:
            target = random.choice(possible_targets)
            await self.channel.send(embed = discord.Embed(description = translate(self.game_state.locale, "roulette_target_timeout", player = player.mention, target = target.mention), color = colors.ERROR))
            return target

    async def _use_remote(self, player: discord.User):
        if len(self.game_state.players) > 2:
            self.game_state.reverse_turn_order()
            direction = (
                translate(self.game_state.locale, "roulette_clockwise") 
                if self.game_state.turn_order == 0 
                else translate(self.game_state.locale, "roulette_counterclockwise")
            )
            await self.channel.send(embed = discord.Embed(description = translate(self.game_state.locale, "roulette_used_remote", player = player.mention, direction = direction), color = colors.SUCCESS))
        else:
            await self.channel.send(embed = discord.Embed(description = translate(self.game_state.locale, "roulette_remote_not_available"), color = colors.ERROR))

    async def _handle_bot_turn(self, bot: discord.User):
        if self.game_state.hp[bot] < 1:
            return self.game_state.advance_turn()
        if bot is self.client.user:
            await self.channel.send(embed = discord.Embed(description = translate(self.game_state.locale, 'roulette_dealer_thinking'), color = colors.JDH))
        else:
            await self.channel.send(embed = discord.Embed(description = translate(self.game_state.locale, 'roulette_bot_thinking', player = bot.mention), color = colors.JDH))
        await asyncio.sleep(2)
        action = await self._get_bot_action(bot, self.game_state.difficulty)
        if action == "shoot_self":
            await self._handle_shoot_self(bot)
        elif action == "shoot_opponent":
            await self._handle_shoot_opponent(bot)
        elif action == "use_item":
            await self._handle_bot_use_item(bot)

    async def _get_bot_action(self, bot: discord.User, difficulty: int) -> str:
        """Эквивалентно уровню сложности 'Пассивный'"""
        acc = self.game_state.items_accumulator
        if self.game_state.items[bot]:
            use_item_chance = 0.3
            if random.random() < use_item_chance and acc < 2:
                acc += 1
                return "use_item"
        shoot_self_chance = 0.2
        if random.random() < shoot_self_chance:
            return "shoot_self"
        else:
            return "shoot_opponent"

    async def _handle_bot_use_item(self, bot: discord.User):
        if not self.game_state.items[bot]:
            return await self._handle_shoot_opponent(bot)
        item_index = random.randint(0, len(self.game_state.items[bot]) - 1)
        selected_item = self.game_state.items[bot][item_index]
        await self._use_item(bot, selected_item, item_index)

    async def _end_game(self):
        winner = self.game_state.get_winner()
        if winner:
            await self._update_game_stats(winner)
            await self.channel.send(embed = discord.Embed(description = translate(self.game_state.locale, 'roulette_winner', winner = winner.mention), color = colors.SUCCESS))
        else:
            await self.channel.send(embed = discord.Embed(description = translate(self.game_state.locale, "roulette_stalemate"), color = colors.WHITE))
        await asyncio.sleep(10)
        await self.channel.delete()

    async def _update_game_stats(self, winner: discord.User):
        try:
            with connect_db('leaderboard') as conn:
                with conn.cursor() as cursor:
                    cursor.execute("UPDATE leaders SET victories = victories + 1 WHERE user_id = %s", (winner.id,))
                    conn.commit()
        except Exception as e:
            LOGS.write(f"Ошибка при обновлении статистики: {e}")
            LOGS.flush()

class Fun(commands.Cog):
    def __init__(self, client):
        self.client: commands.Bot = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Модуль Fun загружен')

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def settings(self, ctx: commands.Context, action: str = 'edit'):
        await ApplySettings(self.client).handle_settings_command(ctx, action)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def leaderboard(self, ctx: commands.Context):
        try:
            with connect_db('leaderboard') as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM leaders ORDER BY victories DESC LIMIT 5")
                    leaders = cursor.fetchall()
            await ctx.send(embed = discord.Embed(title = translate(get_locale(ctx.author.id), "roulette_leaderboard"), description = f'{"\n".join([f"{i + 1}. {self.client.get_user(int(user_id)).mention} - {victories} {get_plural_form(victories, ['победа', 'победы', 'побед'])}" for i, (user_id, victories) in enumerate(leaders)])}', color = colors.JDH))
        except Exception as e:
            LOGS.write(f"Ошибка при получении статистики: {e}")
            LOGS.flush()

    @commands.command()
    @commands.cooldown(1, 20, commands.BucketType.user)
    @commands.bot_has_permissions(manage_channels = True)
    async def roulette(self, ctx: commands.Context, players: commands.Greedy[discord.User] = None):
        if players is None:
            players = [ctx.author, self.client.user]
        settings = RouletteSettings.get_user_settings(self, ctx.author.id)
        if settings is None:
            await self.settings(ctx, 'edit')
        locale = get_locale(ctx.author.id)
        agreed = [ctx.author]
        pending_players = []
        for player in players:
            if player in agreed:
                continue
            if player.bot:
                agreed.append(player)
            else:
                task = asyncio.create_task(self._process_player_invitation(ctx, player, locale))
                pending_players.append((player, task))
        if pending_players:
            for player, task in pending_players:
                try:
                    player_agreed = await task
                    if player_agreed:
                        agreed.append(player)
                except Exception:
                    pass
        if len(agreed) < 2:
            return await ctx.send(embed = discord.Embed(description = translate(locale, "roulette_min_players"), color = colors.ERROR))
        random.shuffle(agreed)
        game = RouletteGame(ctx.bot, ctx, settings, agreed, locale)
        await game.start_game()

    async def _process_player_invitation(self, ctx: commands.Context, player: discord.User, locale: str):
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label = translate(locale, 'roulette_yes'), style = discord.ButtonStyle.green, custom_id = 'yes'))
        view.add_item(discord.ui.Button(label = translate(locale, 'roulette_no'), style = discord.ButtonStyle.red, custom_id = 'no'))
        await ctx.send(embed = discord.Embed(description = translate(locale, 'roulette_play_invite', player = player.mention), color = colors.JDH), view = view)
        try:
            interaction = await self.client.wait_for('interaction', check = lambda i: i.user == player, timeout = 30)
            await interaction.response.defer()
            if interaction.data['custom_id'] == 'yes':
                return True
            else:
                await ctx.send(embed = discord.Embed(description = translate(locale, 'roulette_play_disagree', player = player.mention), color = colors.ERROR))
                return False
        except asyncio.TimeoutError:
            await ctx.send(embed = discord.Embed(description = translate(locale, 'roulette_invite_timeout', player = player.mention), color = colors.ERROR))
            return False

    @commands.command()
    @commands.cooldown(1, 15, commands.BucketType.user)
    @commands.bot_has_permissions(manage_messages = True)
    async def dotersbrain(self, ctx: commands.Context):
        words = ['чё', 'а', 'да', 'нет', 'ок']
        answers = {'чё': 'хуй через плечо', 'а': 'хуй на', 'да': 'пизда', 'нет': 'пидора ответ', 'ок': 'хуй намок'}
        await ctx.send(embed = discord.Embed(description = f'{ctx.author.mention}, через 5 секунд появится одно из слов ({", ".join(words)}), на которое вам нужно будет правильно ответить. На размышление 5 секунд', color = colors.JDH))
        await asyncio.sleep(5)
        sent = await ctx.send(embed = discord.Embed(description = random.choice(words), color = colors.JDH))
        try:
            msg = await self.client.wait_for('message', timeout = 5, check = lambda message: message.author == ctx.author and message.channel == ctx.message.channel)
            if msg.content.lower() == answers[sent.embeds[0].description]:
                await ctx.send(embed = discord.Embed(description = 'Поздравляю, у вас 3 стадия рака!', color = colors.JDH))
            else:
                await ctx.send(embed = discord.Embed(description = 'Вы совершенно здоровый человек! ||попробуйте cy/help dotersbrain||', color = colors.JDH))
        except asyncio.TimeoutError:
            await ctx.send(embed = discord.Embed(description = f'{ctx.author.mention}, слишком медленно.', color = colors.JDH))

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def aghanim(self, ctx: commands.Context):
        rand = random.randint(1, 40)
        if rand >= 15:
            await ctx.send(embed = discord.Embed(description = f'Ого! Твой аганим длиной аж {rand} см!', color = colors.JDH))
        else:
            await ctx.send(embed = discord.Embed(description = f'Длина твоего аганима {rand} см, лошара', color = colors.JDH))

async def setup(client):
    await client.add_cog(Fun(client))
