import cv2
import os
import numpy as np
import facciaRiconoscimentoAI as fr

faceRecognizer = cv2.face.LBPHFaceRecognizer_create()
faceRecognizer.read(r"C:\Users\Siro\Desktop\python\IA\trainedData.yml")

name = {0: "brad Pitt", 1: "Di Caprio", 2: "elon", 3: "Alicius", 4: "ciruzzo", 5: "Ian"}

capture = cv2.VideoCapture(0)
while True:
    ret, test_image = capture.read()
    faceDetect, gray = fr.faceDetection(test_image)

    for face in faceDetect:
        (x, y, w, h) = face
        region = gray[y: y + w, x: x + h]
        label, confidence = faceRecognizer.predict(region)
        print("confidence ", confidence)
        predictedName = name[label]
        print("label ", predictedName)
        fr.draw_Rect(test_image, face)
        predicted_name = name[label]
        if confidence > 60:
            fr.put_name(test_image, "Non Riconosciuto", x, y)
            continue
        fr.put_name(test_image, predictedName, x, y)

    resized = cv2.resize(test_image, (1920, 1080))
    cv2.imshow("faccia trovata", resized)
    cv2.waitKey(10)
