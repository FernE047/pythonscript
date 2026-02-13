
    
def main() -> None:limite = 10000
    for a in range(1, limite + 1):
        for b in range(a, limite + 1):
            numMult = a * b
            numStr = int(str(a) + str(b))
            if numMult == numStr:
                print(numMult)
                print(numStr)
                print(f"{a} | {b}")
                print("")

if __name__ == "__main__":
    main()