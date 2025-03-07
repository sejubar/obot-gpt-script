# obot-gpt-script - Postgres Query Executor Tool

A generic tool to execute SQL queries against a Postgres database.

## Description

This tool allows you to execute SQL queries against a Postgres database. It supports various query types, including **SELECT, INSERT, UPDATE**, and **DELETE**.

## Usage

To use this tool, provide the following arguments:
```
query: The SQL query to execute
host: The Postgres host
port: The Postgres port
database: The Postgres database
user: The Postgres username
password: The Postgres password
```

##Example

To insert a new record into the car_maintainance_invoices table:

```Bash
POSTGRES_QUERY="INSERT INTO public.car_maintainance_invoices( entry_id, created_date, comment, invoice_content) VALUES (DEFAULT, DEFAULT, DEFAULT,'{ \"service_receipt\": { \"invoice_number\": \"J-0046\"} }');" POSTGRES_HOST='127.0.0.1' POSTGRES_PORT='5432' POSTGRES_DATABASE='obotdemo' POSTGRES_USERNAME='postgres' POSTGRES_PASSWORD='fortune2' python postgres_query_executor.py
```

query="INSERT INTO public.car_maintainance_invoices( entry_id, created_date, comment, invoice_content) VALUES (DEFAULT, DEFAULT, DEFAULT,'{ \"service_receipt\": { \"invoice_number\": \"J-0046\"} }');" host='127.0.0.1' port='5432' database='obotdemo' user='postgres' password='fortune2'

This will execute the INSERT query and return a success message if the query is executed successfully.
Requirements

Python 3.x
psycopg2 library
Installation

Install the required libraries using pip: pip install psycopg2
Clone this repository or download the postgres_query_executor.py script.
Contributing

Contributions are welcome! Please submit a pull request with your changes.
License

---
This tool is released under the MIT License.

