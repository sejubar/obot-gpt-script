
echo "## Oracle"
export DB_CONNECTION_STRING=oracle://system/YourPassword123@localhost:1521/PDB1
export QUERY='SELECT * FROM EMPLOYEES e'
python ../db/db_query_executor.py


echo "## MariaDB"
export QUERY='select * from employee e'
export DB_CONNECTION_STRING=mariadb://root:my-secret-pw@localhost:3306/mydatabase
python ../db/db_query_executor.py

echo "## MSSQL"
export QUERY='select * from employees e'
export DB_CONNECTION_STRING="mssql+pyodbc://sa:mssql1Ipw@localhost:1433/MSSQLDB?driver=ODBC+Driver+17+for+SQL+Server"
python db_query_executor.py


