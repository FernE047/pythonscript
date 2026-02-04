from time import time
from typing import Literal

GraphData = list[list[float]]
VertexData = tuple[float, float]


class State:
    def __init__(
        self, graph: GraphData, path: list[int] | None = None, path_cost: float = 0.0
    ) -> None:
        self.path_cost = path_cost
        self.path = path if path is not None else []
        self.graph = graph

    def generate_next_states(self) -> list["State"]:
        next_states: list["State"] = []
        for index in range(len(self.graph)):
            if not self.is_in_path(index):
                next_states.append(self.build_path(index))
        return next_states

    def build_path(self, destination: int) -> "State":
        cost = self.path_cost
        graph = self.graph
        if self.path:
            cost += graph[self.path[-1]][destination]
        path = self.path + [destination]
        return State(graph=graph, path=path, path_cost=cost)

    def walk_path(self) -> None:
        state = State(graph=self.graph)
        for destination in self.path:
            state = state.build_path(destination)
            print(f"Path : {state.path}\nCost : {state.path_cost}\n")

    def is_path_filled(self) -> bool:
        return len(self.path) == len(self.graph)

    def is_in_path(self, vertex: int) -> bool:
        return vertex in self.path

    def __lt__(self, other: "State") -> bool:
        return self.path_cost < other.path_cost

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, State):
            return NotImplemented
        return (
            self.path_cost == other.path_cost
            and self.path == other.path
            and self.graph == other.graph
        )

    def __gt__(self, other: "State") -> bool:
        return self.path_cost > other.path_cost

    def __str__(self) -> str:
        text = ""
        for row in self.graph:
            text += (
                " ".join(
                    [" " * (3 - len(str(element))) + str(element) for element in row]
                )
                + "\n"
            )
        return text


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
    print(sign + ", ".join(parts))


def get_graph_from_file(filename: str, nodes_limit: int | None = None) -> GraphData:
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.read().splitlines()
        vertexes: list[VertexData] = []
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
            vertexes.append((float(x_str), float(y_str)))
            if nodes_limit:
                index += 1
        graph = [[0.0 for _ in vertexes] for _ in vertexes]
        for x, source in enumerate(vertexes):
            for y, destination in enumerate(vertexes):
                distance_x = abs(destination[0] - source[0])
                distance_y = abs(destination[1] - source[1])
                distance = (distance_x**2 + distance_y**2) ** 0.5
                graph[x][y] = distance
    return graph


def print_solution_summary(
    duration: float, counter_manager: CounterManager, solution_state: State
) -> None:
    print(str(solution_state))
    print()
    solution_state.walk_path()
    counter_manager.display_all()
    print_elapsed_time(duration)
    print("\n\n\n")


def depth_first_search(
    state: State, counter_manager: CounterManager, best_state: State | None = None
) -> State:
    if state.is_path_filled():
        if best_state is None:
            return state
        if state < best_state:
            return state
        return best_state
    counter_manager.increment("iterations")
    for index in range(len(state.graph)):
        if state.is_in_path(index):
            continue
        next_state = state.build_path(index)
        if best_state is None:
            best_state = depth_first_search(next_state, counter_manager, best_state)
            continue
        if next_state < best_state:
            best_state = depth_first_search(next_state, counter_manager, best_state)
            continue
        counter_manager.increment("heuristic cuts")
    assert best_state is not None
    return best_state


def breadth_first_search(state: State, counter_manager: CounterManager) -> State:
    counter_manager.increment("iterations")
    best_state: State | None = None
    states = [state]
    while states:
        next_states: list[State] = []
        for state in states:
            next_generation = state.generate_next_states()
            if len(next_generation) == 0:
                if best_state is None:
                    best_state = state
                    continue
                if state < best_state:
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
    initial_state = State(graph)
    if mode:
        solution_state = depth_first_search(initial_state, counter_manager)
    else:
        solution_state = breadth_first_search(initial_state, counter_manager)
    end_time = time()
    elapsed_time = end_time - start_time
    print_solution_summary(elapsed_time, counter_manager, solution_state)


def main() -> None:
    graph: GraphData = [
        [0, 10, 10, 1, 10],
        [10, 0, 1, 10, 10],
        [1, 10, 0, 10, 10],
        [10, 10, 10, 0, 1],
        [10, 1, 10, 10, 0],
    ]
    solve(graph, 0)
    graph = [[0, 1, 2, 4], [1, 0, 2, 3], [2, 2, 0, 5], [4, 3, 5, 0]]
    solve(graph, 1)
    for node_limit in range(1, 23):
        graph = get_graph_from_file("grafo0004.txt", nodes_limit=node_limit)
        solve(graph, 1)


if __name__ == "__main__":
    main()
