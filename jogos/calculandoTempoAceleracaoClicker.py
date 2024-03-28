import textos

def tempoDemoraProducao(quantidadeProdutora,quantidadeProduzida,precoProducao,producaoPrecisa):
    quantidadePorSegundo=quantidadeProduzida*quantidadeProdutora/60
    tempo=0
    while(quantidadePorSegundo<producaoPrecisa):
        tempoAtual=precoProducao/quantidadePorSegundo
        tempo+=tempoAtual
        quantidadeProdutora+=1
        quantidadePorSegundo=quantidadeProduzida*quantidadeProdutora/60
    return tempo

def tempoDemoraFabricas(quantidadeProdutora,quantidadeProduzida,precoProducao,quantidadePrecisa):
    quantidadePorSegundo=quantidadeProduzida*quantidadeProdutora/60
    tempo=0
    while(quantidadeProdutora<quantidadePrecisa):
        tempoAtual=precoProducao/quantidadePorSegundo
        tempo+=tempoAtual
        quantidadeProdutora+=1
        quantidadePorSegundo=quantidadeProduzida*quantidadeProdutora/60
    return tempo

def tempoDemoraProduto(quantidadeProdutora,quantidadeProduzida,precoProducao,produtoPrecisa):
    quantidadePorSegundo=quantidadeProduzida*quantidadeProdutora/60
    produto=0
    tempo=0
    while(produto<produtoPrecisa):
        tempoAtual=precoProducao/quantidadePorSegundo
        tempo+=tempoAtual
        produto+=precoProducao
        quantidadeProdutora+=1
        quantidadePorSegundo=quantidadeProduzida*quantidadeProdutora/60
    return tempo    

quantidadeProdutora=1
quantidadeProduzida=1
precoProducao=1000
tempo=tempoDemoraProducao(1,0.001,1000,1000)
print("\nquantidadeProdutora : {}\n".format(quantidadeProdutora)+textos.embelezeTempo(tempo))
