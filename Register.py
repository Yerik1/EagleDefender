import xml.etree.ElementTree as eT
def registro():
    tree= eT.parse('DataBase')
    root= tree.getroot()

    newClient = eT.Element('Cliente')


    # Agrega atributos al nuevo elemento si es necesario
    newUser = eT.SubElement(newClient, 'User')
    newUser.text='Gabopango'
    newPassword = eT.SubElement(newClient, 'Password')
    newPassword.text = 'jjgDfg#1'
    newName = eT.SubElement(newClient, 'Name')
    newName.text = 'Gabriel'
    newEmail = eT.SubElement(newClient, 'Email')
    newEmail.text = 'gabo@gmail.com'
    newAge = eT.SubElement(newClient, 'Age')
    newAge.text = '19'

    newSongList = eT.Element('Music')

    newSongA =eT.SubElement(newSongList, 'SongA')
    newSongA.text="A"
    newSongB = eT.SubElement(newSongList, 'SongB')
    newSongB.text = "B"
    newSongC = eT.SubElement(newSongList, 'SongC')
    newSongC.text = "C"

    newClient.append(newSongList)

    newProfPic = eT.SubElement(newClient, 'ProfilePic')
    newProfPic.text = 'imagenes/FotosPerfil'+'/Gabopango.jpg'

    newColorPalette = eT.Element('Colors')

    newColorA = eT.SubElement(newColorPalette, 'ColorA')
    newColorA.text = "#A"
    newColorB = eT.SubElement(newColorPalette, 'ColorB')
    newColorB.text = "#B"
    newColorC = eT.SubElement(newColorPalette, 'ColorC')
    newColorC.text = "#C"
    newColorD = eT.SubElement(newColorPalette, 'ColorD')
    newColorD.text = "#D"

    newClient.append(newColorPalette)

    root.append(newClient)
    tree.write('DataBase')

    print("sumadre")

registro()