PRINT_RATE = 1000000
INDENTATION = 20
SIZE = 8
COORDINATES_COUNT = 2

CellData = list[int] | int
RowData = list[CellData]
ColumnData = list[RowData]
MatrixData = list[ColumnData]
CoordData = tuple[int, int]
ICoordData = tuple[int, int, int]


def print_details(matrix: MatrixData | None = None, iterations: int = 0) -> None:
    def get_identation(elemento: RowData) -> str:
        return " " * (INDENTATION - len(str(elemento)))

    print(f"Iteracoes Totais {iterations:,}")
    if matrix is None:
        print("nao existe solução")
        return
    for column in matrix:
        indented_rows = [f"{row}{get_identation(row)}" for row in column]
        print(" ".join(indented_rows))


def get_opposite_coordinate(coordinate: int) -> int:
    return SIZE - coordinate - 1


def get_threatened_positions(current_coord: CoordData) -> list[CoordData]:
    current_y, current_x = current_coord
    threatened_positions: list[CoordData] = []
    for x in range(SIZE):
        if x == current_x:
            continue
        threatened_positions.append((current_y, x))
    for y in range(SIZE):
        if y == current_y:
            continue
        threatened_positions.append((y, current_x))
    if current_x == current_y:
        for x_or_y in range(SIZE):
            if x_or_y == current_x:
                continue
            threatened_positions.append((x_or_y, x_or_y))
    opposite_y = get_opposite_coordinate(current_y)
    if current_x == opposite_y:
        for x_or_y in range(SIZE):
            if x_or_y == current_y:
                continue
            opposite_coord = get_opposite_coordinate(x_or_y)
            threatened_positions.append((x_or_y, opposite_coord))
    return threatened_positions


def get_non_integer_positions(
    matrix: MatrixData, icoord: ICoordData
) -> list[CoordData]:
    current_y, current_x, i = icoord
    non_integer_positions: list[CoordData] = []
    for x in range(SIZE):
        if x == current_x:
            continue
        cell = matrix[current_y][x][i]
        if not isinstance(cell, int):
            non_integer_positions.append((current_y, x))
    for y in range(SIZE):
        if y == current_y:
            continue
        cell = matrix[y][current_x][i]
        if not isinstance(cell, int):
            non_integer_positions.append((y, current_x))
    if current_x == current_y:
        for x_or_y in range(SIZE):
            if x_or_y == current_x:
                continue
            cell = matrix[x_or_y][x_or_y][i]
            if not isinstance(cell, int):
                non_integer_positions.append((x_or_y, x_or_y))
    opposite_y = get_opposite_coordinate(current_y)
    if current_x == opposite_y:
        for x_or_y in range(SIZE):
            if x_or_y == current_y:
                continue
            opposite_coord = get_opposite_coordinate(x_or_y)
            cell = matrix[x_or_y][opposite_coord][i]
            if not isinstance(cell, int):
                non_integer_positions.append((x_or_y, opposite_coord))
    return non_integer_positions


def get_affecting_numbers(matrix: MatrixData, icoord: ICoordData) -> list[int]:
    current_y, current_x, i = icoord
    affected_numbers: list[int] = []
    all_possible_values = [a for a in range(SIZE)]
    for x in range(SIZE):
        if x == current_x:
            continue
        cell = matrix[current_y][x][i]
        if isinstance(cell, int):
            affected_numbers.append(cell)
    for y in range(SIZE):
        if y == current_y:
            continue
        cell = matrix[y][current_x][i]
        if isinstance(cell, int):
            affected_numbers.append(cell)
    if affected_numbers == all_possible_values:
        return all_possible_values
    if current_x == current_y:
        for x_or_y in range(SIZE):
            if x_or_y == current_x:
                continue
            cell = matrix[x_or_y][x_or_y][i]
            if isinstance(cell, int):
                affected_numbers.append(cell)
        if affected_numbers == all_possible_values:
            return all_possible_values
    if current_x == get_opposite_coordinate(current_y):
        for x_or_y in range(SIZE):
            if x_or_y == current_y:
                continue
            opposite_coord = get_opposite_coordinate(x_or_y)
            cell = matrix[x_or_y][opposite_coord][i]
            if isinstance(cell, int):
                affected_numbers.append(cell)
        if affected_numbers == all_possible_values:
            return all_possible_values
    return affected_numbers


def recompute_domain(matrix: MatrixData, icoord: ICoordData) -> None:
    affecting_numbers = get_affecting_numbers(matrix, icoord)
    cell: list[int] = []
    for number in range(SIZE):
        if number not in affecting_numbers:
            cell.append(number)
    insert_in_matrix(matrix, icoord, cell)


