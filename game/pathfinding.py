from game.location_model import Location
from django.db import models
import heapq


class Node:
    def __init__(self, position, passable):
        self.position = position
        self.passable = passable
        self.g = float('inf')  # Cost from start node
        self.h = 0  # Heuristic cost to target node
        self.f = float('inf')  # Total cost
        self.parent = None

    def __lt__(self, other):
        return self.f < other.f


def heuristic(node, target):
    # Example heuristic function - Manhattan distance
    return abs(node.position[0] - target[0]) + abs(node.position[1] - target[1])


def a_star_search(start, target):
    x_min = Location.objects.aggregate(models.Min('x'))['x__min']
    y_min = Location.objects.aggregate(models.Min('y'))['y__min']
    x_max = Location.objects.aggregate(models.Max('x'))['x__max']
    y_max = Location.objects.aggregate(models.Max('y'))['y__max']

    visited = set()
    open_nodes = []
    heapq.heapify(open_nodes)

    start_node = Node(start, passable=True)
    start_node.g = 0
    start_node.h = heuristic(start_node, target)
    start_node.f = start_node.g + start_node.h

    heapq.heappush(open_nodes, (start_node.f, start_node))

    while open_nodes:
        current_node = heapq.heappop(open_nodes)[1]

        if current_node.position == target:
            path = []
            while current_node:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]

        visited.add(current_node.position)

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_x = current_node.position[0] + dx
            new_y = current_node.position[1] + dy

            if x_min <= new_x <= x_max and y_min <= new_y <= y_max:
                passable = Location.objects.get(x=new_x, y=new_y).passable

                if not passable or (new_x, new_y) in visited:
                    continue

                neighbor = Node((new_x, new_y), passable=True)
                neighbor.g = current_node.g + 1
                neighbor.h = heuristic(neighbor, target)
                neighbor.f = neighbor.g + neighbor.h
                neighbor.parent = current_node

                heapq.heappush(open_nodes, (neighbor.f, neighbor))

    return None
