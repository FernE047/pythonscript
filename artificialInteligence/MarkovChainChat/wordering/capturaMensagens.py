import re

file = open('ConversaDoWhatsApp.txt',encoding='utf-8')
output = open('sohMensagens.txt','w',encoding = 'utf-8')
pattern = r"([0-3][0-9][/][0-1][0-9][/]20[21][09] [0-2][0-9][:][0-5][0-9])"
word = file.read(16)
mensagem = ""
while True:
    r2 = re.search(pattern,word)
    if r2:
        if mensagem:
            mensagem = mensagem[3:-17]
            usuario = mensagem[:13]
            print(mensagem)
            output.write(mensagem+"\n")
            mensagem = ""
    while True:
        try:
            letra = file.read(1)
            break
        except:
            pass
    if letra:
        word = word[1:]+letra
        mensagem += letra
    else:
        break
file.close()