def insert_in_matrix(
    matrix: MatrixData,
    icoord: ICoordData,
    value_to_insert: CellData,
) -> bool:
    y, x, i = icoord
    matrix[y][x][i] = value_to_insert
    if not isinstance(value_to_insert, int):
        return True
    for ty, tx in get_threatened_positions((y, x)):
        cell = matrix[ty][tx][i]
        if isinstance(cell, int):
            continue
        if value_to_insert not in cell:
            continue
        if len(cell) == 1:
            return False
        cell.remove(value_to_insert)
    return True


def remove_from_matrix(
    matrix: MatrixData, icoord: ICoordData, value_to_remove: CellData
) -> None:
    y, x, i = icoord
    recompute_domain(matrix, icoord)
    for y, x in get_non_integer_positions(matrix, icoord):
        cell = matrix[y][x][i]
        if isinstance(cell, int):
            raise ValueError(
                "the cell should not be an integer when processing non integer positions"
            )
        if value_to_remove not in get_affecting_numbers(matrix, (y, x, i)) + cell:
            # TODO: Idk what is happening here
            cell.append(value_to_remove)  # type: ignore


def get_lowest_coordinates(
    matrix: MatrixData, occupied_positions: list[list[int]]
) -> ICoordData:
    lowest_value = SIZE + 1
    lowest_coord = (SIZE, SIZE, SIZE)

    def find_lowest_coordinates(
        lowest_value: int, index: int
    ) -> tuple[int, ICoordData | None]:
        for x in range(SIZE):
            for y in range(SIZE):
                cell = matrix[y][x][index]
                if isinstance(cell, int):
                    continue
                tamanhoLista = len(cell)
                if tamanhoLista >= lowest_value:
                    continue
                lowest_value = tamanhoLista
                lowest_coord = (y, x, index)
                if lowest_value == 1:
                    return (lowest_value, lowest_coord)
        return (lowest_value, None)

    if len(occupied_positions) == SIZE:
        lowest_value, new_coord = find_lowest_coordinates(lowest_value, 0)
        if new_coord is not None:
            return new_coord
    if lowest_value != SIZE + 1:
        return lowest_coord
    lowest_value, new_coord = find_lowest_coordinates(lowest_value, 1)
    if new_coord is not None:
        return new_coord
    if lowest_value == SIZE + 1:
        lowest_coord = (0, 0, 0)
    return lowest_coord


def solve(
    matrix: MatrixData, occupied_positions: list[list[int]], iterations: int = 0
) -> tuple[int, MatrixData | None]:
    y, x, i = get_lowest_coordinates(matrix, occupied_positions)
    if iterations % PRINT_RATE == 0:
        print_details(matrix, iterations)
        print()
    iterations += 1
    if len(occupied_positions) >= SIZE**2:
        return (iterations, matrix)
    cell = matrix[y][x][i]
    if isinstance(cell, int):
        raise ValueError(
            "The Lowest coordinate is already occupied, this should not happen"
        )
    poss = cell.copy()
    for possibilidade in poss:
        elemento = []
        if i == 1:
            new_cell = matrix[y][x][0]
            if isinstance(new_cell, list):
                raise ValueError(
                    "The first coordinate should be occupied when the second is being processed"
                )
            elemento = [new_cell, possibilidade]
            if elemento in occupied_positions:
                continue
            else:
                occupied_positions.append(elemento)
        if insert_in_matrix(matrix, (y, x, i), possibilidade):
            matrix[y][x][i] = possibilidade
            iterations, solution = solve(matrix, occupied_positions, iterations)
            if solution:
                return (iterations, solution)
        if i == 1:
            occupied_positions.remove(elemento)
        remove_from_matrix(matrix, (y, x, i), possibilidade)
    return (iterations, None)


def generate_matrix() -> MatrixData:
    matrix: MatrixData = []
    for _ in range(SIZE):
        column: ColumnData = []
        for _ in range(SIZE):
            row: RowData = []
            for _ in range(COORDINATES_COUNT):
                cell = [index for index in range(SIZE)]
                row.append(cell)
            column.append(row)
        matrix.append(column)
    for x in range(SIZE):
        for i in range(COORDINATES_COUNT):
            coord = (0, x, i)
            insert_in_matrix(matrix, coord, x)
    return matrix


def main() -> None:
    matrix = generate_matrix()
    occupied_positions = [[index, index] for index in range(SIZE)]
    iterations, solution = solve(matrix, occupied_positions)
    print_details(solution, iterations)


if __name__ == "__main__":
    main()
