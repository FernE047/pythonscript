from grafos import Graph
from grafos import get_graph_from_file
from estados import State


class Counter:
    def __init__(self, name: str) -> None:
        self.name = name
        self.count = 0

    def reset(self) -> None:
        self.count = 0

    def increment(self) -> None:
        self.count += 1

    def display(self) -> None:
        print(str(self))

    def __str__(self) -> str:
        return f"\n{self.name.title()} : {self.count}"

class CounterManager:
    def __init__(self) -> None:
        self.counters: dict[str, Counter] = {}

    def create_counter(self, name: str) -> None:
        if name not in self.counters:
            self.counters[name] = Counter(name)

    def increment(self, name: str) -> None:
        if name in self.counters:
            self.counters[name].increment()

    def reset(self, name: str) -> None:
        if name in self.counters:
            self.counters[name].reset()

    def reset_all(self) -> None:
        for counter in self.counters.values():
            counter.reset()

    def display_all(self) -> None:
        for counter in self.counters.values():
            counter.display()

def depth_first_search(state: State, counter_manager: CounterManager, lowest_state: State | None = None) -> State:
    counter_manager.increment("iterations")
    next_states = state.next_states()
    if len(next_states) == 0:
        if lowest_state is None:
            return state
        if state.path_cost < lowest_state.path_cost:
            return state
    for potential_solution in next_states:
        if lowest_state is None:
            lowest_state = depth_first_search(potential_solution, counter_manager, lowest_state)
            continue
        if potential_solution.path_cost < lowest_state.path_cost:
            lowest_state = depth_first_search(potential_solution, counter_manager, lowest_state)
            continue
        counter_manager.increment("heuristic cuts")
    assert lowest_state is not None
    return lowest_state


def breadth_first_search(state: State, counter_manager: CounterManager) -> State:
    counter_manager.increment("iterations")
    lowest_state: State | None = None
    states = [state]
    while states:
        next_states: list[State] = []
        for state in states:
            generated_states = state.next_states()
            if len(generated_states) == 0:
                if lowest_state is None:
                    lowest_state = state
                    continue
                if state.path_cost < lowest_state.path_cost:
                    lowest_state = state
                continue
            for generated_state in generated_states:
                if generated_state not in next_states:
                    next_states.append(generated_state)
        states = next_states.copy()
    assert lowest_state is not None
    return lowest_state

def main() -> None:
    counter_manager = CounterManager()
    counter_manager.create_counter("iterations")
    counter_manager.create_counter("heuristic cuts")
    graph_raw: list[list[float]] = [
        [0, 10, 10, 1, 10],
        [10, 0, 1, 10, 10],
        [1, 10, 0, 10, 10],
        [10, 10, 10, 0, 1],
        [10, 1, 10, 10, 0],
    ]
    graph = Graph(base_graph=graph_raw)
    initial_state = State(graph)
    solution_state = breadth_first_search(initial_state, counter_manager)
    solution_state.show_path()
    graph = Graph(4)
    graph.set_element((0, 1), 1)
    graph.set_element((0, 2), 2)
    graph.set_element((0, 3), 4)
    graph.set_element((1, 2), 2)
    graph.set_element((1, 3), 3)
    graph.set_element((2, 3), 5)
    initial_state = State(graph)
    solution_state = depth_first_search(initial_state, counter_manager)
    counter_manager.display_all()
    counter_manager.reset_all()
    solution_state.show_path()
    for max_nodes in range(1, 23):
        graph = get_graph_from_file("grafo0004.txt", limit=max_nodes)
        initial_state = State(graph)
        solution_state = depth_first_search(initial_state, counter_manager)
        solution_state.show_path()
        counter_manager.display_all()
        counter_manager.reset_all()

if __name__ == "__main__":
    main()