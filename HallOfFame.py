from GUIBuilder import GUIBuilder
import Register as register
import ColorFilter
import PIL
from PIL import Image
#from PIL import Image, ImageTk
from PIL import ImageDraw, ImageTk
from tkinter import *
import xml.etree.ElementTree as ET
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter import colorchooser, filedialog, font
from Game import Game
import Spotify as sp

list=[]
width=0
height=0



def begin():
    global list,width,height
    list=load()

    # Crea la ventana del salon de la fama
    hallOfFameScreen = GUIBuilder("#86895d")

    #titleLbl = hallOfFameScreen.addLabel("Hall of Fame", 0.4*(width/30), height/6.7, "flat")


    # Obtener las dimensiones de la pantalla
    width = hallOfFameScreen.root.winfo_screenwidth() # Ancho
    height = hallOfFameScreen.root.winfo_screenheight() # Alto

    titleLbl = hallOfFameScreen.addLabel("Hall of Fame", width/2, height/7,"flat")
    titleLbl.config(font=("Arial",60))

    #rolLbl = hallOfFameScreen.addLabel("Attackers", width/2, height/20,"flat")
    #rolLbl.config(font=("Arial",60))

    #Define los labels de la posicion 1
    user1Lbl= hallOfFameScreen.addLabel(list[0][0], width/3.50,height/3.45,"flat")
    user1Lbl.config(font=("Arial",36))
    dotsLbl = hallOfFameScreen.addLabel("............................", width / 2, height / 3.45, "flat")
    dotsLbl.config(font=("Arial", 36))

    pts1Lbl = hallOfFameScreen.addLabel(str(list[0][1])+" points",width/1.39,height/3.45,"flat")
    pts1Lbl.config(font=("Arial",36))

    #Define los labels de la posicion 2
    user2Lbl = hallOfFameScreen.addLabel(list[1][0], width / 3.50, height /2.55, "flat")
    user2Lbl.config(font=("Arial", 36))

    pts2Lbl = hallOfFameScreen.addLabel(str(list[1][1])+" points", width / 1.39, height / 2.55, "flat")
    pts2Lbl.config(font=("Arial", 36))

    dotsLbl2 = hallOfFameScreen.addLabel("............................", width /2 , height / 2.55 , "flat")
    dotsLbl2.config(font=("Arial", 36))

    #Define los labels de la posicion 3
    user3Lbl = hallOfFameScreen.addLabel(list[2][0], width / 3.50, height /2, "flat")
    user3Lbl.config(font=("Arial", 36))

    pts3Lbl = hallOfFameScreen.addLabel("", width / 1.42 , height / 2, "flat")
    pts3Lbl.config(font=("Arial", 36))

    dotsLbl3 = hallOfFameScreen.addLabel("............................", width / 2, height / 2, "flat")
    dotsLbl3.config(font=("Arial", 36))

    pts3Lbl = hallOfFameScreen.addLabel(str(list[2][1])+" points", width / 1.39, height / 2, "flat")
    pts3Lbl.config(font=("Arial", 36))

    #Determina los labels de la posicion 4
    pos4Lbl= hallOfFameScreen.addLabel("4.",width/5, height/1.65,"flat")
    pos4Lbl.config(font=("Arial",36))

    user4Lbl = hallOfFameScreen.addLabel(list[3][0], width / 3.50, height /1.65, "flat")
    user4Lbl.config(font=("Arial", 36))

    pts4Lbl = hallOfFameScreen.addLabel(str(list[3][1])+" points", width / 1.39, height / 1.65, "flat")
    pts4Lbl.config(font=("Arial", 36))

    dotsLbl4 = hallOfFameScreen.addLabel("............................", width / 2, height / 1.65, "flat")
    dotsLbl4.config(font=("Arial", 36))

    pos5Lbl = hallOfFameScreen.addLabel("5.", width / 5 , height / 1.40, "flat")
    pos5Lbl.config(font=("Arial", 36))

    user5Lbl = hallOfFameScreen.addLabel(list[4][0], width / 3.50, height /1.40 , "flat")
    user5Lbl.config(font=("Arial", 36))

    pts5Lbl = hallOfFameScreen.addLabel(str(list[4][1])+" points", width / 1.39, height / 1.40 , "flat")
    pts5Lbl.config(font=("Arial", 36))
    
    dotsLbl5 = hallOfFameScreen.addLabel("............................", width / 2, height / 1.40, "flat")
    dotsLbl5.config(font=("Arial", 36))

    firstPlace= "./HallOfFameImages/medallaOro.png"
    #copyFirstPlace= Image.open(firstPlace)
    myFirstPlace = ImageTk.PhotoImage(PIL.Image.open(firstPlace).resize((40,40)))

    cFirstPlace = hallOfFameScreen.addCanvas(40,40,width/5.20,height/3.80, "Black")
    cFirstPlace.create_image(21.5, 21.5, image=myFirstPlace, anchor=CENTER)

    secondPlace= "./HallOfFameImages/medallaPlata.png"
    #copyFirstPlace= Image.open(firstPlace)
    mySecondPlace = ImageTk.PhotoImage(PIL.Image.open(secondPlace).resize((42,42)))

    cSecondPlace = hallOfFameScreen.addCanvas(40,40,width/5.20,height/2.75, "Black")
    cSecondPlace.create_image(21.5, 21.5, image=mySecondPlace, anchor=CENTER)

    thirdPlace= "./HallOfFameImages/medallaBronce.png"
    #copyFirstPlace= Image.open(firstPlace)
    myThirdPlace = ImageTk.PhotoImage(PIL.Image.open(thirdPlace).resize((42,42)))

    cThirdPlace = hallOfFameScreen.addCanvas(40,40,width/5.20,height/2.15, "Black")
    cThirdPlace.create_image(21.5, 21.5, image=myThirdPlace, anchor=CENTER)

    logo1= "./HallOfFameImages/Logo.png"
    #copyFirstPlace= Image.open(firstPlace)
    myLogo1 = ImageTk.PhotoImage(PIL.Image.open(logo1).resize((200,200)))

    clogo1 = hallOfFameScreen.addCanvas(200,200,width/35,height/40, "Black")
    clogo1.create_image(100, 100, image=myLogo1, anchor=CENTER)


    logo2= "./HallOfFameImages/Logo.png"
    #copyFirstPlace= Image.open(firstPlace)
    myLogo2 = ImageTk.PhotoImage(PIL.Image.open(logo2).resize((200,200)))

    cLogo2 = hallOfFameScreen.addCanvas(200,200,width/1.2,height/40, "Black")
    cLogo2.create_image(100, 100, image=myLogo1, anchor=CENTER)

    #BUTTONS
    bt1=hallOfFameScreen.buttons("Play",lambda: (playSongs(0,bt1,0)),"White","White",width/1.2,height/3.45)
    bt2 = hallOfFameScreen.buttons("Play", lambda: (playSongs(1, bt2,0)), "White", "White", width / 1.2, height / 2.55)
    bt3 = hallOfFameScreen.buttons("Play", lambda: (playSongs(2, bt3,0)), "White", "White", width / 1.2, height / 2)


    if not(hallOfFameScreen.initialize()):
        return False

