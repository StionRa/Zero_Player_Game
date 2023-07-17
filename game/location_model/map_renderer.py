# map_renderer.py
def get_cell_color(symbol):
    if symbol == '@':
        return 'orange'
    elif symbol == '.':
        return 'green'
    elif symbol == '#':
        return 'grey'
    elif symbol == 'A':
        return 'purple'
    elif symbol == '%':
        return 'red'
    elif symbol == 'C':
        return 'pink'
    elif symbol == '~':
        return 'blue'
    elif symbol == 'O':
        return 'blue'
    else:
        return 'black'  # Цвет по умолчанию
