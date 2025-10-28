from algorithms.lookahead import beam_search
from config import BEAM_WIDTH, OPP_TOPK, get_weights
from state import GameState


def _build_state():
    return {
        "game": {"id": "policy-eval"},
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
                    "body": [{"x": 1, "y": 2}, {"x": 1, "y": 1}, {"x": 1, "y": 0}],
                    "head": {"x": 1, "y": 2},
                },
                {
                    "id": "opp",
                    "name": "Opp",
                    "health": 90,
                    "body": [{"x": 2, "y": 2}],
                    "head": {"x": 2, "y": 2},
                },
            ],
        },
        "you": {
            "id": "me",
            "name": "Me",
            "health": 90,
            "body": [{"x": 1, "y": 2}, {"x": 1, "y": 1}, {"x": 1, "y": 0}],
            "head": {"x": 1, "y": 2},
        },
    }


def test_beam_prefers_safe_path():
    state = GameState.from_json(_build_state())
    weights = get_weights()
    score_left = beam_search(state, "left", depth=1, beam_width=BEAM_WIDTH, opp_topk=OPP_TOPK, weights=weights)
    score_up = beam_search(state, "up", depth=1, beam_width=BEAM_WIDTH, opp_topk=OPP_TOPK, weights=weights)
    assert score_up > score_left
