# calcula probabilidade de cair todos os dados o mesmo numero, de 1 a 20 dados
# imprime a quantidade de seculos, anos, dias, horas, minutos, segundos


def main() -> None:
	for a in range(0,20):
		print("\nquantia de dados: "+str(a+1))
		vezes=6**a
		minuto=0
		hora=0
		dia=0
		ano=0
		seculo=0
		if(vezes>60):
			minuto=int(vezes/12)
		else:
			print("segundos: "+str(vezes))
		if(minuto>=1):
			hora=int(minuto/60)
			minuto=minuto%60
			print("minuto: "+str(minuto))
		if(hora>=1):
			dia=int(hora/24)
			hora=hora%24
			print("horas: "+str(hora))
		if(dia>=1):
			ano=int(dia/365.25)
			dia=dia%365
			print("dia: "+str(dia))
		if(ano>=1):
			seculo=int(ano/100)
			ano=ano%100
			print("ano: "+str(ano))
		if(seculo>=1):
			print("seculo: "+str(seculo))
		print("probabilidade: 1 em "+str(vezes))


if __name__ == "__main__":
    main()