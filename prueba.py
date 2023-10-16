import pygame
import tkinter as tk
from tkinter import *

pygame.init()

# Configuración de la pantalla
window_width, window_height = 600, 600
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Cuadrícula de Cuadros")

# Colores
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Coordenadas iniciales de la cuadrícula
#Cantidad de columnas y filas
grid_cols, grid_rows = 5, 3
#Tamaño en pixeles cuadricula
grid_width, grid_height = 500, 300
#Dimensiones de las celdas
cell_width = 100
cell_height = 100
#Posicion Inicial x
gridX=50
gridY=300


# Coordenadas iniciales del cuadro arrastrable
original_x, original_y = window_width // 2 - 50, 50
blue_rect = pygame.Rect(original_x, original_y, 100, 100)
dragging = False
offset_x, offset_y = 0, 0

# Lista para almacenar copias de la imagen
image_copies = []

# Cargar una imagen inicial
image = pygame.image.load("Barriers/Barrier1.PNG")
image = pygame.transform.scale(image, (blue_rect.width, blue_rect.height))  # Redimensionar la imagen



running = True
image_mode = False

while(running):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if blue_rect.collidepoint(event.pos):
                dragging = True
                offset_x = blue_rect.x - event.pos[0]
                offset_y = blue_rect.y - event.pos[1]

            if blue_rect.collidepoint(event.pos) and not image_mode:
                # Cambiar al modo de carga de imagen cuando se hace clic en el cuadro arrastrable
                image_mode = True
                image_path ="Barriers/Barrier1.PNG"
                try:
                    image = pygame.image.load(image_path)
                    image = pygame.transform.scale(image, (blue_rect.width, blue_rect.height))  # Redimensionar la imagen
                except pygame.error:
                    print("Error al cargar la imagen.")
                    image = None

        if event.type == pygame.MOUSEBUTTONUP:
            if dragging:
                dragging = False
                if image_mode and blue_rect.collidepoint(event.pos) and image is not None:
                    # Verificar si el cuadro azul se soltó dentro de la cuadrícula
                    if grid_width+gridX > event.pos[0] >= gridX and grid_height+gridY > event.pos[1] >= gridY:
                        col = (event.pos[0]-gridX)// cell_width
                        print(col)
                        row = event.pos[1] // cell_height
                        print(row)

                        # Crear una copia de la imagen en el centro de un cuadro de la cuadrícula
                        x_center = col * cell_width + cell_width // 2
                        print(x_center)
                        y_center = (row * cell_height + cell_height // 2)
                        print(y_center)
                        new_copy = image.copy()
                        new_copy_rect = new_copy.get_rect(center=(x_center+gridX, y_center))
                        image_copies.append(new_copy_rect)
                        image_mode = False

                # Devolver el cuadro arrastrable a la posición inicial arriba de la cuadrícula
                blue_rect.topleft = (original_x, original_y)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                # Restablecer la posición del cuadro arrastrable original cuando se presiona la tecla 'r'
                blue_rect.x = original_x
                blue_rect.y = original_y

    if dragging:
        blue_rect.x = pygame.mouse.get_pos()[0] + offset_x
        blue_rect.y = pygame.mouse.get_pos()[1] + offset_y

    # Dibujar el cuadro arrastrable en la pantalla
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, blue_rect)

    # Dibujar la imagen en el cuadro arrastrable
    screen.blit(image, blue_rect.topleft)

    # Dibujar la cuadrícula
    for col in range(grid_cols):
        for row in range(grid_rows):
            rect = pygame.Rect((col * cell_width)+50, (row * cell_height)+300, cell_width, cell_height)
            pygame.draw.rect(screen, BLUE, rect, 2)

    # Dibujar copias de la imagen
    for copy_rect in image_copies:
        screen.blit(image, copy_rect.topleft)

    pygame.display.flip()



pygame.quit()