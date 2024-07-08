"""Flask API Calls"""
import asyncio
from flask import Flask, request, jsonify
from temporalio.client import Client
import jsonschema
import jsonschema.exceptions
from jsonschema import validate
import schemas
from temporal import QueryWorkflow

app = Flask(__name__)


async def executequery(query):
    """executing_query - run_workflow"""
    client = await Client.connect("temporal:7233", namespace="default")
    result = await client.execute_workflow(
        QueryWorkflow.run,
        query,
        task_queue="task-queue",
        id="my-workflow-id",
    )
    return result


def preprocess_args(args, schema):
    """Function to convert request.args type from string to number"""
    processed_args = {}
    for key, value in args.items():
        if key in schema["properties"]:
            expected_type = schema["properties"][key]["type"]
            if expected_type == "number":
                try:
                    processed_args[key] = float(value)
                except ValueError:
                    processed_args[key] = value
            else:
                processed_args[key] = value
        else:
            processed_args[key] = value
    return processed_args


@app.route("/details/<table_name>", methods=["GET"])
def get_data_conditions(table_name):
    """Function to get details in table."""
    if table_name == 'student_details':
        schema = schemas.schema_student_details
    elif table_name == 'students_score':
        schema = schemas.schema_students_score
    else:
        return {"Error": "Invalid table name"}, 400

    args = preprocess_args(request.args.to_dict(), schema)
    try:
        validate(instance=args, schema=schema)
    except jsonschema.exceptions.ValidationError as e:
        return {"Error": str(e)}, 400

    conditions = {}
    columns = []
    query = "SELECT "

    for key, value in args.items():
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

    result = asyncio.run(executequery(query))
    return jsonify(result)


@app.route("/insert_row/<table_name>", methods=["POST"])
def insert_new_row(table_name):
    """Function to insert new row in table."""
    if table_name == 'student_details':
        schema = schemas.schema_student_details
    elif table_name == 'students_score':
        schema = schemas.schema_students_score
    else:
        return {"Error": "Invalid table name"}, 400

    try:
        validate(instance=request.json, schema=schema)
    except jsonschema.exceptions.ValidationError as e:
        return {"error": str(e)}, 400

    data = request.json
    columns = ", ".join(data.keys())
    values = tuple(data.values())

    query = f"INSERT INTO {table_name} ({columns}) VALUES {values}"

    result = asyncio.run(executequery(query))
    return jsonify(result)


@app.route("/delete_row/<table_name>", methods=["DELETE"])
def delete_row(table_name):
    """Function to Delete rows in table."""
    if table_name == 'student_details':
        schema = schemas.schema_student_details
    elif table_name == 'students_score':
        schema = schemas.schema_students_score
    else:
        return {"Error": "Invalid table name"}, 400
    args = preprocess_args(request.args.to_dict(), schema)
    try:
        validate(instance=args, schema=schema)
    except jsonschema.exceptions.ValidationError as e:
        return {"error": str(e)}, 400

    conditions = {}
    query = "DELETE "
    query += f" FROM {table_name}"

    for key, value in args.items():
        conditions[key] = value

    if conditions:
        query += " WHERE "
        query += " AND ".join(
            f"{key} = {value}" for key, value in conditions.items())

    result = asyncio.run(executequery(query))
    return jsonify(result)


@app.route("/update_row/<table_name>", methods=["PATCH", "PUT"])
def update_row(table_name):
    """Function to Update row values"""
    if table_name == 'student_details':
        schema = schemas.schema_student_details
    elif table_name == 'students_score':
        schema = schemas.schema_students_score
    else:
        return {"Error": "Invalid table name"}, 400

    try:
        validate(instance=request.json, schema=schema)
    except jsonschema.exceptions.ValidationError as e:
        return {"error": str(e)}, 400

    args = preprocess_args(request.args.to_dict(), schema)
    if request.method == "PUT":
        conditions = {}
        query = f"UPDATE {table_name} SET "
        data = request.json

        query += ", ".join(f"{key} = {value}" for key, value in data.items())

        for key, value in args.items():
            conditions[key] = value

        if conditions:
            query += " WHERE "
            query += " AND ".join(
                f"{key}={value}" for key, value in conditions.items())

        result = asyncio.run(executequery(query))
        return jsonify(result)

    if request.method == "PATCH":
        conditions = {}
        query = f"UPDATE {table_name} SET "

        for key, value in args.items():
            conditions[key] = value

        data = request.json
        query += ", ".join(f"{key} = {value}" for key, value in data.items())

        if conditions:
            query += " WHERE "
            query += " AND ".join(
                f"{key}={value}" for key, value in conditions.items())

        result = asyncio.run(executequery(query))
        return jsonify(result)


@app.route("/join_tables", methods=["GET"])
def join_tables():
    """function to inner join tables"""
    try:
        validate(instance=request.args.to_dict(), schema=schemas.schema_join)
    except jsonschema.exceptions.ValidationError as e:
        return {"error": str(e)}, 400

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
            return jsonify({"Error": "Invalid condition input"}), 400

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

    result = asyncio.run(executequery(query))
    return jsonify(result)


@app.route("/groupby/<table_name>", methods=["GET"])
def groupby_columns(table_name):
    """function to group columns in a table"""
    if table_name == 'student_details':
        schema = schemas.schema_student_details
    elif table_name == 'students_score':
        schema = schemas.schema_students_score
    else:
        return {"Error": "Invalid table name"}, 400

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
            return jsonify({"Error": "Invalid condition input"}), 400

        conditions = preprocess_args(conditions, schema)
        try:
            validate(instance=conditions, schema=schema)
        except jsonschema.exceptions.ValidationError as e:
            return {"error": str(e)}, 400

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
    result = asyncio.run(executequery(query))
    return jsonify(result)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
