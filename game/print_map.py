import game.game_options as opt

display_width = opt.PLAYER_WIDTH
display_height = opt.PLAYER_HEIGHT
width = opt.WIDTH
height = opt.HEIGHT


def print_map(map_x, character_x_navi, character_y_navi):
    start_x = max(0, character_x_navi - display_width // 2)  # Начальная координата X для отображения
    start_y = max(0, character_y_navi - display_height // 2)  # Начальная координата Y для отображения

    end_x = min(start_x + display_width, width)  # Конечная координата X для отображения
    end_y = min(start_y + display_height, height)  # Конечная координата Y для отображения

    for y in range(start_y, end_y):
        for x in range(start_x, end_x):
            if x == character_x_navi and y == character_y_navi:
                symbol = '@'
            else:
                cell = map_x[y][x]
                if cell is None:
                    symbol = 'X'
                elif cell:
                    symbol = '.'
                else:
                    symbol = '#'
            print(symbol, end=' ')
        print()


def generate_map_html(map_x, character_x_navi, character_y_navi):
    start_x = max(0, character_x_navi - display_width // 2)
    start_y = max(0, character_y_navi - display_height // 2)

    end_x = min(start_x + display_width, width)
    end_y = min(start_y + display_height, height)

    html_output = ""

    for y in range(start_y, end_y):
        for x in range(start_x, end_x):
            if x == character_x_navi and y == character_y_navi:
                symbol = '@'
            else:
                cell = map_x[y][x]
                if cell is None:
                    symbol = 'X'
                elif cell:
                    symbol = '.'
                else:
                    symbol = '#'
            html_output += f"<span>{symbol}</span>"
        html_output += "<br>"

    return html_output
