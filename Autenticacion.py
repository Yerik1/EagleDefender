import tkinter as tk
import xml.etree.ElementTree as ET
from tkinter import messagebox
import Register as register

class Autenticacion:
    def __init__(self, window):
        self.window = window
        window.title("Inicio de Sesión")

        # Etiquetas
        self.label_username = tk.Label(window, text="Nombre de Usuario:")
        self.label_password = tk.Label(window, text="Contraseña:")

        # Campos de entrada
        self.entry_username = tk.Entry(window)
        self.entry_password = tk.Entry(window, show="⧫")  # Para ocultar la contraseña

        # Botones
        self.button_iniciar_sesion = tk.Button(window, text="Iniciar Sesión", command=self.verificarUsuario)
        #self.button_salir = tk.Button(ventana, text="Salir", command=ventana.quit)

        # Diseño de la interfaz
        self.label_username.pack()
        self.entry_username.pack()
        self.label_password.pack()
        self.entry_password.pack()
        self.button_iniciar_sesion.pack()
        #self.button_salir.pack()
        self.window.mainloop()



    def verificarUsuario(self):
        username = self.entry_username.get()
        password = self.entry_password.get()


        register.decrypt()  # Descomentar al unir con las demás clases de devRegistro

        # Cargar el archivo encriptado
        tree = ET.parse("DataBase")
        root = tree.getroot()

        register.encrypt()


        # Desencriptar el contenido del archivo

        # Analizar el XML desencriptado


        for username2 in root.findall('User'):
            Usernamesave = username2.find('User').text
            Contrasave = username2.find('Password').text

            # Comparar el nombre de usuario y la contraseña ingresados con los datos del XML desencriptado
            if Usernamesave == username and Contrasave == password:
                print("exito")
                return True

        print("falla")
        return False

Autenticacion(window=tk.Tk())


