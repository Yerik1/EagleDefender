import threading
import time
import pygame
import math
import os
import glob
from PIL import ImageDraw, ImageTk, Image, ImageFilter
import ColorFilter

player1Rounds=0
player2Rounds=0
win=False

# Ruta de la carpeta que contiene las imágenes
carpeta_imagenes = "Goblin"  # Reemplaza con la ruta de tu carpeta de imágenes

# Patrón de archivos de imagen que deseas buscar (por ejemplo, todos los archivos .png)
patron = "*.png"

# Inicializa una lista para almacenar las rutas de las imágenes encontradas
imagenes = []

# Utiliza la función glob para buscar archivos que coincidan con el patrón en la carpeta
archivos = glob.glob(os.path.join(carpeta_imagenes, patron))

for element in archivos:
    image = pygame.image.load(element)
    image = pygame.transform.scale(image, (50, 50))
    # Agrega las rutas de los archivos encontrados a la lista de imágenes
    imagenes.append(image)

print(imagenes)

class Game:
    def __init__(self,player1,player2):
        pygame.init()
        # Configuración de la pantalla
        self.window_width, self.window_height = 1300, 600
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        self.player1=player1
        self.player2=player2
        pygame.display.set_caption("Rectángulo para Copias")

        self.goblin = pygame.image.load("Goblin/StandUpIzquier.png")
        self.goblin = pygame.transform.scale(self.goblin, (50, 50))
        # Colores
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)  # Color para el contorno del área permitida
        self.RED = (255, 0, 0)    # Color para el puntero seleccionador
        self.BLUE= (0, 0, 255)
        self.movementThreads=[]
        self.player_thread=""
        self.pointer_thread=""
        self.timer_label=""
        self.font=""
        self.timeDefense=0
        self.timeGame=0
        self.game=False
        self.direction=False
    def begin(self):
        global win, imagenes
        self.running = True
        self.cursor_x, self.cursor_y = self.window_width // 4, self.window_height // 2
        self.player_x, self.player_y = 3 * self.window_width // 4, self.window_height // 2
        self.selected_image_to_move = None

        # Iniciar el hilo para el movimiento del jugador
        self.player_thread = threading.Thread(target=self.move_player)
        self.player_thread.start()

        # Crear un hilo para el movimiento del puntero
        self.pointer_thread = threading.Thread(target=self.move_pointer)
        self.pointer_thread.start()



        # Crear instancias para las cuatro imágenes
        self.image1 = Barriers("Barriers/Barrier1.PNG", self.window_width // 4 - 200, 50, 1, 10,self)
        self.image2 = Barriers("Barriers/Barrier2.PNG", self.window_width // 4 - 50, 50, 2, 10,self)
        self.image3 = Barriers("Barriers/Barrier3.PNG", self.window_width // 4 + 100, 50, 3, 10,self)
        self.image4 = Barriers("Eagle/Eagle.png", self.window_width // 4 - 275, 375, 3, 1,self)

        # Crear instancias para las imágenes de Poderes
        self.power1 = Powers("Powers/WaterBalls/WB1.PNG", 3 * self.window_width // 4 - 200, 50, 1, 3,self)
        self.power2 = Powers("Powers/FireBalls/FB1.PNG", 3 * self.window_width // 4 - 50, 50, 2, 2,self)
        self.power3 = Powers("Powers/Bombs/Bomb1.PNG", 3 * self.window_width // 4 + 100, 50, 3, 4,self)

        # Establecer la posición inicial
        self.image1.initial_x, self.image1.initial_y = self.image1.original_x, self.image1.original_y
        self.image2.initial_x, self.image2.initial_y = self.image2.original_x, self.image2.original_y
        self.image3.initial_x, self.image3.initial_y = self.image3.original_x, self.image3.original_y
        self.image4.initial_x, self.image4.initial_y = self.image4.original_x, self.image4.original_y

        # Establecer la posición inicial
        self.power1.initial_x, self.power1.initial_y = self.power1.original_x, self.power1.original_y
        self.power2.initial_x, self.power2.initial_y = self.power2.original_x, self.power2.original_y
        self.power3.initial_x, self.power3.initial_y = self.power3.original_x, self.power3.original_y

        self.bg_image1 = pygame.image.load("Backgrounds/Background2.PNG")
        self.bg_image1 = pygame.transform.scale(self.bg_image1, (600,400))
        self.bg_image1 = Image.frombytes("RGB", self.bg_image1.get_size(),
                                        pygame.image.tostring(self.bg_image1, "RGB", False))
        self.bg_image1 = ColorFilter.colorFilter("#%02x%02x%02x" % self.GREEN, self.bg_image1)
        # Aplica el filtro de color con PIL
        # En este ejemplo, se aplica un filtro de desenfoque a la imagen
        # Convierte la imagen de PIL de nuevo a Pygame
        self.bg_image1 = pygame.image.fromstring(self.bg_image1.tobytes(), self.bg_image1.size, self.bg_image1.mode)

        self.bg_image2 = pygame.image.load("Backgrounds/Background2.PNG")
        self.bg_image2 = pygame.transform.scale(self.bg_image2, (600, 400))
        self.bg_image2 = Image.frombytes("RGB", self.bg_image2.get_size(),
                                         pygame.image.tostring(self.bg_image2, "RGB", False))
        self.bg_image2 = ColorFilter.colorFilter("#%02x%02x%02x" % self.RED, self.bg_image2)
        # Aplica el filtro de color con PIL
        # En este ejemplo, se aplica un filtro de desenfoque a la imagen
        # Convierte la imagen de PIL de nuevo a Pygame
        self.bg_image2 = pygame.image.fromstring(self.bg_image2.tobytes(), self.bg_image2.size, self.bg_image2.mode)

        # Crear puntero
        self.pointer_rect = pygame.Rect(0, 0, 50, 50)
        self.pointer_rect.center = (self.window_width // 4, self.window_height // 2)
        self.pointer_color = self.BLUE

        # Crear atacante
        self.player = pygame.Rect(0, 0, 50, 50)
        self.player.center = (3 * self.window_width // 4, self.window_height // 2)
        self.player_color = self.RED

        self.font = pygame.font.Font(None, 36)  # Fuente predeterminada con un tamaño de 36 puntos

        self.start_timer(60)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    pygame.display.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.timeDefense = 0
                if event.type == pygame.MOUSEBUTTONDOWN :
                    if event.button == 1 :  # Botón izquierdo del ratón
                        selection_x, selection_y = pygame.mouse.get_pos()
                        print(self.timeDefense<=0)
                        if self.is_inside_green_area(selection_x, selection_y) :
                            if self.selected_image_to_move is not None:
                                for power in [self.power1, self.power2, self.power3]:
                                    if self.selected_image_to_move == power:
                                        if power.amount > 0 and self.timeDefense<=0:
                                            destination_x, destination_y = event.pos

                                            # Crear una copia de la imagen seleccionada en la posición del jugador
                                            selected_image_copy = self.selected_image_to_move.create_copy(self.player_x,
                                                                                                          self.player_y)
                                            selected_image_copy.selected = False

                                            # Definir el destino de la copia
                                            selected_image_copy.destination_x = destination_x
                                            selected_image_copy.destination_y = destination_y

                                            # Agregar la copia a la lista de copias del Barrier
                                            self.selected_image_to_move.copies.append(selected_image_copy)

                                            # Iniciar un hilo para mover la copia
                                            movement_thread = threading.Thread(target=self.move_selected_image,
                                                                               args=(selected_image_copy,))
                                            self.movementThreads.append(movement_thread)
                                            movement_thread.start()
                                            power.amount -= 1


                        else:
                            # Comprueba si se hizo clic en las imágenes de Poderes
                            for power in [self.power1, self.power2, self.power3]:
                                if self.check_click(power, selection_x, selection_y):
                                    self.selected_image_to_move = power
            keys = pygame.key.get_pressed()
            other_rects = []
            if self.timeDefense <= 0:
                self.image4.selected = False
                self.image4.check_collision()
                self.image4.movable=False
            for image in [self.image1, self.image2, self.image3, self.image4]:
                if image.selected:
                    other_rects.extend(image.copies)

            for image in [self.image1, self.image2, self.image3, self.image4]:
                if keys[pygame.K_f] and image.selected:
                    image.selected = False
                    image.check_collision()


            if keys[pygame.K_1]:
                if self.image1.movable and not self.image2.selected and not self.image3.selected and not self.image4.selected:
                    if not self.image1.selected:
                        self.image1.selected = True
                    else:
                        self.image1.selected = False
                        self.image1.original_x, self.image1.original_y = self.image1.initial_x, self.image1.initial_y
                    time.sleep(0.2)
            if keys[pygame.K_2]:
                if self.image2.movable and not self.image1.selected and not self.image3.selected and not self.image4.selected:
                    if not self.image2.selected:
                        self.image2.selected = True
                    else:
                        self.image2.selected = False
                        self.image2.original_x, self.image2.original_y = self.image2.initial_x, self.image2.initial_y
                    time.sleep(0.2)
            if keys[pygame.K_3]:
                if self.image3.movable and not self.image1.selected and not self.image2.selected and not self.image4.selected:
                    if not self.image3.selected:
                        self.image3.selected = True
                    else:
                        self.image3.selected = False
                        self.image3.original_x, self.image3.original_y = self.image3.initial_x, self.image3.initial_y
                    time.sleep(0.2)
            if keys[pygame.K_4]:
                if self.image4.movable and not self.image1.selected and not self.image2.selected and not self.image3.selected:
                    if not self.image4.selected:
                        self.image4.selected = True
                    else:
                        self.image4.selected = False
                        self.image4.check_collision()
                    time.sleep(0.2)



            self.pointer_rect.topleft = (self.cursor_x, self.cursor_y)

            # Mantener el puntero dentro del área verde
            self.player_x = max(650, min(self.player_x, 1200))
            self.player_y = max(200, min(self.player_y, 550))

            self.player.topleft = (self.player_x, self.player_y)

            # Dibujar en la pantalla
            self.screen.fill(self.WHITE)

            # Dibujar el rectángulo permitido
            pygame.draw.rect(self.screen, self.GREEN, (50, 200, 600, 400), 2)
            self.screen.blit(self.bg_image1, (50, 200))
            pygame.draw.rect(self.screen, self.RED, (650, 200, 600, 400), 2)
            self.screen.blit(self.bg_image2, (650, 200))
            # Mantener el puntero dentro del área verde
            self.cursor_x = max(50, min(self.cursor_x, 600))
            self.cursor_y = max(200, min(self.cursor_y, 550))

            for image in [self.image1, self.image2, self.image3, self.image4]:
                image.moveDefender(self.cursor_x, self.cursor_y)
                image.draw()

            for image in [self.power1, self.power2, self.power3]:
                image.moveAtacker(self.player_x, self.player_y)
                image.draw()



            # Dibujar el puntero
            pygame.draw.rect(self.screen, self.pointer_color, self.pointer_rect, 2)
            pygame.draw.rect(self.screen, self.player_color, self.player, 2)

            # Crear una superficie de texto (etiqueta)
            text1 = self.font.render(str(self.image1.amount), True, (255, 255, 255))
            text2 = self.font.render(str(self.image2.amount), True, (255, 255, 255))
            text3 = self.font.render(str(self.image3.amount), True, (255, 255, 255))
            text4 = self.font.render(str(self.power1.amount), True, (255, 255, 255))
            text5 = self.font.render(str(self.power2.amount), True, (255, 255, 255))
            text6 = self.font.render(str(self.power3.amount), True, (255, 255, 255))

            if self.game:
                textTime= self.font.render(str(self.timeGame), True, (0, 0, 0))
            else:
                textTime = self.font.render(str(self.timeDefense), True, (0, 0, 0))


            # Posición de la etiqueta
            text1_rect = text1.get_rect()
            text1_rect.center = (self.window_width // 4 - 190, 75)
            text2_rect = text2.get_rect()
            text2_rect.center = (self.window_width // 4 - 40, 75)
            text3_rect = text3.get_rect()
            text3_rect.center = (self.window_width // 4 + 110, 75)
            text4_rect = text1.get_rect()
            text4_rect.center = (3 * self.window_width // 4 - 190, 75)
            text5_rect = text2.get_rect()
            text5_rect.center = (3 * self.window_width // 4 - 40, 75)
            text6_rect = text3.get_rect()
            text6_rect.center = (3 * self.window_width // 4 + 110, 75)
            timer_rect = textTime.get_rect()
            timer_rect.center = (self.window_width // 2, 20)

            # Crear etiquetas para los nombres de los jugadores
            player1_label = self.font.render(self.player1, True, (0, 0, 255))
            player2_label = self.font.render(self.player2, True, (255, 0, 0))

            # Posiciones de las etiquetas de nombres
            player1_rect = player1_label.get_rect()
            player1_rect.center = (self.window_width // 4, 10)  # Ajusta la posición según tus necesidades
            player2_rect = player2_label.get_rect()
            player2_rect.center = (3 * self.window_width // 4, 10)  # Ajusta la posición según tus necesidades



            self.screen.blit(text1, text1_rect.center)
            self.screen.blit(text2, text2_rect.center)
            self.screen.blit(text3, text3_rect.center)
            self.screen.blit(text4, text4_rect.center)
            self.screen.blit(text5, text5_rect.center)
            self.screen.blit(text6, text6_rect.center)
            self.screen.blit(textTime,timer_rect.center)

            # Dibujar las etiquetas de nombres en la pantalla
            self.screen.blit(player1_label, player1_rect.center)
            self.screen.blit(player2_label, player2_rect.center)
            self.screen.blit(self.goblin,(self.player_x, self.player_y))
            pygame.display.flip()
        pygame.time.wait(2400)
        if not win:
            print("win")
            pygame.quit()
            pygame.display.quit()

    def start_timer(self,times):
        global win
        def temporizador():
            if not self.game:
                self.timeDefense = times  # 60 segundos = 1 minuto
                while self.timeDefense > 0:
                    minutos, segundos = divmod(self.timeDefense, 60)
                    tiempo_text = f"Tiempo restante: {minutos:02d}:{segundos:02d}"
                    time.sleep(1)
                    if not self.timeDefense==0:
                        self.timeDefense-= 1
                self.game=True
                self.start_timer(10)
            else:
                    self.timeGame = times  # 60 segundos = 1 minuto
                    while self.timeGame > 0:
                        minutos, segundos = divmod(self.timeGame, 60)
                        tiempo_text = f"Tiempo restante: {minutos:02d}:{segundos:02d}"
                        time.sleep(1)
                        if not self.timeGame == 0:
                            self.timeGame -= 1
                    if self.running:
                        self.stop(self.player1)
        self.timer_thread = threading.Thread(target=temporizador)
        self.timer_thread.start()
    def move_player(self):
        print("movement")
        try:
            while self.running:
                if self.timeDefense<=0:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_LEFT]:
                        self.direction=True
                        self.player_x -= 5
                        self.goblin = imagenes[3]
                        self.screen.blit(self.goblin, (self.player_x, self.player_y))
                        time.sleep(0.05)
                        self.player_x -= 5
                        self.goblin = imagenes[16]
                        self.screen.blit(self.goblin, (self.player_x, self.player_y))
                        time.sleep(0.05)
                        self.player_x -= 5
                        self.goblin = imagenes[17]
                        self.screen.blit(self.goblin, (self.player_x, self.player_y))
                        time.sleep(0.05)
                        self.player_x -= 5
                        self.goblin = imagenes[18]
                        self.screen.blit(self.goblin, (self.player_x, self.player_y))
                        time.sleep(0.05)
                        self.player_x -= 5
                        self.goblin = imagenes[19]
                        self.screen.blit(self.goblin, (self.player_x, self.player_y))
                        time.sleep(0.05)
                    if keys[pygame.K_RIGHT]:
                        self.direction = True
                        self.player_x += 5
                        self.goblin = imagenes[1]
                        self.screen.blit(self.goblin, (self.player_x, self.player_y))
                        time.sleep(0.05)
                        self.player_x += 5
                        self.goblin = imagenes[8]
                        self.screen.blit(self.goblin, (self.player_x, self.player_y))
                        time.sleep(0.05)
                        self.player_x += 5
                        self.goblin = imagenes[9]
                        self.screen.blit(self.goblin, (self.player_x, self.player_y))
                        time.sleep(0.05)
                        self.player_x += 5
                        self.goblin = imagenes[10]
                        self.screen.blit(self.goblin, (self.player_x, self.player_y))
                        time.sleep(0.05)
                        self.player_x += 5
                        self.goblin = imagenes[11]
                        self.screen.blit(self.goblin, (self.player_x, self.player_y))
                        time.sleep(0.05)
                    time.sleep(0.03)
                    if keys[pygame.K_UP]:
                        if not self.direction:
                            self.player_y -= 5
                            self.goblin = imagenes[0]
                            self.screen.blit(self.goblin, (self.player_x, self.player_y))
                            time.sleep(0.05)
                            self.player_y -= 5
                            self.goblin = imagenes[4]
                            self.screen.blit(self.goblin, (self.player_x, self.player_y))
                            time.sleep(0.05)
                            self.player_y -= 5
                            self.goblin = imagenes[5]
                            self.screen.blit(self.goblin, (self.player_x, self.player_y))
                            time.sleep(0.05)
                            self.player_y -= 5
                            self.goblin = imagenes[6]
                            self.screen.blit(self.goblin, (self.player_x, self.player_y))
                            time.sleep(0.05)
                            self.player_y -= 5
                            self.goblin = imagenes[7]
                            self.screen.blit(self.goblin, (self.player_x, self.player_y))
                            time.sleep(0.05)
                        else:
                            self.player_y -= 15
                    if keys[pygame.K_DOWN]:
                        if not self.direction:
                            self.player_y += 5
                            self.goblin = imagenes[2]
                            self.screen.blit(self.goblin, (self.player_x, self.player_y))
                            time.sleep(0.05)
                            self.player_y += 5
                            self.goblin = imagenes[12]
                            self.screen.blit(self.goblin, (self.player_x, self.player_y))
                            time.sleep(0.05)
                            self.player_y += 5
                            self.goblin = imagenes[13]
                            self.screen.blit(self.goblin, (self.player_x, self.player_y))
                            time.sleep(0.05)
                            self.player_y += 5
                            self.goblin = imagenes[14]
                            self.screen.blit(self.goblin, (self.player_x, self.player_y))
                            time.sleep(0.05)
                            self.player_y += 5
                            self.goblin = imagenes[15]
                            self.screen.blit(self.goblin, (self.player_x, self.player_y))
                            time.sleep(0.05)
                        else:
                            self.player_y += 15
                    self.goblin = imagenes[3]
                    self.direction = False
        except: pass

    # Función para el movimiento del puntero en un hilo separado
    def move_pointer(self):
        print("pointer")
        try:
            while self.running:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_w]:
                    self.cursor_y -= 5
                if keys[pygame.K_s]:
                    self.cursor_y += 5
                if keys[pygame.K_a]:
                    self.cursor_x -= 5
                if keys[pygame.K_d]:
                    self.cursor_x += 5
                time.sleep(0.03)
        except: pass


    def check_click(self,image, cursor_x, cursor_y):
        if image.original_x < cursor_x < image.original_x + image.rect_width and \
                image.original_y < cursor_y < image.original_y + image.rect_height:
            image.clicked = True
            if isinstance(image, Powers):  # Verifica si es una imagen de poder
                # Inicia un hilo de movimiento al hacer clic en la imagen de poder
                movement_thread = threading.Thread(target=self.move_selected_image, args=(image,))
                movement_thread.start()
            return True
        else:
            image.clicked = False

    # Función para mover la imagen seleccionada
    def move_selected_image(self,image_copy):
        x, y = image_copy.player_x, image_copy.player_y
        dest_x, dest_y = image_copy.destination_x, image_copy.destination_y

        # Calcular el ángulo y la distancia entre la posición actual y el destino
        angle = math.atan2(dest_y - y, dest_x - x)
        distance = math.hypot(dest_x - x, dest_y - y)
        while distance > 0:
            if self.running:
                step = min(1, distance)  # Mover hasta 1 píxel en cada paso
                x += 3*step * math.cos(angle)
                y += 3* step * math.sin(angle)
                distance -= step
                # Actualizar la posición final de la copia
                image_copy.original_x = x
                image_copy.original_y = y

                # Actualizar la copia en la pantalla

                try:
                    self.screen.blit(image_copy.image_surface, (image_copy.original_x, image_copy.original_y))
                    time.sleep(0.0001)
                except:
                    pass

                # Verificar colisiones con copias de Barrier
                for barrier in [self.image1, self.image2, self.image3, self.image4]:
                    if barrier == self.image4:
                        self.image4.combinedRect = pygame.Rect(self.image4.original_x, self.image4.original_y, self.image4.rect_width,
                                                          self.image4.rect_height)
                        if pygame.Rect(x, y, image_copy.rect_width, image_copy.rect_height).colliderect(
                                self.image4.combinedRect):
                            # Colisión detectada, detener el movimiento y eliminar la copia de Barrier
                            distance = 0
                            print("entro")
                            if (barrier.recieveDamage(image_copy.damage, self.image4)):
                                self.image4.remove_original()
                    else:
                        for copy in barrier.copies:
                            copy.combinedRect = pygame.Rect(copy.original_x, copy.original_y, copy.rect_width, copy.rect_height)
                            if pygame.Rect(x, y, image_copy.rect_width, image_copy.rect_height).colliderect(copy.combinedRect):
                                # Colisión detectada, detener el movimiento y eliminar la copia de Barrier
                                distance = 0
                                print("entro")
                                if (barrier.recieveDamage(image_copy.damage, copy)):  # Actualiza la vida y elimina la copia
                                    barrier.copies.remove(copy)  # Elimina la copia
                                    try:
                                        self.power1.copies.remove(image_copy)
                                    except:
                                        pass
                                    try:
                                        self.power2.copies.remove(image_copy)
                                    except:
                                        pass
                                    try:
                                        self.power3.copies.remove(image_copy)
                                    except:
                                        pass
            else:
                distance=0
                try:
                    for image in self.power1.copies:
                        self.power1.copies.remove(image)
                except:
                    pass
                try:
                    for image in self.power2.copies:
                        self.power2.copies.remove(image)
                except:
                    pass
                try:
                    for image in self.power3.copies:
                        self.power3.copies.remove(image)
                except:
                    pass

    # Función para verificar si el clic está dentro del área verde
    def is_inside_green_area(self,x, y):
        return 50 < x < 650 and 200 < y < 600

    def stop(self,player):
        global player1Rounds, player2Rounds, win
        self.running = False  # Detiene el bucle principal del juego

        # Detén los hilos de movimiento si es necesario (esto dependerá de cómo estén implementados)
        self.stop_threads()  # Detiene los hilos de movimiento
        # Limpia la pantalla
        self.screen.fill(self.WHITE)
        pygame.display.flip()
        font = pygame.font.Font(None, 72)
        if player == self.player2:
            player2Rounds += 1
            if player1Rounds == 2 or player2Rounds == 2:
                text = font.render(player + " Ganó la partida", True, (0, 0, 255)) \
                    if player1Rounds == 2 else font.render(
                    player + " Ganó la partida", True, (255, 0, 0))
            else:
                text = font.render(player + " Ganó", True, (255, 0, 0))
        else:
            player1Rounds += 1
            if player1Rounds == 2 or player2Rounds == 2:
                text = font.render(player + " Ganó la partida", True, (0, 0, 255)) \
                    if player1Rounds == 2 else font.render(
                    player + " Ganó la partida", True, (255, 0, 0))
            else:
                text = font.render(player + " Ganó", True, (0, 0, 255))

        if player1Rounds==2 or player2Rounds==2:
            win=True
        text_rect = text.get_rect(center=(self.window_width // 2, self.window_height // 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        print("preRestart")
        # Esperar 3 segundos
        pygame.time.wait(2500)
        print("restart")

        if player1Rounds == 2 or player2Rounds == 2:
            print("fin")
        else:
            temp = player1Rounds
            player1Rounds = player2Rounds
            player2Rounds = temp
            temp = self.player1
            self.player1 = self.player2
            self.player2 = temp
            print("new round")
            newgame=Game(self.player1,self.player2)
            newgame.begin()

    def stop_threads(self):
        threads_to_join = []

        # Función para detener los hilos de movimiento
        if hasattr(self,
                   'player_thread') and self.player_thread.is_alive() and self.player_thread != threading.current_thread():
            print("movimiento vivo")
            self.player_thread.join()

        if hasattr(self,
                   'pointer_thread') and self.pointer_thread.is_alive() and self.pointer_thread != threading.current_thread():
            print("puntero vivo")
            self.pointer_thread.join()

        # Detener los hilos de movimiento
        for thread in self.movementThreads:
            if thread != threading.current_thread():  # Evitar unir el hilo actual
                threads_to_join.append(thread)

        # Unirse a los hilos
        for thread in threads_to_join:
            if thread.is_alive():
                print("disparo vivo")
                thread.join()

        # Limpiar la lista de hilos de movimiento
        self.movementThreads = []
# Clase para gestionar las imágenes y copias
class Barriers:
    def __init__(self, image_path, x, y,life,amount,game,copy=False,original=None):
        if copy:
            self.original_x, self.original_y = original.original_x, original.original_y
        else:
            self.original_x, self.original_y = x, y
        self.initial_x=x
        self.initial_y=y
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
        self.game=game

    def create_copy(self, player_x, player_y):
        copy = Barriers(self.image_path, self.original_x, self.original_y, self.life, 1,self, copy=True, original=self)
        copy.selected = False
        return copy
    def check_collision(self):
        self.combined_rect = pygame.Rect(self.original_x, self.original_y, self.rect_width, self.rect_height)
        rectangle_rect = pygame.Rect(50, 200, 650, 400)
        outside_bounds = not rectangle_rect.contains(self.combined_rect)

        if outside_bounds:
            # Si está fuera de los límites, devuelve la imagen original a su posición inicial
            self.original_x, self.original_y = self.initial_x, self.initial_y
            return

        placed = False
        for image in [self.game.image1, self.game.image2, self.game.image3, self.game.image4]:
            for copy in image.copies:
                copy.combinedRect = pygame.Rect(copy.original_x, copy.original_y, copy.rect_width, copy.rect_height)
                if self.combined_rect.colliderect(copy.combinedRect):
                    # Copia detectada, detén el movimiento y devuelve la imagen original a su posición inicial
                    self.original_x, self.original_y = self.initial_x, self.initial_y
                    return

            if rectangle_rect.contains(self.combined_rect):
                placed = True

        if placed:
            if not self == self.game.image4:
                if self.amount > 0:
                    self.combinedRect = self.combined_rect
                    self.copies.append(self.create_copy(self.original_x, self.original_y))
                    self.amount -= 1
                self.original_x, self.original_y = self.initial_x, self.initial_y


    def moveDefender(self, cursor_x, cursor_y):
        if self.selected:
            # Restringir el movimiento dentro del área verde
            cursor_x = max(50, min(cursor_x, 650 - self.rect_width))
            cursor_y = max(200, min(cursor_y, 600 - self.rect_height))
            self.original_x = cursor_x
            self.original_y = cursor_y

    def draw(self):
        self.game.screen.blit(self.image_surface, (self.original_x, self.original_y))
        for copy_rect in self.copies:
            self.game.screen.blit(self.image_surface, (copy_rect.original_x, copy_rect.original_y))

    def recieveDamage(self,damage,copy_rect):
        copy_rect.life -= damage
        print("Vida de Barrier:", copy_rect.life)
        if copy_rect.life <= 0:
            return True
        else:
            return False

    def remove_original(self):
        # Restablecer la posición original de la imagen y eliminar todas sus copias
        self.original_x, self.original_y = self.initial_x, self.initial_y
        self.copies = []
        self.movable=False
        if self==self.game.image4:
            self.game.stop(self.game.player2)

# Clase para gestionar las imágenes y copias de Poderes
class Powers:
    def __init__(self, image_path, x, y, damage, amount,game):
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
        self.game=game

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
            pygame.draw.rect(self.game.screen, (255, 255, 0), (self.original_x-2, self.original_y-2, self.rect_width+4, self.rect_height+4), 2)
        self.game.screen.blit(self.image_surface, (self.original_x, self.original_y))

    def create_copy(self, player_x, player_y):
        copy = Powers(self.image_path, player_x, player_y, self.damage, self.amount,self)
        copy.rect_width, copy.rect_height = 20, 20
        copy.image_surface = pygame.Surface((copy.rect_width, copy.rect_height), pygame.SRCALPHA)
        copy.image = pygame.image.load(copy.image_path)
        copy.image = pygame.transform.scale(copy.image, (copy.rect_width,copy.rect_height))
        copy.image_surface.blit(copy.image, (0, 0))
        copy.selected = False
        return copy


main=Game("Juan","Pepe")
main.begin()


