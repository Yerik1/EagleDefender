# Imports
from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
from translationManager import TranslationManager
from tkinter import ttk

class GUIBuilder:
    # Metodo constructor de la clase
    def __init__(self,BG):
        # Crea una nueva ventana de Tkinter
        self.root = Tk()

        # Color de fondo de la ventana
        self.BG = BG

        #asigna el color de fondo de la ventana
        self.root.config(background=self.BG)

        # Obtener las dimensiones de la pantalla
        width = self.root.winfo_screenwidth()  # Ancho
        height = self.root.winfo_screenheight()  # Altura

        # Configurar la ventana en pantalla completa
        self.root.attributes("-fullscreen", True)

        self.translationManager = TranslationManager()

        #self.languageCombobox.bind("<<ComboboxSelected>>", self.updateLanguage)

        # Crea botones para cerrar o minimizar la ventana
        self.buttons(" x ", self.closeEnvironment, "Red","Blue", width-23, -0.5)
        self.buttons(" - ", self.minimize, "Red", "Blue", width-45, -0.5)



        self.translationManager.loadTranslations()
        '''
        self.widgetDict = {
            'funFactDefender': self.addLabel("Fun Facts: ...", width / 8, height / 11, "flat"),
            'musicDefender': self.addLabel("Music", width/15, 2*(height/37), "flat"),
        }
        '''



    def updateLanguage(self,event):
        self.translationManager.setLanguage(self.currentLanguage.get())
        self.translationManager.updateWidgets(self.widgetDict)



    # Metodo encargado de iniciar el bucle de la ventana
    def initialize(self):
        self.root.mainloop()


    # Metodo que retorna el color de fondo de la ventana
    def getBG(self,BG):
        return self.BG
        #self.root.config(background = BG)


    # Agrega canvas y define el fondo y el borde
    def addCanvas(self, w, h, a, b,BG):
        canvas = Canvas(self.root, width=w, height=h, bg=self.BG,  highlightbackground=BG)
        canvas.place(x=a, y=b)
        return canvas


    def addLabel(self, txt, a, b, r):
        label = Label(self.root, text=" "+txt, bg=self.BG, relief=r)
        label.place(x=a, y=b)
        return label

    def editLabel(self,txt,label):
        label.config(text=txt)



    # Metodo constructor de botones
    def buttons(self, title, action, color1,color2, a, b):

        btn = Button(self.root, text=title, command=action, bd=0, relief="sunken", activebackground=self.BG)
        btn.config(bg=color1)
        btn.place(x=a, y=b)

        # Define el fondo del boton cuando el puntero sale
        def change1(event):
            btn.config(bg=color1)

        # Define el fondo del boton cuando el puntero entra
        def change2(event):
            btn.config(bg=color2)

        # Cambia el color del boton cuando el puntero pasa por este
        btn.bind("<Leave>", change1)  # Sale
        btn.bind("<Enter>", change2)  # Entra


    # Metodo que cierra la ventana
    def closeEnvironment(self):
        self.root.destroy()

    # Metodo que minimiza la ventana
    def minimize(self):
        self.root.iconify()

    def addCombox (self):
        self.languages = ["English", "Español"]
        self.currentLanguage = tk.StringVar()
        self.languageCombobox = ttk.Combobox(self.root, textvariable=self.currentLanguage, values=self.languages)
        self.languageCombobox.pack()
        return self.languageCombobox

    def deleteLbl(self):
        print("")


