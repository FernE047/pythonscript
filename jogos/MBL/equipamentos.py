class Equipamento:
    def __init__(self,Apreco,Abonus,passivas,construcao):
        self.preco = Apreco
        self.bonus = Abonus
        self.passivas = Apassivas
        self.construcao = Aconstrucao

    def __str__(self):
        pass

def equipamentos(nome):
    if nome == 'Botas':
        return Equipamento(250,[[0,False,20]],[],[])
    elif nome == 'Bota de Reducao':
        return
    elif nome == 'Bota de Def. Fisica':
        return Equipamento
        
        
