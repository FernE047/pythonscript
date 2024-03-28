import pyautogui
import time
import automation

def clicaEspera(coordenadas,tempo=1):
    pyautogui.click(coordenadas) #windows
    time.sleep(tempo)

clicaEspera((25,750)) #windows
clicaEspera((100,690)) #pesquisa
pyautogui.press('w') #digitar{
pyautogui.press('o')
pyautogui.press('r')
pyautogui.press('d') #}digitar
automation.waitFor((395,150),(132,172,221))
clicaEspera((130,150),0) #word
automation.waitFor((618,500),(240,240,240))
clicaEspera((880,570)) #aviso
clicaEspera((400,150)) #macros
clicaEspera((180,30)) #inserir
clicaEspera((690,110)) #cabeçalho
automation.waitFor((1065,188),(231,232,233))
automation.waitFor((731,188),(19,18,18))
clicaEspera((690,210)) #cabeçalho/val croche
clicaEspera((180,30)) #inserir
clicaEspera((800,110)) #numero da pagina
automation.waitFor((802,150),(59,59,59))
clicaEspera((800,150)) #numero/fim da pagina
automation.waitFor((490,255),(0,0,0))
clicaEspera((500,400)) #numero/fim da pagina/opção
clicaEspera((625,60)) #primeira página diferente
clicaEspera((260,30)) #layout da página
clicaEspera((260,110)) #orientação
automation.waitFor((289,136),(59,59,59))
clicaEspera((260,180)) #orientação
automation.waitFor((130,230),(216,232,245))
pyautogui.doubleClick(200,170) #sair do rodapé
clicaEspera((660,70)) #bordas
automation.waitFor((450,170),(240,240,240))
clicaEspera((660,500)) #bordas
automation.waitFor((600,550),(255,0,0))
for a in range(39):
    pyautogui.press('down') #proxima página
pyautogui.press('enter') #proxima página
for a in range(17):
    pyautogui.press('enter') #proxima página
clicaEspera((370,110)) #colunas
automation.waitFor((420,138),(59,59,59))
#automation.wait(10)
#clicaEspera((1330,10)) #fechar
#clicaEspera((670,400)) #orientação


