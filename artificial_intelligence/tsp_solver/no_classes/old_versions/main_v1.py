from time import time
from typing import Literal, TypedDict

GraphData = list[list[float]]
VertexData = tuple[float, float]


GRAPH_EXAMPLE_1: GraphData = [
    [0, 10, 10, 1, 10],
    [10, 0, 1, 10, 10],
    [1, 10, 0, 10, 10],
    [10, 10, 10, 0, 1],
    [10, 1, 10, 10, 0],
]
GRAPH_EXAMPLE_2: GraphData = [[0, 1, 2, 4], [1, 0, 2, 3], [2, 2, 0, 5], [4, 3, 5, 0]]
MAX_NODES = 22


class StateData(TypedDict):
    path_cost: float
    path: list[int]
    graph: GraphData


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


def print_elapsed_time(seconds: float) -> None:
    if seconds < 0:
        seconds = -seconds
        sign = "-"
    else:
        sign = ""
    total_ms = int(round(seconds * 1000))
    ms = total_ms % 1000
    total_s = total_ms // 1000
    s = total_s % 60
    total_min = total_s // 60
    m = total_min % 60
    total_h = total_min // 60
    h = total_h % 24
    d = total_h // 24
    parts: list[str] = []

    def add(value: int, singular: str, plural: str) -> None:
        if value:
            parts.append(f"{value} {singular if value == 1 else plural}")

    add(d, "day", "days")
    add(h, "hour", "hours")
    add(m, "minute", "minutes")
    add(s, "second", "seconds")
    if ms or not parts:
        parts.append(f"{ms} millisecond" if ms == 1 else f"{ms} milliseconds")
    print(f"{sign}{', '.join(parts)}")


def get_graph_from_file(filename: str, nodes_limit: int | None = None) -> GraphData:
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.read().splitlines()
        vertices: list[VertexData] = []
        index = 0
        if nodes_limit:
            index = 1
        for line in lines:
            line = line.strip()
            if not line:
                break
            if nodes_limit:
                if index == nodes_limit:
                    break
            coordinates = line.split()
            x_str = coordinates[2]
            y_str = coordinates[1]
            vertices.append((float(x_str), float(y_str)))
            if nodes_limit:
                index += 1
        graph = [[0.0 for _ in vertices] for _ in vertices]
        for x, source in enumerate(vertices):
            for y, destination in enumerate(vertices):
                distance_x = abs(destination[0] - source[0])
                distance_y = abs(destination[1] - source[1])
                distance = (distance_x**2 + distance_y**2) ** 0.5
                graph[x][y] = distance
    return graph


def generate_next_states(state: StateData) -> list[StateData]:
    graph = state["graph"]
    next_states: list[StateData] = []
    for index in range(len(graph)):
        if index not in state["path"]:
            next_states.append(build_path(state, index))
    return next_states


def build_path(state: StateData, destination: int) -> StateData:
    cost = state["path_cost"]
    graph = state["graph"]
    if state["path"]:
        cost += graph[state["path"][-1]][destination]
    path = state["path"] + [destination]
    return {"path_cost": cost, "path": path, "graph": graph}


def print_solution_summary(
    duration: float, solution_state: StateData, counter_manager: CounterManager
) -> None:
    graph = solution_state["graph"]
    state: StateData = {"path_cost": 0, "path": [], "graph": graph}
    for line in graph:
        print(
            " ".join([" " * (3 - len(str(element))) + str(element) for element in line])
        )
    print()
    for destination in solution_state["path"]:
        state = build_path(state, destination)
        print(f"caminho : {state['path']}")
        print(f"custo   : {state['path_cost']}\n")
    counter_manager.display_all()
    print_elapsed_time(duration)
    print("\n\n\n")


def depth_first_search(
    state: StateData,
    counter_manager: CounterManager,
    best_state: StateData | None = None,
) -> StateData:
    counter_manager.increment("iterations")
    next_states = generate_next_states(state)
    if len(next_states) == 0:
        if best_state is None:
            return state
        if state["path_cost"] < best_state["path_cost"]:
            return state
    for next_state in next_states:
        if best_state is None:
            best_state = depth_first_search(next_state, counter_manager, best_state)
            continue
        if next_state["path_cost"] < best_state["path_cost"]:
            best_state = depth_first_search(next_state, counter_manager, best_state)
            continue
        counter_manager.increment("heuristic cuts")
    assert best_state is not None
    return best_state


def breadth_first_search(
    state: StateData, counter_manager: CounterManager
) -> StateData:
    counter_manager.increment("iterations")
    best_state: StateData | None = None
    states = [state]
    while states:
        next_states: list[StateData] = []
        for state in states:
            next_generation = generate_next_states(state)
            if len(next_generation) == 0:
                if best_state is None:
                    best_state = state
                    continue
                if state["path_cost"] < best_state["path_cost"]:
                    best_state = state
                continue
            for generated_state in next_generation:
                if generated_state not in next_states:
                    next_states.append(generated_state)
        states = next_states.copy()
    assert best_state is not None
    return best_state


def solve(graph: GraphData, mode: Literal[0, 1] = 1) -> None:
    counter_manager = CounterManager()
    counter_manager.create_counter("iterations")
    counter_manager.create_counter("heuristic cuts")
    start_time = time()
    initial_state: StateData = {"path_cost": 0, "path": [], "graph": graph}
    if mode:
        solution_state = depth_first_search(initial_state, counter_manager)
    else:
        solution_state = breadth_first_search(initial_state, counter_manager)
    end_time = time()
    elapsed_time = end_time - start_time
    print_solution_summary(elapsed_time, solution_state, counter_manager)


def main() -> None:
    graph: GraphData = GRAPH_EXAMPLE_1
    solve(graph, 0)
    graph = GRAPH_EXAMPLE_2
    solve(graph, 1)
    for node_limit in range(1, MAX_NODES + 1):
        graph = get_graph_from_file("grafo0004.txt", nodes_limit=node_limit)
        solve(graph, 1)


if __name__ == "__main__":
    main()
