from GUIBuilder import GUIBuilder
import tkinter as tk
from PIL import ImageDraw, ImageTk, Image, ImageFilter

class Instructions:
    def __init__(self):
        # Crea el objeto ventana
        self.instructionsScreen = GUIBuilder('#86895d')

        # Obtener las dimensiones de la pantalla
        self.width = self.instructionsScreen.root.winfo_screenwidth()  # Ancho
        self.height = self.instructionsScreen.root.winfo_screenheight()  # Alto
        self.position=1

    def initialize(self):
        # Labels usados en la ventana
        self.imageLbl= self.instructionsScreen.addLabel("", self.width / 2, self.height / 2, "flat")
        self.image=Image.open("./InstructionImages/Intructions1.jpg")
        self.image = self.image.resize((int(2*self.width/3), int(self.height/2)))
        self.image = ImageTk.PhotoImage(self.image)
        self.imageLbl.config(image=self.image)
        self.nextButton= self.instructionsScreen.buttons("next", self.nextImage,"White","White",int(3*self.width/4)+50, int(3*self.height/4)+60)
        if not self.instructionsScreen.initialize():
            return False

    def nextImage(self):
        if self.position<8:
            if self.position==7:
                self.nextButton.destroy()
            self.position += 1
            if self.position==2:
                self.prevButton = self.instructionsScreen.buttons("previous", self.prevImage, "White", "White",
                                                                  int(self.width / 4) - 50,
                                                                  int(3*self.height / 4) + 60)

        self.imageLbl = self.instructionsScreen.addLabel("", self.width / 2, self.height / 2, "flat")
        self.image = Image.open("./InstructionImages/Intructions"+str(self.position)+".jpg")
        self.image = self.image.resize((int(2 * self.width / 3), int(self.height / 2)))
        self.image = ImageTk.PhotoImage(self.image)
        self.imageLbl.config(image=self.image)

    def prevImage(self):
        if self.position>1:
            if self.position==2:
                self.prevButton.destroy()
            self.position -= 1
            if self.position==7:
                self.nextButton = self.instructionsScreen.buttons("next", self.nextImage, "White", "White",
                                                                  int(3*self.width / 4) + 50,
                                                                  int(3 * self.height / 4) + 60)
            self.imageLbl = self.instructionsScreen.addLabel("", self.width / 2, self.height / 2, "flat")
            self.image = Image.open("./InstructionImages/Intructions" + str(self.position) + ".jpg")
            self.image = self.image.resize((int(2 * self.width / 3), int(self.height / 2)))
            self.image = ImageTk.PhotoImage(self.image)
            self.imageLbl.config(image=self.image)


