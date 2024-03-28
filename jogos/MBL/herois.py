class Skill:
    def __init__(self,cd,custoMana,Adanos,nivel):
        self.cooldown = cd
        self.consumoDaSkill = custoMana
        self.danos = Adanos

class Heroi:
    def __init__(self, velocidadeMovimento, atkF, atkM, defF, defM, HP, Mana, velocidadeATK, regenHP, regenMP, critBas, critSkill, listaDeSkills):
        self.velocidadeDeMovimento = velocidadeMovimento
        self.ataqueFisico = atkF
        self.poderMagico = atkM
        self.defesaFisica = defF
        self.defesaMagica = defM
        self.hp = HP
        self.mana = Mana
        self.velocidadeDeAtaque = velocidadeATK
        self.regenDeVida = regenHP
        self.regenDeMana = regenMP
        self.chanceDeCriticoNoAtaqueBasico = critBas
        self.chanceDeCriticoNaSkill = critSkill
        self.skills = listaDeSkills

    def __str__(self):
        pass

def herois(nome):
    if(nome == 'lolita'):
        primeira = Skill([10,0],[70,10],[[200,True,55],[7.5,False,0.5]],6)
        primeira = Skill([10,0],[70,10],[[200,True,55],[7.5,False,0.5]],6)
        return Heroi(260,115,0,27,10,2579,480,0.786,48,12,0,0,[primeira,Skill(),Skill()])
