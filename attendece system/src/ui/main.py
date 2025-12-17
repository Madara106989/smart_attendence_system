import tkinter as tk
from tkinter import messagebox
import os
import sqlite3
import datetime
import cv2
from database import init_db,add_student,mark_attendence,get_student_by_id
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors


CASCADE_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
face_cascade = cv2.CascadeClassifier(CASCADE_PATH)
print("Loaded?", face_cascade.empty()) 

root=tk.Tk()

root.title("Smart Attendence System")
root.geometry("600x400")

#database ka function
init_db()

#main frame which comes after opening the app
main_frame=tk.Frame(root)
main_frame.pack(padx=10,pady=10)

def on_register_click():
    sid = entry_id.get()
    name = entry_name.get()
    branch = entry_branch.get()
    year = entry_year.get()

    cap = cv2.VideoCapture(1)
    save_dir = "faces"
    os.makedirs(save_dir, exist_ok=True)

    count = 0

    while count < 25:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            face_roi = gray[y:y+h, x:x+w]  # fixed indexes

            file_path = os.path.join(save_dir, f"{sid}_{count}.jpg")
            cv2.imwrite(file_path, face_roi)
            count += 1

            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, f"Shot {count}/10", (20, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            if count >= 25:
                break

        cv2.imshow("Registration - Press q to capture/quit", frame)

        if cv2.waitKey(500) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    add_student(sid, name, branch, year, None)
    messagebox.showinfo("Register", f"Registered: {sid} - {name}, images: {count}")


def on_start_attendence_click():
    year=att_year.get()
    branch=att_branch.get()
    subject=att_subject.get()

    recognizer=cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("trainer.yml")

    cap=cv2.VideoCapture(1)

    while True:
        ret,frame=cap.read()
        if not ret:
            break

        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces=face_cascade.detectMultiScale(gray,1.3,5)

        for(x,y,w,h) in faces:
            face_roi=gray[y:y+h,x:x+w]

            id_pred,confidence=recognizer.predict(face_roi)

            if confidence<45:
                now=datetime.datetime.now()
                date_str=now.strftime("%Y-%m-%d")
                time_str=now.strftime("%H:%M:%S")
                mark_attendence(str(id_pred),date_str,time_str,branch,year,subject)

                label=f"Id: {id_pred} ({int(confidence)})"
                color=(0,255,0)
                print("accepted",id_pred,confidence)
            else:
                label="unknown"
                color=(0,0,255)
                print("rejected",confidence)

            cv2.rectangle(frame,(x,y),(x+w,y+h),color,2)
            cv2.putText(frame,label,(x,y-10),cv2.FONT_HERSHEY_COMPLEX,0.8,color,2)
        cv2.imshow("Attendence-press q to quit",frame)

        if cv2.waitKey(1) & 0xff==ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

#present student ka output
def get_present_students_today(branch, year, subject):
    conn = sqlite3.connect("attendence.db")
    cur = conn.cursor()
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    cur.execute("""
        SELECT student_id, MIN(time)
        FROM attendence
        WHERE date=? AND branch=? AND year=? AND subject=?
        GROUP BY student_id
    """, (today, branch, year, subject))
    results = cur.fetchall()
    conn.close()
    return results



def on_generate_pdf_click():
    branch = att_branch.get()
    year = att_year.get()
    subject=att_subject.get()

    results = get_present_students_today(branch, year,subject)

    rows = []
    for sid,time in results:
        student = get_student_by_id(sid)  #sid is name, id, brach,year 
        rows.append((sid, student[1],time))  #with[1] hamne id,name hi liya h bus

    if not rows:
        messagebox.showinfo("PDF", "No attendance data for today.")
        return

    data = [["ID", "Name","Time"]] + list(rows)

    filename = f"attendance_{branch}_{year}_{subject}_{datetime.datetime.now().strftime('%Y-%m-%d')}.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4)
    elements = []

    table = Table(data)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
        ("GRID", (0,0), (-1,-1), 0.5, colors.black),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
    ]))

    elements.append(table)
    doc.build(elements)

    messagebox.showinfo("PDF", f"Saved: {filename}")



#here we have created a column at left
reg_frame=tk.LabelFrame(main_frame,text="Register new student")
reg_frame.grid(row=0,column=0,padx=10,pady=10,sticky="nw")

tk.Label(reg_frame,text="Id").grid(row=0,column=0,sticky="w")
entry_id=tk.Entry(reg_frame)
entry_id.grid(row=0,column=1)

tk.Label(reg_frame,text="Name").grid(row=1,column=0,sticky="w")
entry_name=tk.Entry(reg_frame)
entry_name.grid(row=1,column=1)

tk.Label(reg_frame, text="Branch").grid(row=2, column=0, sticky="w")
entry_branch = tk.Entry(reg_frame)
entry_branch.grid(row=2, column=1)

tk.Label(reg_frame, text="Year").grid(row=3, column=0, sticky="w")
entry_year = tk.Entry(reg_frame)
entry_year.grid(row=3, column=1)

btn_register = tk.Button(reg_frame, text="Register & Capture",command=on_register_click)
btn_register.grid(row=4, column=0, columnspan=2, pady=10)

#right column 
att_frame=tk.LabelFrame(main_frame,text="Take Attendence")
att_frame.grid(row=0,column=1,padx=10,pady=10,sticky="ne")

tk.Label(att_frame,text="Year").grid(row=0,column=0,sticky="w")
att_year = tk.Entry(att_frame)
att_year.grid(row=0,column=1)

tk.Label(att_frame,text="Branch").grid(row=1,column=0,sticky="w")
att_branch = tk.Entry(att_frame)
att_branch.grid(row=1,column=1)

tk.Label(att_frame,text="Subject").grid(row=2,column=0,sticky="w")
att_subject = tk.Entry(att_frame)
att_subject.grid(row=2,column=1)

btn_start_att = tk.Button(att_frame,text="Start Attendence",
                          command=on_start_attendence_click)
btn_start_att.grid(row=3,column=0,columnspan=2,pady=10)

btn_generate_pdf = tk.Button(att_frame,text="Generate pdf",
                             command=on_generate_pdf_click)
btn_generate_pdf.grid(row=4,column=0,columnspan=2,pady=10)

root.mainloop()