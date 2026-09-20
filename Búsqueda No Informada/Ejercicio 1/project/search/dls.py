"""Depth-limited search (AIMA Figure 3.17)."""

from __future__ import annotations

from romania.node import Node
from romania.problem import RouteFindingProblem
from search.result import CUTOFF, FAILURE, SUCCESS, SearchResult

_CUTOFF = object()
_FAILURE = object()


def depth_limited_search(problem: RouteFindingProblem, limit: int) -> SearchResult:
    """DFS that never expands a node deeper than `limit`.

    States already on the current path are skipped so cycles cannot loop
    until the depth budget is wasted.
    """
    if limit < 0:
        raise ValueError("limit must be >= 0")

    stats = {"expanded": 0, "generated": 1, "max_frontier": 1}
    result = _recursive_dls(Node(problem.start), problem, limit, stats)
    if result is _CUTOFF:
        return SearchResult(
            CUTOFF,
            nodes_expanded=stats["expanded"],
            nodes_generated=stats["generated"],
            max_frontier=stats["max_frontier"],
            extra=f"limit={limit}",
        )
    if result is _FAILURE:
        return SearchResult(
            FAILURE,
            nodes_expanded=stats["expanded"],
            nodes_generated=stats["generated"],
            max_frontier=stats["max_frontier"],
            extra=f"limit={limit}",
        )
    return SearchResult(
        SUCCESS,
        result,
        nodes_expanded=stats["expanded"],
        nodes_generated=stats["generated"],
        max_frontier=stats["max_frontier"],
        extra=f"limit={limit}",
    )


def _recursive_dls(
    node: Node,
    problem: RouteFindingProblem,
    limit: int,
    stats: dict[str, int],
) -> Node | object:
    if problem.is_goal(node.state):
        return node
    if limit == 0:
        return _CUTOFF

    stats["expanded"] += 1
    cutoff_occurred = False
    on_path = node.path_states()
    children = node.expand(problem)
    stats["max_frontier"] = max(stats["max_frontier"], node.depth + 1 + len(children))

    for child in children:
        stats["generated"] += 1
        if child.state in on_path:
            continue
        result = _recursive_dls(child, problem, limit - 1, stats)
        if result is _CUTOFF:
            cutoff_occurred = True
        elif result is not _FAILURE:
            return result
    return _CUTOFF if cutoff_occurred else _FAILURE
