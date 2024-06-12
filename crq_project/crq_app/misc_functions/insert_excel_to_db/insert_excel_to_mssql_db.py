from dotenv import load_dotenv
import pandas as pd
import pyodbc
import os

load_dotenv()

# Read the Excel file
excel_file_path = 'crq_project\crq_app\misc_functions\insert_excel_to_db\Copy of Wintel Patching Inventory_29-Feb-2024.xlsx'
df = pd.read_excel(excel_file_path, sheet_name='Data')  # Adjust sheet_name as needed

# Select specific columns to insert into the database
columns_to_insert = ['FQDN', 'IP Address', 'Trust Level', 'Operating System', 'Business Unit', 'Application Name', 'Application Owner', 'Asset Group Classification']  # Replace with your column names
df_to_insert = df[columns_to_insert]
df_to_insert.dropna(inplace=True)

# Database connection details
server = str(os.getenv('DB_SERVERNAME'))
database = str(os.getenv('DATABASE'))
username = str(os.getenv('DB_USERNAME'))
password = str(os.getenv('DB_PASSWORD'))
table_name = str(os.getenv('WINTEL_INVENTORY_TABLE_NAME'))

connection = pyodbc.connect('Driver={SQL Server};'
                            f'Server={server}, 1984;'
                            f'Database={database};'
                            f'uid={username};pwd=%s;'
                            'Trusted_Connection=yes;' % (password))
cursor = connection.cursor()

# Function to generate insert query for each row
def insert_row(cursor, table_name, row):
    placeholders = ', '.join(['?'] * len(row))
    columns = ', '.join(row.index)
    # print(placeholders)
    sql = f"INSERT INTO {table_name} (FQDN, IP_Address, Trust_Level, Operating_System, Business_Unit, Application_Name, Application_Owner, Asset_Group_Classification) VALUES ({placeholders})"
    cursor.execute(sql, tuple(row))

# Insert each row into the database
for index, row in df_to_insert.iterrows():
    insert_row(cursor, table_name, row)

# Commit the transaction
connection.commit()

# Close the connection
cursor.close()
connection.close()

print("Data inserted successfully.")
