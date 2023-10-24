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

    titleLbl = hallOfFameScreen.addLabel("Hall of Fame", width/2-250, height/7, "flat")
    titleLbl.config(font=("Arial",60))

    rolLbl = hallOfFameScreen.addLabel("Attackers", width/2-185, height/7-100,"flat")
    rolLbl.config(font=("Arial",60))


    user1Lbl= hallOfFameScreen.addLabel("User1", width/3-100,height/4+40,"flat")
    user1Lbl.config(font=("Arial",40))

    user2Lbl = hallOfFameScreen.addLabel("User2", width / 3-100, height /4 +40+90, "flat")
    user2Lbl.config(font=("Arial", 40))

    user3Lbl = hallOfFameScreen.addLabel("User3", width / 3-100, height /4 +40+180, "flat")
    user3Lbl.config(font=("Arial", 40))


    pos4Lbl= hallOfFameScreen.addLabel("4.",width/3-170, height/4+40+270,"flat")
    pos4Lbl.config(font=("Arial",40))

    user4Lbl = hallOfFameScreen.addLabel("User4", width / 3-100, height /4+40+270 , "flat")
    user4Lbl.config(font=("Arial", 40))

    pos5Lbl = hallOfFameScreen.addLabel("5.", width / 3 - 170, height / 4 + 40 + 360, "flat")
    pos5Lbl.config(font=("Arial", 40))

    user5Lbl = hallOfFameScreen.addLabel("User5", width / 3-100, height /4+40+360 , "flat")
    user5Lbl.config(font=("Arial", 40))

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