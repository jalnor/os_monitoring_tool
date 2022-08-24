import mysql.connector
import os

mydb = mysql.connector.connect(
    host="localhost",
    user="jnor42",
    password=os.environ["db_pword"],
    database="os_monitoring_tool"
)

cursor = mydb.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS processes (name VARCHAR(255), proc_id INT(32), status VARCHAR(255), start_time TIME, stop_time TIME, start_date DATE, end_date DATE)")