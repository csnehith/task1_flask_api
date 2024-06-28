import psycopg2
import os

database_url = os.environ['DATABASE_URL']

conn = psycopg2.connect(database_url)
# conn = psycopg2.connect("host=db port=5432 dbname=mydatabase
#  user=myuser password=password")


def create_tables():
    commands = (
        """
        CREATE TABLE IF NOT EXISTS student_details(
        student_id INT PRIMARY KEY,
        school VARCHAR(50),
        sex VARCHAR(1),
        age INT,
        address_type VARCHAR(10),
        family_size VARCHAR(100),
        parent_status VARCHAR(100),
        mother_education VARCHAR(100),
        father_education VARCHAR(100),
        mother_job VARCHAR(50),
        father_job VARCHAR(50),
        school_choice_reason VARCHAR(50),
        gaurdian VARCHAR(10),
        travel_time VARCHAR(50),
        study_time VARCHAR(25),
        class_failures INT,
        school_support VARCHAR(5),
        family_support VARCHAR(5),
        extra_paid_classes VARCHAR(5),
        activities VARCHAR(5),
        nursery_school VARCHAR(5),
        higher_ed VARCHAR(5),
        internet_access VARCHAR(5),
        romantic_relationship VARCHAR(5),
        family_relationship INT,
        free_time INT,
        social INT,
        weekday_alcohol INT,
        weekend_alcohol INT,
        health INT,
        absences INT
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS students_score(
        math_grade1 INT,
        math_grade2 INT,
        math_final_grade INT,
        portuguese_grade1 INT,
        portuguese_grade2 INT,
        portuguese_final_grade INT,
        student_id INT PRIMARY KEY REFERENCES student_details(student_id)
        )
        """
    )
    cur = conn.cursor()
    for command in commands:
        cur.execute(command)
        conn.commit()
    conn.close()


if __name__ == '__main__':
    create_tables()
