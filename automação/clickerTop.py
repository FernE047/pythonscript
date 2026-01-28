import pyautogui, time

# clicker automatico com mostragem de porcentagem

time.sleep(5)
limite = 10**3
concluido = [0]
apaga = 0
for b in range(1, limite + 1):
    pyautogui.click(780, 460)
    porcentagem = int(b / limite * 100)
    if porcentagem not in concluido:
        concluido.append(porcentagem)
        mensagem = str(porcentagem) + "%"
        print((apaga * "\b") + mensagem, end="", flush=True)
        apaga = len(mensagem)
apaga = input()  # só para pausar
