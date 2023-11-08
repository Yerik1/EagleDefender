import threading
import time
import pygame
import math
import os
import glob
from PIL import ImageDraw, ImageTk, Image, ImageFilter
import ColorFilter
import Spotify
import random
import Register as register
import xml.etree.ElementTree as ET

class Game:
    def __init__(self,player1,player2):
        self.player1Rounds=0
        self.player2Rounds=0
        self.win=False
        # Ruta de la carpeta que contiene las imágenes
        self.carpeta_imagenes = "Goblin"  # Reemplaza con la ruta de tu carpeta de imágenes

        # Patrón de archivos de imagen que deseas buscar (por ejemplo, todos los archivos .png)
        self.patron = "*.png"

        # Inicializa una lista para almacenar las rutas de las imágenes encontradas
        self.imagenes = []

        # Utiliza la función glob para buscar archivos que coincidan con el patrón en la carpeta
        self.archivos = glob.glob(os.path.join(self.carpeta_imagenes, self.patron))
        self.songList =[]
        for element in self.archivos:
            image = pygame.image.load(element)
            image = pygame.transform.scale(image, (50, 50))
            # Agrega las rutas de los archivos encontrados a la lista de imágenes
            self.imagenes.append(image)

        self.player1=self.load(player1)
        self.player2=self.load(player2)
        for item in self.player1:
            if item==self.player1[5] or item==self.player1[6] or item==self.player1[7]:
                if item is not None:
                    self.songList.append(item)
        for item in self.player2:
            if item==self.player2[5] or item==self.player2[6] or item==self.player2[7]:
                if item is not None:
                    self.songList.append(item)
        self.songInfo=Spotify.createPlaylist(self.songList)


    def load(self,user):
        list = []
        register.decrypt()
        # Cargar el archivo encriptado
        tree = ET.parse("DataBase.xml")
        root = tree.getroot()
        register.encrypt()
        for client in root.findall('Cliente'):
            if client.find('User').text == user:
                for data in client:
                    if (data.tag == "Music" or data.tag=="Colors"):
                        for song in data:
                            print(song.text)
                            list.append(song.text)
                    else:
                        print(data.text)
                        list.append(data.text)
        return list
    def initialize(self,player1,player2):
        main = Round(player1, player2, self)
        main.begin()



