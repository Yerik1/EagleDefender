"""
* Imports utilizados
"""
from GUIBuilder import GUIBuilder
import tkinter as tk
import Register as register
import RegisterGUI


# Clase que crea la ventana para la pantalla del Lobby
class Lobby:
    def __init__(self):
        # Crea el objeto ventana
        self.lobbyScreen = GUIBuilder('#86895d')

        # Obtener las dimensiones de la pantalla
        self.width = self.lobbyScreen.root.winfo_screenwidth()  # Ancho
        self.height = self.lobbyScreen.root.winfo_screenheight()  # Alto

        # Labels usados en la ventana

        # Imagenes usadas para los botones
        imagen1 = tk.PhotoImage(file="Default/defaultUserPic.png")
        img1 = imagen1.subsample(5)

        imagen2 = tk.PhotoImage(file="Default/addUserPic.png")
        img2 = imagen2.subsample(2)

        # Bontones usados en la ventana
        edithUser = self.lobbyScreen.buttonImage(img1, lambda: (print("Aqui se edita")), self.width / 40, self.height / 20)

        edithUser = self.lobbyScreen.buttonImage(img2, lambda: (self.register1()), self.width / 1.1, self.height / 10)

        localGameBtn = self.lobbyScreen.buttons("Local Game", lambda: (print("Se inicia el juego")), "Orange"
                                                , "White", 2.5*self.width / 8, self.height / 2)

        onlineGameBtn = self.lobbyScreen.buttons("Online Game", lambda: (print("Esto aun no hace nada")), "Orange",
                                                 "White", 3.5*self.width / 8, self.height / 2)
        onlineGameBtn.config(state="disabled")

        tutorialBtn = self.lobbyScreen.buttons("Tutorial", lambda: (print("Esto aun no hace nada")), "Orange",
                                                 "White", 4.5*self.width / 8, self.height / 2)
        tutorialBtn.config(state="disabled")

        hallOfFamebtn = self.lobbyScreen.buttons("Hall of Fame", lambda: (print("Esto aun no hace nada")), "Orange",
                                               "White", 5.5 * self.width / 8, self.height / 2)
        hallOfFamebtn.config(state="disabled")




        # Inicia la ventana
        self.lobbyScreen.initialize()





    # Funicon que abre la ventana de registro
    def register1(self):
        self.lobbyScreen.closeEnvironment()
        registerWindow = RegisterGUI
        if not (registerWindow.begin(0, "")):
            print("salio")
            Lobby()



#Lobby()
