from state import GameState
from policy import legal_moves


def _base_state():
    return {
        "game": {"id": "test-tail-slip"},
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
                    "body": [{"x": 2, "y": 1}, {"x": 2, "y": 0}],
                    "head": {"x": 2, "y": 1},
                }
            ],
        },
        "you": {
            "id": "me",
            "name": "Me",
            "health": 90,
            "body": [{"x": 2, "y": 1}, {"x": 2, "y": 0}],
            "head": {"x": 2, "y": 1},
        },
    }


def test_tail_slip_allowed_without_food():
    data = _base_state()
    state = GameState.from_json(data)
    moves = legal_moves(state)
    assert "down" in moves, "Tail slip should be legal when tail vacates."


def test_tail_slip_blocked_when_food_on_tail():
    data = _base_state()
    data["board"]["food"] = [{"x": 2, "y": 0}]
    state = GameState.from_json(data)
    moves = legal_moves(state)
    assert "down" not in moves, "Tail slip blocked when eating keeps tail in place."
