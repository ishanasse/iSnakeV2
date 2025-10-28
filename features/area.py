from __future__ import annotations

from algorithms.flood_fill import area_after_move
from state import GameState


def area_feature(state: GameState, move: str) -> tuple[int, float]:
    return area_after_move(state, move)

