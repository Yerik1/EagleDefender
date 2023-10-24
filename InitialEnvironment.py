# Imports
from GUIBuilder import GUIBuilder
import time
import tkinter as tk
from tkinter import *
import Register as register
import xml.etree.ElementTree as ET
from PIL import ImageDraw, ImageTk, Image, ImageFilter
import RegisterGUI
import ColorFilter
def begin(user):
    list= load(user)
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

    woodWalls=initialEnvironmentScreen.addCanvas(50,50, 0.4*(width/30)+150, height/6.7-17,"#000000")
    woodWall=Image.open("./Barriers/Barrier1.PNG")
    woodWall=woodWall.resize((50,50))
    woodWall=ImageTk.PhotoImage(woodWall)
    woodWalls.create_image(27, 27,image=woodWall)

    brickWalls = initialEnvironmentScreen.addCanvas(50, 50, 0.4 * (width / 30) + 250, height / 6.7 - 17, "#000000")
    brickWall = Image.open("./Barriers/Barrier2.PNG")
    brickWall = brickWall.resize((50, 50))
    brickWall = ImageTk.PhotoImage(brickWall)
    brickWalls.create_image(27, 27, image=brickWall)

    steelWalls = initialEnvironmentScreen.addCanvas(50, 50, 0.4 * (width / 30) + 350, height / 6.7 - 17, "#000000")
    steelWall = Image.open("./Barriers/Barrier3.PNG")
    steelWall = steelWall.resize((50, 50))
    steelWall = ImageTk.PhotoImage(steelWall)
    steelWalls.create_image(27, 27, image=steelWall)


    # Label de los poderes del atacante
    powersLb = initialEnvironmentScreen.addLabel("Powers: ", 15.4*(width/30), height/6.7, "flat")


    # Labels de los puntos
    pointsDefender = initialEnvironmentScreen.addLabel("Points: ", 0.4*(width/30),height/11,"flat")
    pointsAttacker = initialEnvironmentScreen.addLabel("Points: ", 15.4*(width/30),height/11,"flat")

    # Labels de los nombres de los usuarios
    userDefender = initialEnvironmentScreen.addLabel("User:  "+user, width/15, height/37, "flat")
    userAttacker = initialEnvironmentScreen.addLabel("User: ", 9*(width/15), height/37, "flat")

    # Labels de la cancion que esta sonando 
    musicDefender = initialEnvironmentScreen.addLabel(" Music: ", width/15, 2*(height/37), "flat")
    musicAttacker = initialEnvironmentScreen.addLabel("Music: ", 9*(width/15), 2*(height/37), "flat")

    # Labels del rol que desarolla cada jugador
    rolDefender = initialEnvironmentScreen.addLabel("Defender", 6.5*(width/15), height/37, "flat")
    rolAttacker = initialEnvironmentScreen.addLabel("Attacker", 14*(width/15), height/37, "flat")

    # Labels de de los datos curiosos de las canciones
    funFactDefender = initialEnvironmentScreen.addLabel("", width/8, height/11, "flat")
    funFactAttacker = initialEnvironmentScreen.addLabel("Fun Facts: ...", 5.25*(width/8), height/11, "flat")

    # Imagenes de perfil
    profilePicAttacker = initialEnvironmentScreen.addLabel("Profile Pic", 8*(width/15), height/25,"flat")

    #Imagen Defensa
    profilePicDefender = initialEnvironmentScreen.addCanvas(70,70, 0, 0,"#86895d")
    profilePicDefender.bind("<Button-1>",lambda event, stage=initialEnvironmentScreen, usr=user: edit(event,stage,usr))
    originalPic = Image.open(list[6]+"/PROFILEPIC.png")
    profilePicPath = originalPic
    # Cambiar el tamaño de la imagen original a 200x200 píxeles
    originalPic = originalPic.resize((70, 70))

    # Crear una máscara en forma de óvalo
    ancho, alto = originalPic.size
    mascara = Image.new("L", (ancho, alto), 0)
    draw = ImageDraw.Draw(mascara)
    draw.ellipse((0, 0, ancho, alto), fill=255)

    # Aplicar la máscara a la imagen original
    reSizePic = Image.new("RGBA", (ancho, alto))
    reSizePic.paste(originalPic, mask=mascara)

    # Convertir la imagen recortada en PhotoImage para mostrarla en el Canvas
    imagen_tk = ImageTk.PhotoImage(reSizePic)
    profilePicDefender.create_image(35,35,image=imagen_tk)
    profilePicDefender.image=imagen_tk

    #Canva Fondo 1
    if(list[8]=="1"):
        bgRoute="./Backgrounds/Background1.png"
    elif(list[8]=="2"):
        bgRoute = "./Backgrounds/Background2.png"
    else:
        bgRoute = "./Backgrounds/Background3.png"
    backGrounDefense=initialEnvironmentScreen.addCanvas(width/2,4*height/5, 0, height/5+5,"#000000")
    bgPic=Image.open(bgRoute)
    bgPic=bgPic.resize((int(width/2)+4,4*int(height/5)+2))
    bgPic=ColorFilter.colorFilter("#272b00", bgPic)
    bgPic=ImageTk.PhotoImage(bgPic)
    backGrounDefense.create_image(width/4+2,2*height/5-2,image=bgPic)

    # Label del tiempo
    GUIBuilder.widgetDict = {
                'funFactDefender': initialEnvironmentScreen.addLabel("Fun Facts: ...", width / 8, height / 11, "flat"),
                'wallsLb': initialEnvironmentScreen.addLabel("Walls: ", 0.4*(width/30), height/6.7, "flat"),
                'powersLb': initialEnvironmentScreen.addLabel("Powers: ", 15.4*(width/30), height/6.7, "flat"),
                'pointsDefender': initialEnvironmentScreen.addLabel("Points: ", 0.4*(width/30),height/11,"flat"),
                'pointsAttacker': initialEnvironmentScreen.addLabel("Points: ", 15.4*(width/30),height/11,"flat"),
                'userDefender': initialEnvironmentScreen.addLabel("User: ", width/15, height/37, "flat"),
                'userAttacker': initialEnvironmentScreen.addLabel("User: ", 9*(width/15), height/37, "flat"),
                'musicDefender': initialEnvironmentScreen.addLabel("", width/15, 2*(height/37), "flat"),
                'musicAttacker': initialEnvironmentScreen.addLabel("Music: ", 9*(width/15), 2*(height/37), "flat"),
                'rolDefender': initialEnvironmentScreen.addLabel("Defender", 6.5*(width/15), height/37, "flat"),
                'rolAttacker': initialEnvironmentScreen.addLabel("Attacker", 14*(width/15), height/37, "flat"),
                'funFactAttacker': initialEnvironmentScreen.addLabel("Fun Facts: ...", 5.25*(width/8), height/11, "flat"),
                #'profilePicDefender': initialEnvironmentScreen.addLabel("Profile Pic", width/43, height/25,"flat"),
                'profilePicAttacker': initialEnvironmentScreen.addLabel("Profile Pic", 8*(width/15), height/25, "flat"),
        }

    comboxChooseLanguage = initialEnvironmentScreen.addCombox()
    comboxChooseLanguage.bind("<<ComboboxSelected>>",lambda event,self=initialEnvironmentScreen: GUIBuilder.updateLanguage(self,event))




    print(width, height)




    # Inizia el bucle de la ventana del ambiente inicial
    if not(initialEnvironmentScreen.initialize()):
        return False

def load(user):
    list=[]
    register.decrypt()
    # Cargar el archivo encriptado
    tree = ET.parse("DataBase.xml")
    root = tree.getroot()
    register.encrypt()
    for client in root.findall('Cliente'):
        if client.find('User').text==user:
            for data in client:
                print(data.text)
                list.append(data.text)

    return list

def edit(event,stage,user):
    GUIBuilder.closeEnvironment(stage)
    RegisterGUI.begin(1,user)
