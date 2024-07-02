FROM python:3.9-slim

WORKDIR /app


RUN pip install Flask psycopg2-binary jsonschema

COPY create.py /app/create.py
COPY load.py /app/load.py
COPY main.py /app/main.py
COPY schemas.py /app/schemas.py
COPY student_details.csv /app/student_details.csv
COPY students_score.csv /app/students_score.csv


CMD ["python schema.py && python3 main.py"]

