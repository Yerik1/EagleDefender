import cv2
from tkinter import *
from PIL import Image, ImageTk

class CamApp:
    def __init__(self,canvas):
        self.window = Tk()
        self.window.title("Cámara en Vivo")
        self.status=True
        self.path=""
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Error: No se pudo abrir la cámara.")
            self.window.destroy()
            return
        self.canva=canvas

        self.capButton = Button(self.window, text="Capturar Foto", command=self.takePicture)
        self.capButton.pack()
        self.window.protocol("WM_DELETE_WINDOW", self.exit)
        self.update()



    def takePicture(self):
        ret, frame = self.cap.read()
        if ret:
            self.path="Temp/foto_capturada.png"
            cv2.imwrite(self.path, frame)
            print("Foto capturada y guardada como 'foto_capturada.png'.")
            self.exit()


    def update(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame)
            # Redimensionar la imagen para que se ajuste a la ventana
            image = image.resize((200, 200))
            imageTk = ImageTk.PhotoImage(image)
            self.canva.config(image=imageTk)
            self.canva.imagen_tk = imageTk
            self.window.after(10, self.update)
        else:
            print("Error: No se pudo capturar el fotograma.")
            self.exit()

    def exit(self):
        self.cap.release()
        cv2.destroyAllWindows()
        self.window.quit()
        self.window.destroy()
        self.status=False

    def begin(self):
        self.window.mainloop()
        while (True):
            if not self.status:
                if self.path=="":
                    return False
                else:
                    return self.path
