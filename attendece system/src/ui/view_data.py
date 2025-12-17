from database import get_connection

conn=get_connection()
cur=conn.cursor()
cur.execute("SELECT id,name,branch,year FROM students")
for row in cur.fetchall():
    print(row)
conn.close()