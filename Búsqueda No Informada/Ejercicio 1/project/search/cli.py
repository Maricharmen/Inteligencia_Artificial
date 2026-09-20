"""Shared CLI and result printing for the six main programs."""

from __future__ import annotations

import argparse

from romania.map import romania_map
from romania.problem import RouteFindingProblem
from search.result import SearchResult

DEFAULT_FROM = "Arad"
DEFAULT_TO = "Bucharest"


def search_parser(description: str, *, with_limit: bool = False) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--from-city", dest="start", default=DEFAULT_FROM, help="Start city")
    parser.add_argument("--to", dest="goal", default=DEFAULT_TO, help="Goal city")
    if with_limit:
        parser.add_argument(
            "--limit",
            type=int,
            default=3,
            help="Depth limit (try 2 for cutoff, 3 to reach Bucharest via Fagaras)",
        )
    return parser


def make_problem(start: str, goal: str) -> RouteFindingProblem:
    return RouteFindingProblem(romania_map(), start, goal)


def print_result(name: str, problem: RouteFindingProblem, result: SearchResult) -> None:
    print(f"Algorithm: {name}")
    print(f"Problem:   {problem.start} → {problem.goal}")
    print(f"Status:    {result.status}")
    if result.extra:
        print(f"Detail:    {result.extra}")
    if result.node is not None:
        print(f"Path:      {' → '.join(result.path)}")
        print(f"Depth:     {result.depth} roads")
        print(f"Cost:      {result.cost:.0f} km")
    print(f"Expanded:  {result.nodes_expanded} nodes")
    print(f"Generated: {result.nodes_generated} nodes")
    print(f"Frontier:  max size {result.max_frontier}")
