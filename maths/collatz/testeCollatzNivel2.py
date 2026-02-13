def barra(x):
    if(x%2==0):
        x/=2
    elif(x%8==5):
        x=(x-1)/4
    elif(x%8==7):
        x=(3*x+1)/2
    elif(x%16==3):
        x=(x-1)/2
    elif(x%16==9):
        x=(3*x+1)/4
    elif(x%16==11):
        x=(3*x+1)/2
    elif(x%32==1):
        x=(3*x+1)/4
    elif(x%64==17):
        x=(3*x-3)/16
    elif(x%128==49):
        x=(3*x-3)/16
    elif(x%128==113):
        x=(x-17)/32
    return(int(x))


def main() -> None:
    x=int(input())
    passos=0
    while(x!=1):
        x=barra(x)
        print(f"{x}")
        passos+=1
    print(f"passos:{passos}")


if __name__ == "__main__":
    main()