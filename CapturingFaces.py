import cv2
import os
import numpy as np
from tkinter import *
import shutil
# pip install opencv-contrib-python

# Configuración de la ventana de instrucciones

class Biometric:
    def __init__(self):
        self.root= Tk()
        self.root.title("Instrucciones")
    def initialice(self,user,mainWindow):
        instructions = Label(self.root, text="", justify="center")
        instructions.pack()

        self.showInstructions(instructions)

        button = Button(self.root, text="Iniciar Reconocimiento", command=lambda usr=user,window=self.root: self.recognition(usr,window))
        button.pack()
        # Iniciar el ciclo principal de Tkinter
        self.root.mainloop()
        mainWindow.destroy()
    def recognition(self,user,window1):
        window1.destroy()
        dataPath = './FacialRecognition/'+user
        os.makedirs(dataPath)
        personPath = dataPath

        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        faceClassif= cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

        count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                return "No Camera"
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            auxFrame = gray.copy()

            faces = faceClassif.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, h), (0, 255, 0), 2)
                face = auxFrame[y:y + h, x:x + w]
                face = cv2.resize(face, (150, 150), interpolation=cv2.INTER_CUBIC)
                cv2.imwrite(personPath + '/rostro_{}.jpg'.format(count), face)
                count = count + 1
            cv2.imshow('frame', frame)

            k = cv2.waitKey(1)
            if k == 27:
                cap.release()
                cv2.destroyAllWindows()
                shutil.rmtree(personPath)
                return("#NO#")
            elif(count >= 100):
                break

        cap.release()
        cv2.destroyAllWindows()

        root2 = Tk()
        root2.title("Success")

        success = Label(root2, text="", justify="center")
        success.pack()

        self.showSuccess(success)

        button2 = Button(root2, text="Exit", command=lambda window=root2: self.training(window))
        button2.pack()



    def training(self,window):
        window.destroy()
        dataPath = "./FacialRecognition"
        os.makedirs(dataPath, exist_ok=True)
        peopleList = os.listdir(dataPath)

        labels = []
        facesData = []
        label = 0

        for nameDir in peopleList:
            personPath = dataPath + '/' + nameDir

            for fileName in os.listdir(personPath):
                labels.append(label)
                facesData.append(cv2.imread(personPath + '/' + fileName, 0))

            label = label + 1
        faceRecognizer = cv2.face.EigenFaceRecognizer.create()

        # Entrando al reconocedor de rostros
        print("Entrenando...")
        faceRecognizer.train(facesData, np.array(labels))


        #Almacenar el modelo obtenido
        faceRecognizer.write('modeloEigenFace.xml')
        print("Almacenando el modelo")
        self.root.quit()

    def showInstructions(self,instructions):
        instructions.config(text="Instrucciones:\n\n"
                                     "1. Colocate en un lugar con buena iluminacion.\n"
                                     "2. Enfoca tu rostro dentro del cuadro.\n"
                                     "3. Si no se muestra el cuadro, busca un lugar con mejor iluminacion.\n"
                                     "4. Cuando se muestre el cuadro prueba mover tu rostro en diferentes posiciones para un mejor registro.\n"
                                     "5. Si no quieres usar biometrica presiona la ´X´ para volver al registro y desactiva la opcion"
                        )
    def showSuccess(self,success):
        success.config(text="Registro Exitoso")

    def destroy(self,window):
        window.destroy()







