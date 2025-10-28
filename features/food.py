from __future__ import annotations

from typing import Iterable, Set

from algorithms.astar import shortest_path_length
from board import manhattan
from simulate import hypothetical_after_move
from state import GameState, Point
from config import LOW_HEALTH


def food_feature(state: GameState, move: str) -> tuple[int, float]:
    hypo_state, _ = hypothetical_after_move(state, move)
    me = hypo_state.me
    low_hp = 1 if me.health < LOW_HEALTH else 0

    candidate_food = _filter_contested_food(hypo_state, hypo_state.food, me.length)
    if not candidate_food:
        return low_hp, 0.0

    blocked: Set[Point] = set()
    for snake in hypo_state.active_snakes:
        blocked.update(snake.body)
    blocked.discard(me.head)

    distance = shortest_path_length(
        start=me.head,
        goals=candidate_food,
        blocked=blocked,
        width=hypo_state.width,
        height=hypo_state.height,
    )
    if distance is None:
        return low_hp, 0.0
    return low_hp, 1.0 / (distance + 1.0)


def _filter_contested_food(state: GameState, food: Iterable[Point], my_length: int) -> Set[Point]:
    candidates: Set[Point] = set()
    for pellet in food:
        contested = False
        for opponent in state.opponents:
            if opponent.length >= my_length:
                if manhattan(opponent.head, pellet) <= manhattan(state.me.head, pellet):
                    contested = True
                    break
        if not contested:
            candidates.add(pellet)
    return candidates

