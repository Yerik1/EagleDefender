from tkinter import *
import tkinter as tk
from tkinter import ttk
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
import colorsys
import Spotify as sp
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
entrySetBarriers= ""
entrySetPowers= ""
buttonProfPic=""
entryUser=""
entryName=""
entryEmail=""
entryAge=""
varCheckbox=""
profilePic=""
profilePicPath=""
picLabel=""
extention=""
combo=""
labelError=""
biometric=False
status=True

#myImg = ImageTk.PhotoImage(Image.open(imageName).resize((100, 100)))
def checkStatus():
    global status
    print("entro")
    while (True):
        if not status:
            closeEnvironment()
            return False
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
    return btn

# Funcion que Agrega labels
def addLabel(txt, a, b, r, s):
    titleFont = font.Font(family="Times New Romans", size=s)
    label = Label(root, text=txt, bg=BG, relief=r, font=titleFont)
    label.place(x=a, y=b)
    return label

# Funcion que cierra la ventana
def closeEnvironment():
    global status, root
    root.protocol("WM_DELETE_WINDOW")
    try:
        os.remove("Temp/foto_capturada.png")
    except Exception as e:
        pass
    root.destroy()


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
    palette=generateColorPalette(b1)
    # Colores en hexadecimal
    color =  palette[0]
    color2 = palette[1]
    color3 = palette[2]
    color4 = palette[3]
    color5 = palette[4]

    # ordena los colores de menor a mayor en hexadecimal
    hex = [color, color2, color3, color4, color5]
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


# Función para generar paleta de colores
def generateColorPalette(baseColor):
    # Convierte los valores RGB en valores HSV
    base_hsv = colorsys.rgb_to_hsv(*[x / 255.0 for x in baseColor])

    # Calcula colores complementarios
    color_palette = []
    for i in range(5):
        hue = (base_hsv[0] + (i / 5)) % 0.75 # Asegúrate de que el valor de matiz esté en el rango [0, 1]
        rgb = colorsys.hsv_to_rgb(hue, base_hsv[1], base_hsv[2])
        rgb = tuple(int(x * 255) for x in rgb)
        color = '#{:02x}{:02x}{:02x}'.format(*rgb)
        color_palette.append(color)


    return color_palette

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

def addSong(song):
    if (entrySA.get() == ""):
        entrySA.config(state="normal")
        entrySA.insert(0, song)
        entrySA.config(state="disabled")
        buttonSA.config(state="normal", bg="red")
        entryMusic.delete(0,"end")
    elif (entrySB.get() == ""):
        entrySB.config(state="normal")
        entrySB.insert(0, song)
        entrySB.config(state="disabled")
        buttonSB.config(state="normal", bg="red")
        entryMusic.delete(0, "end")
    elif (entrySC.get() == ""):
        entrySC.config(state="normal")
        entrySC.insert(0, song)
        entrySC.config(state="disabled")
        buttonSC.config(state="normal", bg="red")
        entryMusic.delete(0, "end")

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

def updateComboBox(e):
    global combo, root
    list=sp.searchSong(entryMusic.get())
    combo.delete(0, 'end')
    if not (entryMusic.get() == ""):
        for item in list:
            combo.insert(tk.END,item)
        combo.place(x=width / 2, y=250, anchor=CENTER)
    else:
        combo.place(x=width / 2, y=230, anchor=CENTER)

def selectOption(e):

    try:
        selected_option = combo.get(combo.curselection())
        addSong(selected_option)
        entryMusic.delete(0, tk.END)
        updateComboBox("")
    except: pass
def selectSetBarriers(event, number):
    entrySetBarriers.config(state="normal")
    entrySetBarriers.delete(0, END)
    entrySetBarriers.insert(0, number)
    entrySetBarriers.config(state="disabled")

