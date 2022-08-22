import cv2
import os
import numpy as np
import facciaRiconoscimentoAI as fr

faces,facesID = fr.training_data (r'C:\Users\Siro\Desktop\python\IA\immagini')
faceRecognizer = fr.train_classifier(faces,facesID)
faceRecognizer.save("trainedData.yml")
print("print")


cv2.waitKey(0)