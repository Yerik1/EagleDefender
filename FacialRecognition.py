import cv2
import os
# pip install opencv-python-headless

class Recogn:
    def __init__(self):
        self.root=""

    def recognition1(self):
        dataPath = "./FacialRecognition/"
        imagePath = os.listdir(dataPath)

        faceRecognizer = cv2.face.EigenFaceRecognizer_create()

        # Leyendo el modelo o datos guardados en el entrenamiento
        faceRecognizer.read("modeloEigenFace.xml")

        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

        while True:
            ret, frame = cap.read()
            if not ret:
                return "No Camera"
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            auxFrame = gray.copy()

            faces = faceClassif.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                face = auxFrame[y:y + h, x:x + w]
                face = cv2.resize(face, (150, 150), interpolation=cv2.INTER_CUBIC)
                result = faceRecognizer.predict(face)

                cv2.putText(frame, '{}'.format(result), (x, y - 5), 1, 1.3, (255, 255, 0), 1, cv2.LINE_AA)

                # EigenFaces
                if result[1] < 3100:
                    folder_name = imagePath[result[0]]  # Obtenemos el nombre de la carpeta
                    cv2.putText(frame, '{}'.format(folder_name), (x, y - 25), 2, 1.1, (0, 255, 0), 1, cv2.LINE_AA)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cap.release()
                    cv2.destroyAllWindows()
                    return folder_name  # Retornar el nombre de la carpeta
                else:
                    cv2.putText(frame, 'Desconocido', (x, y - 20), 2, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.imshow('frame', frame)
            k = cv2.waitKey(1)
            if k == 27:
                break
        cap.release()
        cv2.destroyAllWindows()
        return "#NO#"


