import logging
import time
import typing

from algorithms.lookahead import beam_search
from config import (
    BEAM_WIDTH,
    FALLBACK_MS,
    LOOKAHEAD_DEPTH,
    OPP_TOPK,
    TOPK_RANDOM,
    TIE_MARGIN,
    get_weights,
)
from policy import legal_moves, select_with_topk_random
from state import GameState


logger = logging.getLogger("battlesnake")
if not logger.handlers:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def info() -> typing.Dict:
    print("INFO")
    return {
        "apiversion": "1",
        "author": "IT",
        "color": "#888888",
        "head": "earmuffs",
        "tail": "coffee"
    }


def start(game_state: typing.Dict):
    print("GAME START")


def end(game_state: typing.Dict):
    print("GAME OVER\n")


def move(game_state: typing.Dict) -> typing.Dict:
    state = GameState.from_json(game_state)

    players_snapshot = [
        {
            "id": snake.id,
            "health": snake.health,
            "length": snake.length,
            "head": snake.head,
            "body": list(snake.body),
            "eliminated": snake.eliminated,
        }
        for snake in state.active_snakes
    ]
    logger.info("Turn %s state: %s", state.turn, players_snapshot)

    weights = get_weights()
    moves = legal_moves(state)
    if not moves:
        logger.warning("No legal moves available; defaulting to 'up'.")
        return {"move": "up"}

    start_time = time.perf_counter()
    scored_moves = []
    for direction in moves:
        score = beam_search(
            state=state,
            root_move=direction,
            depth=max(0, LOOKAHEAD_DEPTH),
            beam_width=max(1, BEAM_WIDTH),
            opp_topk=max(1, OPP_TOPK),
            weights=weights,
        )
        scored_moves.append((direction, score))
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        if elapsed_ms > FALLBACK_MS:
            logger.warning(
                "Beam search exceeded fallback budget (%.2f ms > %s ms); stopping early.",
                elapsed_ms,
                FALLBACK_MS,
            )
            break

    if not scored_moves:
        logger.warning("No scored moves after evaluation; falling back to first legal move.")
        return {"move": moves[0]}

    seed = int(state.rng.random() * 1_000_000)
    chosen_move, chosen_score = select_with_topk_random(
        scored_moves,
        k=max(1, TOPK_RANDOM),
        margin=TIE_MARGIN,
        seed=seed,
    )
    ranked_moves = sorted(scored_moves, key=lambda item: item[1], reverse=True)
    logger.info(
        "Turn %s decision: move %s (score %.3f); candidates=%s",
        state.turn,
        chosen_move,
        chosen_score,
        ranked_moves,
    )
    return {"move": chosen_move}


if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
