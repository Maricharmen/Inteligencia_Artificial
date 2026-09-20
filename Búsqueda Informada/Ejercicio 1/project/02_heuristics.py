#!/usr/bin/env python3
"""Program 2: print h(n) for every city (heuristic toward the goal)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from romania.heuristics import heuristic_for  # noqa: E402
from romania.map import romania_map  # noqa: E402
from search.cli import search_parser  # noqa: E402


def main() -> None:
    parser = search_parser("Show heuristic values h(n) toward the goal city.")
    args = parser.parse_args()
    graph = romania_map()
    if not graph.has_city(args.goal):
        raise SystemExit(f"Unknown goal city: {args.goal}")

    h, label = heuristic_for(args.goal)
    rows = sorted(((h(city), city) for city in graph.cities()))
    print(f"Heuristic: {label}")
    print()
    print("  h(n)  city")
    for value, city in rows:
        marker = "  <- start" if city == args.start else ("  <- goal" if city == args.goal else "")
        print(f"  {value:5.0f}  {city}{marker}")


if __name__ == "__main__":
    main()
