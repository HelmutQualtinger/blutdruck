import csv
import mysql.connector
from DB_credentials import db_config # Import the DB-credentials module
from datetime import datetime  # Import the datetime module
import os  # Import os module for file path handling

def create_database_and_table(db_config):
    """Creates the 'Health' database and 'Heart' table if they don't exist."""
    try:
        # Ensure database='mysql' or no database initially to connect
        conn_init = mysql.connector.connect(
            host=db_config["host"],
            user=db_config["user"],
            password=db_config["password"]
        )
        cursor = conn_init.cursor()

        cursor.execute("CREATE DATABASE IF NOT EXISTS Health")
        cursor.execute("USE Health")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Heart (
                id INT AUTO_INCREMENT PRIMARY KEY,
                timestamp DATETIME, # Changed to DATETIME for potentially better handling without timezone issues
                systolic INT,
                diastolic INT,
                heart_rate INT
            )
        """)
        # Check if index exists before adding
        cursor.execute("SHOW INDEX FROM Heart WHERE Key_name = 'idx_timestamp'")
        if not cursor.fetchone():
            cursor.execute("ALTER TABLE Heart ADD INDEX idx_timestamp (timestamp)")
            print("Index 'idx_timestamp' added to 'Heart' table.")
        else:
            print("Index 'idx_timestamp' already exists.")

        conn_init.commit()
        print("Database 'Health' and table 'Heart' created/verified successfully.")
    except mysql.connector.Error as err:
        print(f"Error during setup: {err}")
    finally:
        if 'conn_init' in locals() and conn_init.is_connected():
            cursor.close()
            conn_init.close()

def copy_csv_to_mysql(db_config, csv_file):
    """Copies data from a CSV file to the 'Heart' table in the 'Health' database."""
    conn = None # Initialize conn to None
    try:
        conn = mysql.connector.connect(**db_config, database="Health")
        cursor = conn.cursor()

        insert_query = """
            INSERT INTO Heart (timestamp, systolic, diastolic, heart_rate) 
            VALUES (%s, %s, %s, %s)
        """
        records_to_insert = []
        assumed_year = 2025 # Consistent with your other scripts

        with open(csv_file, 'r') as file:
            csv_data = csv.reader(file)
            header = next(csv_data)  # Skip header row
            print(f"CSV Header: {header}") # Optional: print header to verify columns

            for i, row in enumerate(csv_data):
                try:
                    # Ensure row has the expected number of columns
                    if len(row) == 5: 
                        date_str, time_str, systolic_str, diastolic_str, heart_rate_str = row

                        # --- Date/Time Parsing ---
                        day, month = date_str.split('.')
                        # Construct a string Python's strptime can understand
                        datetime_str_for_parse = f"{assumed_year}-{month}-{day} {time_str}"
                        # Parse the string into a datetime object
                        dt_obj = datetime.strptime(datetime_str_for_parse, '%Y-%m-%d %H:%M')
                        # Format it into MySQL's preferred format
                        mysql_timestamp = dt_obj.strftime('%Y-%m-%d %H:%M:%S')
                        # --- End Date/Time Parsing ---

                        # Convert numeric values safely
                        systolic = int(systolic_str)
                        diastolic = int(diastolic_str)
                        heart_rate = int(heart_rate_str)

                        records_to_insert.append((mysql_timestamp, systolic, diastolic, heart_rate))
                    else:
                        print(f"Skipping row {i+1}: Unexpected number of columns ({len(row)}). Content: {row}")

                except ValueError as ve:
                    print(f"Skipping row {i+1} due to parsing error: {ve}. Row content: {row}")
                except Exception as e:
                    print(f"Skipping row {i+1} due to unexpected error: {e}. Row content: {row}")


        if records_to_insert:
            cursor.executemany(insert_query, records_to_insert)
            conn.commit()
            print(f"{cursor.rowcount} records from '{csv_file}' inserted into 'Heart' table successfully.")
        else:
            print("No valid records found to insert.")

    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        if conn:
            conn.rollback() # Rollback changes on error
    except FileNotFoundError:
        print(f"Error: CSV file '{csv_file}' not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()




# Use an absolute path or ensure the script runs from the correct directory
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_file = os.path.join(script_dir, "puls_data.csv")

# Check if CSV exists before proceeding
if not os.path.exists(csv_file):
    print(f"CRITICAL ERROR: CSV file not found at {csv_file}")
else:
    create_database_and_table(db_config)
    copy_csv_to_mysql(db_config, csv_file)
