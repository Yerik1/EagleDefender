from tkinter import *
from tkinter import colorchooser, filedialog, font
from tkinterdnd2 import DND_FILES, TkinterDnD
import os
from PIL import Image, ImageTk
import PIL
from PIL import ImageDraw
from GUIBuilder import GUIBuilder
from Register import register, validate, decrypt,encrypt
from CapturingFaces import Biometric
from PictureTaker import CamApp
import xml.etree.ElementTree as ET
import cv2
import shutil
width=""
height=""
root=""
BG=""
entryA=""
entryB=""
entryC=""
entryD=""
entryE=""
dispA=""
dispB=""
dispC=""
dispD=""
dispE=""
showPassword=""
entryPassword=""
entryConfPassword=""
entrySA=""
entryMusic=""
buttonSA=""
entrySB=""
buttonSB=""
entrySC=""
buttonSC=""
entryBg=""
entryBr=""
entryWb=""
entryFb=""
entryBmb=""
buttonProfPic=""
entryUser=""
entryName=""
entryEmail=""
entryAge=""
varCheckbox=""
profilePic=""
picLabel=""
status=True

#myImg = ImageTk.PhotoImage(Image.open(imageName).resize((100, 100)))

def cargarImagen(imageName):
    img=Image.open(imageName)
    return img

# Funcion para crear botones
def buttons(title, action, color1, color2, a, b):
    btn = Button(root, text=title, command=action, bd=0, relief="sunken", activebackground="#86895d")
    btn.config(bg=color1)
    btn.place(x=a, y=b)

    # Define el fondo del boton cuando el puntero sale
    def change1(event):
        btn.config(bg=color1)

    # Define el fondo del boton cuando el puntero entra
    def change2(event):
        btn.config(bg=color2)

    # Metodo que cierra la ventana

    # Cambia el color del boton cuando el puntero pasa por este
    btn.bind("<Leave>", change1)  # Sale
    btn.bind("<Enter>", change2)  # Entra

# Funcion que Agrega labels
def addLabel(txt, a, b, r, s):
    titleFont = font.Font(family="Times New Romans", size=s)
    label = Label(root, text=txt, bg=BG, relief=r, font=titleFont)
    label.place(x=a, y=b)

# Funcion que cierra la ventana
def closeEnvironment():
    global status
    root.protocol("WM_DELETE_WINDOW",changeStatus(False))
    try:
        os.remove("Temp/foto_capturada.png")
    except Exception as e:
        print(e)
    root.destroy()
    status=False

# Funcion que minimiza la ventana
def minimize():
    root.iconify()


"""
funcion que convierte de rgb a hexadecimal
"""

def _from_rgb(rgb):
    return "#%02x%02x%02x" % rgb

"""
funcion que permite escoger un color con el mouse y crear la paleta de colores
"""

def colorpic(e):
    global width, height

    # Creacion de paleta de colores
    b1 = Image.open(imageName).resize((100, 100)).convert("RGB")
    b1 = b1.getpixel((e.x, e.y))
    b2 = (b1[1], b1[0], b1[2])
    if (b2[2] <= 130):
        b3 = (b2[0], b2[1], b2[2] + 125)
    elif (b2[1] <= 130):
        b3 = (b2[0], b2[1] + 125, b2[2])
    else:
        b3 = (b2[0], b2[1], b2[2] - 125)

    b4 = (b1[2], abs(b1[1] - 255), b1[0])

    if (b4[2] <= 130):
        b5 = (b4[0], b4[1], b4[2] + 125)

    elif (b4[1] <= 130):
        b5 = (b4[0], b4[1] + 125, b4[2])
    else:
        b5 = (b4[0], b4[1], b4[2] - 125)

    # Colores en hexadecimal
    color = _from_rgb(b1)
    color2 = _from_rgb(b2)
    color3 = _from_rgb(b3)
    color4 = _from_rgb(b4)
    color5 = _from_rgb(b5)

    # ordena los colores de menor a mayor en hexadecimal
    hex = [color, color2, color3, color4, color5]
    hex.sort()

    # Se edita las entries de los colores para mostrar el codigo de color
    entryA.config(state="normal")
    entryA.delete(0, END)
    entryA.insert(0, str(hex[0]))  # hex
    entryA.config(state="disabled")
    entryB.config(state="normal")
    entryB.delete(0, END)
    entryB.insert(0, str(hex[1]))  # hex
    entryB.config(state="disabled")
    entryC.config(state="normal")
    entryC.delete(0, END)
    entryC.insert(0, str(hex[2]))  # hex
    entryC.config(state="disabled")
    entryD.config(state="normal")
    entryD.delete(0, END)
    entryD.insert(0, str(hex[3]))  # hex
    entryD.config(state="disabled")
    entryE.config(state="normal")
    entryE.delete(0, END)
    entryE.insert(0, str(hex[4]))  # hex
    entryE.config(state="disabled")

    # Agregs el color a los botones
    dispA.config(bg=hex[0], fg=hex[0])
    dispB.config(bg=hex[1], fg=hex[1])
    dispC.config(bg=hex[2], fg=hex[2])
    dispD.config(bg=hex[3], fg=hex[3])
    dispE.config(bg=hex[4], fg=hex[4])

