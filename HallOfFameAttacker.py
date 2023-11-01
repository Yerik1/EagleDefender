from GUIBuilder import GUIBuilder
import Register as register
import xml.etree.ElementTree as ET
import RegisterGUI
import ColorFilter
import PIL
from PIL import Image
#from PIL import Image, ImageTk
from PIL import ImageDraw, ImageTk
from tkinter import *
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter import colorchooser, filedialog, font
from Game import Game






def begin(user):
    list= load(user)
    # Colores predeterminados
    color1 = "#272b00"
    color2 = "#54582f"
    color3 = "#86895d"
    color4 = "#bec092"
    chosenColor = "#272b00"

    # Crea la ventana del salon de la fama
    hallOfFameScreen = GUIBuilder("#86895d")

    #titleLbl = hallOfFameScreen.addLabel("Hall of Fame", 0.4*(width/30), height/6.7, "flat")


    # Obtener las dimensiones de la pantalla
    width = hallOfFameScreen.root.winfo_screenwidth() # Ancho
    height = hallOfFameScreen.root.winfo_screenheight() # Alto

    titleLbl = hallOfFameScreen.addLabel("Hall of Fame", width/2, height/7,"flat")
    titleLbl.config(font=("Arial",60))

    rolLbl = hallOfFameScreen.addLabel("Attackers", width/2, height/20,"flat")
    rolLbl.config(font=("Arial",60))

    #Define los labels de la posicion 1
    user1Lbl= hallOfFameScreen.addLabel("", width/3.50,height/3.45,"flat")
    user1Lbl.config(font=("Arial",40))
    dotsLbl = hallOfFameScreen.addLabel("............................", width / 2, height / 3.45, "flat")
    dotsLbl.config(font=("Arial", 40))

    pts1Lbl = hallOfFameScreen.addLabel("points",width/1.42,height/3.45,"flat")
    pts1Lbl.config(font=("Arial",40))

    #Define los labels de la posicion 2
    user2Lbl = hallOfFameScreen.addLabel("", width / 3.50, height /2.55, "flat")
    user2Lbl.config(font=("Arial", 40))

    pts2Lbl = hallOfFameScreen.addLabel("points", width / 1.42, height / 2.55, "flat")
    pts2Lbl.config(font=("Arial", 40))

    dotsLbl2 = hallOfFameScreen.addLabel("............................", width /2 , height / 2.55 , "flat")
    dotsLbl2.config(font=("Arial", 40))

    #Define los labels de la posicion 3
    user3Lbl = hallOfFameScreen.addLabel("", width / 3.50, height /2, "flat")
    user3Lbl.config(font=("Arial", 40))

    pts3Lbl = hallOfFameScreen.addLabel("", width / 1.42 , height / 2, "flat")
    pts3Lbl.config(font=("Arial", 40))

    dotsLbl3 = hallOfFameScreen.addLabel("............................", width / 2, height / 2, "flat")
    dotsLbl3.config(font=("Arial", 40))

    #Determina los labels de la posicion 4
    pos4Lbl= hallOfFameScreen.addLabel("4.",width/5, height/1.65,"flat")
    pos4Lbl.config(font=("Arial",40))

    user4Lbl = hallOfFameScreen.addLabel("", width / 3.50, height /1.65, "flat")
    user4Lbl.config(font=("Arial", 40))

    pts4Lbl = hallOfFameScreen.addLabel("points", width / 1.42, height / 1.65, "flat")
    pts4Lbl.config(font=("Arial", 40))

    dotsLbl4 = hallOfFameScreen.addLabel("............................", width / 2, height / 1.65, "flat")
    dotsLbl4.config(font=("Arial", 40))

    pos5Lbl = hallOfFameScreen.addLabel("5.", width / 5 , height / 1.40, "flat")
    pos5Lbl.config(font=("Arial", 40))

    user5Lbl = hallOfFameScreen.addLabel("", width / 3.50, height /1.40 , "flat")
    user5Lbl.config(font=("Arial", 40))

    pts5Lbl = hallOfFameScreen.addLabel("points", width / 1.42, height / 1.40 , "flat")
    pts5Lbl.config(font=("Arial", 40))
    
    dotsLbl5 = hallOfFameScreen.addLabel("............................", width / 2, height / 1.40, "flat")
    dotsLbl5.config(font=("Arial", 40))

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

    backBtn = hallOfFameScreen.buttons("Back",print('hola'),"White","Blue",width/2, height/1.10)
    backBtn.config(width=5,height=2)





    if not(hallOfFameScreen.initialize()):
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

