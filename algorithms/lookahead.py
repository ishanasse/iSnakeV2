from __future__ import annotations

import itertools
from typing import Dict, List, Sequence, Tuple

from config import LOW_HEALTH
from evaluation import score_state
from policy import legal_moves, legal_moves_for_snake
from simulate import simulate_turn, hypothetical_after_move_for_snake
from state import GameState


def beam_search(
    state: GameState,
    root_move: str,
    depth: int,
    beam_width: int,
    opp_topk: int,
    weights,
) -> float:
    """
    Evaluate a root move using a simple depth-limited beam search.
    """
    root_children = _expand_with_opponents(state, root_move, beam_width, opp_topk, weights)
    if not root_children:
        return score_state(state, weights) - 100.0
    if depth <= 0:
        return _average([score_state(child, weights) for child in root_children])

    child_scores: List[float] = []
    for child in root_children:
        value = _max_future_score(child, depth - 1, beam_width, opp_topk, weights)
        child_scores.append(value)
    return _average(child_scores)


def _max_future_score(
    state: GameState,
    depth: int,
    beam_width: int,
    opp_topk: int,
    weights,
) -> float:
    if depth <= 0:
        return score_state(state, weights)

    moves = legal_moves(state)
    if not moves:
        return score_state(state, weights) - 100.0

    scored_moves: List[Tuple[str, float]] = []
    for move in moves:
        children = _expand_with_opponents(state, move, beam_width, opp_topk, weights)
        if not children:
            scored_moves.append((move, score_state(state, weights) - 100.0))
            continue
        child_scores = [
            score_state(child, weights) if depth == 1 else _max_future_score(child, depth - 1, beam_width, opp_topk, weights)
            for child in children
        ]
        scored_moves.append((move, _average(child_scores)))

    scored_moves.sort(key=lambda item: item[1], reverse=True)
    trimmed = scored_moves[:beam_width]
    return trimmed[0][1]


def _expand_with_opponents(
    state: GameState,
    my_move: str,
    beam_width: int,
    opp_topk: int,
    weights,
) -> List[GameState]:
    opponent_move_ranking = _rank_opponent_moves(state, opp_topk)
    combos = _top_combinations(opponent_move_ranking, beam_width)
    if not combos:
        combos = [{}]
    children: List[Tuple[float, GameState]] = []
    for combo in combos:
        move_map = {state.me_id: my_move}
        move_map.update(combo)
        child_state = simulate_turn(state, move_map)
        children.append((score_state(child_state, weights), child_state))
    children.sort(key=lambda item: item[0], reverse=True)
    return [child for _, child in children[:beam_width]]


def _rank_opponent_moves(state: GameState, opp_topk: int) -> Dict[str, List[Tuple[str, float]]]:
    rankings: Dict[str, List[Tuple[str, float]]] = {}
    for opponent in state.opponents:
        moves = legal_moves_for_snake(state, opponent)
        scored: List[Tuple[str, float]] = []
        for move in moves:
            hypo_state, _ = hypothetical_after_move_for_snake(state, opponent.id, move)
            updated = hypo_state.snakes[opponent.id]
            degree = len(legal_moves_for_snake(hypo_state, updated))
            toward_food = 0.0
            if opponent.health < LOW_HEALTH and hypo_state.food:
                distances = [abs(updated.head[0] - fx) + abs(updated.head[1] - fy) for fx, fy in hypo_state.food]
                if distances:
                    toward_food = 1.0 / (min(distances) + 1.0)
            area_hint = len(updated.body)
            score = degree + toward_food + 0.1 * area_hint
            scored.append((move, score))
        scored.sort(key=lambda item: item[1], reverse=True)
        rankings[opponent.id] = scored[: max(1, opp_topk)]
    return rankings


def _top_combinations(
    rankings: Dict[str, List[Tuple[str, float]]],
    beam_width: int,
) -> List[Dict[str, str]]:
    combos: List[Tuple[Dict[str, str], float]] = [({}, 0.0)]
    for snake_id, moves in rankings.items():
        new_combos: List[Tuple[Dict[str, str], float]] = []
        for combo, combo_score in combos:
            for move, score in moves:
                updated = dict(combo)
                updated[snake_id] = move
                new_combos.append((updated, combo_score + score))
        new_combos.sort(key=lambda item: item[1], reverse=True)
        combos = new_combos[:beam_width] if new_combos else combos
    return [combo for combo, _ in combos]


def _average(values: Sequence[float]) -> float:
    if not values:
        return 0.0
    return sum(values) / len(values)

