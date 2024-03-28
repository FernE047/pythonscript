import random, time
def apresentar(player):
    soma=0
    mensagem=""
    for i in maos[player]:
        mensagem+=str(i)+","
        if(i in ("Q","J","K")):
            soma+=10
        else:
            soma+=int(i)
    mensagem+="\b \n\nsoma:"+str(soma)
    print(mensagem)
    return(soma)

escolhas=1
while(escolhas!=0):
    baralho=[]
    for a in range(1,14):
        if(a==11):
            baralho+=4*["Q"]
        elif(a==12):
            baralho+=4*["J"]
        elif(a==13):
            baralho+=4*["K"]
        else:
            baralho+=4*[a]
    random.shuffle(baralho)
    soma=[0,0]
    maos=[[baralho.pop(-1)],[]]
    while(escolhas!=2):
        print("suas cartas:")
        soma[0]=apresentar(0)
        if(soma[0]>21):
            print("\nEXPLODIU"+3*"\n")
            break
        elif(soma[0]==21):
            print("\nVENCEU"+3*"\n")
            break
        print("\n1:comprar")
        print("2:parar")
        escolhas=int(input())
        if(escolhas==1):
            maos[0].append(baralho.pop(-1))
        else:
            break
    while(soma[1]<=soma[0]):
        if(soma[0]==21):
            break
        maos[1].append(baralho.pop(-1))
        print("dealer cartas:")
        soma[1]=apresentar(1)
        time.sleep(1)
        if(soma[1]>21):
            if(soma[0]>21):
                print("\nDEALER EXPLODIU"+3*"\n",end="")
                if(soma[0]>=soma[1]):
                    print("VOCÊ PERDEU\n")
                else:
                    print("VOCÊ VENCEU\n")
            break
        elif(soma[1]==21):
            print("\nDEALER VENCEU"+3*"\n"+"VOCÊ PERDEU")
            break
    if(soma[0]<=21):
        print(3*"\n"+"VOCÊ VENCEU\n")
    elif((soma[1]>soma[0])and(soma[1]<21)):
        print("\nDEALER VENCEU"+3*"\n"+"VOCÊ PERDEU")
    print("jogar novamente?[1/0]")
    escolhas=int(input())
        
