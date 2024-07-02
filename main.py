"""Flask API Calls"""
from concurrent.futures import ThreadPoolExecutor
import os
from flask import Flask, request, jsonify
from psycopg2 import pool
import jsonschema
from jsonschema import validate
import schemas


database_url = os.environ['DATABASE_URL']
conn_pool = pool.SimpleConnectionPool(1, 20, database_url)

app = Flask(__name__)
executor = ThreadPoolExecutor(max_workers=20)


def executequery(query, params=None):
    """To connect with database and execute the query."""
    conn = conn_pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute(query, params)
            if cur.description:
                columns = [desc[0] for desc in cur.description]
                data = cur.fetchall()
                result = [dict(zip(columns, row)) for row in data]
                return {"data": result}, 200
            conn.commit()
            return {"status": "sucess"}, 200
    except Exception as e:
        if cur.description:
            return {"error": e.args}, 500
        conn.rollback()
        return {"error": e.args}, 500
    finally:
        conn_pool.putconn(conn)


@app.route("/details/<table_name>", methods=["GET"])
def get_data_conditions(table_name):
    """Function to get details in table."""
    if table_name == 'student_details':
        schema = schemas.schema_student_details
    elif table_name == 'students_score':
        schema = schemas.schema_students_score
    else:
        return {"status": "error", "message": "Invalid table name"}, 400

    try:
        validate(instance=request.args.to_dict(), schema=schema)
    except jsonschema.exceptions.ValidationError as e:
        return jsonify({"error": str(e)}), 400

    conditions = {}
    columns = []
    query = "SELECT "

    for key, value in request.args.items():
        if key == 'columns':
            columns.append(value)
        else:
            conditions[key] = value

    if columns:
        query += ", ".join(columns)
    else:
        query += "*"

    query += f" FROM {table_name}"

    if conditions:
        query += " WHERE "
        query += " AND ".join(
            f"{key} = {value}" for key, value in conditions.items())

    future = executor.submit(executequery, query)
    result = future.result()
    return jsonify(result)


@app.route("/insert_row/<table_name>", methods=["POST"])
def insert_new_row(table_name):
    """Function to insert new row in table."""
    if table_name == 'student_details':
        schema = schemas.schema_student_details
    elif table_name == 'students_score':
        schema = schemas.schema_students_score
    else:
        return {"status": "error", "message": "Invalid table name"}, 400

    try:
        validate(instance=request.json, schema=schema)
    except jsonschema.exceptions.ValidationError as e:
        return jsonify({"error": str(e)}), 400

    data = request.json
    columns = ", ".join(data.keys())
    values = tuple(data.values())

    query = f"INSERT INTO {table_name} ({columns}) VALUES {values}"

    future = executor.submit(executequery, query)
    result = future.result()
    return jsonify(result)


@app.route("/delete_row/<table_name>", methods=["DELETE"])
def delete_row(table_name):
    """Function to Delete rows in table."""
    if table_name == 'student_details':
        schema = schemas.schema_student_details
    elif table_name == 'students_score':
        schema = schemas.schema_students_score
    else:
        return {"status": "error", "message": "Invalid table name"}, 400

    try:
        validate(instance=request.args.to_dict(), schema=schema)
    except jsonschema.exceptions.ValidationError as e:
        return jsonify({"error": str(e)}), 400

    conditions = {}
    query = "DELETE "
    query += f" FROM {table_name}"

    for key, value in request.args.items():
        conditions[key] = value

    if conditions:
        query += " WHERE "
        query += " AND ".join(
            f"{key} = {value}" for key, value in conditions.items())

    future = executor.submit(executequery, query)
    result = future.result()
    return jsonify(result)


