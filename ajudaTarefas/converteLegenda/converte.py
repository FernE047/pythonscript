legendaTxt = open('input.txt','r')
legendaStr = open('output.str','w')
linha = ''
caracter = "a"
linhaN = 1
while(caracter):
    caracter = legendaTxt.read(1)
    if caracter != '\n':
        linha += caracter
        continue
    if not linha:
        legendaStr.write('\n')
        linha = ''
        continue
    if linha[0] != '0':
        legendaStr.write(str(linha)+'\n')
        linha = ""
        continue
    #virgula = linha.find(',')
    linhaModifica=list(linha)
    linhaModifica[9] = '.'
    linhaModifica[23] = '.'
    linha = ''.join(linhaModifica)
    inicioTexto = linha[:13] #:virgula]
    finalTexto = linha[14:] #virgula+1:]
    inicioTempo = inicioTexto[:2]+inicioTexto[3:6]+inicioTexto[7:]
    finalTempo = finalTexto[:2]+finalTexto[3:6]+finalTexto[7:]
    legendaStr.write(str(linhaN)+'\n')
    legendaStr.write(inicioTempo+' --> '+finalTempo+'\n')
    linhaN += 1
legendaStr.write(linha)
legendaTxt.close()
legendaStr.close()
