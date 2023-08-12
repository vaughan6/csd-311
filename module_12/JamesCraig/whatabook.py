# This application simulates a book store application that stores book and user data including
# wishlists that a user can modify. The data is stored within a database and it uses SQL queries
# within the application to pull or add data to the user's wishlist within the database.  
import mysql.connector
from mysql.connector import errorcode
import sys

# Setup server configuration details for MySQL connection
config = {
    "user": "whatabook_user",
    "password": "MySQL8IsGreat!",
    "host": "127.0.0.1",
    "database": "whatabook",
    "raise_on_warnings": True
}
# Show menu function that displays the main menu to a user and then takes the user input and calls
# other functions as needed. 
def show_menu():
    # Prompt user for input and store it for processing
    menu_input = (input("╔══════════════════════╗\n" +
                        "║ Welcome to WhatABook ║\n" +
                        "╚══════════════════════╝\n\n" +
                        "Please select a menu option:\n" +
                        "----------------------------\n" +
                        "| 1. View Books            |\n" +
                        "| 2. View Store Locations  |\n" +
                        "| 3. My Account            |\n" +
                        "| 4. Exit Program          |\n" +
                        "----------------------------\n"))
    # Process the input data to display the proper menu option or display message if not valid.
    if menu_input == "1":
        show_books(cursor)
    elif menu_input == "2":
        show_locations(cursor)
    elif menu_input == "3":
        validate_user()
        show_account_menu()
    elif menu_input == "4":
        print("\nThanks for using WhatABook now exiting application.\n")
        sys.exit()
    else:
        print("\nInvalid input please try again.\n")
        show_menu()
    
# Function shows all books within the database
def show_books(_cursor):
    # Use cursor to execute SQL queries and store them within the books variable.
    _cursor.execute("SELECT book_id, book_name, author, details FROM book ORDER BY book_name")
    books = _cursor.fetchall()

    print("\n+-----------------------------------+\n" +
          "|        WhatABook Inventory        |\n" +
          "+-----------------------------------+\n")

    # For each record retrieved from the books retrieved display them to the user..
    for book in books:
        print("Book ID: {}".format(book[0]) + "\nBook Name: {}".format(book[1]) + 
              "\nAuthor: {}".format(book[2])+ "\nDetails: {}".format(book[3]) + "\n")
    input("Press enter to return to the previous menu... ")
    show_menu()

# Method prints all store information in the database.   
def show_locations(_cursor):
    # Execute teh SQL query and store it within the variable stores.
    _cursor.execute("SELECT * FROM store")
    stores = _cursor.fetchall()

    print("\n+-----------------------------------------+\n" +
           "|        WhatABook Store Locations        |\n" +
           "+-----------------------------------------+\n")
    # Display each store stored within the stores variable.
    for store in stores:
        print("Store ID: {}".format(store[0]) + "\nStore Address: {}".format(store[1]) + "\n")
    input("Press enter to return to the previous menu... ")
    show_menu()

# This function validates if a user is within the database and then shows the account menu for the
# user entered.
def validate_user():
    # Storing user id so it can be accessed by other methods to display and modify user data.
    global user_input
    user_input = (input("╔═══════════════╗\n" +
                        "║ Account Login ║\n" +
                        "╚═══════════════╝\n\n" +
                        "Please enter your user ID: "))

    # If block to look for value to exit menu
    if user_input.lower() == "q":
        input("Exiting account login menu press enter to continue... ")
        return show_menu()
    # Try block to retrieve if user is within the database and if successful print welcome message.
    try:
        global users
        cursor.execute("SELECT * FROM user WHERE user_id = " + user_input)
        users = cursor.fetchall()
        print("\nWelcome to the WhatABook application " + users[0][1] + " " + users[0][2] + ".")
    # Throw exception message to user and require reentry of user id.
    except:
        print("\nUser ID " + user_input + " was not found please try again.\n"+
              "Or enter q to quit and exit to pervious menu.")
        return validate_user()

