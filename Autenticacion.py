import tkinter as tk
import xml.etree.ElementTree as ET
from tkinter import messagebox

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


    '''def Autenticacionbio(self, username):
        # Captura de video desde la cámara
        cap = cv2.VideoCapture(0)

        # Cargamos la imagen del usuario desde la base de datos
        user_image = face_recognition.load_image_file("usuarios/usuario1.jpg")
        user_encoding = face_recognition.face_encodings(user_image)[0]

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Detectar caras en el fotograma actual
            face_locations = face_recognition.face_locations(frame)
            if len(face_locations) > 0:
                # Codificar la cara detectada
                face_encoding = face_recognition.face_encodings(frame, face_locations)[0]

                # Comparar la cara con la del usuario en la base de datos
                matches = face_recognition.compare_faces([user_encoding], face_encoding)

                if matches[0]:
                    cap.release()
                    cv2.destroyAllWindows()
                    return True  # Autenticación biométrica exitosa

            # Mostrar el fotograma en una ventana
            cv2.imshow("Escaneo Facial", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        return False  # Autenticación biométrica fallida'''

    def verificarUsuario(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        # Cargar la clave utilizada para la encriptación (reemplaza con tu clave real)

        # Cargar el archivo encriptado
        with open("DataBase.xml", "rb") as archivo:
            contentEncript = archivo.read()

        # Desencriptar el contenido del archivo

        # Analizar el XML desencriptado
        root = ET.fromstring(contentEncript.decode('utf-8'))

        for username2 in root.findall('username'):
            Usernamesave = username2.find('username').text
            Contrasave = username2.find('password').text

            # Comparar el nombre de usuario y la contraseña ingresados con los datos del XML desencriptado
            if Usernamesave == username and Contrasave == password:
                return True
        return False


