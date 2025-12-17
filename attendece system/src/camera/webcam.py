import cv2
import mediapipe as mp


cap=cv2.VideoCapture(0)

mp_face_detection=mp.solutions.face_detection
mp_drawing=mp.solutions.drawing_utils


with mp_face_detection.FaceDetection(model_selection=0,min_detection_confidence=0.5) as face_detection:
    while True:
        ret,frame=cap.read()

        if not ret:
            print("Failed to grab  the frame.")
            break


        frame_rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        results=face_detection.process(frame_rgb)

        if results.detections:
            for detection in results.detections:
                mp_drawing.draw_detection(frame,detection)

        cv2.imshow('mediapie face detection',frame)

        if cv2.waitKey(1) & 0xff==ord('q'):
            break


cap.release()
cv2.destroyAllWindows()
