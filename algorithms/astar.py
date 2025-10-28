from __future__ import annotations

import heapq
from typing import Dict, Iterable, List, Optional, Set, Tuple

from board import manhattan, neighbors
from state import Point


def shortest_path_length(
    start: Point,
    goals: Iterable[Point],
    blocked: Set[Point],
    width: int,
    height: int,
) -> Optional[int]:
    """
    Basic A* search that returns the shortest distance from `start` to any goal.
    Returns None when no goal is reachable.
    """
    goal_set = set(goals)
    if not goal_set:
        return None
    frontier: List[Tuple[int, int, Point]] = []
    heapq.heappush(frontier, (0 + _h(start, goal_set), 0, start))
    costs: Dict[Point, int] = {start: 0}
    visited: Set[Point] = set()

    while frontier:
        _, cost, point = heapq.heappop(frontier)
        if point in visited:
            continue
        visited.add(point)
        if point in goal_set:
            return cost

        for nbr in neighbors(point):
            x, y = nbr
            if not (0 <= x < width and 0 <= y < height):
                continue
            if nbr in blocked:
                continue
            new_cost = cost + 1
            if new_cost < costs.get(nbr, 1_000_000):
                costs[nbr] = new_cost
                priority = new_cost + _h(nbr, goal_set)
                heapq.heappush(frontier, (priority, new_cost, nbr))
    return None


def _h(point: Point, goals: Set[Point]) -> int:
    return min(manhattan(point, goal) for goal in goals)

