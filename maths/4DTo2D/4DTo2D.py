from PIL import Image
import os


def ehNumero(texto: str) -> bool:
    numero = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    if not texto:
        return False
    for carac in texto:
        if carac not in numero:
            return False
    return True


def leCoords(coord):
    trueCoord = []
    numero = ""
    for carac in coord:
        if ehNumero(carac):
            numero += carac
        else:
            if (carac != ",") or (not (ehNumero(numero))):
                return False
            else:
                trueCoord.append(int(numero))
                numero = ""
    if not (ehNumero(numero)):
        return False
    else:
        trueCoord.append(int(numero))
        return trueCoord



def main() -> None:
    coordenadas = []
    coordenada = ""
    while coordenada != "0":
        coordenada = input()
        realCoord = leCoords(coordenada)
        if realCoord:
            coordenadas.append(realCoord)
        print(coordenadas)

if __name__ == "__main__":
    main()