
import cv2
import os
import numpy as np

def faceDetection(img):
    gray =cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    haar_face = cv2.CascadeClassifier(r"C:\Users\Siro\Desktop\python\IA\HARR\haarcascade_frontal_face_default.xml")
    face = haar_face.detectMultiScale(gray,scaleFactor=1.3,minNeighbors =10)
   
    return face,gray

def training_data(directory):
    faces = []
    facesID = []

    for path, subdir, filename in os.walk(directory):
        for filename in filename:
            if filename.startswith("."):
                print("skipping sysem file")
                continue
            id = os.path.basename(path)
            image_path =os.path.join(path,filename)
            img_test=cv2.imread(image_path)
            if img_test is None:
                print("error opening image")
                continue
            face,gray  = faceDetection(img_test)
            if len(face)!=1: 
                continue
            (x,y,w,h) = face[0]
            region = gray[y:y+w,x:x+h]
            faces.append(region)
            facesID.append(int(id))
    return faces, facesID

def train_classifier(faces,facesID):
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.train(faces,np.array(facesID))
    return face_recognizer

def draw_Rect(test_img, faces):
    (x,y,w,h)= faces
    cv2.rectangle(test_img, (x, y), (x+w, y+h), (0,0,255), thickness=5)

def put_name(test_img, text, x,y):
    cv2.putText(test_img,text,(x,y), cv2.QT_FONT_NORMAL, 2, (0,0,255),3)