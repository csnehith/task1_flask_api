"""Load_data"""
import os
import csv
import psycopg2

database_url = os.environ['DATABASE_URL']
conn = psycopg2.connect(database_url)

cur = conn.cursor()

with open('student_details.csv', 'r', encoding='UTF-8') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        cur.execute("""
            INSERT INTO student_details (student_id, school, sex, age,
            address_type, family_size, parent_status, mother_education,
            father_education, mother_job, father_job, school_choice_reason,
            gaurdian, travel_time, study_time, class_failures, school_support,
            family_support, extra_paid_classes, activities, nursery_school,
            higher_ed, internet_access, romantic_relationship,
            family_relationship, free_time, social, weekday_alcohol,
            weekend_alcohol, health, absences)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (student_id)
            DO NOTHING;
        """, row)

with open('students_score.csv', 'r', encoding='UTF-8') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        cur.execute("""
            INSERT INTO students_score (math_grade1, math_grade2,
            math_final_grade, portuguese_grade1,
            portuguese_grade2, portuguese_final_grade, student_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (student_id)
            DO NOTHING;;
        """, row)

conn.commit()
conn.close()
