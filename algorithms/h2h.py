from __future__ import annotations

from board import manhattan
from state import GameState


def h2h_term(state: GameState) -> float:
    """
    Lightweight head-to-head heuristic.
    - Returns -1 when an equal/longer opponent can challenge our head next turn.
    - Returns +1 when we threaten a shorter opponent.
    """
    me = state.me
    losing = False
    winning = False
    for opponent in state.opponents:
        distance = manhattan(me.head, opponent.head)
        if distance != 1:
            continue
        if opponent.length >= me.length:
            losing = True
        elif me.length > opponent.length:
            winning = True
    if losing:
        return -1.0
    if winning:
        return 1.0
    return 0.0

