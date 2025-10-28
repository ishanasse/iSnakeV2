from __future__ import annotations

import hashlib
import random
from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple

from config import SEED

Point = Tuple[int, int]


def _to_point(coord: Dict[str, int]) -> Point:
    return int(coord["x"]), int(coord["y"])


@dataclass(slots=True)
class Snake:
    id: str
    name: str
    health: int
    body: List[Point]
    latency: str = ""
    shout: str = ""
    squad: str = ""
    eliminated: bool = False
    death_cause: Optional[str] = None

    @property
    def head(self) -> Point:
        return self.body[0]

    @property
    def tail(self) -> Point:
        return self.body[-1]

    @property
    def length(self) -> int:
        return len(self.body)

    def copy(self) -> "Snake":
        return Snake(
            id=self.id,
            name=self.name,
            health=self.health,
            body=list(self.body),
            latency=self.latency,
            shout=self.shout,
            squad=self.squad,
            eliminated=self.eliminated,
            death_cause=self.death_cause,
        )


@dataclass(slots=True)
class GameState:
    width: int
    height: int
    turn: int
    snakes: Dict[str, Snake]
    me_id: str
    food: Set[Point] = field(default_factory=set)
    hazards: Set[Point] = field(default_factory=set)
    rng: random.Random = field(default_factory=random.Random)

    @classmethod
    def from_json(cls, data: Dict) -> "GameState":
        board = data["board"]
        width = int(board["width"])
        height = int(board["height"])
        snakes = {
            snake_data["id"]: Snake(
                id=snake_data["id"],
                name=snake_data.get("name", snake_data["id"]),
                health=int(snake_data["health"]),
                body=[_to_point(p) for p in snake_data["body"]],
                latency=snake_data.get("latency", ""),
                shout=snake_data.get("shout", ""),
                squad=snake_data.get("squad", ""),
                eliminated=snake_data.get("eliminated", False),
            )
            for snake_data in board["snakes"]
        }
        you = data["you"]["id"]
        food = {_to_point(p) for p in board.get("food", [])}
        hazards = {_to_point(p) for p in board.get("hazards", [])}
        turn = int(data.get("turn", 0))
        game_id = data.get("game", {}).get("id", "")
        seed_material = f"{SEED}|{game_id}|{turn}"
        seed_int = int(hashlib.sha1(seed_material.encode("utf-8")).hexdigest(), 16) & 0x7FFFFFFF
        rng = random.Random(seed_int)
        return cls(width, height, turn, snakes, you, food, hazards, rng)

    def copy(self) -> "GameState":
        snakes_copy = {sid: snake.copy() for sid, snake in self.snakes.items()}
        new_state = GameState(
            width=self.width,
            height=self.height,
            turn=self.turn,
            snakes=snakes_copy,
            me_id=self.me_id,
            food=set(self.food),
            hazards=set(self.hazards),
            rng=random.Random(),
        )
        new_state.rng.setstate(self.rng.getstate())
        return new_state

    @property
    def me(self) -> Snake:
        return self.snakes[self.me_id]

    @property
    def opponents(self) -> List[Snake]:
        return [s for sid, s in self.snakes.items() if sid != self.me_id and not s.eliminated]

    @property
    def active_snakes(self) -> List[Snake]:
        return [s for s in self.snakes.values() if not s.eliminated]

    def occupied_points(self, exclude: Optional[Sequence[Point]] = None) -> List[Point]:
        exclude_set = set(exclude or [])
        tiles: List[Point] = []
        for snake in self.active_snakes:
            tiles.extend([segment for segment in snake.body if segment not in exclude_set])
        return tiles

    def point_is_hazard(self, point: Point) -> bool:
        return point in self.hazards

    def inside(self, point: Point) -> bool:
        x, y = point
        return 0 <= x < self.width and 0 <= y < self.height

    def is_food(self, point: Point) -> bool:
        return point in self.food
