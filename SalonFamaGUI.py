from GUIBuilder import GUIBuilder
import Register as register
import xml.etree.ElementTree as ET
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

    # Crea la ventana del salon de la fama
    hallOfFameScreen = GUIBuilder("#86895d")

    #titleLbl = hallOfFameScreen.addLabel("Hall of Fame", 0.4*(width/30), height/6.7, "flat")


    # Obtener las dimensiones de la pantalla
    width = hallOfFameScreen.root.winfo_screenwidth() # Ancho
    height = hallOfFameScreen.root.winfo_screenheight() # Alto

    titleLbl = hallOfFameScreen.addLabel("Hall of Fame", width/2.37, height/7, "flat")
    titleLbl.config(font=("Arial",30))




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