"""
funcion que recopila la informacion de los entries
"""

def save():
    global colorA, colorB, colorC, colorD, colorE
    colorA = entryA.get()
    colorB = entryB.get()
    colorC = entryC.get()
    colorD = entryD.get()
    colorD = entryE.get()

def showHidePassword():
    if (showPassword.cget("text") == "Show Password"):
        entryPassword.configure(show="")
        entryConfPassword.configure(show="")
        showPassword.config(text="Hide Password")
    else:
        entryPassword.configure(show="⧫")
        entryConfPassword.configure(show="⧫")
        showPassword.config(text="Show Password")

def addSong(event):
    if (entrySA.get() == ""):
        entrySA.config(state="normal")
        entrySA.insert(0, entryMusic.get())
        entrySA.config(state="disabled")
        buttonSA.config(state="normal", bg="red")
    elif (entrySB.get() == ""):
        entrySB.config(state="normal")
        entrySB.insert(0, entryMusic.get())
        entrySB.config(state="disabled")
        buttonSB.config(state="normal", bg="red")
    elif (entrySC.get() == ""):
        entrySC.config(state="normal")
        entrySC.insert(0, entryMusic.get())
        entrySC.config(state="disabled")
        buttonSC.config(state="normal", bg="red")

def deleteSong1():
    entrySA.config(state="normal")
    entrySA.delete(0, END)
    entrySA.insert(0, entrySB.get())
    entrySA.config(state="disabled")
    if (entrySA.get() == ""):
        buttonSA.config(state="disabled", bg="SystemButtonFace")
        buttonSB.config(state="disabled", bg="SystemButtonFace")
        buttonSC.config(state="disabled", bg="SystemButtonFace")
    deleteSong2()

def deleteSong2():
    entrySB.config(state="normal")
    entrySB.delete(0, END)
    entrySB.insert(0, entrySC.get())
    entrySB.config(state="disabled")
    if (entrySB.get() == ""):
        buttonSB.config(state="disabled", bg="SystemButtonFace")
        buttonSC.config(state="disabled", bg="SystemButtonFace")
    deleteSong3()

def deleteSong3():
    entrySC.config(state="normal")
    entrySC.delete(0, END)
    entrySC.insert(0, "")
    entrySC.config(state="disabled")
    if (entrySC.get() == ""):
        buttonSC.config(state="disabled", bg="SystemButtonFace")

def selectBackground(event, number):
    entryBg.config(state="normal")
    entryBg.delete(0, END)
    entryBg.insert(0, number)
    entryBg.config(state="disabled")

def selectBarrier(event, number):
    entryBr.config(state="normal")
    entryBr.delete(0, END)
    entryBr.insert(0, number)
    entryBr.config(state="disabled")

def selectWB(event, number):
    entryWb.config(state="normal")
    entryWb.delete(0, END)
    entryWb.insert(0, number)
    entryWb.config(state="disabled")

def selectFB(event, number):
    entryFb.config(state="normal")
    entryFb.delete(0, END)
    entryFb.insert(0, number)
    entryFb.config(state="disabled")

def selectBmb(event, number):
    entryBmb.config(state="normal")
    entryBmb.delete(0, END)
    entryBmb.insert(0, number)
    entryBmb.config(state="disabled")

