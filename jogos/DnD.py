import random

def somatudo(x):
    soma=0
    for a in range(x):
        soma+=a+1
    return(soma)

def dado(n):
    return(random.randint(1,n))

def d(n,m):
    lista=[]
    for a in range(n):
        lista+=[dado(m)]
    return(lista)

def vd(m,n=2):
    results=d(n,m)
    return(max(results))

def dd(m,n=2):
    results=d(n,m)
    return(min(results))

def chances(function,m,n=2,potencia=10**6):
    lista=[0 for a in range(m)]
    for a in range(potencia):
        lista[function(m,n)-1]+=1
    for num,elemento in enumerate(lista):
        print(str(num+1)+" : "+str(elemento*100/potencia))

def sequenciaChance(m,sequencia,potencia=10**6):
    n=len(sequencia)
    lista=d(n-1,m)
    total=0
    for a in range(potencia):
        lista+=d(1,m)
        if(lista==sequencia):
            total+=1
        lista.pop(0)
    print(str(sequencia)+" : "+str(total*100/potencia))
    

print("desvantagem:\n")
#chances(dd,20)
print("\nvantagem:\n")
#chances(vd,20)
print("\nnormal:\n")
#chances(dd,20,1)
print("\nsequencia:\n")
sequenciaChance(20,[20,20])
sequenciaChance(20,[20,20,20])
sequenciaChance(20,[20,20,20,20])
    

