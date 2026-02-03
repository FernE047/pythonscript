def print_elapsed_time(seconds: float) -> None:
    if seconds < 0:
        seconds = -seconds
        sign = "-"
    else:
        sign = ""
    total_ms = int(round(seconds * 1000))
    ms = total_ms % 1000
    total_s = total_ms // 1000
    s = total_s % 60
    total_min = total_s // 60
    m = total_min % 60
    total_h = total_min // 60
    h = total_h % 24
    d = total_h // 24
    parts: list[str] = []

    def add(value: int, singular: str, plural: str) -> None:
        if value:
            parts.append(f"{value} {singular if value == 1 else plural}")

    add(d, "day", "days")
    add(h, "hour", "hours")
    add(m, "minute", "minutes")
    add(s, "second", "seconds")
    if ms or not parts:
        parts.append(f"{ms} millisecond" if ms == 1 else f"{ms} milliseconds")
    print(sign + ", ".join(parts))

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


def main() -> None:
    quantidadeProdutora=1
    quantidadeProduzida=1
    precoProducao=1000
    tempo=tempoDemoraProducao(1,0.001,1000,1000)
    print(f"\nquantidadeProdutora : {quantidadeProdutora}\n")
    print_elapsed_time(tempo)


if __name__ == "__main__":
    main()