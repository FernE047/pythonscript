class LevelController:
    def __init__(self) -> None:
        self.level = 0

    def increment(self, value: int = 1) -> None:
        self.level += value

    def decrement(self, value: int = 1) -> None:
        self.level -= value

    def get_level(self) -> int:
        return self.level


def ackerman(m: int, n: int, level_controller: LevelController) -> int:
    level_controller.increment()
    print(f"ackerman({m},{n})\tlevel={level_controller.get_level()}")
    if m <= 0:
        return n + 1
    if (m > 0) and (n <= 0):
        result_value = ackerman(m - 1, 1, level_controller)
        level_controller.decrement()
        return result_value
    if (m > 0) and (n > 0):
        result_value = ackerman(
            m - 1, ackerman(m, n - 1, level_controller), level_controller
        )
        level_controller.decrement(2)
        return result_value
    print("error")
    return n - 1


def main() -> None:
    level_controller = LevelController()
    print(ackerman(3, 10, level_controller))


if __name__ == "__main__":
    main()
