import userUtil

def fractionToNumber(fraction):
    quant=len(fraction)
    a=fraction[-1]
    print(a)
    print()
    for n in range(quant-1):
        print(quant-n-2)
        print(fraction[quant-n-2])
        a=fraction[quant-n-2]+1/a
        print(a)
        print()
    return a

def khinchinPerto(fraction,menor):
    khinchin=2.68545200106530644530971483548179569382038
    result=1
    for a in fraction:
        result*=a
    if(menor):
        if(result<khinchin):
            return True
    else:
        if(result>khinchin):
            return True
    return False

lista=[]
for b in range(10):
    a=0
    while True:
        a+=1
        lista.append(a)
        if khinchinPerto(lista,b%2):
            lista.pop(-1)
            break
        else:
            lista.pop(-1)
    print(lista)
