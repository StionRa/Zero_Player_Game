from game.location_model import Location


def find_path(start_x, start_y, end_x, end_y, visited):

    if start_x > end_x:
        x = start_x - 1
        y = start_y
        step_location = Location.objects.get(x=x, y=y)
        if (x, y) not in visited:
            if step_location.passable:
                return x, y
            else:
                # Вызов рекурсивно для следующего возможного направления
                return find_path(x + 1, y, end_x, end_y, visited)

    elif start_x < end_x:
        x = start_x + 1
        y = start_y
        step_location = Location.objects.get(x=x, y=y)
        if (x, y) not in visited:
            if step_location.passable:
                return x, y
            else:
                return find_path(x - 1, y, end_x, end_y, visited)

    elif start_y > end_y:
        x = start_x
        y = start_y - 1
        step_location = Location.objects.get(x=x, y=y)
        if (x, y) not in visited:
            if step_location.passable:
                return x, y
            else:
                return find_path(x, y + 1, end_x, end_y, visited)

    elif start_y < end_y:
        x = start_x
        y = start_y + 1
        step_location = Location.objects.get(x=x, y=y)
        if (x, y) not in visited:
            if step_location.passable:
                return x, y
            else:
                return find_path(x, y - 1, end_x, end_y, visited)

    # Если ни одно направление не проходит, вернуть None
    return None
