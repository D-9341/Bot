import discord
import psycopg2
import json
import asyncio
import warnings

from discord.ext import commands
from cogs.Logging import LOGS
from cogs.Constants import colors, locales_paths
from main import PASSWORD, CWD, owner_commands
from functions import get_plural_form
from tabulate import tabulate

class Kernel(commands.Cog):
    def __init__(self, client):
        self.client: commands.Bot = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Команды Ядра загружены')

    @commands.command(hidden = True)
    async def disable(self, ctx: commands.Context, *, target: str):
        if ctx.author.id not in self.client.owner_ids:
            raise commands.NotOwner()
        if target.lower() in self.client.all_commands:
            command = self.client.get_command(target)
            if target in owner_commands:
                return await ctx.send(embed = discord.Embed(description = f'`{target}` нельзя отключить', color = colors.ERROR))
            if command.enabled:
                command.enabled = False
                return await ctx.send(embed = discord.Embed(description = f'Команда `{target}` отключена', color = colors.JDH))
            else:
                return await ctx.send(embed = discord.Embed(description = f'Команда `{target}` уже отключена', color = colors.ERROR))
        elif f'cogs.{target.title()}' in self.client.extensions:
            extension = f'cogs.{target.title()}'
            if extension == 'cogs.Events':
                return await ctx.send(embed = discord.Embed(description = 'Модуль `Events` не может быть выгружен', color = colors.ERROR))
            if extension not in self.client.extensions:
                return await ctx.send(embed = discord.Embed(description = f'Модуль `{target}` уже выгружен или не найден', color = colors.ERROR))
            try:
                await self.client.unload_extension(extension)
            except commands.ExtensionNotFound:
                return await ctx.send(embed = discord.Embed(description = f'Модуль `{target}` не найден', color = colors.ERROR))
            else:
                await ctx.send(embed = discord.Embed(description = f'Модуль `{target}` выгружен', color = colors.JDH))
        else:
            return await ctx.send(embed = discord.Embed(description = f'Объект `{target}` не найден или уже отключён', color = colors.ERROR))

    @commands.command(hidden = True)
    async def enable(self, ctx: commands.Context, *, target: str):
        if ctx.author.id not in self.client.owner_ids:
            raise commands.NotOwner()
        if target.lower() in self.client.all_commands:
            command = self.client.get_command(target)
            if not command.enabled:
                command.enabled = True
                await ctx.send(embed = discord.Embed(description = f'Команда `{target}` включена', color = colors.JDH))
            else:
                await ctx.send(embed = discord.Embed(description = f'Команда `{target}` уже включена', color = colors.ERROR))
        else:
            extension = f'cogs.{target.title()}' if target != 'AICUS' else 'cogs.AICUS'
            try:
                await self.client.load_extension(extension)
            except commands.ExtensionNotFound:
                await ctx.send(embed = discord.Embed(description = f'Объект `{target}` не найден', color = colors.ERROR))
            except commands.ExtensionAlreadyLoaded:
                await ctx.send(embed = discord.Embed(description = f'Модуль `{target}` уже загружен', color = colors.ERROR))
            except commands.ExtensionFailed as error:
                await ctx.send(embed = discord.Embed(description = f'Модуль `{target}` не может быть загружен: `{error}`', color = colors.ERROR))
            else:
                await ctx.send(embed = discord.Embed(description = f'Модуль `{target}` загружен', color = colors.JDH))

    @commands.command(hidden = True)
    async def reload(self, ctx: commands.Context):
        if ctx.author.id not in self.client.owner_ids:
            raise commands.NotOwner()
        excepted_modules = {}
        warned_modules = {}
        timedout = False
        for name in list(self.client.extensions):
            with warnings.catch_warnings(record = True) as warnings_list:
                warnings.simplefilter('always')
                try:
                    await self.client.reload_extension(name)
                except commands.ExtensionFailed as error:
                    excepted_modules[f'`{name[5:]}`'] = str(error).replace('cogs.', '')
                for warning in warnings_list:
                    warned_modules[f'`{name[5:]}`'] = str(warning.message).replace('cogs.', '')
        if len(excepted_modules) == len(self.client.extensions):
            return await ctx.send(embed = discord.Embed(description = 'Все модули выдали ошибку', color = colors.ERROR))
        if warned_modules:
            LOGS.write(f'[WARN] Предупреждения при перезагрузке:\n')
            LOGS.write(''.join([f'{name}: {msg}\n' for name, msg in warned_modules.items()]))
            LOGS.flush()
            await ctx.send(embed = discord.Embed(description = f'Предупреждения при перезагрузке:\n{"".join([f'{name}: {msg}\n' for name, msg in warned_modules.items()])}', color = colors.JDH))
        if excepted_modules:
            LOGS.write(f'[ERR] При перезагрузке модулей возникли ошибки:\n{"".join([f'`{name}`: `{error}`\n' for name, error in excepted_modules.items()])}')
            LOGS.flush()
            return await ctx.send(embed = discord.Embed(description = f'{'Модуль' if len(excepted_modules) == 1 else 'Модули'} {', '.join(excepted_modules.keys())} не {'может быть перезагружен' if len(excepted_modules) == 1 else 'могут быть перезагружены'}, {f'пингани {self.client.get_user(338714886001524737).mention}' if ctx.author.id != 338714886001524737 else 'необходимо исправить'}:\n{''.join([f'`{name}`: `{error}`\n' for name, error in excepted_modules.items()])}', color = colors.ERROR))
        try:
            await asyncio.wait_for(self.client.tree.sync(), timeout = 3)
        except asyncio.TimeoutError:
            timedout = True
            LOGS.write(f'[ERR] При синхронизации команд возникла ошибка: превышен лимит времени (3 секунды)\n')
            LOGS.flush()
        except Exception as error:
            LOGS.write(f'[ERR] При синхронизации команд возникла ошибка: {error}\n')
            LOGS.flush()
        await ctx.send(embed = discord.Embed(description = f'Модули перезагружены{', команды синхронизированы' if not timedout else ''}', color = colors.JDH if not timedout else colors.ERROR))

    @commands.command(hidden = True)
    async def pull(self, ctx: commands.Context):
        if ctx.author.id not in self.client.owner_ids:
            raise commands.NotOwner()
        process = await asyncio.create_subprocess_shell('git pull', stdout = asyncio.subprocess.PIPE, stderr = asyncio.subprocess.PIPE)
        stdout, stderr = await process.communicate()
        if process.returncode != 0:
            await ctx.send(embed = discord.Embed(description = f'Не удалось получить обновления: `{stderr.decode("utf-8")}`', color = colors.ERROR))
        else:
            await ctx.send(embed = discord.Embed(description = f'Обновления получены:\n`{stdout.decode("utf-8").strip()}`', color = colors.JDH))
            await asyncio.sleep(self.client.latency)
            await ctx.send(embed = discord.Embed(description = 'Перезагрузка...', color = colors.JDH))
            await asyncio.sleep(self.client.latency)
            await self.reload(ctx)

    @commands.command(hidden = True)
    async def access_db(self, ctx: commands.Context, db: str, *, query: str):
        if ctx.author.id not in self.client.owner_ids:
            raise commands.NotOwner()
        CRITICAL_KEYWORDS = ["DROP", "ALTER", "TRUNCATE", "DELETE", "CREATE", "GRANT", "REVOKE"]
        found_keywords = []
        upper_query = query.upper()
        for keyword in CRITICAL_KEYWORDS:
            if keyword in upper_query:
                found_keywords.append(keyword)
        if found_keywords:
            formatted_lines = []
            highlight_lines = []
            for line in query.split('\n'):
                line_highlights = [' '] * len(line)
                upper_line = line.upper()
                for keyword in found_keywords:
                    start_idx = 0
                    while True:
                        idx = upper_line.find(keyword, start_idx)
                        if idx == -1:
                            break
                        for i in range(idx, idx + len(keyword)):
                            line_highlights[i] = '^'
                        start_idx = idx + len(keyword)
                formatted_lines.append(line)
                highlight_lines.append(''.join(line_highlights))
            display_query = '\n'.join(formatted_lines)
            display_highlight = '\n'.join(highlight_lines)
            view = discord.ui.View()
            view.add_item(discord.ui.Button(label = "Да", style = discord.ButtonStyle.red, custom_id = "confirm"))
            view.add_item(discord.ui.Button(label = "Нет", style = discord.ButtonStyle.green, custom_id = "cancel"))
            emb = discord.Embed(description = f"**Обнаружены опасные команды:** {', '.join(found_keywords)}", color = colors.ERROR)
            emb.add_field(name = "Вы собираетесь выполнить:", value = f"```sql\n{display_query[:1000]}\n{display_highlight[:1000]}\n\nПродолжить?```", inline = False)
            emb.set_footer(text = 'Подсвечены потенциально опасные команды (^)')
            message = await ctx.send(embed = emb, view = view)
            try:
                confirmation = await self.client.wait_for('interaction', check = lambda interaction: interaction.user.id == ctx.author.id and interaction.channel == ctx.channel, timeout = 30.0)
                if confirmation.data["custom_id"] == "confirm":
                    await message.edit(embed = discord.Embed(description = "Выполнение операции...", color = colors.JDH), view = None)
                else:
                    return await message.edit(embed = discord.Embed(description = "Операция отменена", color = colors.ERROR), view = None)
            except asyncio.TimeoutError:
                return await message.edit(embed = discord.Embed(description = "Время подтверждения истекло, операция отменена", color = colors.ERROR), view = None)
        conn = None
        try:
            conn = psycopg2.connect(host = "localhost", database = db, user = "postgres", password = PASSWORD, port = 5432)
            cur = conn.cursor()
            cur.execute(query)
            if query.strip().upper().startswith("SELECT"):
                result = cur.fetchall()
                if not result:
                    output = "Запрос вернул 0 строк"
                else:
                    columns = [desc[0] for desc in cur.description]
                    rows = [dict(zip(columns, row)) for row in result]
                    output = tabulate(rows, headers = "keys", tablefmt = "psql")
                if len(output) > 1900:
                    for i in range(0, len(output), 1900):
                        await ctx.send(f"```sql\n{output[i:i+1900].replace('```', '').replace('apache', '')}\n```")
                else:
                    await ctx.send(f"```sql\n{output.replace('```', '').replace('apache', '')}\n```")
            else:
                conn.commit()
                affected = cur.rowcount
                await ctx.send(f"Успешно выполнено. Затронуто строк: {affected}")
        except psycopg2.Error as e:
            await ctx.send(embed = discord.Embed(description = f"Ошибка PostgreSQL [{e.pgcode}]: {e.pgerror.splitlines()[0]}", color = colors.ERROR))
            if conn:
                conn.rollback()
        except Exception as e:
            await ctx.send(f"Неизвестная ошибка: {str(e)}")
            if conn:
                conn.rollback()
        finally:
            await message.delete()
            if conn:
                cur.close()
                conn.close()

    @commands.command(hidden = True)
    async def update(self, ctx: commands.Context, locale):
        if ctx.author.id not in self.client.owner_ids:
            raise commands.NotOwner()
        conn = psycopg2.connect(host = "localhost", database = "locales", user = "postgres", password = PASSWORD, port = 5432)
        cur = conn.cursor()
        message = await ctx.send(embed = discord.Embed(description = 'Обновление...', color = colors.JDH))
        table_name = locale
        try:
            file_path = rf'{CWD}\locales\{locale}\locale.json'
            with open(file_path, 'r', encoding='utf-8') as f:
                file_data = json.load(f)
            file_keys = set(file_data.keys())
            cur.execute(f"SELECT string_id FROM {table_name}")
            db_keys = {row[0] for row in cur.fetchall()}
            keys_to_delete = db_keys - file_keys
            keys_to_add = file_keys - db_keys
            keys_to_update = file_keys & db_keys
            if keys_to_delete:
                cur.execute(f"DELETE FROM {table_name} WHERE string_id IN %s", (tuple(keys_to_delete),))
            for key, value in file_data.items():
                cur.execute(f"INSERT INTO {table_name} (string_id, value) VALUES (%s, %s) ON CONFLICT (string_id) DO UPDATE SET value = EXCLUDED.value""", (key, value))
            conn.commit()
            result_msg = f'Обновление завершено\nДобавлено: {len(keys_to_add)}\nОбновлено: {len(keys_to_update)}\nУдалено: {len(keys_to_delete)}'
        except Exception as e:
            conn.rollback()
            result_msg = f'Ошибка обновления: {str(e)}'
        finally:
            cur.close()
            conn.close()
        await message.edit(embed = discord.Embed(description = result_msg, color = colors.JDH))

    @commands.command(hidden = True)
    async def diff_locales(self, ctx: commands.Context):
        from collections import OrderedDict
        if ctx.author.id not in self.client.owner_ids:
            raise commands.NotOwner()
        with psycopg2.connect(host = "localhost", database = "locales", user = "postgres", password = PASSWORD, port = 5432) as conn:
            with conn.cursor() as cur:
                keys = {}
                locales = ['ru', 'en', 'gnida']
                for loc in locales:
                    try:
                        cur.execute(f"SELECT string_id FROM {loc}")
                        keys[loc] = {row[0] for row in cur.fetchall()}
                    except psycopg2.Error:
                        keys[loc] = set()
                ru_unique_keys = keys['ru'] - (keys['en'] | keys['gnida'])
                has_ru_unique = bool(ru_unique_keys)
                report = ["=== Уникальные ключи ==="]
                for loc in locales:
                    other_locs = [l for l in locales if l != loc]
                    unique_keys = keys[loc] - keys[other_locs[0]] - keys[other_locs[1]]
                    if unique_keys:
                        report.append(f"{loc} ({len(unique_keys)}):")
                        report.extend(sorted(unique_keys)[:5])
                        if len(unique_keys) > 5:
                            report.append(f"... и ещё {len(unique_keys) - 5}")
                report.append("\n=== Отсутствующие ключи ===")
                all_keys = set().union(*keys.values())
                total_keys = len(all_keys)
                missing_info = {}
                for loc in locales:
                    missing_keys = all_keys - keys[loc]
                    missing_info[loc] = sorted(missing_keys)
                    missing_percent = (len(missing_keys) / total_keys * 100) if total_keys > 0 else 0
                    if missing_keys:
                        report.append(f"Отсутствует в {loc} ({len(missing_keys)} - {missing_percent:.1f}%):")
                        report.extend(map(str, sorted(missing_keys)[:5]))
                        if len(missing_keys) > 5:
                            report.append(f"... и ещё {len(missing_keys) - 5}")
                common_keys = set.intersection(*[keys[loc] for loc in locales])
                common_percent = (len(common_keys) / total_keys * 100) if total_keys > 0 else 0
                report.append(f"\n=== Общие ключи ({len(common_keys)} - {common_percent:.1f}% от всех ключей) ===")
                report.extend(sorted(common_keys)[:10])
                if len(common_keys) > 10:
                    report.append(f"... и ещё {len(common_keys) - 10}")
                output = "\n".join(report)
                emb = discord.Embed(description = f"```diff\n{output[:1990]}...\n```" if len(output) > 2000 else f"```diff\n{output}\n```", color = colors.JDH)
                await ctx.send(embed = emb)
        if not has_ru_unique:
            return
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label = "Добавить", style = discord.ButtonStyle.green, custom_id = "add_keys"))
        view.add_item(discord.ui.Button(label = "Пропустить", style = discord.ButtonStyle.red, custom_id = "skip_keys"))
        emb = discord.Embed(title = "Добавить отсутствующие ключи из ru?", description = "Нажмите на кнопку, чтобы автоматически добавить ru-ключи в другие локали\n ⚠️ **Важно:**\n- Ключи будут вставлены в те же позиции, что и в ru\n- Значения нужно будет заполнить ВРУЧНУЮ\n- Перед тем, как применить, ru будет обновлена автоматически", color = colors.JDH)
        sent = await ctx.send(embed = emb, view = view)
        confirmation = await self.client.wait_for('interaction', check = lambda interaction: interaction.channel == ctx.channel and interaction.user == ctx.author)
        await self.update(ctx, 'ru')
        await sent.edit(embed = emb, view = None)
        if confirmation.data['custom_id'] == 'skip_keys':
            return
        ru_path = locales_paths.RU
        with open(ru_path, 'r', encoding='utf-8') as f:
            ru_data = json.load(f, object_pairs_hook = OrderedDict)
        results = []
        for loc in ['en', 'gnida']:
            to_add = sorted(keys['ru'] - keys[loc])
            if not to_add:
                results.append(f"✅ {loc}: Нет ключей для добавления")
                continue
            try:
                path = locales_paths.GNIDA if loc == 'gnida' else locales_paths.EN
                with open(path, 'r+', encoding='utf-8') as f:
                    loc_data = json.load(f, object_pairs_hook = OrderedDict)
                    new_data = OrderedDict()
                    added_count = 0
                    for key in ru_data:
                        if key in loc_data:
                            new_data[key] = loc_data[key]
                        elif key in to_add:
                            new_data[key] = ""
                            added_count += 1
                    for key, value in loc_data.items():
                        if key not in ru_data:
                            new_data[key] = value
                    f.seek(0)
                    json.dump(new_data, f, indent = 4, ensure_ascii = False)
                    f.truncate()
                results.append(f"✅ {loc}: Добавлено {added_count} {get_plural_form(added_count, ['ключ', 'ключя', 'ключей'])}")
            except Exception as e:
                results.append(f"❌ {loc}: Ошибка ({str(e)})")
        result_embed = discord.Embed(title = "Результат обновления локалей", description = "\n".join(results) if results else "Нет изменений", color = colors.SUCCESS)
        result_embed.add_field(name = "Инструкция", value = "1. Проверьте JSON файлы локалей\n2. **Заполните ВРУЧНУЮ значения** для новых ключей (пустые строки)\n3. Новые ключи вставлены в позиции, соответствующие ru-локали", inline = False)
        await ctx.send(embed = result_embed)

async def setup(client):
    await client.add_cog(Kernel(client))
