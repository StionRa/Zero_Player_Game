# import sqlite3
# import random
#
# conn = sqlite3.connect('map.db')
# c = conn.cursor()
#
# c.execute('''CREATE TABLE IF NOT EXISTS map (
#                 x INTEGER,
#                 y INTEGER,
#                 name TEXT,
#                 passable INTEGER,
#                 PRIMARY KEY (x, y)
#              )''')
#
# width = 20
# height = 20
#
#
# def check_map_existence():
#     c.execute('SELECT COUNT(*) FROM map')
#     result = c.fetchone()
#     map_exists = result[0] > 0
#     return map_exists
#
#
# def generate_map():
#     map_data_generate = []
#     for y in range(height):
#         row = []
#         for x in range(width):
#             name = f"{x},{y}"
#             passable = random.choices([True, False], weights=[17, 3])[0]
#             row.append((x, y, name, passable))
#         map_data_generate.extend(row)
#
#     c.executemany('INSERT OR IGNORE INTO map VALUES (?, ?, ?, ?)', map_data_generate)
#     conn.commit()
#
#
# def add_map_part(part_width, part_height, direction):
#     global width, height
#
#     if direction == 'left':
#         min_x = -part_width
#         max_x = -1
#         min_y = 0
#         max_y = height - 1
#         new_width = width + part_width
#         new_height = height
#     elif direction == 'right':
#         min_x = width
#         max_x = width + part_width - 1
#         min_y = 0
#         max_y = height - 1
#         new_width = width + part_width
#         new_height = height
#     elif direction == 'top':
#         min_x = 0
#         max_x = width - 1
#         min_y = -part_height
#         max_y = -1
#         new_width = width
#         new_height = height + part_height
#     elif direction == 'bottom':
#         min_x = 0
#         max_x = width - 1
#         min_y = height
#         max_y = height + part_height - 1
#         new_width = width
#         new_height = height + part_height
#     else:
#         raise ValueError("Invalid direction. Allowed values: 'left', 'right', 'top', 'bottom'.")
#
#     new_part = []
#     for y in range(min_y, max_y + 1):
#         row = []
#         for x in range(min_x, max_x + 1):
#             name = f"{x},{y}"
#             passable = random.choices([True, False], weights=[17, 3])[0]
#             row.append((x, y, name, passable))
#         new_part.extend(row)
#
#     c.executemany('INSERT OR IGNORE INTO map VALUES (?, ?, ?, ?)', new_part)
#     conn.commit()
#
#     width = new_width
#     height = new_height
#
#
# def load_map():
#     global width, height
#
#     c.execute('SELECT x, y, passable FROM map')
#     rows = c.fetchall()
#
#     # Обновляем значения width и height
#     if rows:
#         x_values, y_values, _ = zip(*rows)
#         width = max(max(x_values) + 1, width)
#         height = max(max(y_values) + 1, height)
#
#     map_load = [[True for _ in range(width)] for _ in range(height)]
#     for row in rows:
#         x, y, passable = row
#         map_load[y][x] = passable
#
#     return map_load
#
#
# def print_map(map_x, character_x_navi, character_y_navi):
#     display_width = 10  # Ширина отображаемой области
#     display_height = 10  # Высота отображаемой области
#
#     start_x = max(0, character_x_navi - display_width // 2)  # Начальная координата X для отображения
#     start_y = max(0, character_y_navi - display_height // 2)  # Начальная координата Y для отображения
#
#     end_x = min(start_x + display_width, width)  # Конечная координата X для отображения
#     end_y = min(start_y + display_height, height)  # Конечная координата Y для отображения
#
#     for y in range(start_y, end_y):
#         for x in range(start_x, end_x):
#             if x == character_x_navi and y == character_y_navi:
#                 symbol = '@'
#             else:
#                 cell = map_x[y][x]
#                 if cell is None:
#                     symbol = 'X'
#                 elif cell:
#                     symbol = '.'
#                 else:
#                     symbol = '#'
#             print(symbol, end=' ')
#         print()
#
#
# map_exists = check_map_existence()
#
# if not map_exists:
#     generate_map()
#
# map_data = load_map()
#
# character_x = random.randint(0, width - 1)
# character_y = random.randint(0, height - 1)
#
# print_map(map_data, character_x, character_y)
#
# while True:
#     move = input("Введите команду для перемещения персонажа (w - вверх, a - влево, s - вниз, d - вправо): ")
#     print(character_y, character_x)
#     if move == 'w' and character_y > 0:
#         if map_data[character_y - 1][character_x]:
#             character_y -= 1
#     elif move == 'w' and character_y == 0:
#         add_map_part(width, height, 'top')
#         character_y = 1
#         map_data = load_map()
#     elif move == 'a' and character_x > 0:
#         if map_data[character_y][character_x - 1]:
#             character_x -= 1
#     elif move == 'a' and character_x == 0:
#         add_map_part(width, height, 'left')
#         character_x = 1
#         map_data = load_map()
#     elif move == 's' and character_y < height - 1:
#         if map_data[character_y + 1][character_x]:
#             character_y += 1
#     elif move == 's' and character_y == height - 1:
#         add_map_part(width, height, 'bottom')
#         character_y = 1
#         map_data = load_map()
#     elif move == 'd' and character_x < width - 1:
#         if map_data[character_y][character_x + 1]:
#             character_x += 1
#     elif move == 'd' and character_x == width - 1:
#         add_map_part(width, height, 'right')
#         character_x = 1
#         map_data = load_map()
#     else:
#         print("Неверная команда.")
#         continue
#
#     print_map(map_data, character_x, character_y)