def selectSetPowers(event, number):
    entrySetPowers.config(state="normal")
    entrySetPowers.delete(0, END)
    entrySetPowers.insert(0, number)
    entrySetPowers.config(state="disabled")

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
    global picLabel,profilePicPath, profilePic
    try:
        picLabel.destroy()
    except : pass
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
            try:
                shutil.rmtree("./FacialRecognition/"+user)
            except: pass
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
    global labelError, profilePicPath, extention, biometric, status
    list = [entryUser, entryPassword, entryConfPassword, entryName, entryEmail, entryAge, entrySA, entrySB, entrySC,
            entryA, entryB
        , entryC, entryD, entryE, entrySetBarriers, entrySetPowers]
    list2 = []
    fileRoute = ""
    flag = True
    if (list[2].get() == list[1].get()):

        for item in list:
            list2.append(item.get())
            # info opcional
            if item != list[6] and item != list[7] and item != list[8] and item != list[9] and item != list[
                10] and item != list[11] and item != list[12] and item != list[13] and item != list[14] and item != list[15]:
                if (item.get() == ""):
                    flag = False
                    break

        if flag:
            text=validate(list2[0], list2[1])
            if isinstance(text,bool):
                bmt=""
                if (case == 1):
                    deleteProfile(entryUser.get())

                fileRoute = "./ProfilePics/" + list2[0]
                if (biometric):
                    bmt = Biometric()
                    bmt.initialice(list2[0], root)
                    print("finish")
                if(bmt!="#NO#"and bmt!="No Camera"):
                    os.makedirs(fileRoute)
                    if(profilePicPath==""):
                        profilePicPlacer("./Default/default.jpg")
                        extention="jpg"
                    profilePicPath.save(fileRoute + "/PROFILEPIC." + extention)
                    fileRoute=fileRoute + "/PROFILEPIC." + extention
                    register(list2, fileRoute)
                    closeEnvironment()
                else:
                    labelError.config(text="Fallo en la biometrica")
            else:
                labelError.config(text=text)


        else:
            labelError.config(text="Porfavor llenar todos los espacios")
    else:
        labelError.config(text="No coinciden las contraseñas")
    labelError.config(fg="red")
    labelError.place(x=width/2,y=650, anchor="center")
def toggle_checkbox():
    global biometric
    if varCheckbox.get():
        biometric = True
    else:
        biometric = False

def changeStatus():
    global status
    status=False

def takepicture(event):
    global picLabel, profilePic, extention
    try:
        picLabel.destroy()
    except : pass
    picLabel = Label(profilePic)
    picLabel.place(x=100, y=100, anchor=CENTER)
    picLabel.bind("<Button-1>", takepicture)
    camera=CamApp(picLabel)
    route=camera.begin()
    #bg=("#%02x%02x%02x" % (root.winfo_rgb(profilePic.cget("image"))))
    if not(isinstance(route,bool)):
        _, format = os.path.splitext(route)
        extention = format[1:].lower()
        profilePicPlacer(route)
    else:
        try:
            picLabel.destroy()
        except:
            pass
        profilePic.create_oval(1, 1, 200, 200, fill="#ffffff")
        font1 = font.Font(family="Times New Romans", size=25)
        picLabel = Label(profilePic, text="+", bg="#ffffff", font=font1)
        picLabel.place(x=100, y=100, anchor=CENTER)
        profilePic.bind("<Button-1>", takepicture)
        picLabel.bind("<Button-1>", takepicture)



