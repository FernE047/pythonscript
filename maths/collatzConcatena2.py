def collatzConcatena2(j):
    if((j%2)==1):
        j=int(str(j)*2)+1
    else:
        j=int(j/2)
    return(j)


precedentes=[]
print("esse programa concatena numero impar 2 vezes")
print("numero par divide por 2")
print("até que chegue a 1")
print("digite a semente")
numero=int(input())
print("digite 1 para printar tudo")
impressao=input()
print(str(numero))
while(numero!=1):
    numero=collatzConcatena2(numero)
    if(impressao=="1"):
        print(str(numero))
    if(numero%2):
        if(impressao!="1"):
            print(str(numero))
        if(numero not in precedentes):
            precedentes.append(numero)
        else:
            break
if(numero==1):
    print("fim esperado")
else:
    print("repetiu")
