from game.ai import make_decision_and_move, take_path, move


def repeat_move(character, target_x, target_y):
    while character.x != target_x or character.y != target_y:
        start_point, target_point = make_decision_and_move(character, target_x, target_y)
        if start_point is None or target_point is None:
            print("Invalid move decision.")
            break

        path = take_path(start_point, target_point)
        if path is not None:
            for point in path:
                move(character, point[0], point[1])
                if character.x == target_x and character.y == target_y:
                    print(f"Character {character.name} reached the target coordinates: ({target_x}, {target_y})")
                    return
        else:
            print("No valid path found.")
            break

    print(f"Unable to reach the target coordinates: ({target_x}, {target_y})")

