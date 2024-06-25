
from flask import Flask, request
import psycopg2 
import os

  
conn = psycopg2.connect("host= 127.0.0.1 dbname=task user=postgres password=deq@123")


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:deq@123@127.0.0.1.docker.internal/task')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


cur = conn.cursor() 


@app.route("/details/:<table>", methods=["GET"])
def get_few_data_conditions(table):
    conditions = {}
    query = "SELECT "
    columns =[]
    for key, value in request.args.items():
        if key=='columns':
            columns.append(value)
        else:
            conditions[key] = value
    
    if columns:
        for key in columns:
            query += f"{key},"
        query = query[:-1]
    else:
        query +="*"
    query += f" FROM {table}"
    if conditions:
        query += " WHERE "
        for key, value in conditions.items():
            query += f"{key} = %s AND "
        query = query[:-5]  
    try:
        cur.execute(query, tuple(conditions.values()))
    except Exception as e:
        conn.rollback()
        return {"error occured":e.args}
    
    return {"data": cur.fetchall()}

@app.route("/insert_row/:<table>", methods =["POST"])
def insert_new_row(table):
    data = request.json
    columns = ", ".join(data.keys())
    values = tuple(data.values())

    query = f"INSERT INTO {table} ({columns}) VALUES {values}"
    
    try:
        cur.execute(query)
    except Exception as e:
        conn.rollback()
        return {"error occured": e.args}
    
    conn.commit() 
    return {"New Row Inserted": "Success"}

@app.route("/delete_row/:<table>", methods =["DELETE"])
def delete_row(table):
    conditions = {}
    query = "DELETE "
    query += f" FROM {table}"
    for key, value in request.args.items():
        conditions[key] = value
    
    if conditions:
        query += " WHERE "
        for key, value in conditions.items():
            query += f"{key} = %s AND "
        query = query[:-5]  

    try:
        cur.execute(query, tuple(conditions.values()))
    except Exception as e:
        conn.rollback()
        return {"error occured":e.args}
    
    conn.commit()
    return {"Row Deleted": "Sucess"}

@app.route("/update_row/:<table>", methods=["PATCH","PUT"])
def update_row(table):
    if request.method == "PUT":
        conditions ={}
        query = f"UPDATE {table}"
        for key, value in request.args.items():
            conditions[key] = value
        
        data = request.json
        keys = data.keys()
        values = tuple(data.values())
        query += " SET "
        for key in keys:
            query += f"{key} = %s,"
        query = query[:-1]

        if conditions:
            query += " WHERE "
            for key, value in conditions.items():
                query += f"{key} = %s AND "
            query = query[:-5] 
        try:
            cur.execute(query, values + tuple(conditions.values()))
        except Exception as e:
            conn.rollback()
            return {"error occured":e.args}
        
        conn.commit() 
        return {"Row Updated": "Success"}

        
    if request.method == "PATCH":
        conditions ={}
        query = f"UPDATE {table}"
        for key, value in request.args.items():
            conditions[key] = value
        
        data = request.json
        keys = data.keys()
        values = tuple(data.values())
        query += " SET "
        for key in keys:
            query += f"{key} = %s,"
        query = query[:-1]

        if conditions:
            query += " WHERE "
            for key, value in conditions.items():
                query += f"{key} = %s AND "
            query = query[:-5] 
      
        try:
            cur.execute(query, values + tuple(conditions.values()))
        except Exception as e:
            conn.rollback()
            return {"error occured":e.args}
        
        conn.commit() 
        return {"Row Updated": "Success"}
    
@app.route("/join_tables", methods=["GET"])
def join_tables():
    table1_name = request.args.get("table1")
    table2_name = request.args.get("table2")
    column_names = request.args.get("columns")
    join_column = request.args.get("join_column")
    conditions ={}
    for key,value in request.args.items():
        if key not in ['table1', 'table2','columns','join_column']:
            conditions[key]=value
    
    query = "SELECT "

    if column_names:
        column_names = [col.strip() for col in column_names.split(",")]
        for key in column_names:
            if key==join_column:
                key = f"{table1_name}."+key
            query += key+","
        query = query[:-1]
    else:
        query +="* "  
    
    query += f"""
        FROM {table1_name}
        INNER JOIN {table2_name}
        ON {table1_name}.{join_column} = {table2_name}.{join_column}
    """
    if conditions:
        query += " WHERE "
        for key, value in conditions.items():
            if key==join_column:
                key = f"{table1_name}."+key
            query += f"{key} = %s AND "
        query = query[:-5] 
    
    try:
        cur.execute(query, tuple(conditions.values()))
    except Exception as e:
        conn.rollback()
        return {"error occured":e.args}
        
    rows = cur.fetchall()
    return {"Data": rows}

@app.route("/groupby/:<table>", methods=["GET"])
def groupby_columns(table):
    columns = request.args.get("columns_togroup")
    column = request.args.get("column_toagg")
    aggfunc = request.args.get("aggregate")
    conditions ={}
    for key,value in request.args.items():
        if key not in ["columns_togroup","aggregate","column_toagg"]:
            conditions[key]=value
    
    query = "SELECT "
    group = " "
    try:
        column_names = [col.strip() for col in columns.split(",")]
        for key in column_names:
            group += key+","
        group = group[:-1]
    except Exception as e:
        return e.args
    
    if aggfunc:
        if column:
            query += f"{aggfunc.upper()}({column}),"  
        else:
            return ["Not entered value of column to apply the aggregate function"]
    else:
        if column:
            query += f"{column},"
        else:
            pass
    query += f"{group} FROM {table}"
    
    if conditions:
        query += " WHERE "
        for key, value in conditions.items():
            query += f"{key} = %s AND "
        query = query[:-5] 
    

    query += f" GROUP BY {group}"
    
    try:
        cur.execute(query, tuple(conditions.values()))
    except Exception as e:
        conn.rollback()
        return {"error occured":e.args}
        
    rows = cur.fetchall()
    return {"Data": rows}



if __name__ == "__main__":
    app.run(debug=True)
