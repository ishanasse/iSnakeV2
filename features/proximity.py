from __future__ import annotations

from board import manhattan
from simulate import hypothetical_after_move
from state import GameState


def proximity_to_longer(state: GameState, move: str) -> float:
    hypo_state, _ = hypothetical_after_move(state, move)
    me = hypo_state.me
    longer = [opp for opp in hypo_state.opponents if opp.length >= me.length]
    if not longer:
        return 0.0
    dist = min(manhattan(me.head, opp.head) for opp in longer)
    return -1.0 / (dist + 1.0)

