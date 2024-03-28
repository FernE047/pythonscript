legendaTxt = open('input.txt','r')
legendaStr = open('output.str','w')
linha = ''
caracter = legendaTxt.read(1)
linhaN = 1
while(caracter):
    if(caracter == '\n'):
        if(linha):
            if(linha[0] == '0'):
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
            else:
                legendaStr.write(str(linha)+'\n')
        else:
            legendaStr.write(str(linha)+'\n')
        linha = ''
    else:
        linha += caracter
    caracter = legendaTxt.read(1)
legendaStr.write(linha)
legendaTxt.close()
legendaStr.close()
