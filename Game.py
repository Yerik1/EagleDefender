import threading
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
BLUE= (0, 0, 255)

# Clase para gestionar las imágenes y copias
class Barriers:
    def __init__(self, image_path, x, y,life,amount,copy=False,original=None):
        if copy:
            self.original_x, self.original_y = original.original_x, original.original_y
        else:
            self.original_x, self.original_y = x, y

        self.player_x, self.player_y = self.original_x, self.original_y
        self.rect_width, self.rect_height = 50, 50
        self.image_path=image_path
        self.image_surface = pygame.Surface((self.rect_width, self.rect_height), pygame.SRCALPHA)
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (self.rect_width, self.rect_height))
        self.image_surface.blit(self.image, (0, 0))
        self.copies = []
        self.selected = False
        self.movable = True
        self.life = life
        self.amount = amount
        self.combinedRect = ""

    def create_copy(self, player_x, player_y):
        copy = Barriers(self.image_path, self.original_x, self.original_y, self.life, 1, copy=True, original=self)
        copy.selected = False
        return copy
    def check_collision(self):
        self.combined_rect = pygame.Rect(self.original_x, self.original_y, self.rect_width, self.rect_height)
        rectangle_rect = pygame.Rect(100, 200, 600, 400)
        outside_bounds = not rectangle_rect.contains(self.combined_rect)

        if outside_bounds:
            return  # No hagas nada si está fuera de los límites

        placed = False
        for image in [image1, image2, image3, image4]:
            for copy in image.copies:
                copy.combinedRect = pygame.Rect(copy.original_x, copy.original_y, copy.rect_width, copy.rect_height)
                if self.combined_rect.colliderect(copy.combinedRect):
                    # Copia detectada, detener el movimiento y recordar con qué Barrier colisionó
                    return

            if rectangle_rect.contains(self.combined_rect):
                placed = True

        if placed:
            if not self == image4:
                if self.amount > 0:
                    self.combinedRect = self.combined_rect
                    self.copies.append(self.create_copy(self.original_x, self.original_y))
                    self.amount -= 1
                self.original_x, self.original_y = self.initial_x, self.initial_y


    def moveDefender(self, cursor_x, cursor_y):
        if self.selected:
            # Restringir el movimiento dentro del área verde
            cursor_x = max(50, min(cursor_x, 600 - self.rect_width))
            cursor_y = max(200, min(cursor_y, 600 - self.rect_height))
            self.original_x = cursor_x
            self.original_y = cursor_y

    def draw(self):
        screen.blit(self.image_surface, (self.original_x, self.original_y))
        for copy_rect in self.copies:
            screen.blit(self.image_surface, (copy_rect.original_x, copy_rect.original_y))

    def recieveDamage(self,damage,copy_rect):
        copy_rect.life -= damage
        print("Vida de Barrier:", copy_rect.life)
        if copy_rect.life <= 0:
            return True
        else:
            return False

# Clase para gestionar las imágenes y copias de Poderes
class Powers:
    def __init__(self, image_path, x, y, damage, amount):
        self.original_x, self.original_y = x, y
        self.player_x, self.player_y = x, y
        self.rect_width, self.rect_height = 50, 50
        self.destination_x=x
        self.destination_y = y
        self.image_path=image_path
        self.image_surface = pygame.Surface((self.rect_width, self.rect_height), pygame.SRCALPHA)
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (self.rect_width, self.rect_height))
        self.image_surface.blit(self.image, (0, 0))
        self.copies = []
        self.selected = False
        self.damage = damage
        self.amount = amount
        self.clicked = False  # Variable para indicar si se ha hecho clic en la imagen

    def check_collision(self):
        # El código de colisión es el mismo que en la clase Barriers
        pass

    def moveAtacker(self, player_x, player_y):
        if self.selected:
            # Restringir el movimiento dentro del área verde
            player_x = max(650, min(player_x, 1200))
            player_y = max(200, min(player_y, 550))
            self.player_x = player_x
            self.player_y = player_y

    def draw(self):
        if self.clicked:
            pygame.draw.rect(screen, (255, 255, 0), (self.original_x-2, self.original_y-2, self.rect_width+4, self.rect_height+4), 2)
        screen.blit(self.image_surface, (self.original_x, self.original_y))

    def create_copy(self, player_x, player_y):
        copy = Powers(self.image_path, player_x, player_y, self.damage, self.amount)
        copy.selected = False
        return copy


