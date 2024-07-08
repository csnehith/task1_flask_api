# First Task

## Table of Contents
- [Introduction](#introduction)
  - [create.py](#createpy)
  - [load.py](#loadpy)
  - [main.py](#mainpy)
- [API Endpoints](#api-endpoints)

## Introduction
This assignment handles database creation, data loading, and API interactions using Flask. It uses Docker for containerization and provides a simple API for accessing the data.

### Installation
1. Clone the repository

2. Build and start the Docker containers:
   docker-compose up --build


### create.py
The `create.py` script is used to create the necessary database schema in the PostgreSQL Docker container.

### load.py
The `load.py` script is used to load data from the `student_details.csv` and `students_score.csv` files into the database.

### main.py
The `main.py` script contains the API calls to interact with the data. It uses Flask to set up the API endpoints.

## API Endpoints
The API provides the following endpoints:

- **GET `/details/<table_name>`**: Fetch data from the specified table in the database.
  - You can specify conditions and columns to view through query parameters.
  - To specify columns directly, use the key `columns` and the value as the column names you want to view from the mentioned table.
  
- **POST `/insert_row/<table_name>`**: Insert data into the specified table in the database.
  - You can insert new values into the mentioned table by providing the details in JSON format.

- **DELETE `/delete_row/<table_name>`**: Delete data from the specified table in the database.
  - You can delete rows from the mentioned table by specifying conditions in the query parameters.

- **PUT or PATCH `/update_row/<table_name>`**: Update data in the specified table in the database.
  - You can update existing values in the mentioned table by providing the details in JSON format.

- **GET `/join_tables`**: View data by performing an inner join on the specified tables in the database.
  - You can join and view columns from the mentioned tables by specifying conditions in the query parameters.
  - Use the following keys and values:
    - `table1`: name of the first table
    - `table2`: name of the second table
    - `join_column`: column through which the tables should be joined
    - `columns`: column names to view
    - `conditions` : you can mention specific conditions for the data you want to see.
  
- **GET `/groupby/<table_name>`**: Group the data of a specified table in the database.
  - You can group the data of specified columns from the mentioned table by specifying conditions in the query parameters.
  - Use the following keys and values:
    - `columns_togroup`: columns to group by
    - `aggregate`: aggregate function to use on a column
    - `column_toagg`: column name on which to apply the aggregate function
    - `conditions` : you can mention specific conditions for the data you want to see.
