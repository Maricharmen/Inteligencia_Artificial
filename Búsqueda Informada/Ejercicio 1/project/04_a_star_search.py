#!/usr/bin/env python3
"""Program 4: A* search on the Romania map."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from search.astar import a_star_search  # noqa: E402
from search.cli import make_problem, print_result, search_parser  # noqa: E402


def main() -> None:
    parser = search_parser("A* search: expand lowest f(n) = g(n) + h(n).")
    args = parser.parse_args()
    problem, h, label = make_problem(args.start, args.goal)
    result = a_star_search(problem, h)
    print_result("A* search", problem, result, h, label)


if __name__ == "__main__":
    main()
