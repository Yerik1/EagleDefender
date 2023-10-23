import time
import pygame
import math

pygame.init()

# Configuración de la pantalla
window_width, window_height = 1300, 600
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Rectángulo para Copias")

# Colores
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)  # Color para el contorno del área permitida
RED = (255, 0, 0)    # Color para el puntero seleccionador

# Clase para gestionar las imágenes y copias
class ImageCopy:
    def __init__(self, image_path, x, y,life,amount):
        self.original_x, self.original_y = x, y
        self.rect_width, self.rect_height = 50, 50
        self.image_surface = pygame.Surface((self.rect_width, self.rect_height), pygame.SRCALPHA)
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (self.rect_width, self.rect_height))
        self.image_surface.blit(self.image, (0, 0))
        self.copies = []
        self.selected = False
        self.movable = True
        self.life=life
        self.amount=amount

    def update(self):
        pass  # No es necesario en esta versión

    def check_collision(self):
        combined_rect = pygame.Rect(self.original_x, self.original_y, self.rect_width, self.rect_height)
        rectangle_rect = pygame.Rect(100, 200, 600, 400)
        outside_bounds = not rectangle_rect.contains(combined_rect)

        if outside_bounds:
            self.original_x, self.original_y = self.initial_x, self.initial_y  # Volver a la posición original
        else:
            placed = False
            for image in [image1, image2, image3, image4]:
                for copy_rect in image.copies:
                    if copy_rect.colliderect(combined_rect):
                        self.original_x, self.original_y = self.initial_x, self.initial_y  # Volver a la posición original
                        return
                if rectangle_rect.contains(combined_rect):
                    placed = True

            if placed:
                if not self == image4:
                    if self.amount>0:
                        self.copies.append(combined_rect)
                        self.amount -= 1
                    self.original_x, self.original_y = self.initial_x, self.initial_y


    def move(self, cursor_x, cursor_y):
        if self.selected:
            # Restringir el movimiento dentro del área verde
            cursor_x = max(100, min(cursor_x, 700 - self.rect_width))
            cursor_y = max(200, min(cursor_y, 600 - self.rect_height))
            self.original_x = cursor_x
            self.original_y = cursor_y

    def draw(self):
        screen.blit(self.image_surface, (self.original_x, self.original_y))
        for copy_rect in self.copies:
            screen.blit(self.image_surface, copy_rect.topleft)

# Crear instancias para las cuatro imágenes
image1 = ImageCopy("Barriers/Barrier1.PNG", window_width // 2 - 200, 50,1,10)
image2 = ImageCopy("Barriers/Barrier2.PNG", window_width // 2 - 50, 50,2,10)
image3 = ImageCopy("Barriers/Barrier3.PNG", window_width // 2 + 100, 50,3,10)
image4 = ImageCopy("Backgrounds/Background2.PNG", window_width // 2 + 250, 50,3,1)

# Establecer la posición inicial
image1.initial_x, image1.initial_y = image1.original_x, image1.original_y
image2.initial_x, image2.initial_y = image2.original_x, image2.original_y
image3.initial_x, image3.initial_y = image3.original_x, image3.original_y
image4.initial_x, image4.initial_y = image4.original_x, image4.original_y

# Crear puntero
pointer_rect = pygame.Rect(0, 0, 50, 50)
pointer_rect.center = (window_width // 2, window_height // 2)
pointer_color = RED

font = pygame.font.Font(None, 36)  # Fuente predeterminada con un tamaño de 36 puntos

running = True
cursor_x, cursor_y = window_width // 2, window_height // 2

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    for image in [image1, image2, image3, image4]:
        if keys[pygame.K_f] and image.selected:
            image.selected = False
            image.check_collision()

    if keys[pygame.K_w]:
        cursor_y -= 5
        time.sleep(0.03)
    if keys[pygame.K_s]:
        cursor_y += 5
        time.sleep(0.03)
    if keys[pygame.K_a]:
        cursor_x -= 5
        time.sleep(0.03)
    if keys[pygame.K_d]:
        cursor_x += 5
        time.sleep(0.03)
    if keys[pygame.K_1]:
        if image1.movable and not image2.selected and not image3.selected and not image4.selected:
            if not image1.selected:
                image1.selected = True
            else:
                image1.selected = False
                image1.original_x, image1.original_y = image1.initial_x, image1.initial_y
            time.sleep(0.2)
    if keys[pygame.K_2]:
        if image2.movable and not image1.selected  and not image3.selected and not image4.selected:
            if not image2.selected:
                image2.selected = True
            else:
                image2.selected = False
                image2.original_x, image2.original_y = image2.initial_x, image2.initial_y
            time.sleep(0.2)
    if keys[pygame.K_3]:
        if image3.movable and not image1.selected and not image2.selected and not image4.selected:
            if not image3.selected:
                image3.selected = True
            else:
                image3.selected = False
                image3.original_x, image3.original_y = image3.initial_x, image3.initial_y
            time.sleep(0.2)
    if keys[pygame.K_4]:
        if image4.movable and not image1.selected and not image2.selected and not image3.selected:
            if not image4.selected:
                image4.selected = True
            else:
                image4.selected = False
                image4.check_collision()
            time.sleep(0.2)


    # Mantener el puntero dentro del área verde
    cursor_x = max(100, min(cursor_x, 650))
    cursor_y = max(200, min(cursor_y, 550))

    pointer_rect.topleft = (cursor_x, cursor_y)

    # Dibujar en la pantalla
    screen.fill(WHITE)

    for image in [image1, image2, image3, image4]:
        image.move(cursor_x, cursor_y)
        image.draw()

    # Dibujar el rectángulo permitido
    pygame.draw.rect(screen, GREEN, (100, 200, 600, 400), 2)

    # Dibujar el puntero
    pygame.draw.rect(screen, pointer_color, pointer_rect, 2)

    # Crear una superficie de texto (etiqueta)
    text1 = font.render(str(image1.amount), True, (255, 255, 255))
    text2 = font.render(str(image2.amount), True, (255, 255, 255))
    text3 = font.render(str(image3.amount), True, (255, 255, 255))

    # Posición de la etiqueta
    text1_rect = text1.get_rect()
    text1_rect.center = (window_width // 2 - 190, 75)
    text2_rect = text2.get_rect()
    text2_rect.center = (window_width // 2-40, 75)
    text3_rect = text3.get_rect()
    text3_rect.center = (window_width // 2 + 110, 75)

    screen.blit(text1, text1_rect.center)
    screen.blit(text2, text2_rect.center)
    screen.blit(text3, text3_rect.center)

    pygame.display.flip()

pygame.quit()
