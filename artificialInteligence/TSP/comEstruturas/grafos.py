CoordData = tuple[int, int]


class Graph:
    def __init__(
        self, size: int | None = None, base_graph: list[list[float]] | None = None
    ) -> None:
        if base_graph is not None:
            self.size = len(base_graph)
            self.graph_matrix = base_graph
            return
        if size is None:
            self.size = 1
            self.graph_matrix = [[0.0]]
            return
        self.size = size
        self.graph_matrix = [[0.0 for _ in range(size)] for _ in range(size)]

    def get_element(self, coord: CoordData) -> float:
        return self.graph_matrix[coord[0]][coord[1]]

    def set_element(
        self, coord: CoordData, value: float, symmetry: bool = True
    ) -> None:
        self.graph_matrix[coord[0]][coord[1]] = value
        if symmetry:
            self.graph_matrix[coord[1]][coord[0]] = value

    def show(self) -> None:
        print(str(self))

    def __str__(self) -> str:
        text: list[str] = []
        for node_row in self.graph_matrix:
            text.append(
                " ".join([" " * (3 - len(str(node))) + str(node) for node in node_row])
            )
        return "\n".join(text)

    def __len__(self) -> int:
        return self.size


def get_graph_from_file(file_name: str, limit: None | int = None) -> Graph:
    with open(file_name, "r", encoding="utf-8") as file:
        line = file.readline()
        vertexes: list[tuple[float, float]] = []
        index = 0
        if limit is not None:
            index = 1
        while line:
            if limit is not None:
                if index == limit:
                    break
            elementos = line.split()
            x_str = elementos[2]
            y_str = elementos[1]
            vertexes.append((float(x_str), float(y_str)))
            line = file.readline()
            if limit is not None:
                index += 1
        graph = Graph(len(vertexes))
        for x, source in enumerate(vertexes):
            for y, destination in enumerate(vertexes):
                coord = (x, y)
                distance = (
                    (destination[0] - source[0]) ** 2
                    + (destination[1] - source[1]) ** 2
                ) ** 0.5
                graph.set_element(coord, distance, False)
    return graph
