import time
from tkinter import *
from GUIBuilder import GUIBuilder
import tkinter as tk
import xml.etree.ElementTree as ET
from tkinter import messagebox
import Register as register
from InitialEnvironment import begin
import RegisterGUI
import FacialRecognition
from Game import Game
from lobbyScreen import Lobby

class Autenticacion:

    def __init__(self):
        self.logInScreen = GUIBuilder('#86895d')

        self.showHide = 0
        # Obtener las dimensiones de la pantalla
        self.width = self.logInScreen.root.winfo_screenwidth()  # Ancho
        self.height = self.logInScreen.root.winfo_screenheight()  # Alto

        # Crea el canva para la linea Vertical -> VL
        self.canvaVL = self.logInScreen.addCanvas(2, self.height / 2, (self.width / 2) + 2, self.height / 8, "black")
        # Parametros para crear VL (x1, y1, x2, y2, color, grosor)
        self.canvaVL.create_line(2, 0, 2, self.height + 5, fill="black", width=4)

        # Entry del user
        self.entryUser = self.logInScreen.addEntry(20, "", self.width / 4, self.height / 4)

        # Entry de la contrasena
        self.entryPassword = self.logInScreen.addEntry(20, "⧫", self.width / 4, 3 * self.height/8)




        # Label con el titulo de la ventana
        self.windowTitle = self.logInScreen.addLabel("Log In", self.width/2, (self.height)/100,"flat")

        # Label de la solicitud del Username
        self.userLb = self.logInScreen.addLabel("User Name: ", self.width/8, self.height/4, "flat")

        # Label de la solicitud del Password
        self.passwordLb = self.logInScreen.addLabel("Password: ", self.width/8, 3 * self.height/8, "flat")

        # Label de la biometrica
        self.biometricLb = self.logInScreen.addLabel("Biometric: ", self.width/1.7, self.height/3.4, "flat")

        # Label de crear una cuenta
        self.newAccountLb = self.logInScreen.addLabel("Create an account?", self.width/2, self.height/1.6, "flat")

        # Label de logearse como un invitado
        # self.logInGuestLb = self.logInScreen.addLabel("Log In as guest?", self.width/2, self.height/1.3, "flat")
        self.currentImage = 0

        # Carga tus tres imágenes aquí (reemplaza 'imagen1.png', 'imagen2.png', 'imagen3.png' con las rutas de tus imágenes)
        imagen1 = tk.PhotoImage(file='Flags/espFlag.png')
        imagen2 = tk.PhotoImage(file='Flags/ingFlag.png')
        imagen3 = tk.PhotoImage(file='Flags/frnFlag.png')

        # Redimenciona las imagenes
        img1 = imagen1.subsample(25)
        img2 = imagen2.subsample(25)
        img3 = imagen3.subsample(25)

        # Crea una lista con las imagenes
        self.imagenes = [img1, img2, img3]
        self.btnFlags = self.logInScreen.buttonImage(img1, lambda: (self.changeImage(), print("Action")), self.width / 60, self.height / 45)

        # Boton mostrar contraseña
        self.showPasBtn = self.logInScreen.buttons("👁",self.showHidePassword, "green", "orange", 1.15 * self.width / 4, 3 * self.height / 8)

        # Boton para hacer el log in
        self.logInBtn = self.logInScreen.buttons("Log In", lambda: self.verificarUsuario(), "white", "red", self.width / 4, self.height / 1.7)

        # Boton de registrarse
        self.registerBtn = self.logInScreen.buttons("Register", lambda: self.register1(), "Red", "orange", self.width / 2, self.height / 1.5)

        # Boton de guest
        # self.guestBtn = self.logInScreen.buttons("Guesst", lambda: print("Soy invitado"), "red", "black", self.width / 2, self.height / 1.2)

        # Boton de biometrica
        self.biometricBtn = self.logInScreen.buttons("Acept", lambda: self.biometric(), "orange", "green", self.width / 1.5, self.height / 3.4)
        self.logInScreen.initialize()
    def verificarUsuario(self):

        print("Entro a verificr")

        username = self.entryUser.get()
        password = self.entryPassword.get()

        # Descomentar al unir con las demás clases de devRegistro
        register.decrypt()

        # Cargar el archivo encriptado
        tree = ET.parse("DataBase.xml")
        root = tree.getroot()
        register.encrypt()

        # Desencriptar el contenido del archivo

        # Analizar el XML desencriptado

        for username2 in root.findall('Cliente'):
            usernameSave = username2.find('User').text
            passSave = username2.find('Password').text

            # Comparar el nombre de usuario y la contraseña ingresados con los datos del XML desencriptado
            if usernameSave == username and passSave == password:

                print("exito")
                self.logInScreen.closeEnvironment()
                flag=True
                lobby=Lobby(username, "")
                # game = Game(username, "Prueba")
                # game.initialize(game.player1, game.player2)
                while(flag):
                    if not (lobby.initialize()):
                        Autenticacion()
                        flag=False
                    """ if (game.win):
                        time.sleep(2)
                        print("entro")
                        Autenticacion()
                        flag=False"""

                print("salio")
                return True
        return False

    def register1(self):

        self.logInScreen.closeEnvironment()
        registerWindow = RegisterGUI
        if not(registerWindow.begin(0,"")):
            print("salio")
            Autenticacion()



    def biometric(self):
        print("entro")
        faceRecogn=FacialRecognition
        faceRecognClass=faceRecogn.Recogn
        faceRecogn=faceRecogn.Recogn
        user=faceRecogn.recognition1(faceRecognClass)
        print(user)
        if(user!="#NO#"):
            if(user!="No Camera"):
                self.logInScreen.closeEnvironment()
                lobby = Lobby(user, "")
                flag = True
                #game = Game(user, "Prueba")
                #game.initialize(game.player1, game.player2)
                while (flag):
                    if not (lobby.initialize()):
                        Autenticacion()
                        flag = False

                print("salio")
            else:
                #Label con exepcion de que no hay camara
                print("No se detecta camara disponible")



