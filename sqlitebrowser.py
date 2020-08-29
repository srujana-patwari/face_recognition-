import sqlite3

con = sqlite3.connect('mycompany.db')  #connection with Database
cObj =  con.cursor()    #Object for cursor

cObj.execute("CREATE TABLE IF NOT EXISTS employees(id INTEGER PRIMARY KEY, name TEXT, salary REAl,department TEXT,position TEXT)")
con.commit()

#insert valuse to Database

def insert_value(id,name,salary,department,position):
    cObj.execute("INSERT INTO employees VALUES(?,?,?,?,?)", (id,name,salary,department,position))
    con.commit()

#the recommanded type of update values is following this can protect from the SQLite injection

def update_department(dep,id):
    cObj.execute("UPDATE employees SET department=? WHERE id=?",(dep,id))
    con.commit()

#to fetch our data 2 methods

def sql_fetch():
    cObj.execute("SELECT * FROM employees")
    result = cObj.fetchall()
    print(result)

#Delete data
def delete_all():
    cObj.execute("DELETE FROM employees")
    con.commit()

#insert_value(3,"pavan",70000,"python","Developer")

delete_all()

cObj.close()
con.close()  #close all connections

