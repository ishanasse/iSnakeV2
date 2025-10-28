from __future__ import annotations

from collections import deque
from typing import Set, Tuple

from board import neighbors
from simulate import hypothetical_after_move
from state import GameState, Point


def area_after_move(state: GameState, move: str) -> Tuple[int, float]:
    """
    Performs a flood-fill from the new head position after making `move`.
    Returns a tuple of (reachable_tiles, normalized_reachable_tiles).
    """
    hypo_state, _ = hypothetical_after_move(state, move)
    start = hypo_state.me.head

    blocked: Set[Point] = set()
    for snake in hypo_state.active_snakes:
        blocked.update(snake.body)
    blocked.discard(start)

    reachable = _flood_fill(start, blocked, hypo_state.width, hypo_state.height)
    total_tiles = hypo_state.width * hypo_state.height
    total_blocked = len(blocked)
    total_empty = max(1, total_tiles - total_blocked)
    normalized = reachable / total_empty
    return reachable, normalized


def _flood_fill(start: Point, blocked: Set[Point], width: int, height: int) -> int:
    queue = deque([start])
    visited: Set[Point] = {start}
    count = 0
    while queue:
        point = queue.popleft()
        count += 1
        for nbr in neighbors(point):
            x, y = nbr
            if not (0 <= x < width and 0 <= y < height):
                continue
            if nbr in blocked or nbr in visited:
                continue
            visited.add(nbr)
            queue.append(nbr)
    return count


def area_from_state(state: GameState) -> Tuple[int, float]:
    """
    Flood-fill using the state's current head position.
    """
    start = state.me.head
    blocked: Set[Point] = set()
    for snake in state.active_snakes:
        blocked.update(snake.body)
    blocked.discard(start)
    reachable = _flood_fill(start, blocked, state.width, state.height)
    total = state.width * state.height
    total_blocked = len(blocked)
    total_empty = max(1, total - total_blocked)
    return reachable, reachable / total_empty
