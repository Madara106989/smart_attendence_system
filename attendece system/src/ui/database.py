import sqlite3

db_name="attendence.db"

def get_connection():
    conn=sqlite3.connect(db_name)
    return conn
def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # students ki table jo pehle se hai
    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            branch TEXT,
            year TEXT,
            face_data BLOB
        )
    """)

    #new student found
    cur.execute("""
                CREATE TABLE IF NOT EXISTS attendence(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT,
                date TEXT,
                time TEXT,
                branch TEXT,
                year TEXT,
                subject TEXT,
                UNIQUE(student_id,date,branch,year,subject))
                """)
    conn.commit()
    conn.close()

def add_student(sid,name,branch,year,face_date=None):
    conn=get_connection()
    cur=conn.cursor()
    cur.execute("INSERT OR REPLACE  INTO students(id,name,branch,year,face_data)Values (?,?,?,?,?)",
                (sid,name,branch,year,face_date))
    conn.commit()
    conn.close()
    
def get_student_by_id(student_id):
    conn=get_connection()
    cur=conn.cursor()
    cur.execute("SELECT id,name,branch,year FROM students WHERE id=?",
                (student_id,))
    row=cur.fetchone()
    conn.close()
    return row

def mark_attendence(student_id,data_str,time_str,branch,year,subject):
    conn=get_connection()
    cur=conn.cursor()
    cur.execute("""
                INSERT OR IGNORE INTO attendence (student_id,date,time,
                branch,year,subject)
                VALUES(?,?,?,?,?,?)
                """,(student_id,data_str,time_str,branch,year,subject))
    conn.commit()
    conn.close()
