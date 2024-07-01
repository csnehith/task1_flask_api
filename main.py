from flask import Flask, request
from psycopg2 import pool
import os

database_url = os.environ['DATABASE_URL']
conn_pool = pool.SimpleConnectionPool(1, 20, database_url)

app = Flask(__name__)


@app.route("/details/<table_name>", methods=["GET"])
def get_data_conditions(table_name):
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
        s = " AND ".join(f"{key} = {conditions[key]}" for key in conditions)
        query += s

    conn = conn_pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            data = cur.fetchall()
            return {"data": data}
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn_pool.putconn(conn)


@app.route("/insert_row/<table_name>", methods=["POST"])
def insert_new_row(table_name):
    data = request.json
    columns = ", ".join(data.keys())
    values = tuple(data.values())

    query = f"INSERT INTO {table_name} ({columns}) VALUES {values}"
    conn = conn_pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute(query)
        conn.commit()
        return {"New Row Inserted": "Success"}
    except Exception as e:
        conn.rollback()
        return {"error occured": e.args}
    finally:
        conn_pool.putconn(conn)


@app.route("/delete_row/<table_name>", methods=["DELETE"])
def delete_row(table_name):
    conditions = {}
    query = "DELETE "
    query += f" FROM {table_name}"

    for key, value in request.args.items():
        conditions[key] = value

    if conditions:
        query += " WHERE "
        str = " AND ".join(f"{key} = {conditions[key]}" for key in conditions)
        query += str
    conn = conn_pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute(query)
        conn.commit()
        return {"Row Deleted": "Sucess"}
    except Exception as e:
        conn.rollback()
        return {"error occured": e.args}
    finally:
        conn_pool.putconn(conn)


@app.route("/update_row/<table_name>", methods=["PATCH", "PUT"])
def update_row(table_name):
    if request.method == "PUT":
        conditions = {}
        query = f"UPDATE {table_name} SET "
        data = request.json

        query += ", ".join(f"{key} = %s" for key in data)

        for key, value in request.args.items():
            conditions[key] = value

        if conditions:
            query += " WHERE "
            s = " AND ".join(f"{key}={conditions[key]}" for key in conditions)
            query += s
        conn = conn_pool.getconn()
        try:
            with conn.cursor() as cur:
                cur.execute(query, tuple(data.values()))
            conn.commit()
            return {"Row Updated": "Success"}
        except Exception as e:
            conn.rollback()
            return {"error": str(e)}
        finally:
            conn_pool.putconn(conn)

    if request.method == "PATCH":
        conditions = {}
        query = f"UPDATE {table_name} SET "

        for key, value in request.args.items():
            conditions[key] = value

        data = request.json
        query += ", ".join(f"{key} = %s" for key in data)

        if conditions:
            query += " WHERE "
            s = " AND ".join(f"{key}={conditions[key]}" for key in conditions)
            query += s

        conn = conn_pool.getconn()
        try:
            with conn.cursor() as cur:
                cur.execute(query, tuple(data.values()))
            conn.commit()
            return {"Row Updated": "Success"}
        except Exception as e:
            conn.rollback()
            return {"error": str(e)}
        finally:
            conn_pool.putconn(conn)


@app.route("/join_tables", methods=["GET"])
def join_tables():
    table1_name = request.args.get("table1")
    table2_name = request.args.get("table2")
    column_names = request.args.get("columns")
    join_column = request.args.get("join_column")
    conditions = {}

    for key, value in request.args.items():
        if key not in ['table1', 'table2', 'columns', 'join_column']:
            conditions[key] = value

    query = "SELECT "

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
    conn = conn_pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
            return {"Data": rows}
    except Exception as e:
        return {"error occured - " + query: e.args}
    finally:
        conn_pool.putconn(conn)


@app.route("/groupby/<table_name>", methods=["GET"])
def groupby_columns(table_name):
    columns = request.args.get("columns_togroup")
    column = request.args.get("column_toagg")
    aggfunc = request.args.get("aggregate")
    conditions = {}
    for key, value in request.args.items():
        if key not in ["columns_togroup", "aggregate", "column_toagg"]:
            conditions[key] = value

    query = "SELECT "
    group = " "
    try:
        column_names = [col.strip() for col in columns.split(",")]
        group += ",".join(key for key in column_names)
    except Exception as e:
        return e.args

    if aggfunc:
        if column:
            query += f"{aggfunc.upper()}({column}),"
        else:
            return ["No value of column to apply the aggregate function"]
    else:
        if column:
            query += f"{column},"
        else:
            pass
    query += f"{group} FROM {table_name}"

    if conditions:
        query += " WHERE "
        s = " AND ".join(f"{key} = {conditions[key]}" for key in conditions)
        query += s

    query += f" GROUP BY {group}"
    conn = conn_pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
            return {"Data": rows}
    except Exception as e:
        return {"error occured": e.args}
    finally:
        conn_pool.putconn(conn)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
