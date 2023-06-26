# map_renderer.py
def get_cell_color(symbol):
    if symbol == '@':
        return 'blue'
    elif symbol == '.':
        return 'green'
    elif symbol == '#':
        return 'red'
    elif symbol == '=':
        return 'yellow'
    else:
        return 'black'  # Цвет по умолчанию
