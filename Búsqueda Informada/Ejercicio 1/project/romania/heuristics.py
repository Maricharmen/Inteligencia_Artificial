"""Heuristics for Romania: AIMA straight-line distances, plus Euclidean fallback."""

from __future__ import annotations

import math
from collections.abc import Callable

# Straight-line distance to Bucharest (AIMA Figure 3.22 / Table). Admissible and consistent.
SLD_TO_BUCHAREST: dict[str, int] = {
    "Arad": 366,
    "Bucharest": 0,
    "Craiova": 160,
    "Drobeta": 242,
    "Eforie": 161,
    "Fagaras": 176,
    "Giurgiu": 77,
    "Hirsova": 151,
    "Iasi": 226,
    "Lugoj": 244,
    "Mehadia": 241,
    "Neamt": 234,
    "Oradea": 380,
    "Pitesti": 100,
    "Rimnicu Vilcea": 193,
    "Sibiu": 253,
    "Timisoara": 329,
    "Urziceni": 80,
    "Vaslui": 199,
    "Zerind": 374,
}

# Approximate map coordinates (aima-python). Used when the goal is not Bucharest.
LOCATIONS: dict[str, tuple[float, float]] = {
    "Arad": (91, 492),
    "Bucharest": (400, 327),
    "Craiova": (253, 288),
    "Drobeta": (165, 299),
    "Eforie": (562, 293),
    "Fagaras": (305, 449),
    "Giurgiu": (375, 270),
    "Hirsova": (534, 350),
    "Iasi": (473, 506),
    "Lugoj": (165, 379),
    "Mehadia": (168, 339),
    "Neamt": (406, 537),
    "Oradea": (131, 571),
    "Pitesti": (320, 368),
    "Rimnicu Vilcea": (233, 410),
    "Sibiu": (207, 457),
    "Timisoara": (94, 410),
    "Urziceni": (456, 350),
    "Vaslui": (509, 444),
    "Zerind": (108, 531),
}


def euclidean(a: str, b: str) -> float:
    if a not in LOCATIONS or b not in LOCATIONS:
        raise KeyError(f"no coordinates for {a!r} or {b!r}")
    x1, y1 = LOCATIONS[a]
    x2, y2 = LOCATIONS[b]
    return math.hypot(x1 - x2, y1 - y2)


def heuristic_for(goal: str) -> tuple[Callable[[str], float], str]:
    """Return h(state) and a short label describing which heuristic is used.

    The AIMA table is only defined for Bucharest. Other goals use Euclidean
    distance on the approximate coordinates.
    """
    if goal == "Bucharest":

        def h_sld(state: str) -> float:
            return float(SLD_TO_BUCHAREST[state])

        return h_sld, "straight-line distance to Bucharest (AIMA table)"

    def h_euclid(state: str) -> float:
        return euclidean(state, goal)

    return h_euclid, f"Euclidean distance to {goal} (map coordinates)"
