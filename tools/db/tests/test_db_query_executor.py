# tests/test_db_query_executor.py
import unittest
from db_query_executor import create_database_connection, execute_query, get_env_variables
import os
import pymssql
import psycopg2
import pymysql
import oracledb

class TestDatabaseQueryExecutor(unittest.TestCase):

    def test_create_database_connection(self):
        # Get the connection string from the environment variable
        db_connection_string = os.environ.get('DB_CONNECTION_STRING')

        # Test create_database_connection function
        conn = create_database_connection(db_connection_string)
        self.assertIsNotNone(conn)

    def test_execute_query(self):
        # Get the connection string and query from the environment variables
        db_connection_string = os.environ.get('DB_CONNECTION_STRING')
        query = os.environ.get('QUERY')

        # Create a database connection
        conn = create_database_connection(db_connection_string)

        # Test execute_query function
        results, status_code = execute_query(conn, query)
        self.assertEqual(status_code, 200)

    def test_get_env_variables(self):
        # Set environment variables for testing
        os.environ['DB_CONNECTION_STRING'] = 'mssql+pyodbc://username:password@localhost:1433/database'
        os.environ['QUERY'] = 'SELECT * FROM table'

        # Test get_env_variables function
        env_variables = get_env_variables()
        self.assertEqual(env_variables['DB_CONNECTION_STRING'], 'mssql+pyodbc://username:password@localhost:1433/database')
        self.assertEqual(env_variables['QUERY'], 'SELECT * FROM table')

    def test_create_database_connection_invalid_connection_string(self):
        # Test create_database_connection function with invalid connection string
        with self.assertRaises(ValueError):
            create_database_connection('invalid_connection_string')

    def test_create_database_connection_missing_database_type(self):
        # Test create_database_connection function with missing database type
        with self.assertRaises(ValueError):
            create_database_connection('://username:password@localhost:1433/database')

    def test_create_database_connection_unknown_database_type(self):
        # Test create_database_connection function with unknown database type
        with self.assertRaises(ValueError):
            create_database_connection('unknown+pyodbc://username:password@localhost:1433/database')

    def test_execute_query_invalid_query(self):
        # Get the connection string from the environment variable
        db_connection_string = os.environ.get('DB_CONNECTION_STRING')

        # Create a database connection
        conn = create_database_connection(db_connection_string)

        # Test execute_query function with invalid query
        with self.assertRaises(ValueError):
            execute_query(conn, 'INVALID QUERY')

    def test_execute_query_connection_closed(self):
        # Get the connection string from the environment variable
        db_connection_string = os.environ.get('DB_CONNECTION_STRING')

        # Create a database connection
        conn = create_database_connection(db_connection_string)
        conn.close()

        # Test execute_query function with closed connection
        with self.assertRaises(ValueError):
            execute_query(conn, 'SELECT * FROM table')

    def test_get_env_variables_missing_variable(self):
        # Delete environment variable for testing
        if 'DB_CONNECTION_STRING' in os.environ:
            os.environ.pop('DB_CONNECTION_STRING')

        # Test get_env_variables function with missing variable
        with self.assertRaises(ValueError):
            get_env_variables()

if __name__ == "__main__":
    unittest.main()