def begin(case,user):
    global labelError, combo, width, height, root, BG, imageName, entryA, entryB, entryC, entryD, entryE, dispA, dispB, dispC, dispD, dispE, showPassword, entryPassword, entryConfPassword, entrySA, entryMusic, buttonSA, entrySB, buttonSB, entrySC, buttonSC, entrySetBarriers, entrySetPowers, buttonProfPic, entryUser, entryName, entryEmail, entryAge, varCheckbox, status, profilePic,picLabel, currentImage
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
    #entryMusic.bind("<Return>",addSong)
    entryMusic.bind("<KeyRelease>",updateComboBox)

    combo= Listbox(root, width=20, height=-50,selectmode="single")
    combo.place(x=width / 2, y=230, anchor=CENTER)
    combo.lift()
    combo.bind("<Button-1>", selectOption)

    # Boton mostrar contraseña
    showPassword = Button(root, text="Show Password", command=showHidePassword)
    showPassword.place(x=width / 2 + 130, y=120, anchor=CENTER)

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

    # Carga tus tres imágenes aquí
    imagen1 = tk.PhotoImage(file='Flags/espFlag.png')
    imagen2 = tk.PhotoImage(file='Flags/ingFlag.png')
    imagen3 = tk.PhotoImage(file='Flags/frnFlag.png')

    # Redimenciona las imagenes
    img1 = imagen1.subsample(25)
    img2 = imagen2.subsample(25)
    img3 = imagen3.subsample(25)

    # Crea una lista con las imagenes
    imagenes = [img1, img2, img3]

    btnFlags = Button(root, image=imagenes[currentImage], command=lambda:(changeImage(), print("Action")), bd=0 , relief="sunken", bg=BG, activebackground=BG )
    btnFlags.place( x = width / 60, y = height / 45)

    # Entries con canciones agregadas
    entrySA = Entry(root, width=30)
    entrySA.place(x=width / 2 + 160, y=185, anchor=CENTER)
    entrySA.config(state="disabled")
    entrySB = Entry(root, width=30)
    entrySB.place(x=width / 2 + 160, y=210, anchor=CENTER)
    entrySB.config(state="disabled")
    entrySC = Entry(root, width=30)
    entrySC.place(x=width / 2 + 160, y=235, anchor=CENTER)
    entrySC.config(state="disabled")

    # Botones para eliminar las canciones
    buttonSA = Button(root, text="X", command=deleteSong1)
    buttonSA.place(x=width / 2 + 265, y=185, anchor=CENTER)
    buttonSA.config(state="disabled")
    buttonSB = Button(root, text="X", command=deleteSong2)
    buttonSB.place(x=width / 2 + 265, y=210, anchor=CENTER)
    buttonSB.config(state="disabled")
    buttonSC = Button(root, text="X", command=deleteSong3)
    buttonSC.place(x=width / 2 + 265, y=235, anchor=CENTER)
    buttonSC.config(state="disabled")

    # se crea el canvas de la rueda de color
    c = Canvas(root, width=97, height=95, bg="black", highlightbackground=BG)
    c.place(x=(width / 2), y=375, anchor=CENTER)
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
    entryA.place(x=width / 2 + 50, y=325)
    entryB = Entry(root, width=10, state="disabled")
    entryB.place(x=width / 2 + 50, y=345)
    entryC = Entry(root, width=10, state="disabled")
    entryC.place(x=width / 2 + 50, y=365)
    entryD = Entry(root, width=10, state="disabled")
    entryD.place(x=width / 2 + 50, y=385)
    entryE = Entry(root, width=10, state="disabled")
    entryE.place(x=width / 2 + 50, y=405)

    dispA = Button(root, text="  ", state="disabled")
    dispA.place(x=width / 2 + 100, y=325)
    dispB = Button(root, text="  ", state="disabled")
    dispB.place(x=width / 2 + 100, y=345)
    dispC = Button(root, text="  ", state="disabled")
    dispC.place(x=width / 2 + 100, y=365)
    dispD = Button(root, text="  ", state="disabled")
    dispD.place(x=width / 2 + 100, y=385)
    dispE = Button(root, text="  ", state="disabled")
    dispE.place(x=width / 2 + 100, y=405)

    # Seleccion de imagenes
    wd1 = "Barriers/Wood/Wood1.PNG"
    copyBg1 = Image.open(wd1)
    myWd1 = ImageTk.PhotoImage(Image.open(wd1).resize((100, 100)))

    cwd1 = Canvas(root, width=100, height=100, bg=BG, highlightbackground=BG)
    cwd1.place(x=(width / 4 - 100), y=410, anchor=CENTER)
    cwd1.create_image(50, 50, image=myWd1, anchor=CENTER)
    cwd1.bind("<Button-1>", lambda event, p=1: selectSetBarriers(event, p))

    sn1 = "Barriers/Stone/Stone1.PNG"
    copyBg1 = Image.open(sn1)
    mySn1 = ImageTk.PhotoImage(Image.open(sn1).resize((100, 100)))

    csn1 = Canvas(root, width=100, height=100, bg=BG, highlightbackground=BG)
    csn1.place(x=(width / 4 ), y=410, anchor=CENTER)
    csn1.create_image(50, 50, image=mySn1, anchor=CENTER)
    csn1.bind("<Button-1>", lambda event, p=1: selectSetBarriers(event, p))

    st1 = "Barriers/Steel/Steel1.PNG"
    copyBg1 = Image.open(st1)
    mySt1 = ImageTk.PhotoImage(Image.open(st1).resize((100, 100)))

    cst1 = Canvas(root, width=100, height=100, bg=BG, highlightbackground=BG)
    cst1.place(x=(width / 4 + 100), y=410, anchor=CENTER)
    cst1.create_image(50, 50, image=mySt1, anchor=CENTER)
    cst1.bind("<Button-1>", lambda event, p=1: selectSetBarriers(event, p))

    #set 2
    wd2 = "Barriers/Wood/Wood2.PNG"
    copyBg1 = Image.open(wd1)
    myWd2 = ImageTk.PhotoImage(Image.open(wd2).resize((100, 100)))

    cwd2 = Canvas(root, width=100, height=100, bg=BG, highlightbackground=BG)
    cwd2.place(x=(width / 4 - 100), y=515, anchor=CENTER)
    cwd2.create_image(50, 50, image=myWd2, anchor=CENTER)
    cwd2.bind("<Button-1>", lambda event, p=2: selectSetBarriers(event, p))

    sn2 = "Barriers/Stone/Stone2.PNG"
    copyBg2 = Image.open(sn2)
    mySn2 = ImageTk.PhotoImage(Image.open(sn2).resize((100, 100)))

    csn2 = Canvas(root, width=100, height=100, bg=BG, highlightbackground=BG)
    csn2.place(x=(width / 4), y=515, anchor=CENTER)
    csn2.create_image(50, 50, image=mySn2, anchor=CENTER)
    csn2.bind("<Button-1>", lambda event, p=2: selectSetBarriers(event, p))

    st2 = "Barriers/Steel/Steel2.PNG"
    copyBg2 = Image.open(st2)
    mySt2 = ImageTk.PhotoImage(Image.open(st2).resize((100, 100)))

    cst2 = Canvas(root, width=100, height=100, bg=BG, highlightbackground=BG)
    cst2.place(x=(width / 4 + 100), y=515, anchor=CENTER)
    cst2.create_image(50, 50, image=mySt2, anchor=CENTER)
    cst2.bind("<Button-1>", lambda event, p=2: selectSetBarriers(event, p))

    wd3 = "Barriers/Wood/Wood3.PNG"
    copyBg3 = Image.open(wd3)
    myWd3 = ImageTk.PhotoImage(Image.open(wd3).resize((100, 100)))

    cwd3 = Canvas(root, width=100, height=100, bg=BG, highlightbackground=BG)
    cwd3.place(x=(width / 4 - 100), y=620, anchor=CENTER)
    cwd3.create_image(50, 50, image=myWd3, anchor=CENTER)
    cwd3.bind("<Button-1>", lambda event, p=3: selectSetBarriers(event, p))

    sn3 = "Barriers/Stone/Stone3.PNG"
    copyBg1 = Image.open(sn3)
    mySn3 = ImageTk.PhotoImage(Image.open(sn3).resize((100, 100)))

    csn3 = Canvas(root, width=100, height=100, bg=BG, highlightbackground=BG)
    csn3.place(x=(width / 4), y=620, anchor=CENTER)
    csn3.create_image(50, 50, image=mySn3, anchor=CENTER)
    csn3.bind("<Button-1>", lambda event, p=3: selectSetBarriers(event, p))

    st3 = "Barriers/Steel/Steel3.PNG"
    copyBg3 = Image.open(st3)
    mySt3 = ImageTk.PhotoImage(Image.open(st3).resize((100, 100)))

    cst3 = Canvas(root, width=100, height=100, bg=BG, highlightbackground=BG)
    cst3.place(x=(width / 4 + 100), y=620, anchor=CENTER)
    cst3.create_image(50, 50, image=mySt3, anchor=CENTER)
    cst3.bind("<Button-1>", lambda event, p=3: selectSetBarriers(event, p))

    entrySetBarriers = Entry(root, width=20)
    entrySetBarriers.place(x=(width / 4), y=725, anchor=CENTER)
    entrySetBarriers.config(state="disabled")


    # Seleccion de imagenes bola agua
    wb1 = "./Powers/WaterBalls/WB1.PNG"
    copyWb1 = Image.open(wb1)
    myWb1 = ImageTk.PhotoImage(Image.open(wb1).resize((100, 100)))

    cwb1 = Canvas(root, width=100, height=100, bg=BG, highlightbackground=BG)
    cwb1.place(x=(3*width / 4 - 100), y=410, anchor=CENTER)
    cwb1.create_image(50, 50, image=myWb1, anchor=CENTER)
    cwb1.bind("<Button-1>", lambda event, p=1: selectSetPowers(event, p))

    wb2 = "./Powers/WaterBalls/WB2.PNG"
    copyWb2 = Image.open(wb1)
    myWb2 = ImageTk.PhotoImage(Image.open(wb2).resize((100, 100)))

    cwb2 = Canvas(root, width=100, height=100, bg=BG, highlightbackground=BG)
    cwb2.place(x=(3*width / 4 - 100), y=515, anchor=CENTER)
    cwb2.create_image(50, 50, image=myWb2, anchor=CENTER)
    cwb2.bind("<Button-1>", lambda event, p=2: selectSetPowers(event, p))

    wb3 = "./Powers/WaterBalls/WB3.PNG"
    copyWb3 = Image.open(wb3)
    myWb3 = ImageTk.PhotoImage(Image.open(wb3).resize((100, 100)))

    cwb3 = Canvas(root, width=100, height=100, bg=BG, highlightbackground=BG)
    cwb3.place(x=(3*width / 4 - 100), y=620, anchor=CENTER)
    cwb3.create_image(50, 50, image=myWb3, anchor=CENTER)
    cwb3.bind("<Button-1>", lambda event, p=3: selectSetPowers(event, p))


    # Seleccion de imagenes bola fuego
    fb1 = "./Powers/FireBalls/FB1.PNG"
    copyFb1 = Image.open(fb1)
    myFb1 = ImageTk.PhotoImage(Image.open(fb1).resize((100, 100)))

    cfb1 = Canvas(root, width=100, height=100, bg="white", highlightbackground=BG)
    cfb1.place(x=(3*width / 4), y=410, anchor=CENTER)
    cfb1.create_image(50, 50, image=myFb1, anchor=CENTER)
    cfb1.bind("<Button-1>", lambda event, p=1: selectSetPowers(event, p))

    fb2 = "./Powers/FireBalls/FB2.PNG"
    copyFb2 = Image.open(fb2)
    myFb2 = ImageTk.PhotoImage(Image.open(fb2).resize((100, 100)))

    cfb2 = Canvas(root, width=100, height=100, bg=BG, highlightbackground=BG)
    cfb2.place(x=(3*width / 4), y=515, anchor=CENTER)
    cfb2.create_image(50, 50, image=myFb2, anchor=CENTER)
    cfb2.bind("<Button-1>", lambda event, p=2: selectSetPowers(event, p))

    fb3 = "./Powers/FireBalls/FB3.PNG"
    copyFb3 = Image.open(fb3)
    myFb3 = ImageTk.PhotoImage(Image.open(fb3).resize((100, 100)))

    cfb3 = Canvas(root, width=100, height=100, bg=BG, highlightbackground=BG)
    cfb3.place(x=(3*width / 4), y=620, anchor=CENTER)
    cfb3.create_image(50, 50, image=myFb3, anchor=CENTER)
    cfb3.bind("<Button-1>", lambda event, p=3: selectSetPowers(event, p))


    # Seleccion de imagenes bola fuego
    bmb1 = "./Powers/Bombs/Bomb1.PNG"
    copyBmb1 = Image.open(bmb1)
    myBmb1 = ImageTk.PhotoImage(Image.open(bmb1).resize((100, 100)))

    cbmb1 = Canvas(root, width=100, height=100, bg=BG, highlightbackground=BG)
    cbmb1.place(x=(3*width / 4 + 100), y=410, anchor=CENTER)
    cbmb1.create_image(50, 50, image=myBmb1, anchor=CENTER)
    cbmb1.bind("<Button-1>", lambda event, p=1: selectSetPowers(event, p))

    bmb2 = "./Powers/Bombs/Bomb2.PNG"
    copyBmb2 = Image.open(bmb2)
    myBmb2 = ImageTk.PhotoImage(Image.open(bmb2).resize((100, 100)))

    cbmb2 = Canvas(root, width=100, height=100, bg=BG, highlightbackground=BG)
    cbmb2.place(x=(3*width / 4 + 100), y=515, anchor=CENTER)
    cbmb2.create_image(50, 50, image=myBmb2, anchor=CENTER)
    cbmb2.bind("<Button-1>", lambda event, p=2: selectSetPowers(event, p))

    bmb3 = "./Powers/Bombs/Bomb3.PNG"
    copyBmb3 = Image.open(bmb3)
    myBmb3 = ImageTk.PhotoImage(Image.open(bmb3).resize((100, 100)))

    cbmb3 = Canvas(root, width=100, height=100, bg=BG, highlightbackground=BG)
    cbmb3.place(x=(3*width / 4 + 100), y=620, anchor=CENTER)
    cbmb3.create_image(50, 50, image=myBmb3, anchor=CENTER)
    cbmb3.bind("<Button-1>", lambda event, p=3: selectSetPowers(event, p))

    entrySetPowers = Entry(root, width=20)
    entrySetPowers.place(x=(3 * width / 4), y=720, anchor=CENTER)
    entrySetPowers.config(state="disabled")

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

    labelError = addLabel("", width / 2 -30, 650, "flat", 12)
    labelError.config(fg="red",anchor="center")
    #Abre la ventana
    root.mainloop()
    return False


