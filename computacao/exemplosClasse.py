class User:

    seq = 0
    objects = []

    def __init__(self, nome, idade):
        self.id = None
        self.nome = nome
        self.idade = idade

    def save(self):
        self.__class__.seq += 1
        self.id = self.__class__.seq
        self.__class__.objects.append(self)

    def __str__(self):
        return self.nome

    def __repr__(self):
        return f'<{self.__class__.__name__}: {self.id} - {self.nome} - {self.idade}>\n'

    @classmethod
    def all(cls):
        return cls.objects

if __name__ == '__main__':
    u1 = User('Regis', 35)
    u1.save()
    print(u1)
    u2 = User('Fabio', 20)
    u2.save()
    print(u2)
    print(User.all())
