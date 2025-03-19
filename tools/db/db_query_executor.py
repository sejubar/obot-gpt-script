import os
import json
from datetime import datetime, date
from decimal import Decimal
import pymssql, pymysql, psycopg2, oracledb
from typing import Dict, Tuple, List
from urllib.parse import urlparse

# Define a custom serialization function for datetime objects
def serialize_datetime(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, date):
        return obj.strftime('%Y-%m-%d')
    elif isinstance(obj, Decimal):
        return float(obj)
    else:
        raise TypeError(f"Type {obj.__class__.__name__} not serializable")

# Extract the tool's arguments from the env
def get_env_variables() -> dict[str, str]:
    required_variables = ['DB_CONNECTION_STRING', 'QUERY']
    env_variables = {}
    for variable in required_variables:
        value = os.getenv(variable)
        if value is None:
            raise ValueError(f"Environment variable {variable} is not set")
        env_variables[variable] = value
    return env_variables

# Define a dictionary that maps the database type to the corresponding library and connection function
database_libraries = {
    'mssql': {'library': pymssql, 'connect': lambda server, database, username, password: pymssql.connect(server=server, database=database, user=username, password=password)},
    'postgres': {'library': psycopg2, 'connect': lambda server, database, username, password: psycopg2.connect(host=server, database=database, user=username, password=password)},
    'oracle': {'library': oracledb, 'connect': lambda server, database, username, password: oracledb.connect(user=username, password=password, dsn=f"{server}/{database}")},
    'mariadb': {'library': pymysql, 'connect': lambda server, database, username, password: pymysql.connect(host=server, database=database, user=username, password=password)}
}

# Create a database connection
def create_database_connection(db_connection_string: str) -> object:
    try:
        # Parse the connection string
        parsed_url = urlparse(db_connection_string)
        username = parsed_url.username
        password = parsed_url.password
        server = parsed_url.hostname
        database = parsed_url.path.strip('/')
        database_type = parsed_url.scheme
        
        # Handle the mssql+pyodbc database type
        if database_type == 'mssql+pyodbc':
            database_type = 'mssql'
        
        # Handle the oracle+oracledb database type
        if database_type == 'oracle+oracledb':
            database_type = 'oracle'

        # Handle the mariadb database type
        if database_type == 'mariadb':
            database_type = 'mariadb'

        # Handle the postgres and postgresql database types
        if database_type in ['postgres', 'postgresql']:
            database_type = 'postgres'

        # Get the corresponding library and connection function
        library_info = database_libraries.get(database_type)
        if library_info is None:
            raise ValueError(f"Unsupported database type: {database_type}")
        
        # Create a database connection
        conn = library_info['connect'](server, database, username, password)
        return conn
    except Exception as e:
        raise ValueError(f"Failed to create database connection: {e}")

# Execute the query
def execute_query(conn: object, query: str) -> tuple[list[dict], int]:
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            if query.lstrip().upper().startswith('SELECT'):
                results = [{column: value for column, value in zip([desc[0] for desc in cursor.description], row)} for row in cursor.fetchall()]
                return results, 200
            else:
                conn.commit()
                return [], 201
    except Exception as e:
        raise ValueError(f"Failed to execute query: {e}")

def main():
    env_variables = get_env_variables()
    conn = create_database_connection(env_variables['DB_CONNECTION_STRING'])
    results, status_code = execute_query(conn, env_variables['QUERY'])
    if status_code == 200:
        print(json.dumps(results, default=serialize_datetime))
    else:
        print('Query executed successfully!')

if __name__ == "__main__":
    main()
