#!/usr/bin/env python3
"""Program 2d: depth-limited search on the Romania map."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from search.cli import make_problem, print_result, search_parser  # noqa: E402
from search.dls import depth_limited_search  # noqa: E402


def main() -> None:
    parser = search_parser("Depth-limited search.", with_limit=True)
    args = parser.parse_args()
    problem = make_problem(args.start, args.goal)
    result = depth_limited_search(problem, args.limit)
    print_result("Depth-limited search", problem, result)


if __name__ == "__main__":
    main()
