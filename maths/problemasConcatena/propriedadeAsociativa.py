def testaBase(num,zero=False,iguais=False):
    for a in range(1,num):
        for b in range(num):
            for c in range(num):
                primeiro=(a*num+b)*c
                segundo=a*int(b*num+c)
                if(primeiro==segundo):
                    if(zero):
                        if(primeiro==0):
                            continue
                    if(iguais):
                        if((a==b)and(b==c)):
                            continue
                    print(str(a)+'|'+str(b)+'|'+str(c))
                    print(primeiro)
                    print('')

for base in range(2,21):
    print('base '+str(base)+' :\n')
    testaBase(base,zero=True,iguais=True)
