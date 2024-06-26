import psycopg2
import os

database_url = os.environ['DATABASE_URL']
conn = psycopg2.connect(database_url)

# conn = psycopg2.connect(data)
# conn = psycopg2.connect("host=db port=5432
# dbname=mydatabase user=myuser password=password")

cur = conn.cursor()

cur.execute("TRUNCATE TABLE student_details RESTART IDENTITY CASCADE;")

with open('student_details.csv', 'r') as f:
    next(f)
    cur.copy_from(f, 'student_details', sep=',', columns=(
        'student_id', 'school', 'sex', 'age',
        'address_type', 'family_size', 'parent_status', 'mother_education',
        'father_education', 'mother_job', 'father_job', 'school_choice_reason',
        'gaurdian', 'travel_time', 'study_time', 'class_failures', 'school_support',
        'family_support', 'extra_paid_classes', 'activities', 'nursery_school',
        'higher_ed', 'internet_access', 'romantic_relationship', 'family_relationship',
        'free_time', 'social', 'weekday_alcohol', 'weekend_alcohol', 'health',
        'absences'))

cur.execute("TRUNCATE TABLE students_score RESTART IDENTITY CASCADE;")

with open('/app/students_score.csv', 'r') as f:
    next(f)
    cur.copy_from(f, 'students_score', sep=',', columns=(
        'math_grade1', 'math_grade2', 'math_final_grade', 'portuguese_grade1',
        'portuguese_grade2', 'portuguese_final_grade', 'student_id'))

conn.commit()
conn.close()
