FROM python:3.9-slim

WORKDIR /app


RUN pip install Flask psycopg2-binary

COPY create.py /app/create.py
COPY load.py /app/load.py
COPY main.py /app/main.py
COPY student_details.csv /app/student_details.csv
COPY students_score.csv /app/students_score.csv


CMD ["python3 main.py"]

