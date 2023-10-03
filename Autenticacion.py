import tkinter as tk
import xml.etree.ElementTree as ET
from tkinter import messagebox
#from Register import encrypt Descomentar al unir con las demás clases de devRegistro
#from Register import decrypt Descomentar al unir con las demás clases de devRegistro

class Autenticacion:
    def __init__(self, window):
        self.window = window
        window.title("Inicio de Sesión")

        # Etiquetas
        self.label_username = tk.Label(window, text="Nombre de Usuario:")
        self.label_password = tk.Label(window, text="Contraseña:")

        # Campos de entrada
        self.entry_username = tk.Entry(window)
        self.entry_password = tk.Entry(window, show="*")  # Para ocultar la contraseña

        # Botones
        self.button_iniciar_sesion = tk.Button(window, text="Iniciar Sesión", command=self.verificarUsuario())
        #self.button_salir = tk.Button(ventana, text="Salir", command=ventana.quit)

        # Diseño de la interfaz
        self.label_username.pack()
        self.entry_username.pack()
        self.label_password.pack()
        self.entry_password.pack()
        self.button_iniciar_sesion.pack()
        #self.button_salir.pack()



    def verificarUsuario(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        #decrypt = decrypt() Descomentar al unir con las demás clases de devRegistro
        #encrypt = encrypt() Descomentar al unir con las demás clases de devRegistro


        # Cargar la clave utilizada para la encriptación (reemplaza con tu clave real)

        # Cargar el archivo encriptado
        with open("DataBase.xml", "rb") as archivo:
            contentEncript = archivo.read()

        # Desencriptar el contenido del archivo
        #dencryptedXml = decrypt(contentEncript) Descomentar al unir con las demás clases de devRegistro

        # Analizar el XML desencriptado
        root = ET.fromstring(contentEncript.decode('utf-8'))

        for username2 in root.findall('username'):
            Usernamesave = username2.find('username').text
            Contrasave = username2.find('password').text

            # Comparar el nombre de usuario y la contraseña ingresados con los datos del XML desencriptado
            if Usernamesave == username and Contrasave == password:
                #encrypted_xml = encrypt(contentEncript) Descomentar al unir con las demás clases de devRegistro
                return True
        #encrypted_xml = encrypt(contentEncript) Descomentar al unir con las demás clases de devRegistro
        return False




