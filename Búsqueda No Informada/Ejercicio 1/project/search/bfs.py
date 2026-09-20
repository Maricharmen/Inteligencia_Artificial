"""Breadth-first search (AIMA Figure 3.11). Graph search, FIFO frontier."""

from __future__ import annotations

from collections import deque

from romania.node import Node
from romania.problem import RouteFindingProblem
from search.result import FAILURE, SUCCESS, SearchResult


def breadth_first_search(problem: RouteFindingProblem) -> SearchResult:
    """Finds a path with the fewest roads (not necessarily the fewest km)."""
    node = Node(problem.start)
    if problem.is_goal(node.state):
        return SearchResult(SUCCESS, node, nodes_generated=1)

    frontier: deque[Node] = deque([node])
    frontier_states = {node.state}
    explored: set[str] = set()
    expanded = 0
    generated = 1
    max_frontier = 1

    while frontier:
        node = frontier.popleft()
        frontier_states.remove(node.state)
        explored.add(node.state)
        expanded += 1

        for child in node.expand(problem):
            generated += 1
            s = child.state
            if s in explored or s in frontier_states:
                continue
            if problem.is_goal(s):
                return SearchResult(
                    SUCCESS,
                    child,
                    nodes_expanded=expanded,
                    nodes_generated=generated,
                    max_frontier=max_frontier,
                )
            frontier.append(child)
            frontier_states.add(s)
            max_frontier = max(max_frontier, len(frontier))

    return SearchResult(
        FAILURE,
        nodes_expanded=expanded,
        nodes_generated=generated,
        max_frontier=max_frontier,
    )
