""" 
    Title: db_to_textfiles.py
    Author: James Vaughan
    Date: 10 August 2023
    Description: Program to print mySQL database tables to word documents. It should really only be used for smallish databases. :) 
"""

import mysql.connector

# Database configuration
config = {
    "user": "whatabook_user",
    "password": "MySQL8IsGreat!",
    "host": "127.0.0.1",
    "database": "whatabook",
    "raise_on_warnings": True
}

# Function to query the database and save results to a text file
def query_and_save_to_text(query, filename):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    try:
        cursor.execute(query)
        results = cursor.fetchall()

        with open(filename, "w") as file:
            for row in results:
                file.write(str(row) + "\n")

        print("Query results saved to", filename)
    except mysql.connector.Error as err:
        print("Error:", err)
    finally:
        cursor.close()
        connection.close()

def main():
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    try:
        # Get the list of table names from the information schema
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = %s", (config["database"],))
        table_names = [table[0] for table in cursor.fetchall()]

        for table_name in table_names:
            query = f"SELECT * FROM {table_name}"
            filename = f"query_results_{table_name}.txt"

            query_and_save_to_text(query, filename)

        print("Query results saved for all tables")
    except mysql.connector.Error as err:
        print("Error:", err)
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    main()