# Crear instancias para las cuatro imágenes
image1 = Barriers("Barriers/Barrier1.PNG", window_width // 4 - 200, 50, 1, 10)
image2 = Barriers("Barriers/Barrier2.PNG", window_width // 4 - 50, 50, 2, 10)
image3 = Barriers("Barriers/Barrier3.PNG", window_width // 4 + 100, 50, 3, 10)
image4 = Barriers("Backgrounds/Background2.PNG", window_width // 4 + 250, 50, 3, 1)

# Crear instancias para las imágenes de Poderes
power1 = Powers("Powers/WaterBalls/WB1.PNG", 3*window_width // 4 - 200, 50, 1, 3)
power2 = Powers("Powers/FireBalls/FB1.PNG", 3*window_width // 4 - 50, 50, 2, 2)
power3 = Powers("Powers/Bombs/Bomb1.PNG", 3*window_width // 4 + 100, 50, 3, 4)



# Establecer la posición inicial
image1.initial_x, image1.initial_y = image1.original_x, image1.original_y
image2.initial_x, image2.initial_y = image2.original_x, image2.original_y
image3.initial_x, image3.initial_y = image3.original_x, image3.original_y
image4.initial_x, image4.initial_y = image4.original_x, image4.original_y

# Establecer la posición inicial
power1.initial_x, power1.initial_y = power1.original_x, power1.original_y
power2.initial_x, power2.initial_y = power2.original_x, power2.original_y
power3.initial_x, power3.initial_y = power3.original_x, power3.original_y

# Crear puntero
pointer_rect = pygame.Rect(0, 0, 50, 50)
pointer_rect.center = (window_width // 4, window_height // 2)
pointer_color = BLUE

# Crear atacante
player = pygame.Rect(0, 0, 50, 50)
player.center = (3*window_width // 4, window_height // 2)
player_color = RED
font = pygame.font.Font(None, 36)  # Fuente predeterminada con un tamaño de 36 puntos

running = True
cursor_x, cursor_y = window_width // 4, window_height // 2
player_x, player_y = 3*window_width // 4, window_height // 2

selected_image_to_move = None
def move_player():
    global player_x, player_y
    while running:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player_y -= 5
        if keys[pygame.K_DOWN]:
            player_y += 5
        if keys[pygame.K_LEFT]:
            player_x -= 5
        if keys[pygame.K_RIGHT]:
            player_x += 5
        time.sleep(0.03)

# Función para el movimiento del puntero en un hilo separado
def move_pointer():
    global cursor_x, cursor_y
    while running:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            cursor_y -= 5
        if keys[pygame.K_s]:
            cursor_y += 5
        if keys[pygame.K_a]:
            cursor_x -= 5
        if keys[pygame.K_d]:
            cursor_x += 5
        time.sleep(0.03)

def check_click(image, cursor_x, cursor_y):
    if image.original_x < cursor_x < image.original_x + image.rect_width and \
            image.original_y < cursor_y < image.original_y + image.rect_height:
        image.clicked = True
        if isinstance(image, Powers):  # Verifica si es una imagen de poder
            # Inicia un hilo de movimiento al hacer clic en la imagen de poder
            movement_thread = threading.Thread(target=move_selected_image, args=(image,))
            movement_thread.start()
        return True
    else:
        image.clicked = False

# Función para mover la imagen seleccionada
def move_selected_image(image_copy):
    x, y = image_copy.player_x, image_copy.player_y
    dest_x, dest_y = image_copy.destination_x, image_copy.destination_y

    # Calcular el ángulo y la distancia entre la posición actual y el destino
    angle = math.atan2(dest_y - y, dest_x - x)
    distance = math.hypot(dest_x - x, dest_y - y)

    while distance > 0:
        step = min(1, distance)  # Mover hasta 1 píxel en cada paso
        x += step * math.cos(angle)
        y += step * math.sin(angle)
        distance -= step

        # Verificar colisiones con copias de Barrier
        for barrier in [image1, image2, image3, image4]:
            for copy in barrier.copies:
                copy.combinedRect = pygame.Rect(copy.original_x, copy.original_y, copy.rect_width, copy.rect_height)
                if pygame.Rect(x, y, image_copy.rect_width, image_copy.rect_height).colliderect(copy.combinedRect):
                    # Colisión detectada, detener el movimiento y eliminar la copia de Barrier
                    distance = 0
                    print("entro")
                    if(barrier.recieveDamage(image_copy.damage, copy) ): # Actualiza la vida y elimina la copia
                        barrier.copies.remove(copy)  # Elimina la copia
                        power1.copies.remove(image_copy)
                        power2.copies.remove(image_copy)
                        power3.copies.remove(image_copy)

        # Actualizar la posición final de la copia
        image_copy.original_x = x
        image_copy.original_y = y

        # Actualizar la copia en la pantalla

        screen.blit(image_copy.image_surface, (image_copy.original_x, image_copy.original_y))
        pygame.display.flip()
        time.sleep(0.0005)



# Función para verificar si el clic está dentro del área verde
def is_inside_green_area(x, y):
    return 50 < x < 650 and 200 < y < 600


# Iniciar el hilo para el movimiento del jugador
player_thread = threading.Thread(target=move_player)
player_thread.start()

# Crear un hilo para el movimiento del puntero
pointer_thread = threading.Thread(target=move_pointer)
pointer_thread.start()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    other_rects = []
    for image in [image1, image2, image3, image4]:
        if image.selected:
            other_rects.extend(image.copies)

    for image in [image1, image2, image3, image4]:
        if keys[pygame.K_f] and image.selected:
            image.selected = False
            image.check_collision()

    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:  # Botón izquierdo del ratón
            selection_x, selection_y = pygame.mouse.get_pos()
            if is_inside_green_area(selection_x, selection_y):
                if selected_image_to_move is not None:
                    for power in [power1, power2, power3]:
                        if selected_image_to_move == power:
                            power.amount -= 1
                    destination_x, destination_y = event.pos

                    # Crear una copia de la imagen seleccionada en la posición del jugador
                    selected_image_copy = selected_image_to_move.create_copy(player_x, player_y)
                    selected_image_copy.selected = False

                    # Definir el destino de la copia
                    selected_image_copy.destination_x = destination_x
                    selected_image_copy.destination_y = destination_y

                    # Agregar la copia a la lista de copias del Barrier
                    selected_image_to_move.copies.append(selected_image_copy)

                    # Iniciar un hilo para mover la copia
                    movement_thread = threading.Thread(target=move_selected_image, args=(selected_image_copy,))
                    movement_thread.start()
                    time.sleep(0.3)
            else:
                # Comprueba si se hizo clic en las imágenes de Poderes
                for power in [power1, power2, power3]:
                    if check_click(power, selection_x, selection_y):
                        selected_image_to_move=power

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
    cursor_x = max(50, min(cursor_x, 600))
    cursor_y = max(200, min(cursor_y, 550))

    pointer_rect.topleft = (cursor_x, cursor_y)

    # Mantener el puntero dentro del área verde
    player_x = max(650, min(player_x, 1200))
    player_y = max(200, min(player_y, 550))

    player.topleft = (player_x, player_y)

    # Dibujar en la pantalla
    screen.fill(WHITE)

    for image in [image1, image2, image3, image4]:
        image.moveDefender(cursor_x, cursor_y)
        image.draw()

    for image in [power1, power2, power3]:
        image.moveAtacker(player_x, player_y)
        image.draw()


    # Dibujar el rectángulo permitido
    pygame.draw.rect(screen, GREEN, (50, 200, 600, 400), 2)
    pygame.draw.rect(screen, RED, (650, 200, 600, 400), 2)

    # Dibujar el puntero
    pygame.draw.rect(screen, pointer_color, pointer_rect, 2)
    pygame.draw.rect(screen, player_color, player, 2)

    # Crear una superficie de texto (etiqueta)
    text1 = font.render(str(image1.amount), True, (255, 255, 255))
    text2 = font.render(str(image2.amount), True, (255, 255, 255))
    text3 = font.render(str(image3.amount), True, (255, 255, 255))
    text4 = font.render(str(power1.amount), True, (255, 255, 255))
    text5 = font.render(str(power2.amount), True, (255, 255, 255))
    text6 = font.render(str(power3.amount), True, (255, 255, 255))

    # Posición de la etiqueta
    text1_rect = text1.get_rect()
    text1_rect.center = (window_width // 4 - 190, 75)
    text2_rect = text2.get_rect()
    text2_rect.center = (window_width // 4-40, 75)
    text3_rect = text3.get_rect()
    text3_rect.center = (window_width // 4 + 110, 75)
    text4_rect = text1.get_rect()
    text4_rect.center = (3*window_width // 4 - 190, 75)
    text5_rect = text2.get_rect()
    text5_rect.center = (3*window_width // 4 - 40, 75)
    text6_rect = text3.get_rect()
    text6_rect.center = (3*window_width // 4 + 110, 75)

    screen.blit(text1, text1_rect.center)
    screen.blit(text2, text2_rect.center)
    screen.blit(text3, text3_rect.center)
    screen.blit(text4, text4_rect.center)
    screen.blit(text5, text5_rect.center)
    screen.blit(text6, text6_rect.center)

    pygame.display.flip()

pygame.quit()
