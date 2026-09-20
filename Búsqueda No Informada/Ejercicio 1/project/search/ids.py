"""Iterative deepening search (AIMA Figure 3.18)."""

from __future__ import annotations

from romania.problem import RouteFindingProblem
from search.dls import depth_limited_search
from search.result import CUTOFF, SearchResult


def iterative_deepening_search(
    problem: RouteFindingProblem,
    max_limit: int | None = None,
) -> SearchResult:
    """Calls depth-limited search with limit = 0, 1, 2, ... until success or failure.

    Completeness and hop-optimality match BFS; memory stays closer to DFS.
    """
    cap = max_limit if max_limit is not None else len(problem.graph.cities())
    expanded = 0
    generated = 0
    max_frontier = 0

    for limit in range(0, cap + 1):
        result = depth_limited_search(problem, limit)
        expanded += result.nodes_expanded
        generated += result.nodes_generated
        max_frontier = max(max_frontier, result.max_frontier)
        if result.status != CUTOFF:
            result.nodes_expanded = expanded
            result.nodes_generated = generated
            result.max_frontier = max_frontier
            result.extra = f"last_limit={limit}"
            return result

    return SearchResult(
        CUTOFF,
        nodes_expanded=expanded,
        nodes_generated=generated,
        max_frontier=max_frontier,
        extra=f"last_limit={cap}",
    )
