import psycopg2

conn = psycopg2.connect("host= 127.0.0.1 dbname=task user=postgres password=deq@123")
print("Connecting to Database")
cur = conn.cursor()


with open('/home/deq/Desktop/task/data/student_details.csv', 'r') as f:
    next(f)
    cur.copy_from(f, 'student_details', sep=',', columns=('"student_id"', '"school"', '"sex"','"age"','"address_type"',
            '"family_size"','"parent_status"','"mother_education"','"father_education"','"mother_job"','"father_job"','"school_choice_reason"','"gaurdian"','"travel_time"','"study_time"','"class_failures"',
            '"school_support"','"family_support"','"extra_paid_classes"','"activities"','"nursery_school"','"higher_ed"','"internet_access"','"romantic_relationship"','"family_relationship"','"free_time"',
            '"social"','"weekday_alcohol"','"weekend_alcohol"','"health"','"absences"'))

with open('/home/deq/Desktop/task/data/students_score.csv', 'r') as f:
    next(f)
    cur.copy_from(f, 'students_score', sep=',', columns=('"math_grade1"','"math_grade2"','"math_final_grade"','"portuguese_grade1"','"portuguese_grade2"','"portuguese_final_grade"','"student_id"'))

conn.commit()
conn.close()

