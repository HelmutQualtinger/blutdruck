# Import necessary modules from Flask and standard libraries
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy # Note: SQLAlchemy is imported but not used, consider removing if not needed
from datetime import datetime, date
import mysql.connector # Import the MySQL connector for database interaction
from DB_credentials import db_config  # Import the database configuration

# Initialize the Flask application
app = Flask("Blutdruck")
# Configure a secret key for session management and flashing messages
app.config['SECRET_KEY'] = 'your_secret_key_here' # Replace with a strong, random secret key

def get_db_connection():
    """Establishes a connection to the MySQL database using credentials from db_config."""
    try:
        # Connect to the database using the imported configuration
        conn = mysql.connector.connect(**db_config, database="Health")
        return conn
    except mysql.connector.Error as err:
        # Print an error message if the connection fails
        print(f"Error connecting to database: {err}")
        # Return None to indicate failure
        return None

def create_table_if_not_exists():
    """Creates the 'Heart' table in the 'Health' database if it doesn't already exist."""
    conn = get_db_connection() # Get a database connection
    if conn: # Proceed only if the connection was successful
        try:
            cursor = conn.cursor() # Create a cursor object to execute SQL queries
            # SQL query to create the 'Heart' table if it doesn't exist
            # Defines columns: id (auto-incrementing primary key), timestamp, systolic, diastolic, heart_rate
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Heart (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    systolic INT,
                    diastolic INT,
                    heart_rate INT
                )
            """)
            conn.commit() # Commit the changes to the database
            print("Table 'Heart' checked/created successfully.") # Confirmation message
        except mysql.connector.Error as err:
            print(f"Error creating table: {err}") # Print error if table creation fails
        finally:
            # Ensure cursor and connection are closed regardless of success or failure
            if cursor:
                cursor.close()
            if conn:
                conn.close()

# Call the function to ensure the table exists when the application starts
create_table_if_not_exists()

@app.route('/')
def index():
    """Displays all heart rate entries from the database on the main page."""
    conn = get_db_connection() # Get a database connection
    hearts = [] # Initialize an empty list to store heart data
    if conn: # Proceed only if the connection was successful
        try:
            # Create a cursor that returns results as dictionaries
            cursor = conn.cursor(dictionary=True)
            # Select all records from the Heart table, ordered by timestamp descending
            cursor.execute("SELECT * FROM Heart ORDER BY timestamp DESC")
            hearts = cursor.fetchall() # Fetch all results
        except mysql.connector.Error as err:
            flash(f"Database error fetching data: {err}", "error") # Show error message to user
        finally:
            # Ensure cursor and connection are closed
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    else:
        # If connection failed, show an error message
        flash("Failed to connect to the database.", "error")

    # Render the 'index.html' template, passing the fetched heart data
    return render_template('index.html', hearts=hearts)

@app.route('/add', methods=['POST'])
def add():
    """Handles the submission of the form to add a new heart rate entry."""
    conn = None # Initialize connection variable
    cursor = None # Initialize cursor variable
    try:
        # Get data from the submitted form
        timestamp_str = request.form.get('timestamp')
        systolic = request.form.get('systolic')
        diastolic = request.form.get('diastolic')
        heart_rate = request.form.get('heart_rate')

        # Basic validation: check if all fields are provided
        if not all([timestamp_str, systolic, diastolic, heart_rate]):
            flash("All fields are required.", "error") # Show error if any field is missing
            return redirect(url_for('index')) # Redirect back to the index page

        # Convert timestamp string to a datetime object
        # Assumes the input format from datetime-local input: YYYY-MM-DDTHH:MM
        timestamp = datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M')
        # Convert numeric fields from string to integer
        systolic = int(systolic)
        diastolic = int(diastolic)
        heart_rate = int(heart_rate)

        conn = get_db_connection() # Get a database connection
        if conn: # Proceed only if connection is successful
            cursor = conn.cursor() # Create a cursor
            # SQL query to insert the new data into the Heart table
            cursor.execute(
                "INSERT INTO Heart (timestamp, systolic, diastolic, heart_rate) VALUES (%s, %s, %s, %s)",
                (timestamp, systolic, diastolic, heart_rate)
            )
            conn.commit() # Commit the transaction
            flash("Heart rate entry added successfully.", "success") # Show success message
        else:
            # Show error if database connection failed
            flash("Failed to connect to the database.", "error")

    except ValueError:
        # Handle errors during data type conversion (e.g., non-numeric input for numbers)
        flash("Invalid input. Please check the values.", "error")
    except mysql.connector.Error as err:
        # Handle potential database errors during insertion
        flash(f"Database error: {err}", "error")
        if conn:
            conn.rollback() # Rollback the transaction on error to maintain data integrity
    except Exception as e:
        # Handle any other unexpected errors
        flash(f"An unexpected error occurred: {e}", "error")
    finally:
        # Ensure cursor and connection are closed
        if cursor:
            cursor.close()
        if conn and conn.is_connected(): # Check if connection exists and is open before closing
            conn.close()

    # Redirect back to the index page after attempting to add the entry
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    """Handles editing an existing heart rate entry identified by its ID."""
    conn = None # Initialize connection variable
    cursor = None # Initialize cursor variable

    if request.method == 'POST':
        # Handle the form submission for updating the entry
        try:
            # Get updated data from the form
            timestamp_str = request.form.get('timestamp')
            systolic = request.form.get('systolic')
            diastolic = request.form.get('diastolic')
            heart_rate = request.form.get('heart_rate')

            # Validate and convert data (similar to the 'add' route)
            if not all([timestamp_str, systolic, diastolic, heart_rate]):
                flash("All fields are required.", "error")
                # Fetch the data again to render the edit page with the error
                conn_get = get_db_connection()
                if conn_get:
                    cursor_get = conn_get.cursor(dictionary=True)
                    cursor_get.execute("SELECT * FROM Heart WHERE id = %s", (id,))
                    heart = cursor_get.fetchone()
                    cursor_get.close()
                    conn_get.close()
                    return render_template('edit.html', heart=heart) # Re-render edit page
                else:
                    flash("Failed to connect to database to reload edit form.", "error")
                    return redirect(url_for('index')) # Fallback redirect

            timestamp = datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M')
            systolic = int(systolic)
            diastolic = int(diastolic)
            heart_rate = int(heart_rate)

            conn = get_db_connection() # Get database connection
            if conn:
                cursor = conn.cursor() # Create cursor
                # SQL query to update the record with the matching ID
                cursor.execute(
                    "UPDATE Heart SET timestamp = %s, systolic = %s, diastolic = %s, heart_rate = %s WHERE id = %s",
                    (timestamp, systolic, diastolic, heart_rate, id)
                )
                conn.commit() # Commit the transaction
                flash("Heart rate entry updated successfully.", "success") # Show success message
                return redirect(url_for('index')) # Redirect to index after successful update
            else:
                flash("Failed to connect to the database for update.", "error")

        except ValueError:
            flash("Invalid input. Please check the values.", "error")
        except mysql.connector.Error as err:
            flash(f"Database error during update: {err}", "error")
            if conn:
                conn.rollback() # Rollback on error
        except Exception as e:
            flash(f"An unexpected error occurred during update: {e}", "error")
        finally:
            # Ensure cursor and connection are closed
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()
        # If update failed, try to fetch data again to re-render edit page with error
        conn_get = get_db_connection()
        heart = None
        if conn_get:
            try:
                cursor_get = conn_get.cursor(dictionary=True)
                cursor_get.execute("SELECT * FROM Heart WHERE id = %s", (id,))
                heart = cursor_get.fetchone()
            except mysql.connector.Error as err:
                 flash(f"Database error reloading edit form: {err}", "error")
            finally:
                if 'cursor_get' in locals() and cursor_get: cursor_get.close()
                if conn_get: conn_get.close()
        else:
             flash("Failed to connect to database to reload edit form.", "error")

        if heart:
             # Format timestamp for datetime-local input field before rendering
             if heart.get('timestamp'):
                 heart['timestamp_str'] = heart['timestamp'].strftime('%Y-%m-%dT%H:%M')
             return render_template('edit.html', heart=heart)
        else:
             # If fetching data fails after an update error, redirect to index
             return redirect(url_for('index'))

    else: # request.method == 'GET'
        # Display the form to edit the entry
        conn = get_db_connection() # Get database connection
        heart = None # Initialize heart data variable
        if conn:
            try:
                cursor = conn.cursor(dictionary=True) # Use dictionary cursor
                # Fetch the specific entry to be edited
                cursor.execute("SELECT * FROM Heart WHERE id = %s", (id,))
                heart = cursor.fetchone() # Get the single result
                if heart and heart.get('timestamp'):
                    # Format the timestamp for the datetime-local input field
                    heart['timestamp_str'] = heart['timestamp'].strftime('%Y-%m-%dT%H:%M')
            except mysql.connector.Error as err:
                flash(f"Database error fetching record for edit: {err}", "error")
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()
        else:
            flash("Failed to connect to the database to load edit form.", "error")
            return redirect(url_for('index')) # Redirect if connection fails

        if heart:
            # Render the 'edit.html' template with the fetched data
            return render_template('edit.html', heart=heart)
        else:
            # If the entry with the given ID doesn't exist or couldn't be fetched
            flash("Heart rate entry not found.", "error")
            return redirect(url_for('index')) # Redirect back to the index page

@app.route('/delete/<int:id>')
def delete(id):
    """Deletes a heart rate entry identified by its ID."""
    conn = get_db_connection() # Get database connection
    cursor = None # Initialize cursor variable
    try:
        if conn: # Proceed only if connection is successful
            cursor = conn.cursor() # Create cursor
            # SQL query to delete the record with the matching ID
            cursor.execute("DELETE FROM Heart WHERE id = %s", (id,))
            conn.commit() # Commit the transaction
            flash("Heart rate entry deleted successfully.", "success") # Show success message
        else:
            # Show error if database connection failed
            flash("Failed to connect to the database.", "error")
    except mysql.connector.Error as err:
         flash(f"Database error during deletion: {err}", "error")
         if conn:
             conn.rollback() # Rollback on error
    except Exception as e:
        # Handle any other unexpected errors
        flash(f"An unexpected error occurred during deletion: {e}", "error")
    finally:
        # Ensure cursor and connection are closed
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
    # Redirect back to the index page after attempting deletion
    return redirect(url_for('index'))

# Add this block to run the app directly for development/testing
if __name__ == '__main__':
    # Set debug=True for development; it enables auto-reloading and detailed error pages.
    # Set debug=False for production.
    app.run(debug=True, host='0.0.0.0', port=5001) # Run on port 5001 to avoid conflicts