class Round:
    def __init__(self,player1,player2,game):
        pygame.init()
        self.Game=game
        self.songNumber=random.randrange(len(game.songList))
        self.songTempo=0
        self.songTime=0
        self.songBeats=0
        self.points=0
        info = pygame.display.Info()
        # Utiliza las dimensiones del monitor principal
        self.window_width, self.window_height = info.current_w, info.current_h
        # Configuración de la pantalla
        self.screen = pygame.display.set_mode((self.window_width, self.window_height),pygame.FULLSCREEN)


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
        self.image1 = Barriers("Barriers/Wood/Wood"+self.player2[14]+".PNG", self.window_width // 4 - 200, 200, 1, 10, self)
        self.image2 = Barriers("Barriers/Stone/Stone"+self.player2[14]+".PNG", self.window_width // 4 - 50, 200, 2, 10, self)
        self.image3 = Barriers("Barriers/Steel/Steel"+self.player2[14]+".PNG", self.window_width // 4 + 100, 200, 3, 10, self)
        self.image4 = Barriers("Eagle/Eagle.png", 75, 525, 3, 1,self)


        # Crear instancias para las imágenes de Poderes
        self.power1 = Powers("Powers/WaterBalls/WB"+self.player2[15]+".PNG", 3 * self.window_width // 4 - 200, 200, 1, 3,self)
        self.power2 = Powers("Powers/FireBalls/FB"+self.player2[15]+".PNG", 3 * self.window_width // 4 - 50, 200, 2, 2,self)
        self.power3 = Powers("Powers/Bombs/Bomb"+self.player2[15]+".PNG", 3 * self.window_width // 4 + 100, 200, 3, 4,self)

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
        self.bg_image1 = ColorFilter.colorFilter(self.player1[11], self.bg_image1)
        # Aplica el filtro de color con PIL
        # Convierte la imagen de PIL de nuevo a Pygame
        self.bg_image1 = pygame.image.fromstring(self.bg_image1.tobytes(), self.bg_image1.size, self.bg_image1.mode)

        self.bg_image2 = pygame.image.load("Backgrounds/Background2.PNG")
        self.bg_image2 = pygame.transform.scale(self.bg_image2, (600, 400))
        self.bg_image2 = Image.frombytes("RGB", self.bg_image2.get_size(),
                                         pygame.image.tostring(self.bg_image2, "RGB", False))
        self.bg_image2 = ColorFilter.colorFilter(self.player2[11], self.bg_image2)
        # Aplica el filtro de color con PIL
        # Convierte la imagen de PIL de nuevo a Pygame
        self.bg_image2 = pygame.image.fromstring(self.bg_image2.tobytes(), self.bg_image2.size, self.bg_image2.mode)

        self.defenderPic = Image.open(self.player1[8])
        self.defenderPic = self.defenderPic.resize((70, 70))
        # Crear una máscara en forma de óvalo
        ancho, alto = self.defenderPic.size
        mascara = Image.new("L", (ancho, alto), 0)
        draw = ImageDraw.Draw(mascara)
        draw.ellipse((0, 0, ancho, alto), fill=255)

        # Aplicar la máscara a la imagen original
        self.defenderPict = Image.new("RGBA", (ancho, alto))
        self.defenderPict.paste(self.defenderPic, mask=mascara)
        self.defenderPict=pygame.image.fromstring(self.defenderPict.tobytes(), self.defenderPict.size, self.defenderPict.mode)

        self.atackerPic = Image.open(self.player2[8])
        self.atackerPic = self.atackerPic.resize((70, 70))
        # Crear una máscara en forma de óvalo
        ancho, alto = self.atackerPic.size
        mascara = Image.new("L", (ancho, alto), 0)
        draw = ImageDraw.Draw(mascara)
        draw.ellipse((0, 0, ancho, alto), fill=255)

        # Aplicar la máscara a la imagen original
        self.atackerPict = Image.new("RGBA", (ancho, alto))
        self.atackerPict.paste(self.atackerPic, mask=mascara)
        self.atackerPict = pygame.image.fromstring(self.atackerPict.tobytes(), self.atackerPict.size,
                                                    self.atackerPict.mode)

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
        self.selectBarrier_thread = threading.Thread(target=self.selectBarrier)
        self.selectBarrier_thread.start()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    try:
                        Spotify.pauseSong()
                    except: pass
                    try:
                        pygame.mixer.music.stop()
                    except: pass
                    pygame.quit()
                    pygame.display.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.timeDefense = 0
                if event.type == pygame.MOUSEBUTTONDOWN :
                    if event.button == 1 :  # Botón izquierdo del ratón
                        print("click")
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
                                            if power==self.power1:
                                                pygame.mixer.music.load("SoundEfects/WaterBall.mp3")
                                                pygame.mixer.music.play()
                                            if power==self.power2:
                                                pygame.mixer.music.load("SoundEfects/FireBall.mp3")
                                                pygame.mixer.music.play()
                                            if power==self.power3:
                                                pygame.mixer.music.load("SoundEfects/Bomb.mp3")
                                                pygame.mixer.music.play()


                        else:
                            # Comprueba si se hizo clic en las imágenes de Poderes
                            for power in [self.power1, self.power2, self.power3]:
                                if self.check_click(power, selection_x, selection_y):
                                    self.selected_image_to_move = power



            self.pointer_rect.topleft = (self.cursor_x, self.cursor_y)

            # Mantener el puntero dentro del área verde
            self.player_x = max(675, min(self.player_x, 1225))
            self.player_y = max(350, min(self.player_y, 700))

            self.player.topleft = (self.player_x, self.player_y)

            # Dibujar en la pantalla
            self.screen.fill(self.WHITE)

            # Dibujar el rectángulo permitido
            pygame.draw.rect(self.screen, self.GREEN, (75, 350, 600, 400), 2)
            self.screen.blit(self.bg_image1, (75, 350))
            pygame.draw.rect(self.screen, self.RED, (675, 350, 600, 400), 2)
            self.screen.blit(self.bg_image2, (675, 350))
            self.screen.blit(self.defenderPict,(self.window_width // 4, 50))
            self.screen.blit(self.atackerPict, (3*self.window_width // 4, 50))
            # Mantener el puntero dentro del área verde
            self.cursor_x = max(75, min(self.cursor_x, 625))
            self.cursor_y = max(350, min(self.cursor_y, 700))

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
            text1 = self.font.render(str(self.image1.amount), True, (0, 0, 0))
            text2 = self.font.render(str(self.image2.amount), True, (0, 0, 0))
            text3 = self.font.render(str(self.image3.amount), True, (0, 0, 0))
            text4 = self.font.render(str(self.power1.amount), True, (0, 0, 0))
            text5 = self.font.render(str(self.power2.amount), True, (0, 0, 0))
            text6 = self.font.render(str(self.power3.amount), True, (0, 0, 0))

            if self.game:
                textTime= self.font.render(str(self.timeGame), True, (0, 0, 0))

            else:
                textTime = self.font.render(str(self.timeDefense), True, (0, 0, 0))

            textPoints1 = self.font.render("Puntos: " + str(self.points), True, (0, 0, 0))
            textPoints2 = self.font.render("Puntos: " + str(self.timeGame), True, (0, 0, 0))
            # Posición de la etiqueta
            text1_rect = text1.get_rect()
            text1_rect.center = (self.window_width // 4 - 190, 260)
            text2_rect = text2.get_rect()
            text2_rect.center = (self.window_width // 4 - 40, 260)
            text3_rect = text3.get_rect()
            text3_rect.center = (self.window_width // 4 + 110, 260)
            text4_rect = text1.get_rect()
            text4_rect.center = (3 * self.window_width // 4 - 190, 260)
            text5_rect = text2.get_rect()
            text5_rect.center = (3 * self.window_width // 4 - 40, 260)
            text6_rect = text3.get_rect()
            text6_rect.center = (3 * self.window_width // 4 + 110, 260)
            timer_rect = textTime.get_rect()
            timer_rect.center = (self.window_width // 2, 20)
            points_rect1=textPoints1.get_rect()
            points_rect2=textPoints2.get_rect()
            points_rect1.center = (self.window_width // 4, 175)
            points_rect2.center = (3*self.window_width // 4, 175)

            # Crear etiquetas para los nombres de los jugadores
            player1_label = self.font.render(self.player1[0], True, (0, 0, 255))
            player2_label = self.font.render(self.player2[0], True, (255, 0, 0))

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
            self.screen.blit(textPoints1,points_rect1.center)
            self.screen.blit(textPoints2, points_rect2.center)

            # Dibujar las etiquetas de nombres en la pantalla
            self.screen.blit(player1_label, player1_rect.center)
            self.screen.blit(player2_label, player2_rect.center)
            self.screen.blit(self.goblin,(self.player_x, self.player_y))
            pygame.display.flip()
        pygame.time.wait(2400)
        print("win")
        pygame.quit()
        pygame.display.quit()

    def start_timer(self,times):
        def temporizador():
            if not self.game:
                self.timeDefense = times  # 60 segundos = 1 minuto
                pygame.mixer.music.load("SoundEfects/Waiting.mp3")
                pygame.mixer.music.play()
                while self.timeDefense > 0:
                    minutos, segundos = divmod(self.timeDefense, 60)
                    tiempo_text = f"Tiempo restante: {minutos:02d}:{segundos:02d}"
                    pygame.time.wait(1000)
                    if not self.timeDefense==0:
                        self.timeDefense-= 1
                self.game=True
                pygame.mixer.music.stop()
                self.start_timer(10)
            else:
                list = Spotify.playSong(self.Game.songInfo[0], self.Game.songInfo[1], self.songNumber)
                self.songTime = list[0]
                self.songTempo = list[1]
                self.timeGame = self.songTime//1000  # 60 segundos = 1 minuto
                beats=0
                songBeat=self.songTempo//60
                while self.timeGame > 0:
                    if self.running:
                        self.points +=1
                        if self.timeGame%songBeat==0:
                            beats+=1
                            print(beats)
                            if beats%25==0:
                                self.image1.amount+=1
                                self.image2.amount += 1
                                self.image3.amount += 1
                            if beats%30==0:
                                self.power1.amount+=1
                                self.power2.amount += 1
                                self.power3.amount += 1
                        minutos, segundos = divmod(self.timeGame, 60)
                        tiempo_text = f"Tiempo restante: {minutos:02d}:{segundos:02d}"
                        pygame.time.wait(1000)
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
                        self.goblin = self.Game.imagenes[3]
                        self.screen.blit(self.goblin, (self.player_x, self.player_y))
                        pygame.time.wait(50)
                        self.player_x -= 5
                        self.goblin = self.Game.imagenes[16]
                        self.screen.blit(self.goblin, (self.player_x, self.player_y))
                        pygame.time.wait(50)
                        self.player_x -= 5
                        self.goblin = self.Game.imagenes[17]
                        self.screen.blit(self.goblin, (self.player_x, self.player_y))
                        pygame.time.wait(50)
                        self.player_x -= 5
                        self.goblin = self.Game.imagenes[18]
                        self.screen.blit(self.goblin, (self.player_x, self.player_y))
                        pygame.time.wait(50)
                        self.player_x -= 5
                        self.goblin = self.Game.imagenes[19]
                        self.screen.blit(self.goblin, (self.player_x, self.player_y))
                        pygame.time.wait(50)
                    if keys[pygame.K_RIGHT]:
                        self.direction = True
                        self.player_x += 5
                        self.goblin = self.Game.imagenes[1]
                        self.screen.blit(self.goblin, (self.player_x, self.player_y))
                        pygame.time.wait(50)
                        self.player_x += 5
                        self.goblin = self.Game.imagenes[8]
                        self.screen.blit(self.goblin, (self.player_x, self.player_y))
                        pygame.time.wait(50)
                        self.player_x += 5
                        self.goblin = self.Game.imagenes[9]
                        self.screen.blit(self.goblin, (self.player_x, self.player_y))
                        pygame.time.wait(50)
                        self.player_x += 5
                        self.goblin = self.Game.imagenes[10]
                        self.screen.blit(self.goblin, (self.player_x, self.player_y))
                        pygame.time.wait(50)
                        self.player_x += 5
                        self.goblin = self.Game.imagenes[11]
                        self.screen.blit(self.goblin, (self.player_x, self.player_y))
                        pygame.time.wait(50)
                    pygame.time.wait(30)
                    if keys[pygame.K_UP]:
                        if not self.direction:
                            self.player_y -= 5
                            self.goblin = self.Game.imagenes[0]
                            self.screen.blit(self.goblin, (self.player_x, self.player_y))
                            pygame.time.wait(50)
                            self.player_y -= 5
                            self.goblin = self.Game.imagenes[4]
                            self.screen.blit(self.goblin, (self.player_x, self.player_y))
                            pygame.time.wait(50)
                            self.player_y -= 5
                            self.goblin = self.Game.imagenes[5]
                            self.screen.blit(self.goblin, (self.player_x, self.player_y))
                            pygame.time.wait(50)
                            self.player_y -= 5
                            self.goblin = self.Game.imagenes[6]
                            self.screen.blit(self.goblin, (self.player_x, self.player_y))
                            pygame.time.wait(50)
                            self.player_y -= 5
                            self.goblin = self.Game.imagenes[7]
                            self.screen.blit(self.goblin, (self.player_x, self.player_y))
                            pygame.time.wait(50)
                        else:
                            self.player_y -= 15
                    if keys[pygame.K_DOWN]:
                        if not self.direction:
                            self.player_y += 5
                            self.goblin = self.Game.imagenes[2]
                            self.screen.blit(self.goblin, (self.player_x, self.player_y))
                            pygame.time.wait(50)
                            self.player_y += 5
                            self.goblin = self.Game.imagenes[12]
                            self.screen.blit(self.goblin, (self.player_x, self.player_y))
                            pygame.time.wait(50)
                            self.player_y += 5
                            self.goblin = self.Game.imagenes[13]
                            self.screen.blit(self.goblin, (self.player_x, self.player_y))
                            pygame.time.wait(50)
                            self.player_y += 5
                            self.goblin = self.Game.imagenes[14]
                            self.screen.blit(self.goblin, (self.player_x, self.player_y))
                            pygame.time.wait(50)
                            self.player_y += 5
                            self.goblin = self.Game.imagenes[15]
                            self.screen.blit(self.goblin, (self.player_x, self.player_y))
                            pygame.time.wait(50)
                        else:
                            self.player_y += 15
                    self.goblin = self.Game.imagenes[3]
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
                pygame.time.wait(30)
        except: pass

    def selectBarrier(self):
        try:
            while self.running:
                keys = pygame.key.get_pressed()
                other_rects = []
                if self.timeDefense <= 0:
                    self.image4.selected = False
                    self.image4.check_collision()
                    self.image4.movable = False
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
                        pygame.time.wait(200)

                if keys[pygame.K_2]:
                    if self.image2.movable and not self.image1.selected and not self.image3.selected and not self.image4.selected:
                        if not self.image2.selected:
                            self.image2.selected = True
                        else:
                            self.image2.selected = False
                            self.image2.original_x, self.image2.original_y = self.image2.initial_x, self.image2.initial_y
                        pygame.time.wait(200)
                if keys[pygame.K_3]:
                    if self.image3.movable and not self.image1.selected and not self.image2.selected and not self.image4.selected:
                        if not self.image3.selected:
                            self.image3.selected = True
                        else:
                            self.image3.selected = False
                            self.image3.original_x, self.image3.original_y = self.image3.initial_x, self.image3.initial_y
                        pygame.time.wait(200)
                if keys[pygame.K_4]:
                    if self.image4.movable and not self.image1.selected and not self.image2.selected and not self.image3.selected:
                        if not self.image4.selected:
                            self.image4.selected = True
                        else:
                            self.image4.selected = False
                            self.image4.check_collision()
                        pygame.time.wait(200)
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
        movement=True
        while distance > 0:
            if self.running and movement:
                step = min(1, distance)  # Mover hasta 1 píxel en cada paso
                x += 3*step * math.cos(angle)
                y += 3* step * math.sin(angle)
                if 75<x and 350<y and y<725:
                    distance -= step
                    # Actualizar la posición final de la copia
                    image_copy.original_x = x
                    image_copy.original_y = y
                else:
                    print("fuera")
                    movement=False


                # Actualizar la copia en la pantalla

                try:
                    self.screen.blit(image_copy.image_surface, (image_copy.original_x, image_copy.original_y))
                    pygame.time.wait(1)
                except:
                    movement=False

                # Verificar colisiones con copias de Barrier
                for barrier in [self.image1, self.image2, self.image3, self.image4]:
                    if barrier == self.image4 and movement:
                        self.image4.combinedRect = pygame.Rect(self.image4.original_x, self.image4.original_y, self.image4.rect_width,
                                                          self.image4.rect_height)
                        if pygame.Rect(x, y, image_copy.rect_width, image_copy.rect_height).colliderect(
                                self.image4.combinedRect):
                            # Colisión detectada, detener el movimiento y eliminar la copia de Barrier
                            distance = 0
                            print("entro")
                            if (image_copy.damage == 1):
                                pygame.mixer.music.load("SoundEfects/WaterBallColide.mp3")
                                pygame.mixer.music.play()
                            elif (image_copy.damage == 2):
                                pygame.mixer.music.load("SoundEfects/FireBallColide.mp3")
                                pygame.mixer.music.play()
                            else:
                                pygame.mixer.music.load("SoundEfects/BombColide.mp3")
                                pygame.mixer.music.play()
                            movement=False
                            if (barrier.recieveDamage(image_copy.damage, self.image4)):
                                self.image4.remove_original()
                    else:
                        for copy in barrier.copies:
                            copy.combinedRect = pygame.Rect(copy.original_x, copy.original_y, copy.rect_width, copy.rect_height)
                            if pygame.Rect(x, y, image_copy.rect_width, image_copy.rect_height).colliderect(copy.combinedRect):
                                # Colisión detectada, detener el movimiento y eliminar la copia de Barrier
                                distance = 0
                                print("entro")
                                if(image_copy.damage==1):
                                    pygame.mixer.music.load("SoundEfects/WaterBallColide.mp3")
                                    pygame.mixer.music.play()
                                elif(image_copy.damage==2):
                                    pygame.mixer.music.load("SoundEfects/FireBallColide.mp3")
                                    pygame.mixer.music.play()
                                else:
                                    pygame.mixer.music.load("SoundEfects/BombColide.mp3")
                                    pygame.mixer.music.play()
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
        return 75 < x < 675 and 350 < y < 750

    def stop(self,player):
        self.running = False  # Detiene el bucle principal del juego
        try:
            Spotify.pauseSong()
        except: pass
        # Detén los hilos de movimiento si es necesario (esto dependerá de cómo estén implementados)
        self.stop_threads()  # Detiene los hilos de movimiento
        # Limpia la pantalla
        self.screen.fill(self.WHITE)
        pygame.display.flip()
        font = pygame.font.Font(None, 72)
        if player[0] == self.player2[0]:
            self.Game.player2Rounds += 1
            if self.Game.player2Rounds == 2:
                text = font.render(player[0] + " Ganó la partida", True, (0, 0, 255)) \
                    if self.Game.player1Rounds == 2 else font.render(
                    player[0] + " Ganó la partida", True, (255, 0, 0))
                pygame.mixer.music.load("SoundEfects/GameWin.mp3")
                pygame.mixer.music.play()
            else:
                text = font.render(player[0] + " Ganó", True, (255, 0, 0))
                pygame.mixer.music.load("SoundEfects/RoundWin.mp3")
                pygame.mixer.music.play()
        if player[0] == self.player1[0]:
            self.Game.player1Rounds += 1
            if self.Game.player1Rounds == 2:
                text = font.render(player[0] + " Ganó la partida", True, (0, 0, 255)) \
                    if self.Game.player1Rounds == 2 else font.render(
                    player[0] + " Ganó la partida", True, (255, 0, 0))
                pygame.mixer.music.load("SoundEfects/GameWin.mp3")
                pygame.mixer.music.play()
            else:
                text = font.render(player[0] + " Ganó", True, (0, 0, 255))
                pygame.mixer.music.load("SoundEfects/RoundWin.mp3")
                pygame.mixer.music.play()
        if self.Game.player1Rounds==2 or self.Game.player2Rounds==2:
            self.Game.win=True
        text_rect = text.get_rect(center=(self.window_width // 2, self.window_height // 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        print("preRestart")
        # Esperar 3 segundos
        pygame.time.wait(2500)
        print("restart")

        if self.Game.player1Rounds == 2 or self.Game.player2Rounds == 2:
            print("fin")
        else:
            temp = self.Game.player1Rounds
            self.Game.player1Rounds = self.Game.player2Rounds
            self.Game.player2Rounds = temp
            temp = self.player1
            self.player1 = self.player2
            self.player2 = temp
            print("new round")
            newgame=Round(self.player1, self.player2,self.Game)
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
        self.combinedRect = pygame.Rect(self.original_x, self.original_y, self.rect_width, self.rect_height)
        self.game=game

    def create_copy(self, player_x, player_y):
        copy = Barriers(self.image_path, self.original_x, self.original_y, self.life, 1,self, copy=True, original=self)
        copy.selected = False
        return copy
    def check_collision(self):
        self.combinedRect = pygame.Rect(self.original_x, self.original_y, self.rect_width, self.rect_height)
        rectangle_rect = pygame.Rect(75, 350, 675, 750)
        outside_bounds = not rectangle_rect.contains(self.combinedRect)

        if outside_bounds:
            # Si está fuera de los límites, devuelve la imagen original a su posición inicial
            self.original_x, self.original_y = self.initial_x, self.initial_y
            return

        placed = False

        # Comprobar la colisión con la imagen 4 antes de las otras imágenes
        if self != self.game.image4 and self.game.image4.combinedRect.colliderect(self.combinedRect):
            # No puedes colocar la copia en la ubicación de la imagen 4
            self.original_x, self.original_y = self.initial_x, self.initial_y
            return

        for image in [self.game.image1, self.game.image2, self.game.image3]:
            for copy in image.copies:
                if copy == self:
                    continue  # Salta la comprobación de colisión con uno mismo

                copy.combinedRect = pygame.Rect(copy.original_x, copy.original_y, copy.rect_width, copy.rect_height)
                if self.combinedRect.colliderect(copy.combinedRect):
                    # Copia detectada, detén el movimiento y devuelve la imagen original a su posición inicial
                    self.original_x, self.original_y = self.initial_x, self.initial_y
                    return

            if rectangle_rect.contains(self.combinedRect):
                placed = True

        if placed:
            if self != self.game.image4:
                if self.amount > 0:
                    self.combinedRect = self.combinedRect
                    self.copies.append(self.create_copy(self.original_x, self.original_y))
                    self.amount -= 1
                self.original_x, self.original_y = self.initial_x, self.initial_y
            else:
                self.game.image4.combinedRect = self.combinedRect


    def moveDefender(self, cursor_x, cursor_y):
        if self.selected:
            # Restringir el movimiento dentro del área verde
            cursor_x = max(75, min(cursor_x, 675 - self.rect_width))
            cursor_y = max(350, min(cursor_y, 750 - self.rect_height))
            self.original_x = cursor_x
            self.original_y = cursor_y

    def draw(self):
        self.game.screen.blit(self.image_surface, (self.original_x, self.original_y))
        for copy_rect in self.copies:
            self.game.screen.blit(copy_rect.image_surface, (copy_rect.original_x, copy_rect.original_y))

    def recieveDamage(self,damage,copy_rect):
        copy_rect.life -= damage
        if(copy_rect.life==2):
            copy_rect.image = Image.frombytes("RGB", copy_rect.image.get_size(),
                                             pygame.image.tostring(self.image, "RGB", False))
            copy_rect.image = ColorFilter.colorFilter("#FFA500", copy_rect.image)
            copy_rect.image = pygame.image.fromstring(copy_rect.image.tobytes(), copy_rect.image.size, copy_rect.image.mode)
            copy_rect.image_surface.blit(copy_rect.image, (0, 0))
        elif (copy_rect.life==1):
            copy_rect.image = Image.frombytes("RGB", copy_rect.image.get_size(),
                                              pygame.image.tostring(self.image, "RGB", False))
            copy_rect.image = ColorFilter.colorFilter("#FF0000", copy_rect.image)
            copy_rect.image = pygame.image.fromstring(copy_rect.image.tobytes(), copy_rect.image.size,
                                                      copy_rect.image.mode)
            copy_rect.image_surface.blit(copy_rect.image, (0, 0))

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
            player_y = max(350, min(player_y, 700))
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

