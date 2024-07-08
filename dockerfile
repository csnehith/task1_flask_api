FROM python:3.9-slim

WORKDIR /app


RUN pip install Flask[async] psycopg2-binary jsonschema aiopg asyncio temporalio

COPY create.py /app/create.py
COPY load.py /app/load.py
COPY main1.py /app/main1.py
COPY schemas.py /app/schemas.py
COPY temporal.py /app/temporal.py
COPY temporal_worker.py /app/temporal_worker.py
COPY student_details.csv /app/student_details.csv
COPY students_score.csv /app/students_score.csv


CMD ["python schema.py && python3 main.py"]

