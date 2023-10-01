from tkinter import *
from tkinter import colorchooser, filedialog
from PIL import Image, ImageTk
import PIL

root = Tk()
root.title(" Click on any where on image to pick a color  ")
width = root.winfo_screenwidth()  # Ancho de la pantalla
height = root.winfo_screenheight() - 50  # Alto de la pantalla menos 50 píxeles para la barra de tareas

# Establecer las dimensiones de la ventana
root.geometry(f"{width}x{height}+-7+0")

colorA=""
colorB=""
colorC=""
colorD=""
colorE=""

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
    global entry, entry1, disp
    global newFrame

    #Creacion de paleta de colores
    b1 = Image.open(imageName).resize((200, 200)).convert("RGB")
    b1 = b1.getpixel((e.x, e.y))
    b2=(b1[1],b1[0],b1[2])
    if(b2[2]<=130):
        b3 = (b2[0], b2[1], b2[2] + 125)
    elif (b2[1] <= 130):
        b3 = (b2[0], b2[1] + 125, b2[2])
    else:
        b3 = (b2[0], b2[1], b2[2] - 125)

    b4 = (b1[2], abs(b1[1] - 255), b1[0])

    if (b4[2] <= 130):
        b5 = (b4[0], b4[1], b4[2] + 125)

    elif(b4[1] <= 130):
        b5 = (b4[0], b4[1]+125, b4[2])
    else:
        b5 = (b4[0], b4[1], b4[2] - 125)

    #Colores en hexadecimal
    color = _from_rgb(b1)
    color2 = _from_rgb(b2)
    color3=_from_rgb(b3)
    color4 = _from_rgb(b4)
    color5=_from_rgb(b5)

    #ordena los colores de menor a mayor en hexadecimal
    hex=[color,color2,color3,color4,color5]
    hex.sort()

    #Se edita las entries de los colores para mostrar el codigo de color
    entryA.config(state="normal")
    entryA.delete(0, END)
    entryA.insert(0, str(hex[0])) #hex
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

    #Agregs el color a los botones
    dispA.config(bg=hex[0], fg=hex[0])
    dispB.config(bg=hex[1], fg=hex[1])
    dispC.config(bg=hex[2], fg=hex[2])
    dispD.config(bg=hex[3], fg=hex[3])
    dispE.config(bg=hex[4], fg=hex[4])

"""
funcion que recopila la informacion de las entries
"""
def save():
    global colorA,colorB,colorC,colorD,colorE
    colorA=entryA.get()
    colorB=entryB.get()
    colorC=entryC.get()
    colorD = entryD.get()
    colorD = entryE.get()

#Puede servir para el importar imagenes
#imgname=filedialog.askopenfilename(initialdir="/Desktop/python codes",title="open images",filetypes=(("png files","*.png"),("jpg files","*.jpg"),("jpeg files","*.jpeg")))

#se agrega la rueda de color como imagen
imageName = "./ColorWheel.png"
copy = Image.open(imageName)
myImg = ImageTk.PhotoImage(Image.open(imageName).resize((200, 200)))

#se crea el canvas de la rueda de color
c = Canvas(root,width=400, height=200)
c.place(x=(width/2),y=(height*5/8), anchor=CENTER)
c.create_image(100, 100, anchor=CENTER, image=myImg)
c.bind("<Button-1>", colorpic)

#Se crean los lugares donde aparece el codigo de color y se muestra el color
entryA = Entry(c, width=10)
entryA.place(x=220,y=10)
entryB = Entry(c, width=10)
entryB.place(x=220,y=50)
entryC = Entry(c, width=10)
entryC.place(x=220,y=90)
entryD = Entry(c, width=10)
entryD.place(x=220,y=130)
entryE = Entry(c, width=10)
entryE.place(x=220,y=170)
dispA = Button(c, text="  ")
dispA.place(x=300,y=10)
dispB = Button(c, text="  ")
dispB.place(x=300,y=50)
dispC = Button(c, text="  ")
dispC.place(x=300,y=90)
dispD = Button(c, text="  ")
dispD.place(x=300,y=130)
dispE = Button(c, text="  ")
dispE.place(x=300,y=170)

#Abre la ventana
root.mainloop()

