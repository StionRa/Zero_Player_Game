# get_color_temp.py
def get_color_temp(temp):
    if temp <= -10:
        return 'bg-info'
    elif -9.99 <= temp <= 10:
        return None
    elif 10.01 <= temp < 25.99:
        return 'bg-success'
    elif 26.00 <= temp < 30.99:
        return 'bg-warning'
    elif 31 <= temp < 35:
        return 'bg-danger'
    else:
        return 'bg-info'
