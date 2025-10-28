from features.food import food_feature
from state import GameState


def _build_state(low_hp: int = 20):
    return {
        "game": {"id": "food-test"},
        "turn": 0,
        "board": {
            "height": 7,
            "width": 7,
            "food": [{"x": 3, "y": 1}],
            "hazards": [],
            "snakes": [
                {
                    "id": "me",
                    "name": "Me",
                    "health": low_hp,
                    "body": [{"x": 1, "y": 1}],
                    "head": {"x": 1, "y": 1},
                },
                {
                    "id": "opp",
                    "name": "Opp",
                    "health": 90,
                    "body": [{"x": 4, "y": 1}, {"x": 4, "y": 0}, {"x": 3, "y": 0}, {"x": 2, "y": 0}],
                    "head": {"x": 4, "y": 1},
                },
            ],
        },
        "you": {
            "id": "me",
            "name": "Me",
            "health": low_hp,
            "body": [{"x": 1, "y": 1}],
            "head": {"x": 1, "y": 1},
        },
    }


def test_low_hp_food_signal():
    state = GameState.from_json(_build_state())
    lowhp, inv_food = food_feature(state, "right")
    assert lowhp == 1
    assert inv_food == 0.0, "Food contested by longer opponent should be ignored."


def test_food_available_when_uncontested():
    data = _build_state()
    data["board"]["snakes"].pop()  # remove opponent
    state = GameState.from_json(data)
    lowhp, inv_food = food_feature(state, "right")
    assert lowhp == 1
    assert inv_food > 0.0
