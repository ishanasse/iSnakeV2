from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Weights:
    area: float = 3.5
    food: float = 45.0
    corridor: float = 3.0
    hazard: float = 0.0
    h2h: float = 4.0
    center: float = 0.08
    degree: float = 0.9
    longer: float = 5.0
    stability: float = 2.0
    voronoi: float = 0.8


LOW_HEALTH = int(os.environ.get("LOW_HEALTH", 35))
W_AREA = float(os.environ.get("W_AREA", 3.5))
W_FOOD = float(os.environ.get("W_FOOD", 45.0))
W_CORRIDOR = float(os.environ.get("W_CORRIDOR", 3.0))
W_HAZARD = float(os.environ.get("W_HAZARD", 0.0))
W_H2H = float(os.environ.get("W_H2H", 4.0))
W_CENTER = float(os.environ.get("W_CENTER", 0.08))
W_DEGREE = float(os.environ.get("W_DEGREE", 0.9))
W_LONGER = float(os.environ.get("W_LONGER", 5.0))
W_STABILITY = float(os.environ.get("W_STABILITY", 2.0))
W_VORONOI = float(os.environ.get("W_VORONOI", 0.8))
TOPK_RANDOM = int(os.environ.get("TOPK_RANDOM", 2))
TIE_MARGIN = float(os.environ.get("TIE_MARGIN", 0.02))
SEED = int(os.environ.get("SEED", 42))
FALLBACK_MS = int(os.environ.get("FALLBACK_MS", 250))
LOOKAHEAD_DEPTH = int(os.environ.get("LOOKAHEAD_DEPTH", 2))
BEAM_WIDTH = int(os.environ.get("BEAM_WIDTH", 3))
OPP_TOPK = int(os.environ.get("OPP_TOPK", 2))


def get_weights() -> Weights:
    """
    Returns a weight configuration using environment overrides when present.
    """
    return Weights(
        area=W_AREA,
        food=W_FOOD,
        corridor=W_CORRIDOR,
        hazard=W_HAZARD,
        h2h=W_H2H,
        center=W_CENTER,
        degree=W_DEGREE,
        longer=W_LONGER,
        stability=W_STABILITY,
        voronoi=W_VORONOI,
    )

