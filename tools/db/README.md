# OBot Database Tool


A versatile tool for interacting with multiple databases, including Oracle, MSSQL, MariaDB, and Postgres.

## Overview

This tool provides a simple and unified way to execute SQL queries against various databases. It supports multiple database management systems and allows users to easily switch between them.

## Features

Execute SQL queries against Oracle, MSSQL, MariaDB, and Postgres databases
Unified interface for interacting with multiple databases
Support for environment variables and credentials
Easy to use and extend

## Usage

Clone the repository and navigate to the db directory.
Update the credential file with your database credentials.
Run the tool using the command python db_query_executor.py.
Provide the SQL query as an input when prompted.

## Testing the Tool

To test the tool, set the DB_CONNECTION_STRING and QUERY environment variables and then run the db_query_executor.py script.

## Oracle


```
Bash
export DB_CONNECTION_STRING=oracle+oracledb://system:YourPassword123@localhost:1521/?service_name=PDB1
export QUERY='SELECT * FROM EMPLOYEES e'
python db/db_query_executor.py
```

## Postgres

```
Bash
export QUERY='select * from common_english_names;'
export DB_CONNECTION_STRING=postgresql://neondb_owner:npg_9xCX4VUuvaKL@ep-holy-salad-a8qhn40c-pooler.eastus2.azure.neon.tech/neondb?sslmode=require
python db/db_query_executor.py
```

## MariaDB

```
Bash
export QUERY='select * from employee e'
export DB_CONNECTION_STRING=mariadb://root:my-secret-pw@localhost:3306/mydatabase
python db/db_query_executor.py
```

## MSSQL

```
Bash
export DB_CONNECTION_STRING="mssql+pyodbc://sa:mssql1Ipw@localhost:1433/MSSQLDB?driver=ODBC+Driver+17+for+SQL+Server"
python db/db_query_executor.py
```

## Requirements

Python 3.x
SQLAlchemy library
PyODBC library (for MSSQL and Oracle)
psycopg2 library (for Postgres)
mariadb library (for MariaDB)

## Contributing

Contributions are welcome! If you'd like to add support for more databases or improve the tool's functionality, please submit a pull request.

License
-------
This project is licensed under the MIT License. See the LICENSE file for details.