@app.route("/update_row/<table_name>", methods=["PATCH", "PUT"])
def update_row(table_name):
    """Function to Update row values"""
    if table_name == 'student_details':
        schema = schemas.schema_student_details
    elif table_name == 'students_score':
        schema = schemas.schema_students_score
    else:
        return {"status": "error", "message": "Invalid table name"}, 400

    try:
        validate(instance=request.json, schema=schema)
    except jsonschema.exceptions.ValidationError as e:
        return jsonify({"error": str(e)}), 400

    if request.method == "PUT":
        conditions = {}
        query = f"UPDATE {table_name} SET "
        data = request.json

        query += ", ".join(f"{key} = %s" for key in data)

        for key, value in request.args.items():
            conditions[key] = value

        if conditions:
            query += " WHERE "
            query += " AND ".join(
                f"{key}={value}" for key, value in conditions.items())

        future = executor.submit(executequery, query, tuple(data.values()))
        result = future.result()
        return jsonify(result)

    if request.method == "PATCH":
        conditions = {}
        query = f"UPDATE {table_name} SET "

        for key, value in request.args.items():
            conditions[key] = value

        data = request.json
        query += ", ".join(f"{key} = %s" for key in data)

        if conditions:
            query += " WHERE "
            query += " AND ".join(
                f"{key}={value}" for key, value in conditions.items())

        future = executor.submit(executequery, query, tuple(data.values()))
        result = future.result()
        return jsonify(result)


@app.route("/join_tables", methods=["GET"])
def join_tables():
    """function to inner join tables"""
    try:
        validate(instance=request.args.to_dict(), schema=schemas.schema_join)
    except jsonschema.exceptions.ValidationError as e:
        return jsonify({"error": str(e)}), 400

    table1_name = request.args.get("table1")
    table2_name = request.args.get("table2")
    column_names = request.args.get("columns")
    join_column = request.args.get("join_column")
    conditions_string = request.args.get("conditions")
    query = "SELECT "
    conditions = {}
    if conditions_string:
        try:
            conditions = {key.strip(): value.strip()
                          for key, value in
                          (cond.split("=")
                           for cond in conditions_string.split(","))}
        except ValueError:
            return {"Error": "Invalid condition input"}
    if column_names:
        column_names = [col.strip() for col in column_names.split(",")]
        query += ", ".join(
            f"{table1_name}.{key}" if key == join_column else key
            for key in column_names
        )
    else:
        query += "* "

    query += f"""
        FROM {table1_name}
        INNER JOIN {table2_name}
        ON {table1_name}.{join_column} = {table2_name}.{join_column}
    """
    if conditions:
        query += " WHERE "
        query += " AND ".join(
            f"{table1_name}.{key} = {value}" if key == join_column else
            f"{key} = {value}" for key, value in conditions.items()
        )

    future = executor.submit(executequery, query)
    result = future.result()
    return jsonify(result)


@app.route("/groupby/<table_name>", methods=["GET"])
def groupby_columns(table_name):
    """function to group columns in a table"""
    try:
        validate(instance=request.args.to_dict(), schema=schemas.schema_group)
    except jsonschema.exceptions.ValidationError as e:
        return jsonify({"error": str(e)}), 400

    columns = request.args.get("columns_togroup")
    column = request.args.get("column_toagg")
    aggfunc = request.args.get("aggregate")
    conditions_string = request.args.get("conditions")
    conditions = {}
    if conditions_string:
        try:
            conditions = {key.strip(): value.strip()
                          for key, value in
                          (cond.split("=")
                           for cond in conditions_string.split(","))}
        except ValueError:
            return {"Error": "Invalid condition input"}

    query = "SELECT "
    group = " "
    column_names = [col.strip() for col in columns.split(",")]
    group += ",".join(key for key in column_names)

    if aggfunc:
        if column:
            query += f"{aggfunc.upper()}({column}),"
        else:
            return ["No value of column to apply the aggregate function"]
    else:
        if column:
            query += f"{column},"
    query += f"{group} FROM {table_name}"

    if conditions:
        query += " WHERE "
        query += " AND ".join(
                f"{key} = {value}" for key, value in conditions.items())

    query += f" GROUP BY {group}"
    future = executor.submit(executequery, query)
    result = future.result()
    return jsonify(result)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
