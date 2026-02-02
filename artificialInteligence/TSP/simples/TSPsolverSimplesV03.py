from time import time

GraphData = list[list[float]]
VertexData = tuple[float, float]
StateData = tuple[float, list[int]]


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


def get_graph_from_file(file_name: str, nodes_limit: int | None = None) -> GraphData:
    with open(file_name, "r", encoding="utf-8") as file:
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


def print_solution_summary(duration: float) -> None:
    global graph
    global solution_state
    state: StateData = (0, [])
    for line in graph:
        print(
            " ".join([" " * (3 - len(str(element))) + str(element) for element in line])
        )
    print()
    for destination in solution_state[1]:
        if state[1]:
            state = (state[0] + graph[state[1][-1]][destination], state[1])
        state = (state[0], state[1] + [destination])
        print(f"caminho : {state[1]}")
        print(f"custo   : {state[0]}\n")
    print(f"iteracoes : {iterations}")
    print(f"cortes    : {cut_count}")
    print_elapsed_time(duration)
    print("\n\n\n")


def depth_first_search(
    state: StateData, best_state: StateData | None = None
) -> StateData:
    global iterations
    global cut_count
    global graph
    if len(state[1]) == len(graph):
        if best_state is None:
            return (state[0], state[1].copy())
        if state[0] < best_state[0]:
            return (state[0], state[1].copy())
        return best_state
    iterations += 1
    for index in range(len(graph)):
        if index in state[1]:
            continue
        if state[1]:
            state = (state[0] + graph[state[1][-1]][index], state[1])
        state[1].append(index)
        if best_state is None:
            best_state = depth_first_search(state, best_state)
        else:
            if state[0] < best_state[0]:
                best_state = depth_first_search(state, best_state)
            else:
                cut_count += 1
        state[1].remove(index)
        if state[1]:
            state = (state[0] - graph[state[1][-1]][index], state[1])
    assert best_state is not None
    return best_state


def solve() -> None:
    global iterations
    global cut_count
    global solution_state
    start_time = time()
    iterations = 0
    cut_count = 0
    initial_state: StateData = (0, [])
    solution_state = depth_first_search(initial_state)
    end_time = time()
    print_solution_summary(end_time - start_time)


iterations = 0
cut_count = 0
solution_state: StateData = (0, [])

graph: GraphData = [
    [0, 10, 10, 1, 10],
    [10, 0, 1, 10, 10],
    [1, 10, 0, 10, 10],
    [10, 10, 10, 0, 1],
    [10, 1, 10, 10, 0],
]

solve()

graph = [[0, 1, 2, 4], [1, 0, 2, 3], [2, 2, 0, 5], [4, 3, 5, 0]]

solve()

for node_limit in range(1, 23):
    graph = get_graph_from_file("grafo0004.txt", nodes_limit=node_limit)
    solve()
