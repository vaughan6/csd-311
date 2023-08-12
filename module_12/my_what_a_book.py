""" 
    Title: my_what_a_book.py
    Author: James Vaughan
    Date: 12 August 2023
    Description: Program for interacting with whatabook database
"""

import mysql.connector
from mysql.connector import errorcode
from tabulate import tabulate

# Database configuration
config = {
    "user": "whatabook_user",
    "password": "MySQL8IsGreat!",
    "host": "127.0.0.1",
    "database": "whatabook",
    "raise_on_warnings": True
}

# Function to establish a connection to the MySQL database
def create_connection():
    return mysql.connector.connect(**config)

# Function to display the main menu
def display_main_menu():
    print("===== Main Menu =====")
    print("1. View Books")
    print("2. View Store Locations")
    print("3. My Account")
    print("4. Exit Program")

# Function to display the Wishlist menu
def display_wishlist_menu():
    print("\n===== Wishlist Menu =====")
    print("1. Wishlist")
    print("2. Add Book to Wishlist")
    print("3. Main Menu")

# Function to display the Wishlist menu and handle user choices
def wishlist_menu(connection, user_id):
    while True:
        display_wishlist_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            view_user_wishlist(connection, user_id)
        elif choice == "2":
            add_book_to_wishlist(connection, user_id)
        elif choice == "3":
            break  # Exit the loop and return to the main menu
        else:
            print("Invalid choice. Please try again.")

# Function to view available books from the "book" table
def view_books(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT book_id, book_name, author, details FROM book")
    books = cursor.fetchall()
    print("\n===== Available Books =====")
    print(tabulate(books, headers=["Book ID", "Book Name", "Author", "Details"], tablefmt="grid"))
    input("Press enter to return to the previous menu... ")

# Function to view store locations and hours with store numbers
def view_store_locations(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT store_id, locale FROM store")
    store_locations = cursor.fetchall()

    print("\n===== Store Locations and Hours =====")
    for store_id, location in store_locations:
        print(f"Store #{store_id}:\n\t{location}")
    input("Press enter to return to the previous menu... ")

# Function to handle user account and wishlist interactions
def my_account(connection):
    while True:
        user_id = input("\nEnter your user_id: ")
        try:
            user_id_int = int(user_id)
        except ValueError:
            input("Invalid input. Press enter to continue.")
            continue  # Restart the loop to get a valid input

        cursor = connection.cursor()

        # Check if the user exists and get their first name and last name
        cursor.execute("SELECT user_id, first_name, last_name FROM user WHERE user_id = %s", (user_id_int,))
        user = cursor.fetchone()

        if user:
            user_id, first_name, last_name = user
            print(f"\nWelcome, {first_name} {last_name}!")

            wishlist_menu(connection, user_id_int)
            break  # Exit the loop if wishlist_menu is done
        else:
            print("Invalid user_id. Please try again.")




# Function to view user's wishlist from the "wishlist" table
def view_user_wishlist(connection, user_id):
    cursor = connection.cursor()
    cursor.execute("SELECT w.wishlist_id, b.book_name, b.author, b.details "
                   "FROM wishlist w "
                   "JOIN book b ON w.book_id = b.book_id "
                   "WHERE w.user_id = %s", (user_id,))
    wishlist = cursor.fetchall()

    print("\n===== Your Wishlist =====")
    print(tabulate(wishlist, headers=["Wishlist ID", "Book Name", "Author", "Details"], tablefmt="grid"))
    input("Press enter to return to the previous menu... ")


# Function to add a book to the user's wishlist
def add_book_to_wishlist(connection, user_id):
    cursor = connection.cursor()

    while True:
        # Retrieve books not in the user's wishlist
        cursor.execute("SELECT b.book_id, b.book_name, b.author, b.details "
                       "FROM book b "
                       "WHERE b.book_id NOT IN (SELECT w.book_id FROM wishlist w WHERE w.user_id = %s)", (user_id,))
        available_books = cursor.fetchall()

        print("\n===== Available Books =====")
        print(tabulate(available_books, headers=["Book ID", "Book Name", "Author", "Details"], tablefmt="grid"))

        book_id = input("\nEnter the Book ID you want to add to your wishlist (or 'cancel' to go back to the previous menu): ")

        if book_id.lower() == "cancel":
            break  # Exit the loop and return to the previous menu

        try:
            book_id_int = int(book_id)
        except ValueError:
            input("Invalid input. Press enter to display the list again.")
            continue  # Go to the next iteration of the loop

        # Check if the selected book_id is available
        selected_book = next((book for book in available_books if book[0] == book_id_int), None)
        
        if selected_book:
            # Insert the book into the wishlist
            cursor.execute("INSERT INTO wishlist (user_id, book_id) VALUES (%s, %s)", (user_id, book_id_int))
            connection.commit()
            
            keep_adding = input("Book added to your wishlist successfully! Would you like to add another? (yes/no)")
            
            if keep_adding.lower() == "no":
                break  # Exit the loop and return to the previous menu
            elif keep_adding.lower() == "yes":
                continue
            else:
                input("Your input is not understood. Press Enter to see what you can add to your wishlist.")
        else:
            input("Invalid Book ID. Please try again. (Press Enter to continue)")



        



# Main function to run the program
def main():
    connection = None

    try:
        connection = create_connection()

        while True:
            display_main_menu()
            choice = input("Enter your choice: ")

            if choice == "1":
                view_books(connection)
            elif choice == "2":
                view_store_locations(connection)
            elif choice == "3":
                my_account(connection)
            elif choice == "4":
                print("Exiting the program. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
    except mysql.connector.Error as err:
        # Handle errors
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("The supplied username or password is invalid.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("The specified database does not exist.")
        else:
            print("Error:", err)
    finally:
        # Close the connection to MySQL
        if connection:
            connection.close()

if __name__ == "__main__":
    main()