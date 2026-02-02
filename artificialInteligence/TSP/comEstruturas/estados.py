from typing import Any
from artificialInteligence.TSP.comEstruturas.grafos import Graph


class State:
    def __init__(
        self,
        graph: Graph,
        current_path: list[int] | None = None,
        total_cost: float | int | None = None,
    ):
        self.graph = graph
        if current_path is None:
            self.path = []
        else:
            self.path = current_path
        if total_cost is None:
            self.path_cost = 0.0
        else:
            self.path_cost = float(total_cost)

    def next_states(self) -> list["State"]:
        children: list["State"] = []
        for index in range(len(self.graph)):
            if index not in self.path:
                children.append(self.apply_move(index))
        return children

    def apply_move(self, move: int) -> "State":
        total_cost = self.path_cost
        if self.path:
            total_cost += self.graph.get_element((self.path[-1], move))
        path_done = self.path + [move]
        return State(self.graph, path_done, total_cost)

    def show_path(self) -> "State":
        # show the full path step by step
        state = State(self.graph)
        self.graph.show()
        print()
        print(str(state), end="\n\n")
        for move in self.path[1:]:
            state = state.apply_move(move)
            print(str(state), end="\n\n")
        print("\n\n\n\n\n\n")
        return state

    def __str__(self) -> str:
        return f"path : {self.path}\ncost : {self.path_cost}"

    def __eq__(self, other_state: Any) -> bool:
        if not isinstance(other_state, State):
            return False
        if self.path_cost != other_state.path_cost:
            return False
        for node in self.path:
            if node not in other_state.path:
                return False
        return True
