#deciframento

c=3
while(1):
    d=0
    e=0
    f=1
    while(not((c>=0)and(c<=2))):
        print("modo 1:so exemplos\nmodo 2:com respostas\nmodo 0:SAIR")
        c=int(input())
    if(c==0):
        break
    a=int(input())
    if(a==0):
        break
    b=int(input())
    if(b==0):
        break
    if(c==2):
        d=int(input())
        if(d==0):
            break
        e=int(input())
        f=int(input())
        if(f==0):
            break
    maior=len(str(int(a*10+b)))
    mensagem="{0:"+str(maior)+"d}:{1:"+str(maior+1)+"d}"
    for c in range(11):
        print(mensagem.format(int(a*c+b),int((d*(a*c+b)+e)/f)))
    input()
