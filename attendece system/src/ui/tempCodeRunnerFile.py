    recognizer=cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("trainer.yml")

    cap=cv2.VideoCapture[1]

    while True:
        ret,frame=cap.read()
        if not ret:
            break

        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces=face_cascade.detectMultiScale(gray,1.3,5)

        for(x,y,w,h) in faces:
            face_roi=gray[y:y+h,x:x+w]

            id_pred,confidence=recognizer.predict(face_roi)

            if confidence<70:
                label=f"Id: {id_pred} ({int(confidence)})"
                color=(0,255,0)
            else:
                label="unknown"
                color=(0,0,255)

            cv2.rectangle(frame,(x,y),(x+w,y+h),color,2)
            cv2.putText(frame,label,(x,y-10),cv2.FONT_HERSHEY_COMPLEX,0.8,color,2)
        cv2.imshow("Attendence-press q to quit",frame)

        if cv2.waitKey(1) & 0xff==ord('q'):
            break
    cap.release()