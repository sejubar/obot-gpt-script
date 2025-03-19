import os
import json
from datetime import datetime
from decimal import Decimal
from sqlalchemy import create_engine, text
from typing import Dict, List, Tuple
import pymysql

pymysql.install_as_MySQLdb()

# Define a custom serialization function for datetime objects

from datetime import date, datetime

def serialize_datetime(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    elif isinstance(obj, Decimal):
        return float(obj)
    else:
        raise TypeError(f"Type {obj.__class__.__name__} not serializable")

# Extract the tool's arguments from the env
def get_env_variables() -> Dict[str, str]:
    required_variables = ['DB_CONNECTION_STRING', 'QUERY']
    env_variables = {}
    for variable in required_variables:
        value = os.getenv(variable)
        if value is None:
            raise ValueError(f"Environment variable {variable} is not set")
        env_variables[variable] = value
    return env_variables

# Create a database engine
def create_database_engine(db_connection_string: str) -> object:
    try:
        engine = create_engine(db_connection_string)
        return engine
    except Exception as e:
        raise ValueError(f"Failed to create database engine: {e}")

# Execute the query
def execute_query(engine: object, query: str) -> Tuple[List[Dict], int]:
    try:
        with engine.connect() as conn:
            result = conn.execute(text(query))
            if query.lstrip().upper().startswith('SELECT'):
                results = [row._asdict() for row in result.fetchall()]
                return results, 200
            else:
                conn.commit()
                return [], 201
    except Exception as e:
        raise ValueError(f"Failed to execute query: {e}")

def main():
    env_variables = get_env_variables()
    engine = create_database_engine(env_variables['DB_CONNECTION_STRING'])
    results, status_code = execute_query(engine, env_variables['QUERY'])
    if status_code == 200:
        print(json.dumps(results, default=serialize_datetime))
    else:
        print('Query executed successfully!')

if __name__ == "__main__":
    main()
