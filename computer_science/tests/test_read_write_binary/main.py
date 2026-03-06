from pathlib import Path


def main() -> None:
    diretorio = Path.cwd()
    image_path = list(diretorio.iterdir())[0]
    with open(diretorio / "copia.py", "wb") as novoArquivo:
        with open(image_path, "rb") as arquivo:
            novoArquivo.write(arquivo.read())
        with open(image_path, "rb") as arquivo:
            byte = arquivo.read(1)
            while byte:
                novoArquivo.write(byte)
                byte_as_integer = int.from_bytes(byte, byteorder="big")
                byte_as_char = bin(byte_as_integer)
                byte_as_char = byte_as_char.lstrip("0b")
                while len(byte_as_char) < 8:
                    byte_as_char = f"0{byte_as_char}"
                print(byte_as_char)
                byte = arquivo.read(1)


if __name__ == "__main__":
    main()