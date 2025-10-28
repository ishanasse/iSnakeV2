from __future__ import annotations

from board import board_center, manhattan
from simulate import hypothetical_after_move
from state import GameState


def center_feature(state: GameState, move: str) -> float:
    hypo_state, _ = hypothetical_after_move(state, move)
    center = board_center(hypo_state)
    distance = manhattan(hypo_state.me.head, center)
    return -float(distance)

