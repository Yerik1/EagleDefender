
from PIL import Image

def applyColorTint(image, targetColorHex):
    # Abre la imagen utilizando Pillow
    img = image

    # Convierte el color hexadecimal en una tupla de RGB
    targetColorRgb = tuple(int(targetColorHex[i:i + 2], 16) for i in (1, 3, 5))

    # Crea una capa de color semitransparente
    colorLayer = Image.new('RGBA', img.size, (targetColorRgb[0], targetColorRgb[1], targetColorRgb[2], 128))

    # Superpone la capa de color sobre la imagen original
    tintedImage = Image.alpha_composite(img.convert('RGBA'), colorLayer)

    return tintedImage

def colorFilter(color, image):
    newImage = applyColorTint(image, color)
    return newImage

