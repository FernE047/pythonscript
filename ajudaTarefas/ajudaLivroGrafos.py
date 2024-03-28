import pyautogui
import time

#ajuda a nomear as fotos retiradas do livro 'Grafos'

a=90;
for a in range(230,314):
    for c in range(2):
        b=input();
        pyautogui.click(340,750);
        pyautogui.keyDown('ctrlleft');
        pyautogui.keyDown('shiftleft');
        pyautogui.press('x');
        pyautogui.keyUp('shiftleft');
        pyautogui.keyUp('ctrlleft');
        time.sleep(2);
        if ((c%2)==1):
            pyautogui.keyDown('ctrlleft');
            pyautogui.press('h');
            pyautogui.keyUp('ctrlleft');
        else:
            pyautogui.keyDown('ctrlleft');
            pyautogui.press('g');
            pyautogui.keyUp('ctrlleft');
        pyautogui.keyDown('ctrlleft');
        pyautogui.press('w');
        pyautogui.keyUp('ctrlleft');
        pyautogui.press('enter');
        pyautogui.press('enter');
        time.sleep(2);
        pyautogui.press('altleft');
        pyautogui.press('a');
        pyautogui.press('a');
        time.sleep(1);
        nome='A'+str(a+1);
        if(c==0):
            nome=nome+'A'
        else:
            nome=nome+'B'
        nome=nome+'.jpg'
        pyautogui.typewrite(nome);
        pyautogui.press('enter');
