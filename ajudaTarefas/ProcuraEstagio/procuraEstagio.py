import requests, bs4, re, webbrowser
import internet
import textos
import userUtil

def apenasVagas(informacao):
    vagas = []
    for info in informacao:
        descricaoTalvez = info.select('.descricao-vaga')
        if(descricaoTalvez):
            titulo = info.get('title')
            site = info.get('href')
            descricao = info.find('p').getText()
            vagas.append({'titulo' : titulo, 'site' : site, 'descricao' : descricao})
    return(vagas)

def limpaVagas(vagas,pesquisa,procura):
    vagasLimpas = []
    for vaga in vagas:
        for termo in pesquisa:
            termo = termo.lower()
            for chave in procura:
                texto = vaga[chave].lower()
                palavras = textos.separaPalavras(texto)
                if(termo in palavras):
                    vagasLimpas.append(vaga)
                    break
    return(vagasLimpas)

sites = ["http://empregacampinas.com.br/page/{}/?s=est%C3%A1gio","http://empregacampinas.com.br/categoria/vaga/page/{}/"]
escolha = userUtil.entradaNaLista("",["estágio","emprego","tudo"],retorno="numerico")
if(escolha<2):
    sites = [sites[escolha]]
local = ["Campinas","Sumaré","Sumare"]
termos = ["e-commerce","TI","tecnologia","programador","programadores","Web"]
navegador=webbrowser.get("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s")
vagasFinais=[]
for site in sites:
    for a in range(1,10):
        informacao = internet.siteProcura(site.format(a),'.thumbnail')
        vagasDisponiveis = apenasVagas(informacao)
        if(local):
            vagasDisponiveis = limpaVagas(vagasDisponiveis,local,['titulo'])
        if(termos):
            vagasDisponiveis = limpaVagas(vagasDisponiveis,termos,['titulo','descricao'])
        vagasFinais+=vagasDisponiveis
while True:
    opcoes=[vaga['titulo'] for vaga in vagasFinais]
    escolha=userUtil.entradaNaLista("escolha : ",opcoes+["todos","sair"],retorno='numerico')
    if(escolha<len(opcoes)):
        navegador.open(vagasFinais[escolha]['site'])
        vagasFinais.pop(escolha)
    else:
        escolha-=len(opcoes)
        if(escolha==0):
            for vaga in vagasFinais:
                navegador.open(vaga['site'])
                vagasFinais=[]
        break
                
            
    