# Function displays account menu and calls other functions to display and modify user's account.
def show_account_menu():
    # Store and process user's input for account menu.
    acc_input = input("╔════════════╗\n" +
                      "║ My Account ║\n" +
                      "╚════════════╝\n\n" +"Please select a menu option:\n" +
                      "----------------------------\n" +
                      "| 1. View Wishlist         |\n" +
                      "| 2. Add Book to Wishlist  |\n" +
                      "| 3. Main Menu             |\n" + 
                      "----------------------------\n")
    #Call the appropriate function to ensure the user gets the requested menu.
    if acc_input == "1":
        show_wishlist(cursor, user_input)
    elif acc_input == "2":
        show_books_to_add(cursor, user_input)
    elif acc_input == "3":
        show_menu()
    else:
        print("Invalid input please try again.")

# Function to pull user's wishlist data from the database and display it.
def show_wishlist(_cursor, _user_id):
    # Execute SQL query to pull wishlist data for a specific user based on the user input
    # that was validated previously. Then store it within wishlists variable.
    _cursor.execute("SELECT book.book_id, book_name, author, details " +
                   "FROM user " +
                   "INNER JOIN wishlist ON user.user_id = wishlist.user_id " +
                   "INNER JOIN book ON wishlist.book_id = book.book_id " +
                   "WHERE user.user_id =" + _user_id + " ORDER BY book_name")
    wishlists = _cursor.fetchall()
    # Display user's wishlisted books and then return to the account menu.
    print("\n+--------------------------------------+\n" +
        "|      " + users[0][1] + " " + users[0][2] + "'s Wishlist      |\n" +
        "+--------------------------------------+\n")
    for wishlist in wishlists:
        print("Book ID: {}".format(wishlist[0]) + "\nBook Name: {}".format(wishlist[1]) + 
              "\nAuthor: {}".format(wishlist[2])+ "\nDetails: {}".format(wishlist[3]) + "\n")
    input("Press enter to return to the previous menu... ")
    show_account_menu()

# Function to display books that are available for user to wishlist. Books not currently wishlisted
# by them. 
def show_books_to_add(_cursor, _user_id):
    # Perform SQL query to pull books available to the user and store them within availbook variable.
    print("\n+-----------------------------------+\n" +
          "|          Available Books          |\n" +
          "+-----------------------------------+\n")
    _cursor.execute("SELECT book_id, book_name, author, details "+
                   "FROM book " +
                   "WHERE book_id NOT IN (SELECT book_id FROM wishlist WHERE user_id = " + 
                   _user_id +") ORDER BY book_name;")
    availbooks = _cursor.fetchall()

    # This handles if there are no books available if a user has every book wishlisted.
    if len(availbooks) == 0:
        input("There are no available books to add to the wishlist. Press enter to continue.")
        show_account_menu()
    # Otherwise if there are available books we print each one along with an option number 
    # the user will enter to easily select books with fewer numbers needing to be entered.
    else:
        counter = 0
        for availbook in availbooks:
            print("+-------------+\n|  Option: {}".format(counter + 1) + "  |\n+-------------+\n" +
                   "Book ID: {}".format(availbook[0]) + "\nBook Name: {}".format(availbook[1]) + 
              "\nAuthor: {}".format(availbook[2])+ "\nDetails: {}".format(availbook[3]) + "\n")
            counter += 1
        # Try block that inserts the wishlisted book option into the wishlist table for the user.
        try:
            # Prompt for book option from user and store the book_id for the specific book.
            book_opt = int(input("Please enter an option for which book to add: "))
            book_id = str(availbooks[book_opt-1][0])
            # Execute SQL INSERT statement to add value to the wishlist table for the user and
            # the book ID selected by the user.
            _cursor.execute("INSERT INTO wishlist (user_id, book_id) " +
                       "VALUES (" + str(_user_id) + ", " + book_id + ")")
            print("\nAdded " + availbooks[book_opt-1][1] + " to the wishlist sucessfully.")
            input("Press enter to continue...")
        # Throws an exception if the option is not valid within the current options for available
        # books
        except:
            print("Invalid book option please try again")
            show_books_to_add(cursor, _user_id)
        # After adding the book successfully return to the previous account menu for the user.
        show_account_menu()
# Try/except block for handling potential MySQL database errors
try:
    db = mysql.connector.connect(**config) # connect to the WhatABook database 
    cursor = db.cursor() # cursor for MySQL queries
    show_menu()
# Throws an exception if there is an error.
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("  The supplied username or password are invalid")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("  The specified database does not exist")
    else:
        print(err)
# Close connection to database after determining an exception error.
finally:
    """ close the connection to MySQL """
    db.close()
