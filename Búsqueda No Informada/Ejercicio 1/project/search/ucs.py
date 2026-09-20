"""Uniform-cost search (AIMA Figure 3.14). Optimal for non-negative road costs."""

from __future__ import annotations

import heapq

from romania.node import Node
from romania.problem import RouteFindingProblem
from search.result import FAILURE, SUCCESS, SearchResult


def uniform_cost_search(problem: RouteFindingProblem) -> SearchResult:
    """Finds a cheapest path in km. Goal test is applied when a node is expanded."""
    node = Node(problem.start)
    frontier: list[tuple[float, int, Node]] = []
    counter = 0
    heapq.heappush(frontier, (node.path_cost, counter, node))
    best_cost = {node.state: 0.0}
    explored: set[str] = set()
    expanded = 0
    generated = 1
    max_frontier = 1

    while frontier:
        _cost, _i, node = heapq.heappop(frontier)
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
            if s in explored:
                continue
            if s not in best_cost or child.path_cost < best_cost[s]:
                best_cost[s] = child.path_cost
                counter += 1
                heapq.heappush(frontier, (child.path_cost, counter, child))
                max_frontier = max(max_frontier, len(frontier))

    return SearchResult(
        FAILURE,
        nodes_expanded=expanded,
        nodes_generated=generated,
        max_frontier=max_frontier,
    )
