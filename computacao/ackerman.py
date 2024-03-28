def ackerman(m,n):
    global nivel
    nivel+=1
    print("ackerman({},{})\tnivel={}".format(m,n,nivel))
    if(m<=0):
        return(n+1)
    if((m>0)and(n<=0)):
        retorno=ackerman(m-1,1)
        nivel-=1
        return(retorno)
    if((m>0)and(n>0)):
        retorno=ackerman(m-1,ackerman(m,n-1))
        nivel-=2
        return(retorno)
    print("erro")
    return(n-1)

nivel=0
print(ackerman(3,10))