def load():
    register.decrypt()
    # Cargar el archivo "HallOfFame.xml" con los usuarios del Salón de la Fama
    tree_hall_of_fame = ET.parse('HallOfFame.xml')
    root_hall_of_fame = tree_hall_of_fame.getroot()

    hallOfFameList=[]

    # Recorrer los usuarios del Salón de la Fama
    for user_elem in root_hall_of_fame.findall("User"):
        username = user_elem.text
        user_points = int(user_elem.find("Points").text)
        # Cargar el archivo "DataBase.xml" para buscar información de usuarios
        tree_database = ET.parse("DataBase.xml")
        root = tree_database.getroot()
        list = []
        # Buscar el usuario en "DataBase.xml" por su nombre de usuario
        for client in root.findall('Cliente'):
            if client.find('User').text == username:
                # Crear una lista para almacenar la información de los usuarios
                list.append(username)
                list.append(user_points)
                for data in client:
                    if (data.tag == "Music"):
                        for song in data:
                            print(song.text)
                            list.append(song.text)
        hallOfFameList.append(list)

    register.encrypt()
    print(hallOfFameList)
    return hallOfFameList


def entryHallOfFame(user,points):
    tree = ET.parse('HallOfFame.xml')
    root = tree.getroot()

    # Crear un diccionario para almacenar los usuarios y sus puntajes
    users_dict = {}

    # Recopilar los usuarios y sus puntajes actuales en un diccionario
    for user_elem in root.findall("User"):
        username = user_elem.text
        user_points = int(user_elem.find("Points").text)
        users_dict[username] = user_points

    # Agregar el nuevo usuario y puntaje al diccionario
    users_dict[user] = points

    # Ordenar el diccionario por puntajes en orden descendente
    sorted_users = sorted(users_dict.items(), key=lambda x: x[1], reverse=True)

    # Limitar la cantidad de usuarios en el Salón de la Fama a 5
    if len(sorted_users) > 5:
        sorted_users = sorted_users[:5]

    # Actualizar el XML con los usuarios en el Salón de la Fama
    root.clear()
    for username, user_points in sorted_users:
        user_elem = ET.Element('User')
        user_elem.text = username
        points_elem = ET.SubElement(user_elem, 'Points')
        points_elem.text = str(user_points)
        root.append(user_elem)

    # Guardar los cambios en el archivo XML
    tree.write('HallOfFame.xml')

def playSongs(position, button,state):
    global list
    if state==0:
        sp.play(list[position][2])
        button.config(command=lambda:playSongs(position,button,1),text="pause")
    else:
        sp.pauseSong()
        button.config(command=lambda: playSongs(position, button, 0), text="play")