'''
# Apartado de Ranking ==============================================================================================================================
# Transformar de txt de nombres a lista ------------------------------------
def conseguir_nombres(lista_nombres):
    with open('Ranking_Nombres.txt') as nombres_txt:
        lines = nombres_txt.readlines()
        lista_nombres = lines
        return sort_nombres(lista_nombres, 0)


# Acomoda los nombres con respecto a la posición del jugador
def sort_nombres(lista_nombres, conteo):
    global lista_nombres_completados, posicion, nombre_usuario, lista_nombres_completados
    posicion = int(posicion)
    if posicion > 5:
        return 0
    if posicion > conteo + 1:
        conteo += 1
        lista_nombres_completados.append(lista_nombres[0])
        return sort_nombres(lista_nombres[1:], conteo)
    else:
        nombre_usuario += '\n'
        lista_nombres_completados.append(nombre_usuario.replace('\r', ''))
        tamaño = int(len(lista_nombres) - 1)
        lista_nombres_completados = lista_nombres_completados + lista_nombres[0:tamaño]
        return sobreescribir_txt(lista_nombres_completados)


# Reescribe los los nombres al txt
def sobreescribir_txt(lista):
    with open('Ranking_Nombres.txt', 'w') as nombres_txt:
        nombres_txt.write(lista[0])
        nombres_txt.write(lista[1])
        nombres_txt.write(lista[2])
        nombres_txt.write(lista[3])
        nombres_txt.write(lista[4])
        nombres_txt.write(lista[5])
        nombres_txt.write(lista[6])
        nombres_txt.write(lista[7])
        nombres_txt.write(lista[8])
        nombres_txt.write(lista[9])
        return 0


# Transformar de txt a lista ------------------------------------
def cont(conteo, lista, seek):
    global posicion
    MiArchi1 = open('Ranking.txt', 'r+')
    posicion = 1
    if conteo < 5:
        MiArchi1.seek(seek)
        num = MiArchi1.readline()
        lista.append(int(num))
        conteo += 1
        seek += 5
        return cont(conteo, lista, seek)
    else:
        MiArchi1.close()
        return insert_sort(lista)


# Ordenar de menor a mayor la lista -------------------------------------
def insert_sort(Lista):
    return insert_sort_aux(Lista, 1, len(Lista))


def insert_sort_aux(Lista, i, n):
    if i == n:
        return aux_invierta(Lista, [])
    Aux = Lista[i]
    j = incluye_orden(Lista, i, Aux)
    Lista[j] = Aux
    return insert_sort_aux(Lista, i + 1, n)


def incluye_orden(Lista, j, Aux):
    if j <= 0 or Lista[j - 1] <= Aux:
        return j
    Lista[j] = Lista[j - 1]
    return incluye_orden(Lista, j - 1, Aux)


# Invertir lista ------------------------------------------
def aux_invierta(lista, lista_final):
    if lista != []:
        num = lista[-1]
        lista_final.append(num)
        return aux_invierta(lista[:-1], lista_final)
    else:
        return comparar(lista_final, [])


# Comparar la lista con el puntaje obtenido --------------------------
def comparar(lista, lista_completa):
    global posicion, puntaje_obtenido, volver
    puntaje_obtenido = int(puntaje_obtenido)
    if lista == []:
        volver = WINNER_FONT.render('volverás a la pantalla de forma automática', 1, (255, 255, 255))
        return 0
    if puntaje_obtenido < lista[0]:
        num_mayor = lista[0]
        posicion += 1
        lista_completa.append(num_mayor)
        return comparar(lista[1:], lista_completa)
    else:
        lista_completa.append(puntaje_obtenido)
        tamaño = int(len(lista) - 1)
        lista_completa = lista_completa + lista[0:tamaño]
        return nueva_lista(lista_completa, 0, 0)


# Agregar nuevos elementos a la lista completa ----------
def nueva_lista(lista, num, seek):
    global posicion, volver
    MiArchi1 = open('Ranking.txt', 'r+')
    if lista == []:
        MiArchi1.close()
        conseguir_nombres([])
        posicion = str(posicion)
        volver = WINNER_FONT.render('Felicidades! Quedaste en la posición: ' + posicion, 1, (255, 255, 255))
        return 0
    else:
        MiArchi1.seek(seek)
        num = lista[0]
        num = str(num) + '\n'
        MiArchi1.write(num)
        seek += 5
        return nueva_lista(lista[1:], 0, seek)
'''

def edit(event,stage,user):
    GUIBuilder.closeEnvironment(stage)
    RegisterGUI.begin(1,user)


begin("Yerik1")