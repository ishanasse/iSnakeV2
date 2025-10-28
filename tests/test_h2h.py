from algorithms.h2h import h2h_term
from state import GameState


def _build_state(my_length: int, opp_length: int):
    return {
        "game": {"id": "h2h"},
        "turn": 0,
        "board": {
            "height": 5,
            "width": 5,
            "food": [],
            "hazards": [],
            "snakes": [
                {
                    "id": "me",
                    "name": "Me",
                    "health": 90,
                    "body": [{"x": 2, "y": 2}] + [{"x": 2, "y": 1}] * (my_length - 1),
                    "head": {"x": 2, "y": 2},
                },
                {
                    "id": "opp",
                    "name": "Opp",
                    "health": 90,
                    "body": [{"x": 3, "y": 2}] + [{"x": 3, "y": 1}] * (opp_length - 1),
                    "head": {"x": 3, "y": 2},
                },
            ],
        },
        "you": {
            "id": "me",
            "name": "Me",
            "health": 90,
            "body": [{"x": 2, "y": 2}] + [{"x": 2, "y": 1}] * (my_length - 1),
            "head": {"x": 2, "y": 2},
        },
    }


def test_h2h_losing_signal():
    state = GameState.from_json(_build_state(my_length=3, opp_length=4))
    assert h2h_term(state) < 0


def test_h2h_winning_signal():
    state = GameState.from_json(_build_state(my_length=5, opp_length=3))
    assert h2h_term(state) > 0

