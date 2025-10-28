from algorithms.flood_fill import area_after_move
from state import GameState


def test_flood_fill_normalized_space():
    data = {
        "game": {"id": "test-flood"},
        "turn": 0,
        "board": {
            "height": 3,
            "width": 3,
            "food": [],
            "hazards": [],
            "snakes": [
                {
                    "id": "me",
                    "name": "Me",
                    "health": 90,
                    "body": [{"x": 1, "y": 1}],
                    "head": {"x": 1, "y": 1},
                }
            ],
        },
        "you": {
            "id": "me",
            "name": "Me",
            "health": 90,
            "body": [{"x": 1, "y": 1}],
            "head": {"x": 1, "y": 1},
        },
    }
    state = GameState.from_json(data)
    count, normalized = area_after_move(state, "up")
    assert count == 9
    assert normalized == 1.0