def profilePicMaker():
    global extention
    # Cargar la imagen
    pictureRoute = filedialog.askopenfilename(initialdir="/Desktop/python codes", title="open images", filetypes=(
    ("png files", "*.png"), ("jpg files", "*.jpg"), ("jpeg files", "*.jpeg"), ("svh files", "*.svh"),
    ("pdf files", "*.pdf")))

    # Obtener la extensión del archivo
    _, format = os.path.splitext(pictureRoute)
    extention = format[1:].lower()  # Elimina el punto y convierte a minúsculas
    profilePicPlacer(pictureRoute)

def profilePicPlacer(pictureRoute):
    global profilePicPath, profilePic
    originalPic = Image.open(pictureRoute)
    profilePicPath = originalPic
    # Cambiar el tamaño de la imagen original a 200x200 píxeles
    originalPic = originalPic.resize((200, 200))

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

    # Mostrar la imagen en el Canvas
    profilePic.create_image(100, 100, image=imagen_tk)
    profilePic.image = imagen_tk  # Evita que la imagen sea eliminada por el recolector de basura
    buttonProfPic.place(x=width / 4, y=25, anchor=CENTER)

    # guarda la foto de perfil y la ruta

def dragPic(event):
    global profilePicPath, extention
    picture = event.data
    # Obtener la extensión del archivo
    _, format = os.path.splitext(picture)
    extention = format[1:].lower()  # Elimina el punto y convierte a minúsculas
    profilePicPlacer(picture)

def deleteProfile(user):
    decrypt()
    tree = ET.parse("DataBase.xml")
    root = tree.getroot()
    encrypt()
    for username2 in root.findall('Cliente'):
        usernameSave = username2.find('User').text
        if usernameSave == user:
            root.remove(username2)
            shutil.rmtree("./FacialRecognition/"+user)
            shutil.rmtree("./ProfilePics/"+user)
            break
def editProfile(user):
    flag=True
    newUser=entryUser.get()
    if(newUser!=user):
        decrypt()
        tree = ET.parse("DataBase.xml")
        root = tree.getroot()
        encrypt()

        # Analizar el XML desencriptado

        for username2 in root.findall('Cliente'):
            usernameSave = username2.find('User').text
            if usernameSave==newUser:
                print("Usuario ya existe")
                flag=False
                break

    if flag:
        registerGUI(1)


def registerGUI(case):
    global profilePicPath, extention, biometric, status
    list = [entryUser, entryPassword, entryConfPassword, entryName, entryEmail, entryAge, entrySA, entrySB, entrySC,
            entryA, entryB
        , entryC, entryD, entryE, entryBr, entryBg, entryWb, entryFb, entryBmb]
    list2 = []
    fileRoute = ""
    flag = True
    if (list[2].get() == list[1].get()):

        for item in list:
            list2.append(item.get())
            # info opcional
            if item != list[6] and item != list[7] and item != list[8] and item != list[9] and item != list[
                10] and item != list[11] and item != list[12] and item != list[13] and item != list[14] and item != list[15] and item != list[16] and item != list[17] and item != list[18]:
                if (item.get() == ""):
                    flag = False
                    break

        if flag:
            if validate(list2[0], list2[1]):
                bmt=""
                if (case == 1):
                    deleteProfile(entryUser.get())
                if (profilePicPath != ""):
                    fileRoute = "./ProfilePics/" + list2[0]

                if (biometric):
                    bmt = Biometric()
                    bmt.initialice(list2[0], root)
                    print("finish")
                if(bmt!="#NO#"and bmt!="No Camera"):
                    os.makedirs(fileRoute)
                    profilePicPath.save(fileRoute + "/PROFILEPIC." + extention)
                    register(list2, fileRoute)
                    status=False


        else:
            print("Porfavor llenar todos los espacios")
    else:
        print("No coinciden las contraseñas")

def toggle_checkbox():
    global biometric
    if varCheckbox.get():
        biometric = True
    else:
        biometric = False

def changeStatus(state):
    global status
    status=state

def takepicture(event):
    global picLabel, profilePic, extention
    try:
        picLabel.destroy()
    except Exception as e:
        print(e)
    picLabel = Label(profilePic)
    picLabel.place(x=100, y=100, anchor=CENTER)
    picLabel.bind("<Button-1>", takepicture)
    camera=CamApp(picLabel)
    route=camera.begin()
    #bg=("#%02x%02x%02x" % (root.winfo_rgb(profilePic.cget("image"))))
    _, format = os.path.splitext(route)
    extention = format[1:].lower()
    profilePicPlacer(route)
    picLabel.configure(image="",text="")
    picLabel.destroy()


