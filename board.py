from __future__ import annotations

from typing import Dict, Iterable, List, Tuple

from state import GameState, Point, Snake

DELTAS: Dict[str, Point] = {
    "up": (0, 1),
    "down": (0, -1),
    "left": (-1, 0),
    "right": (1, 0),
}


def add_points(a: Point, b: Point) -> Point:
    return a[0] + b[0], a[1] + b[1]


def neighbors(point: Point) -> List[Point]:
    return [add_points(point, delta) for delta in DELTAS.values()]


def manhattan(a: Point, b: Point) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def direction_to_delta(direction: str) -> Point:
    return DELTAS[direction]


def delta_to_direction(delta: Point) -> str:
    for direction, d in DELTAS.items():
        if d == delta:
            return direction
    raise ValueError(f"Unknown delta {delta}")


def within_bounds(state: GameState, point: Point) -> bool:
    return state.inside(point)


def is_body_collision(state: GameState, point: Point, snake: Snake, will_eat: bool) -> bool:
    """
    Checks whether moving the provided snake into the given point causes a body collision.
    Tail-slip is allowed when the snake will not eat and the point corresponds to its tail.
    """
    if not state.inside(point):
        return True

    for other in state.active_snakes:
        for index, segment in enumerate(other.body):
            if segment != point:
                continue
            tail_index = len(other.body) - 1
            if other.id == snake.id and not will_eat and index == tail_index:
                continue
            return True
    return False


def board_center(state: GameState) -> Point:
    return (state.width - 1) // 2, (state.height - 1) // 2


def legal_neighbor_tiles(state: GameState, point: Point) -> List[Point]:
    return [nbr for nbr in neighbors(point) if state.inside(nbr)]
