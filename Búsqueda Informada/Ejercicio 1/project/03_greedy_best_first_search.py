#!/usr/bin/env python3
"""Program 3: greedy best-first search on the Romania map."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from search.cli import make_problem, print_result, search_parser  # noqa: E402
from search.greedy import greedy_best_first_search  # noqa: E402


def main() -> None:
    parser = search_parser("Greedy best-first search: expand lowest h(n).")
    args = parser.parse_args()
    problem, h, label = make_problem(args.start, args.goal)
    result = greedy_best_first_search(problem, h)
    print_result("Greedy best-first search", problem, result, h, label)


if __name__ == "__main__":
    main()
