from __future__ import annotations

from policy import count_safe_moves
from simulate import hypothetical_after_move
from state import GameState


def corridor_penalty(state: GameState, move: str) -> int:
    """
    Simple corridor heuristic: penalise moves that leave us with ≤ 2 escape options.
    """
    hypo_state, _ = hypothetical_after_move(state, move)
    moves_available = count_safe_moves(hypo_state, hypo_state.me)
    if moves_available <= 1:
        return 2
    if moves_available == 2:
        return 1
    return 0

