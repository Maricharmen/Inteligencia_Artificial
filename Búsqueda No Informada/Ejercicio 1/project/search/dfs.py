"""Depth-first search. Graph search with a LIFO frontier (AIMA ch. 3)."""

from __future__ import annotations

from romania.node import Node
from romania.problem import RouteFindingProblem
from search.result import FAILURE, SUCCESS, SearchResult


def depth_first_search(problem: RouteFindingProblem) -> SearchResult:
    """Not optimal. An explored set is used so Romania's cycles do not loop forever."""
    node = Node(problem.start)
    if problem.is_goal(node.state):
        return SearchResult(SUCCESS, node, nodes_generated=1)

    frontier: list[Node] = [node]
    frontier_states = {node.state}
    explored: set[str] = set()
    expanded = 0
    generated = 1
    max_frontier = 1

    while frontier:
        node = frontier.pop()
        frontier_states.remove(node.state)
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
        # Push alphabetical neighbors last-to-first so the first neighbor is tried first.
        children = node.expand(problem)
        for child in reversed(children):
            generated += 1
            s = child.state
            if s in explored or s in frontier_states:
                continue
            frontier.append(child)
            frontier_states.add(s)
        max_frontier = max(max_frontier, len(frontier))

    return SearchResult(
        FAILURE,
        nodes_expanded=expanded,
        nodes_generated=generated,
        max_frontier=max_frontier,
    )
