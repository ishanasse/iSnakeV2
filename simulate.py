from __future__ import annotations

from collections import defaultdict
from typing import Dict, Iterable, List, Tuple

from board import add_points, direction_to_delta, manhattan
from config import LOW_HEALTH
from state import GameState, Point, Snake

# Health restored on food per Battlesnake rules.
FOOD_HEALTH = 100
HAZARD_DAMAGE = 15


def hypothetical_after_move(state: GameState, move: str) -> Tuple[GameState, bool]:
    return hypothetical_after_move_for_snake(state, state.me_id, move)


def hypothetical_after_move_for_snake(
    state: GameState, snake_id: str, move: str
) -> Tuple[GameState, bool]:
    """
    Applies a move for the specified snake only. Used for local heuristics.
    Opponents remain stationary which is acceptable for localized scoring heuristics.
    """
    new_state = state.copy()
    snake = new_state.snakes[snake_id]
    delta = direction_to_delta(move)
    new_head = add_points(snake.head, delta)
    will_eat = new_head in new_state.food
    snake.body.insert(0, new_head)
    if will_eat:
        new_state.food.discard(new_head)
        snake.health = FOOD_HEALTH
    else:
        # Tail slip is naturally handled by popping the last segment.
        snake.body.pop()
        snake.health = max(0, snake.health - 1)
    return new_state, will_eat


def simulate_turn(state: GameState, move_map: Dict[str, str]) -> GameState:
    """
    Applies a collection of moves (including our own) and returns the new game state.
    """
    new_state = state.copy()
    original_snakes = {sid: s.copy() for sid, s in state.snakes.items()}
    planned: Dict[str, Dict] = {}

    for snake in state.active_snakes:
        move = move_map.get(snake.id)
        if snake.eliminated or move is None:
            # If a snake has no move it dies this turn.
            snake_ref = new_state.snakes[snake.id]
            snake_ref.eliminated = True
            snake_ref.death_cause = "no-move"
            continue
        delta = direction_to_delta(move)
        new_head = add_points(snake.head, delta)
        will_eat = new_head in state.food
        planned[snake.id] = {
            "new_head": new_head,
            "will_eat": will_eat,
            "move": move,
        }

    # Pre-compute body occupancy ignoring tails that will move away.
    body_footprint: Dict[str, set[Point]] = {}
    for sid, snake in original_snakes.items():
        plan = planned.get(sid)
        if plan and plan["will_eat"]:
            segments = set(snake.body)
        else:
            segments = set(snake.body[:-1])
        body_footprint[sid] = segments

    eliminated: Dict[str, str] = {}

    # Check wall and body collisions.
    for sid, plan in planned.items():
        snake = original_snakes[sid]
        new_head = plan["new_head"]
        if not state.inside(new_head):
            eliminated[sid] = "wall"
            continue
        for other_id, footprint in body_footprint.items():
            if other_id == sid:
                continue
            if new_head in footprint:
                eliminated[sid] = "body"
                break
        if eliminated.get(sid):
            continue
        # Self body collision (excluding tail when not eating).
        own_segments = body_footprint[sid]
        if new_head in own_segments:
            eliminated[sid] = "self"

    # Handle head-to-head collisions.
    heads_to_snakes: Dict[Point, List[str]] = defaultdict(list)
    for sid, plan in planned.items():
        if sid in eliminated:
            continue
        heads_to_snakes[plan["new_head"]].append(sid)

    for point, participants in heads_to_snakes.items():
        if len(participants) <= 1:
            continue
        lengths = [original_snakes[sid].length for sid in participants]
        max_length = max(lengths)
        survivors = [
            sid for sid in participants if original_snakes[sid].length == max_length
        ]
        if len(survivors) > 1:
            for sid in participants:
                eliminated[sid] = "head-to-head"
        else:
            winner = survivors[0]
            for sid in participants:
                if sid != winner:
                    eliminated[sid] = "head-to-head"

    # Apply transitions.
    new_food = set(state.food)
    for sid, snake in new_state.snakes.items():
        plan = planned.get(sid)
        if sid in eliminated:
            snake.eliminated = True
            snake.death_cause = eliminated[sid]
            continue
        if not plan:
            snake.eliminated = True
            snake.death_cause = "no-move"
            continue
        new_head = plan["new_head"]
        will_eat = plan["will_eat"]
        prior = original_snakes[sid]

        new_health = prior.health - 1
        if new_head in state.hazards:
            new_health -= HAZARD_DAMAGE
        if will_eat:
            new_health = FOOD_HEALTH
        snake.health = max(0, new_health)

        if will_eat:
            snake.body = [new_head] + prior.body
            new_food.discard(new_head)
        else:
            snake.body = [new_head] + prior.body[:-1]

        if snake.health <= 0:
            snake.eliminated = True
            snake.death_cause = "starvation"

    new_state.food = new_food
    new_state.turn = state.turn + 1
    return new_state