def begin(case,user):
    global width, height, root, BG, imageName, entryA, entryB, entryC, entryD, entryE, dispA, dispB, dispC, dispD, dispE, showPassword, entryPassword, entryConfPassword, entrySA, entryMusic, buttonSA, entrySB, buttonSB, entrySC, buttonSC, entryBg, entryBr, entryWb, entryFb, entryBmb, buttonProfPic, entryUser, entryName, entryEmail, entryAge, varCheckbox, status, profilePic,picLabel
    # Creacion de la ventana
    root=TkinterDnD.Tk()
    root.config(background="#86895d")
    root.drop_target_register(DND_FILES)
    root.attributes("-fullscreen", True)

    BG = "#86895d"

    # Obtener las dimensiones de la pantalla
    width = root.winfo_screenwidth()  # Ancho de la pantalla
    height = root.winfo_screenheight()  # Alto de la pantalla menos 50 píxeles para la barra de tareas

    # Pone los botones para cerrar y minimizar la ventana
    buttons(" x ", closeEnvironment, "Red", "Blue", width - 23, -0.5)
    buttons(" - ", minimize, "Red", "Blue", width - 45, -0.5)

    # Agraga el label del titulo
    addLabel("Register", width / 2 - 60, 0.1 * (height / 30), "flat", 25)

    # Agrega los labels de la ventana de Registro

    addLabel("Name", width / 2 - 110, 48, "flat", 12)

    addLabel("User", width / 2 - 103, 74, "flat", 12)

    addLabel("Password", width / 2 - 140, 98, "flat", 12)

    addLabel("Confirm Password", width / 2 - 198, 123, "flat", 12)

    addLabel("Email", width / 2 - 110, 148, "flat", 12)

    addLabel("Age", width / 2 - 99, 173, "flat", 12)

    addLabel("Music", width / 2 - 111, 199, "flat", 12)

    profilePicPath = ""
    extention = ""
    biometric = False
    # Establecer las dimensiones de la ventana
    root.geometry(f"{width}x{height}+-7+0")

    # Se crean las entries del registro
    entryUser = Entry(root, width=20)
    entryUser.place(x=width / 2, y=85, anchor=CENTER)

    entryPassword = Entry(root, width=20, show="⧫")
    entryPassword.place(x=width / 2, y=110, anchor=CENTER)

    entryConfPassword = Entry(root, width=20, show="⧫")
    entryConfPassword.place(x=width / 2, y=135, anchor=CENTER)

    entryName = Entry(root, width=20)
    entryName.place(x=width / 2, y=60, anchor=CENTER)

    entryEmail = Entry(root, width=20)
    entryEmail.place(x=width / 2, y=160, anchor=CENTER)

    entryAge = Entry(root, width=20)
    entryAge.place(x=width / 2, y=185, anchor=CENTER)

    entryMusic = Entry(root, width=20)
    entryMusic.place(x=width / 2, y=210, anchor=CENTER)
    entryMusic.bind("<Return>",addSong)

    # Boton mostrar contraseña
    showPassword = Button(root, text="Show Password", command=showHidePassword)
    showPassword.place(x=width / 2 + 130, y=120, anchor=CENTER)


    # Entries con canciones agregadas
    entrySA = Entry(root, width=20)
    entrySA.place(x=width / 2 + 140, y=185, anchor=CENTER)
    entrySA.config(state="disabled")
    entrySB = Entry(root, width=20)
    entrySB.place(x=width / 2 + 140, y=210, anchor=CENTER)
    entrySB.config(state="disabled")
    entrySC = Entry(root, width=20)
    entrySC.place(x=width / 2 + 140, y=235, anchor=CENTER)
    entrySC.config(state="disabled")

    # Botones para eliminar las canciones
    buttonSA = Button(root, text="X", command=deleteSong1)
    buttonSA.place(x=width / 2 + 230, y=185, anchor=CENTER)
    buttonSA.config(state="disabled")
    buttonSB = Button(root, text="X", command=deleteSong2)
    buttonSB.place(x=width / 2 + 230, y=210, anchor=CENTER)
    buttonSB.config(state="disabled")
    buttonSC = Button(root, text="X", command=deleteSong3)
    buttonSC.place(x=width / 2 + 230, y=235, anchor=CENTER)
    buttonSC.config(state="disabled")

    # se crea el canvas de la rueda de color
    c = Canvas(root, width=97, height=95, bg="black", highlightbackground=BG)
    c.place(x=(width / 2), y=300, anchor=CENTER)
    imageName="./ColorWheel.png"
    myImg=cargarImagen(imageName)
    # se agrega la rueda de color como imagen
    try:
        myImg = myImg.resize((100, 100))
        myImg = ImageTk.PhotoImage(myImg)
        c.create_image(50, 50, image=myImg, anchor=CENTER)
        c.bind("<Button-1>", colorpic)
    except Exception as e:
        print("Error al cargar o procesar la imagen:", e)

    profilePic = Canvas(root, width=200, height=200, bg="#86895d", highlightbackground="#86895d")
    profilePic.place(x=width / 4 - 100, y=50)
    profilePic.create_oval(1,1,200,200, fill= "#ffffff")
    font1 = font.Font(family="Times New Romans", size=25)
    picLabel=Label(profilePic, text="+",bg="#ffffff",font=font1)
    picLabel.place(x=100,y=100,anchor=CENTER)
    profilePic.bind("<Button-1>",takepicture)
    picLabel.bind("<Button-1>",takepicture)



    # Se crean los lugares donde aparece el codigo de color y se muestra el color
    entryA = Entry(root, width=10, state="disabled")
    entryA.place(x=width / 2 + 50, y=250)
    entryB = Entry(root, width=10, state="disabled")
    entryB.place(x=width / 2 + 50, y=270)
    entryC = Entry(root, width=10, state="disabled")
    entryC.place(x=width / 2 + 50, y=290)
    entryD = Entry(root, width=10, state="disabled")
    entryD.place(x=width / 2 + 50, y=310)
    entryE = Entry(root, width=10, state="disabled")
    entryE.place(x=width / 2 + 50, y=330)

    dispA = Button(root, text="  ", state="disabled")
    dispA.place(x=width / 2 + 100, y=250)
    dispB = Button(root, text="  ", state="disabled")
    dispB.place(x=width / 2 + 100, y=270)
    dispC = Button(root, text="  ", state="disabled")
    dispC.place(x=width / 2 + 100, y=290)
    dispD = Button(root, text="  ", state="disabled")
    dispD.place(x=width / 2 + 100, y=310)
    dispE = Button(root, text="  ", state="disabled")
    dispE.place(x=width / 2 + 100, y=330)

    # Seleccion de imagenes
    bg1 = "./Backgrounds/Background1.PNG"
    copyBg1 = Image.open(bg1)
    myBg1 = ImageTk.PhotoImage(Image.open(bg1).resize((100, 100)))

    cbg1 = Canvas(root, width=100, height=100, bg=BG, highlightbackground=BG)
    cbg1.place(x=(width / 3 - 100), y=410, anchor=CENTER)
    cbg1.create_image(50, 50, image=myBg1, anchor=CENTER)
    cbg1.bind("<Button-1>", lambda event, p=1: selectBackground(event, p))

    bg2 = "./Backgrounds/Background2.PNG"
    copyBg2 = Image.open(bg2)
    myBg2 = ImageTk.PhotoImage(Image.open(bg2).resize((100, 100)))

    cbg2 = Canvas(root, width=100, height=100, bg=BG, highlightbackground=BG)
    cbg2.place(x=(width / 3), y=410, anchor=CENTER)
    cbg2.create_image(50, 50, image=myBg2, anchor=CENTER)
    cbg2.bind("<Button-1>", lambda event, p=2: selectBackground(event, p))

    bg3 = "./Backgrounds/Background3.PNG"
    copyBg3 = Image.open(bg3)
    myBg3 = ImageTk.PhotoImage(Image.open(bg3).resize((100, 100)))

    cbg3 = Canvas(root, width=100, height=100, bg=BG, highlightbackground=BG)
    cbg3.place(x=(width / 3 + 100), y=410, anchor=CENTER)
    cbg3.create_image(50, 50, image=myBg3, anchor=CENTER)
    cbg3.bind("<Button-1>", lambda event, p=3: selectBackground(event, p))

    entryBg = Entry(root, width=20)
    entryBg.place(x=(width / 3), y=475, anchor=CENTER)
    entryBg.config(state="disabled")

    # Seleccion de imagenes barreras
    br1 = "./Barriers/Barrier1.PNG"
    copyBr1 = Image.open(br1)
    myBr1 = ImageTk.PhotoImage(Image.open(br1).resize((100, 100)))

    cbr1 = Canvas(root, width=100, height=100, bg=BG, highlightbackground=BG)
    cbr1.place(x=(2 * width / 3 - 100), y=410, anchor=CENTER)
    cbr1.create_image(50, 50, image=myBr1, anchor=CENTER)
    cbr1.bind("<Button-1>", lambda event, p=1: selectBarrier(event, p))

    br2 = "./Barriers/Barrier2.PNG"
    copyBr2 = Image.open(bg2)
    myBr2 = ImageTk.PhotoImage(Image.open(br2).resize((100, 100)))

    cbr2 = Canvas(root, width=100, height=100, bg=BG, highlightbackground=BG)
    cbr2.place(x=(2 * width / 3), y=410, anchor=CENTER)
    cbr2.create_image(50, 50, image=myBr2, anchor=CENTER)
    cbr2.bind("<Button-1>", lambda event, p=2: selectBarrier(event, p))

    br3 = "./Barriers/Barrier3.PNG"
    copyBr3 = Image.open(bg3)
    myBr3 = ImageTk.PhotoImage(Image.open(br3).resize((100, 100)))

    cbr3 = Canvas(root, width=100, height=100, bg=BG, highlightbackground=BG)
    cbr3.place(x=(2 * width / 3 + 100), y=410, anchor=CENTER)
    cbr3.create_image(50, 50, image=myBr3, anchor=CENTER)
    cbr3.bind("<Button-1>", lambda event, p=3: selectBarrier(event, p))

    entryBr = Entry(root, width=20)
    entryBr.place(x=(2 * width / 3), y=475, anchor=CENTER)
    entryBr.config(state="disabled")

    # Seleccion de imagenes bola agua
    wb1 = "./Powers/WaterBalls/WB1.PNG"
    copyWb1 = Image.open(wb1)
    myWb1 = ImageTk.PhotoImage(Image.open(wb1).resize((100, 100)))

    cwb1 = Canvas(root, width=100, height=100, bg=BG, highlightbackground=BG)
    cwb1.place(x=(width / 4 - 100), y=550, anchor=CENTER)
    cwb1.create_image(50, 50, image=myWb1, anchor=CENTER)
    cwb1.bind("<Button-1>", lambda event, p=1: selectWB(event, p))

    wb2 = "./Powers/WaterBalls/WB2.PNG"
    copyWb2 = Image.open(wb1)
    myWb2 = ImageTk.PhotoImage(Image.open(wb2).resize((100, 100)))

    cwb2 = Canvas(root, width=100, height=100, bg=BG, highlightbackground=BG)
    cwb2.place(x=(width / 4), y=550, anchor=CENTER)
    cwb2.create_image(50, 50, image=myWb2, anchor=CENTER)
    cwb2.bind("<Button-1>", lambda event, p=2: selectWB(event, p))

    wb3 = "./Powers/WaterBalls/WB3.PNG"
    copyWb3 = Image.open(wb3)
    myWb3 = ImageTk.PhotoImage(Image.open(wb3).resize((100, 100)))

    cwb3 = Canvas(root, width=100, height=100, bg=BG, highlightbackground=BG)
    cwb3.place(x=(width / 4) + 100, y=550, anchor=CENTER)
    cwb3.create_image(50, 50, image=myWb3, anchor=CENTER)
    cwb3.bind("<Button-1>", lambda event, p=3: selectWB(event, p))

    entryWb = Entry(root, width=20)
    entryWb.place(x=(width / 4), y=615, anchor=CENTER)
    entryWb.config(state="disabled")

    # Seleccion de imagenes bola fuego
    fb1 = "./Powers/FireBalls/FB1.PNG"
    copyFb1 = Image.open(fb1)
    myFb1 = ImageTk.PhotoImage(Image.open(fb1).resize((100, 100)))

    cfb1 = Canvas(root, width=100, height=100, bg="white", highlightbackground=BG)
    cfb1.place(x=(width / 2 - 100), y=550, anchor=CENTER)
    cfb1.create_image(50, 50, image=myFb1, anchor=CENTER)
    cfb1.bind("<Button-1>", lambda event, p=1: selectFB(event, p))

    fb2 = "./Powers/FireBalls/FB2.PNG"
    copyFb2 = Image.open(fb2)
    myFb2 = ImageTk.PhotoImage(Image.open(fb2).resize((100, 100)))

    cfb2 = Canvas(root, width=100, height=100, bg=BG, highlightbackground=BG)
    cfb2.place(x=(width / 2), y=550, anchor=CENTER)
    cfb2.create_image(50, 50, image=myFb2, anchor=CENTER)
    cfb2.bind("<Button-1>", lambda event, p=2: selectFB(event, p))

    fb3 = "./Powers/FireBalls/FB3.PNG"
    copyFb3 = Image.open(fb3)
    myFb3 = ImageTk.PhotoImage(Image.open(fb3).resize((100, 100)))

    cfb3 = Canvas(root, width=100, height=100, bg=BG, highlightbackground=BG)
    cfb3.place(x=(width / 2) + 100, y=550, anchor=CENTER)
    cfb3.create_image(50, 50, image=myFb3, anchor=CENTER)
    cfb3.bind("<Button-1>", lambda event, p=3: selectFB(event, p))

    entryFb = Entry(root, width=20)
    entryFb.place(x=(width / 2), y=615, anchor=CENTER)
    entryFb.config(state="disabled")

    # Seleccion de imagenes bola fuego
    bmb1 = "./Powers/Bombs/Bomb1.PNG"
    copyBmb1 = Image.open(bmb1)
    myBmb1 = ImageTk.PhotoImage(Image.open(bmb1).resize((100, 100)))

    cbmb1 = Canvas(root, width=100, height=100, bg=BG, highlightbackground=BG)
    cbmb1.place(x=(3 * width / 4 - 100), y=550, anchor=CENTER)
    cbmb1.create_image(50, 50, image=myBmb1, anchor=CENTER)
    cbmb1.bind("<Button-1>", lambda event, p=1: selectBmb(event, p))

    bmb2 = "./Powers/Bombs/Bomb2.PNG"
    copyBmb2 = Image.open(bmb2)
    myBmb2 = ImageTk.PhotoImage(Image.open(bmb2).resize((100, 100)))

    cbmb2 = Canvas(root, width=100, height=100, bg=BG, highlightbackground=BG)
    cbmb2.place(x=(3 * width / 4), y=550, anchor=CENTER)
    cbmb2.create_image(50, 50, image=myBmb2, anchor=CENTER)
    cbmb2.bind("<Button-1>", lambda event, p=2: selectBmb(event, p))

    bmb3 = "./Powers/Bombs/Bomb3.PNG"
    copyBmb3 = Image.open(bmb3)
    myBmb3 = ImageTk.PhotoImage(Image.open(bmb3).resize((100, 100)))

    cbmb3 = Canvas(root, width=100, height=100, bg=BG, highlightbackground=BG)
    cbmb3.place(x=(3 * width / 4 + 100), y=550, anchor=CENTER)
    cbmb3.create_image(50, 50, image=myBmb3, anchor=CENTER)
    cbmb3.bind("<Button-1>", lambda event, p=3: selectBmb(event, p))

    entryBmb = Entry(root, width=20)
    entryBmb.place(x=(3 * width / 4), y=615, anchor=CENTER)
    entryBmb.config(state="disabled")

    buttonProfPic = Button(root, text="Add Profile Picture", command=profilePicMaker)
    buttonProfPic.place(x=width / 4, y=25, anchor=CENTER)

    if case==0:
        # Boton para registrarse
        buttonRegister = Button(root, text="Register", command=lambda:registerGUI(case), bd=0, relief="sunken",
                                activebackground="SystemButtonFace")
        buttonRegister.place(x=width / 2 - 30, y=700)
    else:
        # Boton para registrarse
        buttonRegister = Button(root, text="Edit", command=lambda:editProfile(user), bd=0, relief="sunken",
                                activebackground="SystemButtonFace")
        buttonRegister.place(x=width / 2 - 30, y=700)

    root.dnd_bind('<<Drop>>', dragPic)

    # Variable para rastrear el estado de la casilla de verificación
    varCheckbox = BooleanVar()

    # Crear la casilla de verificación
    checkbox = Checkbutton(root, text="Biometric", variable=varCheckbox, command=toggle_checkbox)
    checkbox.place(x=width / 4, y=300)
    #Abre la ventana
    root.mainloop()
    while(True):
        if not status:
            return False
    
