from tkinter import *
import tkinter as tk

class GUIBuilder:
    # Metodo constructor de la clase
    def __init__(self):

        # Crea una nueva ventana de Tkinter
        self.root = Tk()

        # Obtener las dimensiones de la pantalla
        width = self.root.winfo_screenwidth() # Ancho
        height = self.root.winfo_screenheight() # Altura

        # Configurar la ventana en pantalla completa
        self.root.attributes("-fullscreen", True)

        self.buttons("X", self.closeEnvironment, "Red","Blue", width-15, 0)


    # Metodo encargado de iniciar el bucle de la ventana
    def initialize(self):
        self.root.mainloop()


    # Metodo constructor de botones
    def buttons(self, title, action, color1,color2, a, b):

        btn = Button(self.root,text = title, command = action)
        btn.config(bg=color1)
        btn.place(x=a, y=b)

        # Define el fondo del boton
        def change1(event):
            btn.config(bg = color1)

        # Define el fondo del boton
        def change2(event):
            btn.config(bg = color2)

        # Cambia el color del boton cuando el puntero pasa por este
        btn.bind("<Leave>", change1)
        btn.bind("<Enter>", change2)

    # Metodo que cierra la ventana
    def closeEnvironment(self):
        self.root.destroy()
