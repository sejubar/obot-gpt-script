import os
import psycopg2
import json
from datetime import datetime

# Define a custom serialization function for datetime objects
def serialize_datetime(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {obj.__class__.__name__} not serializable")

# Extract the tool's arguments from the env
query = os.getenv('QUERY')
host = os.getenv('POSTGRES_HOST')
port = os.getenv('POSTGRES_PORT')
database = os.getenv('POSTGRES_DATABASE')
user = os.getenv('POSTGRES_USERNAME')
password = os.getenv('POSTGRES_PASSWORD')

# Establish a connection to the Postgres database
conn = psycopg2.connect(
    host=host,
    port=port,
    database=database,
    user=user,
    password=password
)

# Create a cursor object
cur = conn.cursor()

# Execute the query
cur.execute(query)

# Check if the query is a SELECT query
if query.lstrip().upper().startswith('SELECT'):
    # Fetch the results
    results = cur.fetchall()
    # Return the results as JSON
    print(json.dumps(results, default=serialize_datetime))
else:
    # Commit the changes
    conn.commit()
    # Return a success message
    print('Query executed successfully!')

# Close the cursor and connection
cur.close()
conn.close()