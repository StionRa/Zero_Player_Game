# get_color_temp.py
def get_color_temp(temp):
    if temp <= -10.00:
        return 'bg-info'
    elif temp >= -9.00 or temp <= 9.00:
        return 'bg-success'
    elif temp >= 10.00 or temp <= 28.00:
        return 'bg-warning'
    elif temp >= 29.00:
        return 'bg-danger'
    else:
        return None  # Цвет по умолчанию
