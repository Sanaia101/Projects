###THIS IS FROM MY CLASS NOTES AND FROM HW 2 ####
import mysql.connector #connects mysql to python
from mysql.connector import Error #imports class Error from mysql

# creates a MySQL connection to my database
def creating_connection(hostname, userid, pwd, dbname):
    connect = None
    try:
        connect = mysql.connector.connect(
            host=hostname,
            user=userid,
            password=pwd,
            database=dbname
        )
        print("The Database was Created Successfully!")  # Tells the user that the connection to the database was successful
    except Error as h:
        print("The Error for creating the table identifies as ", h) # Prints error message if the connection fails
    return connect

#This function is a general function to get the data from my database, can use this function for (select) statement 
def execute_sql_query(conn, sql):
    rows = None
    cursor = conn.cursor(dictionary=True)
    try:
        
        cursor.execute(sql)   ##fetch users table information
        rows = cursor.fetchall()
        return rows
    except Error as e:
        print("Your error message is ", e)

#This function updates data to my database, can have two functions: (insert,update)
def execute_update_query(conn, sql):
    rows = None
    cursor = conn.cursor(dictionary=True)
    try:
        
        cursor.execute(sql)   ##fetch users table information
        conn.commit()
        print("The query has been executed successfully!")
    except Error as e:
        print("Your error message is ", e)


###THIS IS FROM MY CLASS NOTES AND FROM HW 2###
