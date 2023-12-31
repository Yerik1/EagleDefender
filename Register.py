#Biblioteca para la edicion de archivos xml
import xml.etree.ElementTree as eT

#Biblioteca para la encriptacion rsa
import rsa
import re

#importar la llave publica
#importar la llave publica
with open("public.pem","rb") as f:
    publicKey=rsa.PublicKey.load_pkcs1(f.read())

#importar la llave privada
with open("private.pem","rb") as f:
    privateKey = rsa.PrivateKey.load_pkcs1(f.read())

"""
Funcion que permite encriptar la base de datos utilizando rsa
"""
def encrypt():
    # Se abre el archivo de la base de datos y se guarda la informacion en una variable
    with open("DataBase", "rb") as f:
        data = f.read()

    # tamaño de los bloques en los que se va a dividir la informacion
    blockSize = 100
    # lista donde se guardan los bloques de informacion
    encryptedBlocks = []
    # posicion inicial
    start = 0
    # se va a encriptar cada bloque de informacion hasta que se acabe la informacion
    while start < len(data):
        # se define el fin del slicing como la posicion inicial mas el tamaño de los bloques
        end = start + blockSize
        # se define el bloque haciendo slicing desde la posicion inicial hasta la final
        block = data[start:end]
        # se encripta el bloque hecho utilizando la llave publica
        encryptedBlock = rsa.encrypt(block, publicKey)
        # se agrega el bloque a la lista
        encryptedBlocks.append(encryptedBlock)
        # se definine la posicion inicial como el fin del slicing anterior
        start = end

    # se reescribe el documento con los bloques encriptados
    with open("DataBase", "wb") as f:
        for block in encryptedBlocks:
            f.write(block)

"""
funcion que desencripta el archivo de la base de datos
"""

def decrypt():
#se genera una lista para almacenar bloques encriptados
    encryptedBlocks = []
    #se abre el documento de la base de datos
    with open("DataBase", "rb") as f:
        state=True
        while state:
            #se generan bloque del tamaño de la llave privada con informacion de la base de datos
            block = f.read(privateKey.n.bit_length() // 8)
            #cuando ya no se pueda generar un bloque se termina el ciclo
            if not block:
                state=False
            else:
                encryptedBlocks.append(block)

    # Desencriptar cada bloque y concatenarlos para obtener el mensaje original
    decryptedData = b""
    #se recorre cada bloque y se desencripta para convertirlo en texto
    for block in encryptedBlocks:
        decryptedBlock = rsa.decrypt(block, privateKey)
        #se agrega el texto desencriptado al string
        decryptedData += decryptedBlock

    #se sobreescribe la base de datos con la informacion desencriptada
    with open("DataBase", "wb") as f:
        f.write(decryptedData)



"""
funcion que permite agregar un usuario con su informacion a la base de datos
"""
def register(list,profPicRoute):
    decrypt()
    #arbol con la informacion del archivo xml
    tree= eT.parse('DataBase')
    #raiz del arbol
    root= tree.getroot()

    #se crea un nuevo elemento cliente para almacenar la informacion
    newClient = eT.Element('Cliente')

    # agrega atributos al nuevo elemento
    newUser = eT.SubElement(newClient, 'User')  # nombre de usuario
    newUser.text = list[0]
    newPassword = eT.SubElement(newClient, 'Password')  # contraseña
    newPassword.text = list[1]
    newName = eT.SubElement(newClient, 'Name')  # nombre del cliente
    newName.text = list[3]
    newEmail = eT.SubElement(newClient, 'Email')  # correo electronico
    newEmail.text = list[4]
    newAge = eT.SubElement(newClient, 'Age')  # edad del cliente
    newAge.text = list[5]
    #Se crea el elemento de la lista de canciones
    newSongList = eT.Element('Music')

    newSongA =eT.SubElement(newSongList, 'SongA') #cancion A
    newSongA.text=list[6]
    newSongB = eT.SubElement(newSongList, 'SongB') #cancion B
    newSongB.text = list[7]
    newSongC = eT.SubElement(newSongList, 'SongC') #cancion C
    newSongC.text = list[8]

    #se agrega la lista de canciones al cliente
    newClient.append(newSongList)

    newProfPic = eT.SubElement(newClient, 'ProfilePic') #ruta de la foto de perfil
    newProfPic.text = profPicRoute

    #Paleta de colores del usuario
    newColorPalette = eT.Element('Colors')

    newColorA = eT.SubElement(newColorPalette, 'ColorA')#color A
    newColorA.text = list[9]
    newColorB = eT.SubElement(newColorPalette, 'ColorB')#color B
    newColorB.text = list[10]
    newColorC = eT.SubElement(newColorPalette, 'ColorC')#color C
    newColorC.text = list[11]
    newColorD = eT.SubElement(newColorPalette, 'ColorD')#color D
    newColorD.text = list[12]
    newColorD = eT.SubElement(newColorPalette, 'ColorE')  # color D
    newColorD.text = list[13]
    # Se agrega la paleta de colores al cliente
    newClient.append(newColorPalette)

    #se agrega las texturas escogidas
    newWalls = eT.SubElement(newClient, 'Wall')  # numero del sprite de barerra
    newWalls.text = list[14]

    newBackGround = eT.SubElement(newClient, 'BackGround')  # numero del sprite de fondo
    newBackGround.text = list[15]

    newWaterBall = eT.SubElement(newClient, 'WaterBall')  # numero del sprite de bola de agua
    newWaterBall.text = list[16]

    newFireBall = eT.SubElement(newClient, 'FireBall')  # numero del sprite de bola de fuego
    newFireBall.text = list[17]

    newBomb = eT.SubElement(newClient, 'Bomb')  # numero del sprite de bomba
    newBomb.text = list[18]


    #se agrega el cliente a la raiz
    root.append(newClient)
    #se escribe la informacion en la base de datos
    tree.write('DataBase')
    encrypt()
    print("piola")

"""
funcion que valida el usuario, contraseña y edad
"""
def validate(user,password):
    if not(safeUser(user)):
        if(safePassword(password)):
            print("safe")
            return True
        else:
            print("Contraseña invalida")
    else:
        print("Usuario invalido")
    return False

"""
funcion que verifica si se puede usar el usuario
"""
def safeUser(word):
    if not(re.search(r'[^a-zA-Z0-9_]+',word)):
        with open("BannedWords.txt","r")as f:
            for line in f:
                # Comprueba si la palabra está en la línea actual
                if word.lower() in line:
                    return True  # La palabra se encontró en el archivo
            # Si la palabra no se encontró en ninguna línea
            return False
    else:
        return True

"""
funcion que verifica si la contraseña es segura
"""
def safePassword(password):
    # Verificar si la contraseña tiene al menos 8 caracteres
    if len(password) < 8:
        return False
    # Verificar si hay al menos una letra minúscula
    if not re.search(r'[a-z]', password):
        return False

    # Verificar si hay al menos una letra mayúscula
    if not re.search(r'[A-Z]', password):
        return False

    # Verificar si hay al menos un carácter especial (cualquier carácter que no sea letra o número)
    if not re.search(r'[0123456789!@#$%^&*()_+{}\[\]:;<>,.?~\\-]', password):
        return False

    # Si la contraseña cumple con todos los requisitos
    return True
