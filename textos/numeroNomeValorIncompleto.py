#ele imprime quantos caracteres tem o numero por extenso incompleto

listas=((0,2,4,4,6,5,4,4,4,4),(3,4,4,5,7,6,8,8,7,8),(3,5,8,9,12,10,10,10,10,10),(3,6,6,7,10,10,9,9,8,8,8))
passados=[]
caminhos=[]

def valor_de_number(n):
    if len(str(n))>=4:
        if len(str(n))%3==0:
            for a in range(0,len(str(n)),step=3):
                pedaco=[for](str(n))

