from __future__ import annotations

from simulate import hypothetical_after_move
from state import GameState
from policy import count_safe_moves


def safe_degree_after_move(state: GameState, move: str) -> int:
    hypo_state, _ = hypothetical_after_move(state, move)
    return count_safe_moves(hypo_state, hypo_state.me)

