import pyautogui
import cv2
import numpy as np
import time

minimap_top_left_screen_window_pixel_horizontal = 1729
minimap_top_left_screen_window_pixel_vertical = 29
minimap_center_character_screen_window_pixel_horizontal = 1806
minimap_center_character_screen_window_pixel_vertical = 81
tile_size = 4
size_mapa_pixel_horizontal = 26
size_mapa_pixel_vertical = 26
metade_size_mapa_pixel_horizontal = 13
metade_size_mapa_pixel_vertical = 13

# https://www.tibiabr.com/downloads/mapas/
coordenada_player_start_x = 32681
coordenada_player_start_y = 31683
coordenada_player_atual_x = coordenada_player_start_x
coordenada_player_atual_y = coordenada_player_start_y
coordenada_player_destination_x = 32681
coordenada_player_destination_y = 31690
coordenada_top_left_start_x = coordenada_player_start_x - 13
coordenada_top_left_start_y = coordenada_player_start_y - 13
player_is_walking = False
player_moving_to_destination = False

# x, y, width, height
region_minimap = (1751, 25, 112, 114)

waypoint_atual = 1
waypoints = (32681, 31683, 32681, 31690)

def verifica_mudanca_entre_imagens(imagem1, imagem2, limiar=30):
  # Converte as imagens para escala de cinza
  cinza1 = cv2.cvtColor(np.array(imagem1), cv2.COLOR_BGR2GRAY)
  cinza2 = cv2.cvtColor(np.array(imagem2), cv2.COLOR_BGR2GRAY)

  # Calcula a diferença absoluta entre as imagens
  diff = cv2.absdiff(cinza1, cinza2)

  # Aplica um limiar para destacar as diferenças
  _, threshold = cv2.threshold(diff, limiar, 255, cv2.THRESH_BINARY)

  # Conta o número de pixels diferentes
  total_pixels_diferentes = int(np.sum(threshold) / 255)

  # Exibe o número de pixels diferentes
  #print(f"Número de pixels diferentes: {int(total_pixels_diferentes)}")
  return total_pixels_diferentes > 0

def characterPositionToScreenPositionMinimap(coordenada_x, coordenada_y):
  global minimap_center_character_screen_window_pixel_horizontal
  global minimap_center_character_screen_window_pixel_vertical
  global tile_size
  global coordenada_player_atual_x
  global coordenada_player_atual_y

  position_screen_window_x = 0
  different_x = coordenada_player_atual_x - coordenada_x
  if(different_x < 0):
    # É da esquerda para direita
    position_screen_window_x = minimap_center_character_screen_window_pixel_horizontal + tile_size * (different_x * -1)
  else:
    # É da direita para esquerda
    position_screen_window_x = minimap_center_character_screen_window_pixel_horizontal - tile_size * different_x

  position_screen_window_y = 0
  different_y = coordenada_y - coordenada_player_atual_y
  if(different_y < 0):
    # É de baixo para cima
    position_screen_window_y = minimap_center_character_screen_window_pixel_vertical + tile_size * different_y
  else:
    # É de cima para baixo
    position_screen_window_y = minimap_center_character_screen_window_pixel_vertical + tile_size * different_y


  return (position_screen_window_x, position_screen_window_y)

def goToPositionByMinimap(coordenada_mapa_destination_x, coordenada_mapa_destination_y):
  global player_moving_to_destination
  position_screen_window = characterPositionToScreenPositionMinimap(coordenada_mapa_destination_x, coordenada_mapa_destination_y)
  pyautogui.click(position_screen_window[0], position_screen_window[1])
  player_moving_to_destination = True
  print("PLAYER MOVENDO PARA COORDENADA!")

goToPositionByMinimap(coordenada_player_destination_x, coordenada_player_destination_y)
while(True):
  img = pyautogui.screenshot(region=region_minimap)
  time.sleep(0.25)
  img2 = pyautogui.screenshot(region=region_minimap)
  player_is_walking = verifica_mudanca_entre_imagens(img, img2, 0.98)

  if(player_moving_to_destination and player_is_walking is False):
    player_moving_to_destination = False
    player_is_walking = False
    coordenada_player_atual_x = coordenada_player_destination_x
    coordenada_player_atual_y = coordenada_player_destination_y
    print("CHEGOU NO DESTINO!")
    time.sleep(3)
    waypoint_atual += 1
    if(waypoint_atual == 3):
      waypoint_atual = 1

    if(waypoint_atual == 1):
      coordenada_player_destination_x = waypoints[2]
      coordenada_player_destination_y = waypoints[3]
      goToPositionByMinimap(coordenada_player_destination_x, coordenada_player_destination_y)
    elif(waypoint_atual == 2):
      coordenada_player_destination_x = coordenada_player_start_x
      coordenada_player_destination_y = coordenada_player_start_y
      goToPositionByMinimap(coordenada_player_destination_x, coordenada_player_destination_y)
    
