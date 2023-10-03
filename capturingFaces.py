import cv2
import os
import numpy as np

dataPath = 'Nombre de la carpeta donde se van a almacenar los rostros'
personPath = dataPath

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

faceClassif: cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

count = 0
while True:
    ret, frame = cap.read()
    if not ret: break
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
    if k == 27 or count >= 300:
        break

cap.release()
cv2.destroyAllWindows()


class training():
    dataPath = 'Dirección donde esta almacenando'
    peopleList = os.listdir(dataPath)

    labels = []
    facesData = []
    label = 0

    for nameDir in peopleList:
        personPath = dataPath + '/' + nameDir

        for fileName in os.listdir(personPath):
            labels.append(label)
            facesData.append(cv2.imread(personPath + '/' + fileName, 0))
            image = cv2.imread(personPath + '/' + fileName, 0)
        label = label + 1

    faceRecognizer = cv2.face.EigenFaceRecognizer_create()

    # Entrando al reconocedor de rostros
    print("Entrenando...")
    faceRecognizer.train(facesData, np.array(labels))

    #Almacenar el modelo obtenido
    faceRecognizer.write('modeloEigenFace.xml')
    print("Almacenando el modelo")
