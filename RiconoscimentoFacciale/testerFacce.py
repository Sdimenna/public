import cv2
import os
import numpy as np
import facciaRiconoscimentoAI as fr

test_image = cv2.imread(r"C:\Users\Siro\Desktop\python\IA\test\WIN_20220707_15_33_05_Pro (3).jpg")
face, gray = fr.faceDetection(test_image)

# faces,facesID = fr.training_data (r'C:\Users\Siro\Desktop\python\IA\immagini')
# faceRecognizer = fr.train_classifier(faces,facesID)
# faceRecognizer.save("trainedData.yml")


faceRecognizer = cv2.face.LBPHFaceRecognizer_create()
faceRecognizer.read(r"C:\Users\Siro\Desktop\python\IA\trainedData.yml")

name = {0: "brad Pitt", 1: "Di Caprio", 2: "elon"}

for face in face:
    (x, y, w, h) = face
    region = gray[y: y + h, x: x + w]
    label, confidence = faceRecognizer.predict(region)
    print("confidence ", confidence)
    print("label ", label)
    fr.draw_Rect(test_image, face)
    predicted_name = name[label]
    if confidence > 60:
        continue
    fr.put_name(test_image, predicted_name, x, y)

resized = cv2.resize(test_image, (1920, 1080))
cv2.imshow("faccia trovata", resized)
cv2.waitKey(0)
cv2.destroyAllWindows()
