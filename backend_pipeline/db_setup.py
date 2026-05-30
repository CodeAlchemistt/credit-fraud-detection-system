import mysql.connector
from mysql.connector import Error
import pandas as pd

def create_db_connection(host_name=None, user_name=None, user_password=None, db_name=None):
    import mysql.connector
    from mysql.connector import Error

    connection = None

    try:
        connection = mysql.connector.connect(
            host="zephyr.proxy.rlwy.net",
            user="root",
            password="AiGjhoFBkvmmWsngnEMlAADkoQZzAVTW",
            database="railway",
            port=51784
        )

        print("MySQL Database connection successful")

    except Error as err:
        print(f"Error: '{err}'")

    return connection

def setup_schema(connection):
    """
    Creates the 'transactions' table specifically for the Kaggle dataset.
    
    Inputs: Active MySQL connection
    Outputs: None
    """
    cursor = connection.cursor()
    # Create the table matching the standard Kaggle dataset format
    create_table_query = """
    CREATE TABLE IF NOT EXISTS transactions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        Time FLOAT,
        V1 FLOAT, V2 FLOAT, V3 FLOAT, V4 FLOAT, V5 FLOAT, V6 FLOAT, V7 FLOAT, 
        V8 FLOAT, V9 FLOAT, V10 FLOAT, V11 FLOAT, V12 FLOAT, V13 FLOAT, V14 FLOAT, 
        V15 FLOAT, V16 FLOAT, V17 FLOAT, V18 FLOAT, V19 FLOAT, V20 FLOAT, V21 FLOAT, 
        V22 FLOAT, V23 FLOAT, V24 FLOAT, V25 FLOAT, V26 FLOAT, V27 FLOAT, V28 FLOAT,
        Amount FLOAT,
        Class INT
    );
    """
    try:
        cursor.execute(create_table_query)
        connection.commit()
        print("Table 'transactions' created successfully.")
    except Error as err:
        print(f"Error: '{err}'")

def insert_data_in_batches(connection, csv_path, batch_size=5000):
    """
    Reads the CSV in chunks and inserts it into MySQL to handle large files efficiently.
    
    Inputs: connection object, path to the dataset, batch size integer
    Outputs: None
    """
    cursor = connection.cursor()
    # Read CSV in chunks so we don't overwhelm the RAM
    for chunk in pd.read_csv(csv_path, chunksize=batch_size):
        # Create a list of tuples containing the row data
        data = [tuple(x) for x in chunk.to_numpy()]
        
        # Prepare the SQL insert query
        placeholders = ', '.join(['%s'] * 31) # 1 Time + 28 V's + 1 Amount + 1 Class
        insert_query = f"INSERT INTO transactions (Time, V1, V2, V3, V4, V5, V6, V7, V8, V9, V10, V11, V12, V13, V14, V15, V16, V17, V18, V19, V20, V21, V22, V23, V24, V25, V26, V27, V28, Amount, Class) VALUES ({placeholders})"
        
        try:
            cursor.executemany(insert_query, data)
            connection.commit()
            print(f"Inserted {len(data)} rows")
        except Error as err:
                           print(f"Error inserting batch: '{err}'")
                           print("Data ingestion complete.")

if __name__ == "__main__":
    import os

    CSV_FILE_PATH = "data/creditcard.csv"

    print("Connecting to MySQL...")

    connection = create_db_connection(None, None, None)

    if connection:
        print(
            f"Using database: {os.getenv('MYSQLDATABASE', 'railway')}"
        )

        # Create the transactions table
        setup_schema(connection)

        print("Starting data insertion. This might take a few minutes...")
        insert_data_in_batches(
            connection,
            CSV_FILE_PATH,
            batch_size=10000
        )

        connection.close()
        print("Pipeline complete. Connection closed.")

    else:
        print("Failed to connect to database.")