from numpy.random import choice

def randomMidVowels():
    letrasPossiveis = list('aeiou')
    probabilidade = [0.35697057404727445, 0.23323685479980705, 0.20839363241678727, 0.123251326579836, 0.07814761215629522]
    return choice(letrasPossiveis,1,p=probabilidade)[0]

def randomMidCons():
    letrasPossiveis = list('bcdfghjklmnpqrstvwxyz')
    probabilidade = [0.030587833219412174, 0.035201640464798366, 0.052973342447026665, 0.016233766233766236, 0.029049897470950107, 0.07928913192071088, 0.02665755297334245, 0.042549555707450455, 0.08817498291182503, 0.06049213943950787, 0.13841421736158582, 0.022727272727272735, 0.0039302802460697206, 0.10731373889268628, 0.09005468215994533, 0.06766917293233084, 0.018284347231715656, 0.01503759398496241, 0.0037593984962406026, 0.05092276144907725, 0.02067669172932331]
    return choice(letrasPossiveis,1,p=probabilidade)[0]

def beginLetter(sex=''):
    letraAdicional=''
    letrasPossiveis = list('abcdefghijklmnopqrstuvwxyz')
    if(sex):
        if(sex=='m'):
            probabilidade = [0.048949999999999994, 0.037450000000000004, 0.05985, 0.07582, 0.034140000000000004, 0.01898, 0.036680000000000004, 0.02092, 0.0038, 0.15882, 0.026160000000000003, 0.03212, 0.0696, 0.01138, 0.00417, 0.025019999999999997, 0.00048, 0.10253999999999999, 0.040780000000000004, 0.04253, 0.0001, 0.006540000000000001, 0.04216, 0.00013, 0.00013, 0.10075000000000012]
        elif(sex=='f'):
            probabilidade = [0.06784, 0.04605000000000001, 0.06999, 0.05779, 0.04868, 0.01252, 0.02231, 0.01966, 0.00933, 0.08178, 0.04764, 0.06896, 0.11114, 0.02147, 0.00398, 0.03129, 0.00017, 0.04157, 0.07035, 0.033530000000000004, 0.0003, 0.02015, 0.008, 8e-05, 0.00391, 0.10151000000000013]
        else:
            probabilidade = [0.058570000000000004, 0.04183, 0.06501, 0.06663999999999999, 0.04154, 0.01569, 0.029369999999999997, 0.02028, 0.00661, 0.11961000000000001, 0.03709, 0.05087, 0.09074, 0.01652, 0.00407, 0.028210000000000002, 0.00032, 0.07151, 0.055830000000000005, 0.03795, 0.0002, 0.01347, 0.02477, 0.0001, 0.0020499999999999997, 0.10115000000000003] 
    else:
        probabilidade = [0.058570000000000004, 0.04183, 0.06501, 0.06663999999999999, 0.04154, 0.01569, 0.029369999999999997, 0.02028, 0.00661, 0.11961000000000001, 0.03709, 0.05087, 0.09074, 0.01652, 0.00407, 0.028210000000000002, 0.00032, 0.07151, 0.055830000000000005, 0.03795, 0.0002, 0.01347, 0.02477, 0.0001, 0.0020499999999999997, 0.10115000000000003]
    letra = choice(letrasPossiveis,1,p=probabilidade)[0]
    if (letra == 'q'):
        letraAdicional = 'u'
    if letra in ['b','c','d','f','g','k','p','t','v']:
        chanceAdicional = choice([0,1],1,p=[0.95,0.05])
        if(chanceAdicional):
            letraAdicional = randomMidCons()
            while(letraAdicional not in ['l','r','h']):
                letraAdicional = randomMidCons()
    return letra+letraAdicional

def randomEnd(quant,isFirstVowel=True):
    mid = ''
    consoanteAdicional = 0
    for a in range(quant):
        if( (bool(a%2)) == isFirstVowel ):
            mid += randomMidVowels()
            consoanteAdicional=0
        else:
            letra = randomMidCons()
            if(letra == 'q'):
                mid += 'qu'
            elif(letra in ['l','s','r','y','w','z','x','n','m']):
                if(not(consoanteAdicional)):
                    consoanteAdicional = choice([0,1],1,p=[0.75,0.25])[0]
                    if(consoanteAdicional):
                        isFirstVowel = not(isFirstVowel)
                mid += letra
            else:
                mid += letra
                if(letra not in ['h','j']):
                    consoanteAdicional = choice([0,1],1,p=[0.95,0.05])
                    if(consoanteAdicional):
                        letra = randomMidCons()
                        while(letra not in ['l','r','h']):
                            letra = randomMidCons()
                        mid += letra
    return mid

def makeName(lenght,sex=''):
    begin = beginLetter(sex = sex)
    end = randomEnd(lenght-1 , isFirstVowel = (begin in ['a','e','i','o','u']) )
    return begin+end

def makeRandomName(sex=''):
    numerosPossiveis = [3,4,5,6,7,8,9,10]
    probabilidade = [0.0248, 0.0908, 0.2184, 0.26030000000000003, 0.20440000000000003, 0.12140000000000001, 0.0557, 0.024199999999999878]
    lenght = choice(numerosPossiveis,1,p=probabilidade)[0]
    return(makeName(lenght,sex = sex))

def makeRandomFullName(sex=''):
    quantPossiveis = [2,3,4]
    probabilidade = [0.45,0.45,0.1]
    quant = choice(quantPossiveis,1,p=probabilidade)[0]
    lista = [makeRandomName(sex)]
    for a in range(quant-1):
        lista.append(makeRandomName())
    return ' '.join(lista)

s=['m','f']
g=['\nmasculinos:','\nfemininos:']
for n in range(2):
    print(g[n])
    for b in range(100):
        print('{:02d} : '.format(b)+makeRandomFullName(s[n]))
