import psycopg2

conn = psycopg2.connect("host= 127.0.0.1 dbname=task1 user=postgres password=deq@123")
print("Connecting to Database")
cur = conn.cursor()


with open('/home/deq/Desktop/task/students_score.csv', 'r') as f:
    next(f)
    cur.copy_from(f, 'students_score', sep=',', columns=('"math_grade1"','"math_grade2"','"math_final_grade"','"portuguese_grade1"','"portuguese_grade2"','"portuguese_final_grade"','"student_id"'))

conn.commit()
conn.close()