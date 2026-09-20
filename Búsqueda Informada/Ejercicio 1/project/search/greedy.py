"""Greedy best-first search (AIMA Figure 3.23). Expands the node with lowest h(n)."""

from __future__ import annotations

import heapq
from collections.abc import Callable

from romania.node import Node
from romania.problem import RouteFindingProblem
from search.result import FAILURE, SUCCESS, SearchResult


def greedy_best_first_search(
    problem: RouteFindingProblem,
    h: Callable[[str], float],
) -> SearchResult:
    """Not optimal. Follows the heuristic and ignores the path cost g(n)."""
    node = Node(problem.start)
    frontier: list[tuple[float, int, Node]] = []
    counter = 0
    heapq.heappush(frontier, (h(node.state), counter, node))
    frontier_states = {node.state}
    explored: set[str] = set()
    expanded = 0
    generated = 1
    max_frontier = 1

    while frontier:
        _h, _i, node = heapq.heappop(frontier)
        frontier_states.discard(node.state)
        if node.state in explored:
            continue
        if problem.is_goal(node.state):
            return SearchResult(
                SUCCESS,
                node,
                nodes_expanded=expanded,
                nodes_generated=generated,
                max_frontier=max_frontier,
            )

        explored.add(node.state)
        expanded += 1
        for child in node.expand(problem):
            generated += 1
            s = child.state
            if s in explored or s in frontier_states:
                continue
            counter += 1
            heapq.heappush(frontier, (h(s), counter, child))
            frontier_states.add(s)
            max_frontier = max(max_frontier, len(frontier))

    return SearchResult(
        FAILURE,
        nodes_expanded=expanded,
        nodes_generated=generated,
        max_frontier=max_frontier,
    )
