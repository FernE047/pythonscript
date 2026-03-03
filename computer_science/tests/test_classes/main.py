# this was one of the first times I used classes in python


class User:
    seq = 0
    objects: list["User"] = []

    def __init__(self, nome: str, idade: int) -> None:
        self.id: None | int = None
        self.nome = nome
        self.idade = idade

    def save(self) -> None:
        self.__class__.seq += 1
        self.id = self.__class__.seq
        self.__class__.objects.append(self)

    def __str__(self) -> str:
        return self.nome

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.id} - {self.nome} - {self.idade}>\n"

    @classmethod
    def all(cls) -> list["User"]:
        return cls.objects



def main() -> None:
    user_1 = User("Regis", 35)
    user_1.save()
    print(user_1)
    user_2 = User("Fabio", 20)
    user_2.save()
    print(user_2)
    print(User.all())


if __name__ == "__main__":
    main()