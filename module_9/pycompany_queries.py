""" 
    Title: pycompany_queries.py
    Author: James Vaughan
    Date: 22 July 2023
    Description: Test program for executing queries against the pycompany database. 
"""

""" import statements """
import mysql.connector
from mysql.connector import errorcode

""" database config object """
config = {
    "user": "root",
    "password": "^kEbO9H%57J4:(k&g$z",
    "host": "127.0.0.1",
    "database": "pycompany",
    "raise_on_warnings": True
}

try:
    """ try/catch block for handling potential MySQL database errors """ 

    db = mysql.connector.connect(**config) # connect to the pycompany database 

    cursor = db.cursor()

    # select query from the department table 
    cursor.execute("SELECT department_id, department_name, department_size FROM department")

    # get the results from the cursor object 
    departments = cursor.fetchall()

    print("\n  -- DISPLAYING department RECORDS --")
    
    # iterate over the departments data set and display the results 
    for department in departments: 
        print("  department ID: {}\n  department Name: {}\n  department_size: {}\n".format(department[0], department[1], department[2]))

    # select query for the employee table 
    cursor.execute("SELECT employee_id, employee_name, birth_month, department_id FROM employee")

    # get the results from the cursor object 
    employees = cursor.fetchall()

    print ("\n  -- DISPLAYING employee RECORDS --")

    # iterate over the employees data set and display the results
    for employee in employees:
        print("  employee ID: {}\n  Name: {}\n  Birth Month: {}\n  department ID: {}\n".format(employee[0], employee[1], employee[2], employee[3]))

    input("\n\n  Press any key to continue... ")

except mysql.connector.Error as err:
    """ handle errors """

    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("  The supplied username or password are invalid")

    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("  The specified database does not exist")

    else:
        print(err)

finally:
    """ close the connection to MySQL """
    
    db.close()