# Metodo que cambia la imagen de los idiomas
    def changeImage(self):

        if self.currentImage == 0:
            self.currentImage = 1
        elif self.currentImage == 1:
            self.currentImage = 2
        else:
            self.currentImage = 0

        imagen = self.imagenes[self.currentImage]
        self.btnFlags.config(image=imagen)

    def showHidePassword(self):
        if (self.showHide == 0):
            self.entryPassword.configure(show="")
            self.showHide=1
        else:
            self.entryPassword.configure(show="⧫")
            self.showHide = 0


Autenticacion()



"""
Clase donde se realiza la autenticacion
"""
"""
class Autentication:
    def __init__(self, window):
        self.window = window
        self.window.title("Log In")
        self.registerWindow=""
        self.faceRecogn=""
        self.faceRecognClass=""

        # Etiquetas
        self.labelUsername = tk.Label(window, text="User Name:")
        self.labelPassword = tk.Label(window, text="Contraseña:")

        # Campos de entrada
        self.entryUsername = tk.Entry(window)
        self.entryPassword = tk.Entry(window, show="⧫")  # Para ocultar la contraseña

        # Botones
        self.buttonIniciarSesion = tk.Button(window, text="Log In", command=self.verificarUsuario)
        self.buttonRegister = tk.Button(window, text="Register", command=self.register)
        self.buttonBiometric = tk.Button(window,text="Biometric", command=self.biometric)
        #self.button_salir = tk.Button(ventana, text="Salir", command=ventana.quit)

        # Diseño de la interfaz
        self.labelUsername.pack()
        self.entryUsername.pack()
        self.labelPassword.pack()
        self.entryPassword.pack()
        self.buttonIniciarSesion.pack()
        self.buttonRegister.pack()
        self.buttonBiometric.pack()
        #self.button_salir.pack()
        self.window.mainloop()



    def verificarUsuario(self):
        print("Entro al verificar")
        username = self.entryUsername.get()
        password = self.entryPassword.get()

        # Descomentar al unir con las demás clases de devRegistro
        register.decrypt()
        # Cargar el archivo encriptado
        tree = ET.parse("DataBase.xml")
        root = tree.getroot()
        register.encrypt()


        # Desencriptar el contenido del archivo

        # Analizar el XML desencriptado


        for username2 in root.findall('Cliente'):
            usernameSave = username2.find('User').text
            passSave = username2.find('Password').text


            # Comparar el nombre de usuario y la contraseña ingresados con los datos del XML desencriptado
            if usernameSave == username and passSave == password:

                print("exito")
                self.window.destroy()
                self.window.quit()
                if not(begin(username)):
                    Autentication(tk.Tk())
                return True
        return False

    def register(self):
        self.window.destroy()
        self.window.quit()
        self.registerWindow = RegisterGUI
        if not(self.registerWindow.begin(0,"")):
            Autentication(tk.Tk())
        #root = tk.Tk()
        #app = RegisterApp(root, "ColorWheel.png")
        #root.mainloop()

    def biometric(self):
        print("entro")
        self.faceRecogn=FacialRecognition
        self.faceRecognClass=self.faceRecogn.Recogn
        self.faceRecogn=self.faceRecogn.Recogn
        user=self.faceRecogn.recognition1(self.faceRecognClass)
        print(user)
        if(user!="#NO#"):
            if(user!="No Camera"):
                self.window.destroy()
                self.window.quit()
                if not(begin(user)):
                    Autentication(tk.Tk())
            else:
                #Label con exepcion de que no hay camara
                print("")


#Autentication(tk.Tk())
"""


