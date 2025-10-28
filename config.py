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


# Core tuning knobs; override via environment variables to experiment without code edits.
LOW_HEALTH = int(os.environ.get("LOW_HEALTH", 35))  # HP threshold that marks us as hungry.
W_AREA = float(os.environ.get("W_AREA", 3.5))  # Weight for accessible space (flood-fill area).
W_FOOD = float(os.environ.get("W_FOOD", 45.0))  # Food incentive when LOW_HEALTH is met.
W_CORRIDOR = float(os.environ.get("W_CORRIDOR", 3.0))  # Penalty for low-degree tunnel positions.
W_HAZARD = float(os.environ.get("W_HAZARD", 0.0))  # Soft cost for spending time in hazards.
W_H2H = float(os.environ.get("W_H2H", 4.0))  # Head-to-head contest emphasis.
W_CENTER = float(os.environ.get("W_CENTER", 0.08))  # Nudges us toward centre control.
W_DEGREE = float(os.environ.get("W_DEGREE", 0.9))  # Rewards keeping multiple safe exits.
W_LONGER = float(os.environ.get("W_LONGER", 5.0))  # Deterrent for proximity to longer snakes.
W_STABILITY = float(os.environ.get("W_STABILITY", 2.0))  # Preference for preserving area over time.
W_VORONOI = float(os.environ.get("W_VORONOI", 0.8))  # Bonus for territory control share.
TOPK_RANDOM = int(os.environ.get("TOPK_RANDOM", 2))  # Candidate count kept for tie randomisation.
TIE_MARGIN = float(os.environ.get("TIE_MARGIN", 0.02))  # Normalised score gap treated as a tie.
SEED = int(os.environ.get("SEED", 42))  # Base deterministic seed (mixed with game state).
FALLBACK_MS = int(os.environ.get("FALLBACK_MS", 250))  # Time budget per move before falling back.
LOOKAHEAD_DEPTH = int(os.environ.get("LOOKAHEAD_DEPTH", 2))  # Beam search ply depth (0-2 supported).
BEAM_WIDTH = int(os.environ.get("BEAM_WIDTH", 3))  # States retained per layer of the beam.
OPP_TOPK = int(os.environ.get("OPP_TOPK", 2))  # Opponent move options considered at each branch.


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
