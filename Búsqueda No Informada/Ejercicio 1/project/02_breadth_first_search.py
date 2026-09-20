#!/usr/bin/env python3
"""Program 2a: breadth-first search on the Romania map."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from search.bfs import breadth_first_search  # noqa: E402
from search.cli import make_problem, print_result, search_parser  # noqa: E402


def main() -> None:
    parser = search_parser("Breadth-first search: fewest roads, not fewest km.")
    args = parser.parse_args()
    problem = make_problem(args.start, args.goal)
    result = breadth_first_search(problem)
    print_result("Breadth-first search", problem, result)


if __name__ == "__main__":
    main()
