from __future__ import annotations

from math import inf
from typing import Tuple

from algorithms.flood_fill import area_from_state
from algorithms.h2h import h2h_term
from algorithms.voronoi import voronoi_control
from board import manhattan
from config import LOW_HEALTH, Weights
from policy import count_safe_moves
from state import GameState


def score_state(state: GameState, weights: Weights) -> float:
    """
    Computes the heuristic score for a fully simulated game state.
    """
    me = state.me
    area_count, area_norm = area_from_state(state)
    low_hp = 1 if me.health < LOW_HEALTH else 0
    inv_food = _inv_food_distance(state)
    corridor_penalty = _corridor_penalty_from_state(state)
    hazard_cost = 1.0 if me.head in state.hazards else 0.0
    h2h_value = h2h_term(state)
    longest = max((opp.length for opp in state.opponents), default=0)
    if longest <= 0:
        h2h_eff = h2h_value
    else:
        h2h_eff = h2h_value * min(1.0, me.length / (longest + 1e-9))
    to_center = -float(manhattan(me.head, ((state.width - 1) // 2, (state.height - 1) // 2)))
    safe_degree = float(count_safe_moves(state, me))
    longer_term = _longer_proximity_term(state)
    stability = _area_stability(state, area_count)
    voronoi = voronoi_control(state)

    score = (
        weights.area * area_norm
        + weights.food * low_hp * inv_food
        + weights.corridor * (-corridor_penalty)
        + weights.hazard * (-hazard_cost)
        + weights.h2h * h2h_eff
        + weights.center * to_center
        + weights.degree * safe_degree
        + weights.longer * longer_term
        + weights.stability * stability
        + weights.voronoi * voronoi
    )
    return score


def _inv_food_distance(state: GameState) -> float:
    me = state.me
    if not state.food:
        return 0.0
    min_dist = inf
    for food in state.food:
        dist = manhattan(me.head, food)
        min_dist = min(min_dist, dist)
    if min_dist == inf:
        return 0.0
    return 1.0 / (min_dist + 1.0)


def _corridor_penalty_from_state(state: GameState) -> int:
    degree = count_safe_moves(state, state.me)
    if degree <= 1:
        return 2
    if degree == 2:
        return 1
    return 0


def _longer_proximity_term(state: GameState) -> float:
    longer = [opp for opp in state.opponents if opp.length >= state.me.length]
    if not longer:
        return 0.0
    dist = min(manhattan(state.me.head, opp.head) for opp in longer)
    return -1.0 / (dist + 1.0)


def _area_stability(state: GameState, area_now: int) -> float:
    # Without historical context we approximate stability via relative area.
    max_area = state.width * state.height
    return area_now / max(1, max_area)
