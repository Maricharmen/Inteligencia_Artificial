"""Shared CLI and result printing."""

from __future__ import annotations

import argparse
from collections.abc import Callable

from romania.heuristics import heuristic_for
from romania.map import romania_map
from romania.node import Node
from romania.problem import RouteFindingProblem
from search.result import SearchResult

DEFAULT_FROM = "Arad"
DEFAULT_TO = "Bucharest"


def search_parser(description: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--from-city", dest="start", default=DEFAULT_FROM, help="Start city")
    parser.add_argument("--to", dest="goal", default=DEFAULT_TO, help="Goal city")
    return parser


def make_problem(start: str, goal: str) -> tuple[RouteFindingProblem, Callable[[str], float], str]:
    problem = RouteFindingProblem(romania_map(), start, goal)
    h, label = heuristic_for(goal)
    return problem, h, label


def print_result(
    name: str,
    problem: RouteFindingProblem,
    result: SearchResult,
    h: Callable[[str], float],
    h_label: str,
) -> None:
    print(f"Algorithm: {name}")
    print(f"Problem:   {problem.start} → {problem.goal}")
    print(f"Heuristic: {h_label}")
    print(f"Status:    {result.status}")
    if result.extra:
        print(f"Detail:    {result.extra}")
    if result.node is not None:
        print(f"Path:      {' → '.join(result.path)}")
        print(f"Depth:     {result.depth} roads")
        print(f"Cost:      {result.cost:.0f} km")
        print()
        print("  city                  g     h     f")
        for city, g, hv, f in _g_h_f_along(result.node, h):
            print(f"  {city:<20} {g:5.0f} {hv:5.0f} {f:5.0f}")
    print()
    print(f"Expanded:  {result.nodes_expanded} nodes")
    print(f"Generated: {result.nodes_generated} nodes")
    print(f"Frontier:  max size {result.max_frontier}")


def _g_h_f_along(node: Node, h: Callable[[str], float]) -> list[tuple[str, float, float, float]]:
    rows = []
    chain: list[Node] = []
    cur: Node | None = node
    while cur is not None:
        chain.append(cur)
        cur = cur.parent
    chain.reverse()
    for n in chain:
        hv = h(n.state)
        rows.append((n.state, n.path_cost, hv, n.path_cost + hv))
    return rows
