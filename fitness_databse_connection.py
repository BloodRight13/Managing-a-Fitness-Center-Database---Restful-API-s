import mysql.connector
from mysql.connector import Error
from mypassword import my_password

def get_db_connection():
    db_name = 'Fitness_Center_db'
    user = 'root'
    password = my_password # your password
    host ='localhost'

    try:
        conn = mysql.connector.connect(
            database = db_name,
            user = user,
            password = password,
            host = host
        )

        print('Connected to MySQL database succesfully')
        return conn
    
    except Error as e:
        print(f"Error: {e}")
        return None