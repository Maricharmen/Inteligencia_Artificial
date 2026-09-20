#!/usr/bin/env python3
"""Program 1: print the Romania road map from AIMA Figure 3.2."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from romania.map import romania_map  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Show the AIMA Romania road map.")
    parser.add_argument(
        "--from-city",
        dest="city",
        default=None,
        help="If set, print only this city's neighbors",
    )
    args = parser.parse_args()
    graph = romania_map()
    cities = graph.cities()

    print("Romania road map (AIMA Figure 3.2)")
    print(f"Cities: {len(cities)}   Roads: {graph.edge_count()}")
    print()

    if args.city:
        if not graph.has_city(args.city):
            raise SystemExit(f"Unknown city: {args.city}\nKnown: {', '.join(cities)}")
        _print_city(graph, args.city)
        return

    for city in cities:
        _print_city(graph, city)


def _print_city(graph, city: str) -> None:
    roads = ", ".join(f"{nbr} {km} km" for nbr, km in graph.neighbors(city))
    print(f"  {city}: {roads}")


if __name__ == "__main__":
    main()
