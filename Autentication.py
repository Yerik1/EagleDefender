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


logInScreen = GUIBuilder('#86895d')


# Obtener las dimensiones de la pantalla
width = logInScreen.root.winfo_screenwidth()  # Ancho
height = logInScreen.root.winfo_screenheight()  # Alto

# Crea el canva para la linea Vertical -> VL
canvaVL = logInScreen.addCanvas(2, height / 2, (width / 2) + 2, height / 8, "black")
# Parametros para crear VL (x1, y1, x2, y2, color, grosor)
canvaVL.create_line(2, 0, 2, height + 5, fill="black", width=4)

# Entry del user
entryUser = logInScreen.addEntry(20, "", width / 4, height / 4)

# Entry de la contrasena
entryPassword = logInScreen.addEntry(20, "⧫", width / 4, 3 * height/8)




# Label con el titulo de la ventana
windowTitle = logInScreen.addLabel("Log In", width/2, (height)/100,"raised")

# Label de la solicitud del Username
userLb = logInScreen.addLabel("User Name: ", width/8, height/4, "flat")

# Label de la solicitud del Password
passwordLb = logInScreen.addLabel("Password: ", width/8, 3 * height/8, "flat")

# Label de la biometrica
biometricLb = logInScreen.addLabel("Biometric: ", width/1.7, height/3.4, "flat")

# Label de crear una cuenta
newAccountLb = logInScreen.addLabel("Create an account?", width/2, height/1.6, "flat")

# Label de logearse como un invitado
logInGuestLb = logInScreen.addLabel("Log In as guest?", width/2, height/1.3, "flat")


def verificarUsuario():
    global entryUser, entryPassword

    print("Entro a verificr")

    username = entryUser.get()
    password = entryPassword.get()

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
            logInScreen.closeEnvironment()

            if not (Game("Yerik1","Luis").initialize("Yerik1","Luis")):


                logInScreen.initialize()

            return True
    return False

def register1():

    logInScreen.closeEnvironment()
    registerWindow = RegisterGUI
    if not(registerWindow.begin(0,"")):
        logInScreen.initialize()



def biometric():
    print("entro")
    faceRecogn=FacialRecognition
    faceRecognClass=faceRecogn.Recogn
    faceRecogn=faceRecogn.Recogn
    user=faceRecogn.recognition1(faceRecognClass)
    print(user)
    if(user!="#NO#"):
        if(user!="No Camera"):
            logInScreen.closeEnvironment()
            if not(Game("Yerik1","Luis")):
                logInScreen.initialize()
        else:
            #Label con exepcion de que no hay camara
            print("No se detecta camara disponible")


currentImage = 0
# Metodo que cambia la imagen de los idiomas
def changeImage():
    global currentImage

    if currentImage == 0:
        currentImage = 1
    elif currentImage == 1:
        currentImage = 2
    else:
        currentImage = 0

    imagen = imagenes[currentImage]
    btnFlags.config(image=imagen)


# Carga tus tres imágenes aquí (reemplaza 'imagen1.png', 'imagen2.png', 'imagen3.png' con las rutas de tus imágenes)
imagen1 = tk.PhotoImage(file='Flags/espFlag.png')
imagen2 = tk.PhotoImage(file='Flags/ingFlag.png')
imagen3 = tk.PhotoImage(file='Flags/frnFlag.png')

# Redimenciona las imagenes
img1 = imagen1.subsample(25)
img2 = imagen2.subsample(25)
img3 = imagen3.subsample(25)

# Crea una lista con las imagenes
imagenes = [img1, img2, img3]

btnFlags = logInScreen.buttonImage(img1, lambda:(changeImage(), print("Action")), width/60, height/45)



# Boton mostrar contraseña
showPasBtn = logInScreen.buttons("👁", "", "green", "orange", 1.15 * width / 4,  3 * height/8)

# Boton para hacer el log in
logInBtn = logInScreen.buttons("Log In", lambda: verificarUsuario(), "white", "red", width/4, height/1.7)

# Boton de registrarse
registerBtn = logInScreen.buttons("Register", lambda: register1(), "Red", "orange", width/2, height/1.5)

# Boton de guest
guestBtn = logInScreen.buttons("Guesst", lambda: print("Soy invitado"), "red", "black", width/2, height/1.2)

# Boton de biometrica
biometricBtn = logInScreen.buttons("Acept",lambda: biometric(), "orange", "green", width/1.5, height/3.4)



logInScreen.initialize()



"""
Clase donde se realiza la autenticacion
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



