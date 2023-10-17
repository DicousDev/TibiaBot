#import numpy as np
#import cv2

#big_image = cv2.imread("tibia.png")
#small_image = cv2.imread("vida_mana.png")

#w, h = small_image.shape[:-1]
#res = cv2.matchTemplate(big_image, small_image, cv2.TM_CCOEFF_NORMED)

#threshold = 0.8
#loc = np.where(res >= threshold)

#for pt in zip(*loc[::-1]):
  #print(f"pt: {pt[0]} - {pt[1]}")
  #cv2.rectangle(big_image, pt, (pt[0] + h, pt[1] + w), (0, 0, 255), 2)

#cv2.imwrite("resultado.png", big_image)


#from PIL import Image
#import pytesseract
#import re

##def filtrar_numeros(texto):
  #return re.findall(r'\d+', texto)

#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
#valores = pytesseract.image_to_string(Image.open('vida_mana.png'))
#vida_e_mana = filtrar_numeros(valores)
#vida = vida_e_mana[0]
#mana = vida_e_mana[1]
#print(f"vida: {vida} - mana: {mana}")

from PIL import ImageGrab
from pynput import mouse
import pytesseract
import re
from pynput.keyboard import Key, Controller

keyboard = Controller()
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def filtrar_numeros(texto):
  return re.findall(r'\d+', texto)

def capturar_tela(nome_arquivo='captura_tela.png'):
    #Capturar
    imagem = ImageGrab.grab()
    #Salvar
    imagem.save(nome_arquivo)
    print(f'A captura de tela foi salva como "{nome_arquivo}".')

def obter_vida_e_mana(box):
  imagem = ImageGrab.grab()
  imagem_recortada = imagem.crop(box)
  valores = pytesseract.image_to_string(imagem_recortada)
  vida_e_mana = filtrar_numeros(valores)

  vida = 1
  mana = 1
  if(len(vida_e_mana) == 2):
    vida = vida_e_mana[0]
    mana = vida_e_mana[1]
  return {'vida': vida, 'mana': mana}

def curar_quando_for_necessario(box):

  vida_mana = obter_vida_e_mana(box)
  vida = vida_mana['vida']
  mana = vida_mana['mana']
  print(f"vida: {vida} - mana: {mana}")
  if(int(vida) <= 2000):
    keyboard.press(Key.f1)

quantidade_clicks = 0
origin_x = 0
origin_y = 0
final_x = 0
final_y = 0

def on_click(x, y, button, pressed):
  global quantidade_clicks
  global origin_x
  global origin_y
  global final_x
  global final_y
  if(button is mouse.Button.left and pressed and quantidade_clicks < 2):
    quantidade_clicks += 1

    print(f"Clicado {quantidade_clicks}.")
    if(quantidade_clicks == 1):
      origin_x = x
      origin_y = y
    elif(quantidade_clicks == 2):
      final_x = x
      final_y = y
      capturar_tela()
      print("Configurado com sucesso!")

  elif(button is mouse.Button.right and pressed and quantidade_clicks >= 2):
    print("Resetado!")
    #quantidade_clicks = 0

listener = mouse.Listener(on_click=on_click)
listener.start()

while(True):
  if(quantidade_clicks >= 2):
    box = (origin_x, 
           origin_y, 
           final_x,
           final_y)
    print(box)
    curar_quando_for_necessario(box)