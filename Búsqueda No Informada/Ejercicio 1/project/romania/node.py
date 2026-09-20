"""Search tree node (AIMA Figure 3.6)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from romania.problem import RouteFindingProblem


@dataclass
class Node:
    state: str
    parent: Node | None = None
    action: str | None = None
    path_cost: float = 0.0
    depth: int = 0

    def path(self) -> list[str]:
        """Cities from the root to this node."""
        node: Node | None = self
        cities: list[str] = []
        while node is not None:
            cities.append(node.state)
            node = node.parent
        cities.reverse()
        return cities

    def path_states(self) -> set[str]:
        return set(self.path())

    def expand(self, problem: RouteFindingProblem) -> list[Node]:
        children = []
        for action in problem.actions(self.state):
            children.append(child_node(problem, self, action))
        return children


def child_node(problem: RouteFindingProblem, parent: Node, action: str) -> Node:
    next_state = problem.result(parent.state, action)
    return Node(
        state=next_state,
        parent=parent,
        action=action,
        path_cost=parent.path_cost + problem.step_cost(parent.state, action),
        depth=parent.depth + 1,
    )
