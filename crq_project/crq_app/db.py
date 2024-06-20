from dotenv import load_dotenv
import os
import pyodbc

load_dotenv()

# Database connection details
server = str(os.getenv('DB_SERVERNAME'))
database = str(os.getenv('DATABASE'))
username = str(os.getenv('DB_USERNAME'))
password = str(os.getenv('DB_PASSWORD'))

def get_data(sql_query):
    connection = pyodbc.connect('Driver={SQL Server};'
                                f'Server={server}, 1984;'
                                f'Database={database};'
                                f'uid={username};pwd=%s;'
                                'Trusted_Connection=yes;' % (password))
    cursor = connection.cursor()
    
    cursor.execute(sql_query)
    result = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return result