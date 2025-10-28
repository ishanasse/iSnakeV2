from __future__ import annotations

from typing import Iterable

from board import manhattan
from state import GameState


def voronoi_control(state: GameState) -> float:
    """
    Approximate Voronoi control by counting cells where our head is closer than any opponent.
    Uses Manhattan distance for speed; adequate for heuristic scoring.
    """
    me = state.me
    opponents = state.opponents
    if not opponents:
        return 1.0
    total = 0
    controlled = 0
    occupied = {seg for snake in state.active_snakes for seg in snake.body}
    for x in range(state.width):
        for y in range(state.height):
            cell = (x, y)
            if cell in occupied:
                continue
            total += 1
            my_dist = manhattan(me.head, cell)
            opp_dist = min(manhattan(opp.head, cell) for opp in opponents)
            if my_dist < opp_dist:
                controlled += 1
    if total == 0:
        return 0.0
    return controlled / total

