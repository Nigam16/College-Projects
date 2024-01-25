import pymysql
import time

mydb = pymysql.connect(
  host="localhost",
  user="root",
  password="",
  database="attendance"
)

name="samar"

mycursor = mydb.cursor()

mycursor.execute("SELECT id FROM attendance WHERE Name=\"Sudhir\" AND inout_flag= \"in\"")

myresult = mycursor.fetchall()
if myresult:
  date_string = "2012-12-12 10:10:10"
  print("THERE IS DATA")
  mycursor = mydb.cursor()
  mycursor.execute("UPDATE attendance SET checkout_at= %s  WHERE id=1", date_string)
  mydb.commit()
  
else:
  print ("There is no data")
  mycursor = mydb.cursor()
  sql = "INSERT INTO attendance (Name) VALUES (\"Sudhir\")"
  mycursor.execute(sql)
  mydb.commit()
  print(mycursor.rowcount, "record inserted.")

for x in myresult:
  print(x)
