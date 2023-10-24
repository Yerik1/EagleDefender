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

    titleLbl = hallOfFameScreen.addLabel("Hall of Fame", width/2-250, height/7, "flat")
    titleLbl.config(font=("Arial",60))

    rolLbl = hallOfFameScreen.addLabel("Attackers", width/2-187, height/7-100,"flat")
    rolLbl.config(font=("Arial",60))


    user1Lbl= hallOfFameScreen.addLabel("User1", width/3-100,height/4+40,"flat")
    user1Lbl.config(font=("Arial",40))

    pts1Lbl = hallOfFameScreen.addLabel("points",width/3+600,height/4+40,"flat")
    pts1Lbl.config(font=("Arial",40))


    user2Lbl = hallOfFameScreen.addLabel("User2", width / 3-100, height /4 +40+90, "flat")
    user2Lbl.config(font=("Arial", 40))

    pts2Lbl = hallOfFameScreen.addLabel("points", width / 3 + 600, height / 4 + 40+90, "flat")
    pts2Lbl.config(font=("Arial", 40))

    user3Lbl = hallOfFameScreen.addLabel("User3", width / 3-100, height /4 +40+180, "flat")
    user3Lbl.config(font=("Arial", 40))

    pts3Lbl = hallOfFameScreen.addLabel("points", width / 3 + 600, height / 4 + 40+180, "flat")
    pts3Lbl.config(font=("Arial", 40))


    pos4Lbl= hallOfFameScreen.addLabel("4.",width/3-170, height/4+40+270,"flat")
    pos4Lbl.config(font=("Arial",40))

    user4Lbl = hallOfFameScreen.addLabel("User4", width / 3-100, height /4+40+270 , "flat")
    user4Lbl.config(font=("Arial", 40))

    pts4Lbl = hallOfFameScreen.addLabel("points", width / 3 + 600, height / 4 + 40+270, "flat")
    pts4Lbl.config(font=("Arial", 40))

    pos5Lbl = hallOfFameScreen.addLabel("5.", width / 3 - 170, height / 4 + 40 + 360, "flat")
    pos5Lbl.config(font=("Arial", 40))

    user5Lbl = hallOfFameScreen.addLabel("User5", width / 3-100, height /4+40+360 , "flat")
    user5Lbl.config(font=("Arial", 40))

    pts5Lbl = hallOfFameScreen.addLabel("points", width / 3 + 600, height / 4 + 40+360, "flat")
    pts5Lbl.config(font=("Arial", 40))

    dotsLbl= hallOfFameScreen.addLabel(".....................", width/3+100,height/4+40,"flat")
    dotsLbl.config(font=("Arial",40))

    dotsLbl2 = hallOfFameScreen.addLabel(".....................", width / 3 + 100, height / 4 + 40+90, "flat")
    dotsLbl2.config(font=("Arial", 40))

    dotsLbl3 = hallOfFameScreen.addLabel(".....................", width / 3 + 100, height / 4 + 40+180, "flat")
    dotsLbl3.config(font=("Arial", 40))

    dotsLbl4 = hallOfFameScreen.addLabel(".....................", width / 3 + 100, height / 4 + 40+270, "flat")
    dotsLbl4.config(font=("Arial", 40))

    dotsLbl5 = hallOfFameScreen.addLabel(".....................", width / 3 + 100, height / 4 + 40+360, "flat")
    dotsLbl5.config(font=("Arial", 40))

    firstPlace= "./HallOfFameImages/medallaOro.png"
    #copyFirstPlace= Image.open(firstPlace)
    myFirstPlace = ImageTk.PhotoImage(PIL.Image.open(firstPlace).resize((40,40)))

    cFirstPlace = hallOfFameScreen.addCanvas(40,40,width/3-150,height/4+50, "Black")
    cFirstPlace.create_image(21.5, 21.5, image=myFirstPlace, anchor=CENTER)

    secondPlace= "./HallOfFameImages/medallaPlata.png"
    #copyFirstPlace= Image.open(firstPlace)
    mySecondPlace = ImageTk.PhotoImage(PIL.Image.open(secondPlace).resize((42,42)))

    cSecondPlace = hallOfFameScreen.addCanvas(40,40,width/3-150,height/4+140, "Black")
    cSecondPlace.create_image(21.5, 21.5, image=mySecondPlace, anchor=CENTER)

    thirdPlace= "./HallOfFameImages/medallaBronce.png"
    #copyFirstPlace= Image.open(firstPlace)
    myThirdPlace = ImageTk.PhotoImage(PIL.Image.open(thirdPlace).resize((42,42)))

    cThirdPlace = hallOfFameScreen.addCanvas(40,40,width/3-150,height/4+230, "Black")
    cThirdPlace.create_image(21.5, 21.5, image=myThirdPlace, anchor=CENTER)

    logo1= "./HallOfFameImages/Logo.png"
    #copyFirstPlace= Image.open(firstPlace)
    myLogo1 = ImageTk.PhotoImage(PIL.Image.open(logo1).resize((200,200)))

    clogo1 = hallOfFameScreen.addCanvas(200,200,width/3-480,height/4-200, "Black")
    clogo1.create_image(100, 100, image=myLogo1, anchor=CENTER)

    logo2= "./HallOfFameImages/Logo.png"
    #copyFirstPlace= Image.open(firstPlace)
    myLogo2 = ImageTk.PhotoImage(PIL.Image.open(logo2).resize((200,200)))

    cLogo2 = hallOfFameScreen.addCanvas(200,200,width/3+940,height/4-200, "Black")
    cLogo2.create_image(100, 100, image=myLogo1, anchor=CENTER)





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



def edit(event,stage,user):
    GUIBuilder.closeEnvironment(stage)
    RegisterGUI.begin(1,user)


begin("Yerik1")