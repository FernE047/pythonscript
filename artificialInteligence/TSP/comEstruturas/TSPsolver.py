from grafos import Graph
from grafos import get_graph_from_file
from estados import State


def depth_first_search(state: State, lowest_state: State | None = None) -> State:
    global iterations
    global cut_count
    iterations += 1
    next_states = state.next_states()
    if len(next_states) == 0:
        if lowest_state is None:
            return state
        if state.path_cost < lowest_state.path_cost:
            return state
    for potential_solution in next_states:
        if lowest_state is None:
            lowest_state = depth_first_search(potential_solution, lowest_state)
            continue
        if potential_solution.path_cost < lowest_state.path_cost:
            lowest_state = depth_first_search(potential_solution, lowest_state)
            continue
        cut_count += 1
    assert lowest_state is not None
    return lowest_state


def breadth_first_search(state: State) -> State:
    global iterations
    iterations += 1
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


iterations = 0
cut_count = 0
graph_raw: list[list[float]] = [
    [0, 10, 10, 1, 10],
    [10, 0, 1, 10, 10],
    [1, 10, 0, 10, 10],
    [10, 10, 10, 0, 1],
    [10, 1, 10, 10, 0],
]
graph = Graph(base_graph=graph_raw)
initial_state = State(graph)
solution_state = breadth_first_search(initial_state)
solution_state.show_path()
graph = Graph(4)
graph.set_element((0, 1), 1)
graph.set_element((0, 2), 2)
graph.set_element((0, 3), 4)
graph.set_element((1, 2), 2)
graph.set_element((1, 3), 3)
graph.set_element((2, 3), 5)
initial_state = State(graph)
solution_state = depth_first_search(initial_state)
print(iterations)
print(cut_count)
iterations = 0
cut_count = 0
solution_state.show_path()
for max_nodes in range(1, 23):
    graph = get_graph_from_file("grafo0004.txt", limit=max_nodes)
    initial_state = State(graph)
    solution_state = depth_first_search(initial_state)
    solution_state.show_path()
    print(f"iterations : {iterations}\ncut_count  : {cut_count}\n\n\n")
    iterations = 0
    cut_count = 0
