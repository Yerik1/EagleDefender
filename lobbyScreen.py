"""
* Imports utilizados
"""
from GUIBuilder import GUIBuilder
import tkinter as tk
import Register as register
import RegisterGUI
import xml.etree.ElementTree as ET
from PIL import ImageDraw, ImageTk, Image, ImageFilter
from LogIn import LogIn
from Game import Game
import time

# Clase que crea la ventana para la pantalla del Lobby
class Lobby:
    def __init__(self,user1,user2):
        # Crea el objeto ventana
        self.lobbyScreen = GUIBuilder('#86895d')

        # Obtener las dimensiones de la pantalla
        self.width = self.lobbyScreen.root.winfo_screenwidth()  # Ancho
        self.height = self.lobbyScreen.root.winfo_screenheight()  # Alto
        self.user1=self.load(user1)
        self.user2 = self.load(user2)





        # Inicia la ventana
        #self.lobbyScreen.initialize()





    # Funicon que abre la ventana de registro
    def register1(self):
        self.lobbyScreen.closeEnvironment()
        registerWindow = RegisterGUI
        if not (registerWindow.begin(0, "")):
            print("salio")
            lobby=Lobby(self.user1[0],"")
            lobby.initialize()

    def logIn(self):
        self.lobbyScreen.closeEnvironment()
        logIn = LogIn()
        lobby = Lobby(self.user1[0],logIn.begin())
        print("salio")
        lobby.initialize()
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

    def play(self):
        if self.user2!=[]:
            self.lobbyScreen.closeEnvironment()
            game = Game(self.user1[0], self.user2[0])
            game.initialize(game.player1, game.player2)
            flag=True
            while (flag):
                if (game.win):
                    time.sleep(4)
                    print("entro")
                    Lobby(self.user1[0], self.user2[0]).initialize()
                    flag = False

            print("salio")
    def initialize(self):
        # Labels usados en la ventana

        # Imagenes usadas para los botones
        imagen1 = Image.open(self.user1[8])
        imagen1 = imagen1.resize((100, 100))
        # Crear una máscara en forma de óvalo
        ancho, alto = imagen1.size
        mascara = Image.new("L", (ancho, alto), 0)
        draw = ImageDraw.Draw(mascara)
        draw.ellipse((0, 0, ancho, alto), fill=255)
        # Aplicar la máscara a la imagen original
        img1 = Image.new("RGBA", (ancho, alto))
        img1.paste(imagen1, mask=mascara)
        img1 = ImageTk.PhotoImage(img1)
        if self.user2==[]:

            imagen2 = tk.PhotoImage(file="Default/addUserPic.png")
            img2 = imagen2.subsample(3)
            self.lobbyScreen.addLabel("Register ->",10*self.width / 12,self.height / 10, "flat")

        else:
            imagen2 = Image.open(self.user2[8])
            imagen2 = imagen2.resize((100, 100))
            # Crear una máscara en forma de óvalo
            ancho, alto = imagen2.size
            mascara = Image.new("L", (ancho, alto), 0)
            draw = ImageDraw.Draw(mascara)
            draw.ellipse((0, 0, ancho, alto), fill=255)
            # Aplicar la máscara a la imagen original
            img2 = Image.new("RGBA", (ancho, alto))
            img2.paste(imagen2, mask=mascara)
            img2 = ImageTk.PhotoImage(img2)


        # Bontones usados en la ventana
        self.edithUser1 = self.lobbyScreen.buttonImage(img1, lambda: (print("Aqui se edita")),
                                                      self.width / self.width + 85, self.height / 10)

        if(self.user2==[]):
            self.addUser = self.lobbyScreen.buttonImage(img2, lambda: (self.register1()), self.width / 1.1,
                                                          self.height / 10)
            self.logUser = self.lobbyScreen.buttons("Log In", lambda: (self.logIn()),"Orange","White", self.width / 1.1,
                                                        self.height / 4.8)
        else:
            self.edithUser2 = self.lobbyScreen.buttonImage(img2, lambda: (print("Aqui se edita")), self.width / 1.1,
                                                        self.height / 10)
        self.localGameBtn = self.lobbyScreen.buttons("Local Game", lambda: (self.play()), "Orange"
                                                     , "White", 2.5 * self.width / 8, self.height / 2)

        onlineGameBtn = self.lobbyScreen.buttons("Online Game", lambda: (print("Esto aun no hace nada")), "Orange",
                                                 "White", 3.5 * self.width / 8, self.height / 2)
        onlineGameBtn.config(state="disabled")

        tutorialBtn = self.lobbyScreen.buttons("Tutorial", lambda: (print("Esto aun no hace nada")), "Orange",
                                               "White", 4.5 * self.width / 8, self.height / 2)
        tutorialBtn.config(state="disabled")

        hallOfFamebtn = self.lobbyScreen.buttons("Hall of Fame", lambda: (print("Esto aun no hace nada")), "Orange",
                                                 "White", 5.5 * self.width / 8, self.height / 2)
        hallOfFamebtn.config(state="disabled")
        if not self.lobbyScreen.initialize():
            return False

#Lobby()
