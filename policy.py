from __future__ import annotations

import random
from typing import Dict, Iterable, List, Sequence, Tuple

from board import DELTAS, add_points, is_body_collision
from config import SEED, TIE_MARGIN, TOPK_RANDOM
from state import GameState, Point, Snake


def legal_moves(state: GameState) -> List[str]:
    snake = state.me
    return legal_moves_for_snake(state, snake)


def legal_moves_for_snake(state: GameState, snake: Snake) -> List[str]:
    moves: List[str] = []
    my_length = snake.length
    for move, delta in DELTAS.items():
        target = add_points(snake.head, delta)
        will_eat = target in state.food
        if is_body_collision(state, target, snake, will_eat):
            continue
        if is_losing_head_to_head(state, snake, target, my_length):
            continue
        moves.append(move)
    return moves


def is_losing_head_to_head(state: GameState, snake: Snake, target: Point, my_length: int) -> bool:
    for opponent in state.opponents:
        if opponent.id == snake.id:
            continue
        if opponent.eliminated:
            continue
        for delta in DELTAS.values():
            opp_target = add_points(opponent.head, delta)
            will_eat = opp_target in state.food
            if is_body_collision(state, opp_target, opponent, will_eat):
                continue
            if opp_target == target and opponent.length >= my_length:
                return True
    return False


def select_with_topk_random(
    scored_moves: Sequence[Tuple[str, float]],
    k: int,
    margin: float,
    seed: int,
) -> Tuple[str, float]:
    if not scored_moves:
        raise ValueError("select_with_topk_random requires at least one move.")
    ordered = sorted(scored_moves, key=lambda item: item[1], reverse=True)
    top_score = ordered[0][1]
    denom = max(1.0, abs(top_score))
    candidates = [
        item for item in ordered if (top_score - item[1]) / denom <= margin
    ]
    candidates = candidates[: max(1, k)]
    rng = random.Random(seed)
    choice = rng.choice(candidates)
    return choice


def count_safe_moves(state: GameState, snake: Snake) -> int:
    moves = legal_moves_for_snake(state, snake)
    return len(moves)
