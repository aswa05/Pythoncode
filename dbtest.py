import pyodbc
import pymysql
import mysql.connector
conn = pyodbc.connect(
    "Driver={SQL Server Native Client 11.0};"
    "Server=LENOVO;"
    "Database=ChangeRequest;"
    "Trusted_Connection=yes;"
)

conn = pymysql.connect(host="localhost", user="root", password="", database="dbnames")
cur=conn.cursor()
sql="select * from dbo.login"
cur.execute(sql)
res=cur.fetchall()

print(res)
