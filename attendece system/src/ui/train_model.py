import os
import cv2
import numpy as np

face_dir="faces"

#recognizer code
recognizer=cv2.face.LBPHFaceRecognizer_create()

x_train=[]
y_label=[]

for filename in os.listdir(face_dir):
    if not filename.lower().endswith(".jpg"):
        continue
    
    path=os.path.join(face_dir,filename)
    img=cv2.imread(path,cv2.IMREAD_GRAYSCALE)
    if img is None:
        continue

    sid_str=filename.split("_")[0]
    sid=int(sid_str)

    x_train.append(img)
    y_label.append(sid)

y_label=np.array(y_label)

recognizer.train(x_train,y_label)
recognizer.save("trainer.yml")
print("Model trained and saved as trainer.yml")
