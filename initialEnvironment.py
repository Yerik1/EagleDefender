# Imports
from GUIBuilder import GUIBuilder
import time
import tkinter as tk
from tkinter import *

def begin():
    # Colores predeterminados
    color1 = "#272b00"
    color2 = "#54582f"
    color3 = "#86895d"
    color4 = "#bec092"
    chosenColor = "#272b00"

    # Crea la ventana del ambiente inicial
    initialEnvironmentScreen = GUIBuilder("#86895d")


    # Obtener las dimensiones de la pantalla
    width = initialEnvironmentScreen.root.winfo_screenwidth() # Ancho
    height = initialEnvironmentScreen.root.winfo_screenheight() # Alto


    # Crea el canva para la Linea Horizontal -> HL
    canvaHL = initialEnvironmentScreen.addCanvas(width+5,2,-1,height/8.5,"black")
    # Parametros para crear HL (x1, y1, x2, y2, color, grosor)
    canvaHL.create_line(0,2,width+5,2,fill="black",width=4)


    # Crea el canva para la Linea Horizontal2 -> HL2
    canvaHL2 = initialEnvironmentScreen.addCanvas(width+5,2,-1,(height/10)*2,"black")
    # Parametros para crear HL2 (x1, y1, x2, y2, color, grosor)
    canvaHL2.create_line(0,2,width+5,2,fill="black",width=4)


    # Crea el canva para la linea Vertical -> VL
    canvaVL = initialEnvironmentScreen.addCanvas(2,height+5,(width/2)+4,-1,"black")
    # Parametros para crear VL (x1, y1, x2, y2, color, grosor)
    canvaVL.create_line(2, 0, 2, height+5,fill="black",width=4)


    # Label de las paredes del defensor
    wallsLb = initialEnvironmentScreen.addLabel("Walls: ", 0.4*(width/30), height/6.7, "flat")


    # Label de los poderes del atacante
    powersLb = initialEnvironmentScreen.addLabel("Powers: ", 15.4*(width/30), height/6.7, "flat")


    # Labels de los puntos
    pointsDefender = initialEnvironmentScreen.addLabel("Points: ", 0.4*(width/30),height/11,"flat")
    pointsAttacker = initialEnvironmentScreen.addLabel("Points: ", 15.4*(width/30),height/11,"flat")

    # Labels de los nombres de los usuarios
    userDefender = initialEnvironmentScreen.addLabel("User: ", width/15, height/37, "flat")
    userAttacker = initialEnvironmentScreen.addLabel("User: ", 9*(width/15), height/37, "flat")

    # Labels de la cancion que esta sonando
    musicDefender = initialEnvironmentScreen.addLabel("Music: ", width/15, 2*(height/37), "flat")
    musicAttacker = initialEnvironmentScreen.addLabel("Music: ", 9*(width/15), 2*(height/37), "flat")

    # Labels del rol que desarolla cada jugador
    rolDefender = initialEnvironmentScreen.addLabel("Defender", 6.5*(width/15), height/37, "flat")
    rolAttacker = initialEnvironmentScreen.addLabel("Attacker", 14.5*(width/15), height/37, "flat")

    # Labels de de los datos curiosos de las cansiones
    funFactDefender = initialEnvironmentScreen.addLabel("Fun Facts: ...", width/8, height/11, "flat")
    funFactAttacker = initialEnvironmentScreen.addLabel("Fun Facts: ...", 5.25*(width/8), height/11, "flat")

    # Imagenes de perfil
    profilePicDefender = initialEnvironmentScreen.addLabel("Profile Pic", width/43, height/25,"flat")
    profilePicAttacker = initialEnvironmentScreen.addLabel("Profile Pic", 8*(width/15), height/25, "flat")

    # Label del tiempo



    print(width, height)




    # Inizia el bucle de la ventana del ambiente inicial
    initialEnvironmentScreen.initialize()


