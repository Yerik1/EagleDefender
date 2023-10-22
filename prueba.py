import pygame
import time
pygame.init()

# Configuración de la pantalla
window_width, window_height = 1200, 600
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Cuadrícula de Cuadros")

moving_left = False
moving_right = False
moving_up = False
moving_down = False

red_sqr_timer = 0
movement_delay = 100  # 100 milisegundos
# Colores
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Coordenadas iniciales de la cuadrícula
grid_cols, grid_rows = 10, 6
grid_width, grid_height = 500, 300
cell_width = 50
cell_height = 50
gridX = 50
gridY = 300

# Coordenadas iniciales de los cuadros arrastrables
original_x, original_y = gridX + 2*grid_width // 4 - 50, 50

# Coordenadas iniciales del cuadro rojo (mitad derecha)
red_sqr = pygame.Rect(gridX + grid_width // 2, 300, 50, 50)
red_sqr_speed = 50  # Velocidad de movimiento del cuadro rojo

# Crear rectángulos para los cuadros arrastrables
blue_rect = pygame.Rect(original_x, original_y, 50, 50)
green_rect = pygame.Rect(original_x-150, original_y, 50, 50)
red_rect = pygame.Rect(original_x+150, original_y, 50, 50)

# Variables para rastrear el estado de arrastre de los cuadros
dragging_blue = False
dragging_green = False
dragging_red = False

offset_x = 0
offset_y = 0

# Lista para almacenar copias de la imagen
image1_copies = []
image2_copies = []
image3_copies = []

# Matriz para registrar los bloques en la cuadrícula
grid_matrix = [[0] * grid_cols for _ in range(grid_rows)]

# Cargar una imagen inicial
image2 = pygame.image.load("Barriers/Barrier2.PNG")
image2 = pygame.transform.scale(image2, (blue_rect.width, blue_rect.height))

# Cargar una imagen inicial
image1 = pygame.image.load("Barriers/Barrier1.PNG")
image1 = pygame.transform.scale(image1, (blue_rect.width, blue_rect.height))

# Cargar una imagen inicial
image3 = pygame.image.load("Barriers/Barrier3.PNG")
image3 = pygame.transform.scale(image3, (blue_rect.width, blue_rect.height))


def decrease_value(row, col, image_copies, cell_width, cell_height, gridX, gridY):
    if grid_matrix[row][col] > 0:
        grid_matrix[row][col] -= 1
        if grid_matrix[row][col] == 0:
            # Convertir las coordenadas de píxeles a posiciones de celdas
            pixel_x = col * cell_width + gridX
            pixel_y = row * cell_height + gridY
            # Eliminar la imagen correspondiente en base a las coordenadas de píxeles
            for copy in list(image_copies):
                if copy.collidepoint(pixel_x, pixel_y):
                    image_copies.remove(copy)
    for casilla in grid_matrix:
        print(casilla)

def is_cell_empty(row, col):
    flag=True
    if grid_matrix[row][col] > 0:
        flag=False
    return flag


running = True
image_mode = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            case = ""
            if blue_rect.collidepoint(event.pos):
                case = "2"
                dragging_blue = True
                offset_x = blue_rect.x - event.pos[0]
                offset_y = blue_rect.y - event.pos[1]
            elif green_rect.collidepoint(event.pos):
                case = "1"
                dragging_green = True
                offset_x = green_rect.x - event.pos[0]
                offset_y = green_rect.y - event.pos[1]
            elif red_rect.collidepoint(event.pos):
                case = "3"
                dragging_red = True
                offset_x = red_rect.x - event.pos[0]
                offset_y = red_rect.y - event.pos[1]

            if any([rect.collidepoint(event.pos) for rect in [blue_rect, green_rect, red_rect]]) and not image_mode:
                image_mode = True
                image_path = "Barriers/Barrier" + case + ".PNG"
                try:
                    image = pygame.image.load(image_path)
                    image = pygame.transform.scale(image, (blue_rect.width, blue_rect.height))
                except pygame.error:
                    print("Error al cargar la imagen.")
                    image = None

        if event.type == pygame.MOUSEBUTTONUP:
            if dragging_blue:
                dragging_blue = False
                if image_mode and blue_rect.collidepoint(event.pos) and image2 is not None:
                    if grid_width + gridX > event.pos[0] >= gridX and grid_height + gridY > event.pos[1] >= gridY:
                        col = (event.pos[0] - gridX) // cell_width
                        row = (event.pos[1] - gridY) // cell_height
                        x_center = col * cell_width + cell_width // 2
                        y_center = row * cell_height + cell_height // 2
                        if is_cell_empty(row, col):
                            new_copy = image2.copy()
                            new_copy_rect = new_copy.get_rect(center=(x_center + gridX, y_center + gridY))
                            image2_copies.append(new_copy_rect)
                            image2_mode = False
                            grid_matrix[row][col] = 2
                    blue_rect.topleft = (original_x, original_y)

            elif dragging_green:
                dragging_green = False
                if image_mode and green_rect.collidepoint(event.pos) and image1 is not None:
                    if grid_width + gridX > event.pos[0] >= gridX and grid_height + gridY > event.pos[1] >= gridY:
                        col = (event.pos[0] - gridX) // cell_width
                        row = (event.pos[1] - gridY) // cell_height
                        x_center = col * cell_width + cell_width // 2
                        y_center = row * cell_height + cell_height // 2
                        if is_cell_empty(row, col):
                            new_copy = image1.copy()
                            new_copy_rect = new_copy.get_rect(center=(x_center + gridX, y_center + gridY))
                            image1_copies.append(new_copy_rect)
                            image1_mode = False
                            grid_matrix[row][col] = 1
                    green_rect.topleft = (original_x - 150, original_y)

            elif dragging_red:
                dragging_red = False
                if image_mode and red_rect.collidepoint(event.pos) and image3 is not None:
                    if grid_width + gridX > event.pos[0] >= gridX and grid_height + gridY > event.pos[1] >= gridY:
                        col = (event.pos[0] - gridX) // cell_width
                        row = (event.pos[1] - gridY) // cell_height
                        x_center = col * cell_width + cell_width // 2
                        y_center = row * cell_height + cell_height // 2
                        if is_cell_empty(row, col):
                            new_copy = image3.copy()
                            new_copy_rect = new_copy.get_rect(center=(x_center + gridX, y_center + gridY))
                            image3_copies.append(new_copy_rect)
                            image3_mode = False
                            grid_matrix[row][col] = 3
                    red_rect.topleft = (original_x + 150, original_y)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            # Manejar el clic derecho para disminuir el valor de la matriz
            col = (event.pos[0] - gridX) // cell_width
            row = (event.pos[1] - gridY) // cell_height
            if 0 <= row < grid_rows and 0 <= col < grid_cols:
                if grid_matrix[row][col] > 0:
                    if any([copy.collidepoint(event.pos) for copy in image2_copies]):
                        decrease_value(row, col, image2_copies, cell_width, cell_height, gridX, gridY)
                    elif any([copy.collidepoint(event.pos) for copy in image1_copies]):
                        decrease_value(row, col, image1_copies, cell_width, cell_height, gridX, gridY)
                    elif any([copy.collidepoint(event.pos) for copy in image3_copies]):
                        decrease_value(row, col, image3_copies, cell_width, cell_height, gridX, gridY)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                blue_rect.topleft = (original_x, original_y)
                green_rect.topleft = (original_x - 150, original_y)
                red_rect.topleft = (original_x + 150, original_y)
                grid_matrix = [["0"] * grid_cols for _ in range(grid_rows)]
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    moving_left = True
                elif event.key == pygame.K_RIGHT:
                    moving_right = True
                elif event.key == pygame.K_UP:
                    moving_up = True
                elif event.key == pygame.K_DOWN:
                    moving_down = True
                #red_sqr_timer = pygame.time.get_ticks()

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                moving_left = False
            elif event.key == pygame.K_RIGHT:
                moving_right = False
            elif event.key == pygame.K_UP:
                moving_up = False
            elif event.key == pygame.K_DOWN:
                moving_down = False

        if moving_left:
            red_sqr.x -= red_sqr_speed
            moving_left = False
            # keys_pressed.discard(pygame.K_LEFT)
            time.sleep(0.1)
        if moving_right:
            red_sqr.x += red_sqr_speed
            moving_right = False
            #keys_pressed.discard(pygame.K_RIGHT)
            time.sleep(0.1)
        if moving_up:
            red_sqr.y -= red_sqr_speed
            moving_up = False
            #keys_pressed.discard(pygame.K_UP)
            time.sleep(0.1)
        if moving_down:
            red_sqr.y += red_sqr_speed
            moving_down = False
            #keys_pressed.discard(pygame.K_DOWN)
            time.sleep(0.1)
        #red_sqr_timer = pygame.time.get_ticks()





    # Asegurarnos de que el cuadro rojo esté confinado a la mitad derecha de la cuadrícula
    red_sqr.x = max(gridX + 2*grid_width // 2, min(red_sqr.x, gridX + 2*grid_width - cell_width))
    red_sqr.y = max(gridY, min(red_sqr.y, gridY + grid_height - cell_height))
    if dragging_blue:
        blue_rect.x = pygame.mouse.get_pos()[0] + offset_x
        blue_rect.y = pygame.mouse.get_pos()[1] + offset_y
    elif dragging_green:
        green_rect.x = pygame.mouse.get_pos()[0] + offset_x
        green_rect.y = pygame.mouse.get_pos()[1] + offset_y
    elif dragging_red:
        red_rect.x = pygame.mouse.get_pos()[0] + offset_x
        red_rect.y = pygame.mouse.get_pos()[1] + offset_y

    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, blue_rect)
    pygame.draw.rect(screen, (0, 255, 0), green_rect)
    pygame.draw.rect(screen, (255, 0, 0), red_rect)
    pygame.draw.rect(screen,RED,red_sqr)

    screen.blit(image2, blue_rect.topleft)
    screen.blit(image1, green_rect.topleft)
    screen.blit(image3, red_rect.topleft)

    for col in range(grid_cols):
        for row in range(grid_rows):
            rect = pygame.Rect((col * cell_width) + 50, (row * cell_height) + 300, cell_width, cell_height)
            pygame.draw.rect(screen, BLUE, rect, 2)

    for copy_rect in image2_copies:
        screen.blit(image2, copy_rect.topleft)
    for copy_rect in image3_copies:
        screen.blit(image3, copy_rect.topleft)
    for copy_rect in image1_copies:
        screen.blit(image1, copy_rect.topleft)

    pygame.display.flip()

pygame.quit()