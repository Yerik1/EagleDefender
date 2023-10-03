import tkinter as tk
import xml.etree.ElementTree as ET
from tkinter import messagebox
import Register as register
from initialEnvironment import begin
import RegisterGUI
import FacialRecognition

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
        username = self.entryUsername.get()
        password = self.entryPassword.get()



         # Descomentar al unir con las demás clases de devRegistro
        register.decrypt()
        # Cargar el archivo encriptado
        tree = ET.parse("DataBase")
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
                begin()
                return True
        return False

    def register(self):
        self.registerWindow=RegisterGUI
        self.registerWindow.begin()

    def biometric(self):
        print("entro")
        self.faceRecogn=FacialRecognition
        self.faceRecognClass=self.faceRecogn.Recogn
        self.faceRecogn=self.faceRecogn.Recogn
        print(self.faceRecogn.recognition1(self.faceRecognClass))
        self.window.destroy()
        self.window.quit()
        begin()



Autentication(window=tk.Tk())



