""" 
    Title: what_a_book.py
    Author: Ashlyn Barrett
    Due: 08/12/2023
    Assignment: WhatABook 
"""

""" import statements """
import sys
import mysql.connector
from mysql.connector import errorcode

""" database config object """
config = {
    "user": "whatabook_user",
    "password": "MySQL8IsGreat!",
    "host": "127.0.0.1",
    "database": "whatabook",
    "raise_on_warnings": True
}
"""create main menu"""
def show_menu():
  """Displays the main menu and gets the user's choice."""

  print("\n  -- Main Menu --")

  print("    1. View Books")
  print("    2. View Store Locations")
  print("    3. My Account")
  print("    4. Exit Program")

  try:
        choice = int(input('      ---Enter either 1, 2, 3, or 4---   : '))

        return choice
  except ValueError:
        print("\n  Invalid number, program terminated...\n")

        sys.exit(0)

def show_books(_cursor):
    """inner join query"""
    _cursor.execute("SELECT book_id, book_name, author, details FROM book")

    """get the results from the cursor object""" 
    books = _cursor.fetchall()

    print("\n  -- Here are the books --")
    
    """iterate over the player data set and display the results""" 
    for book in books:
     print("Book ID: {}".format(book[0])
            + "\nBook Name: {}".format(book[1])
              +  "\nAuthor: {}".format(book[2])
              + "\nDetails: {}".format(book[3])
                + "\n")
    input("Press enter for main menu ")

def show_locations(_cursor):
    _cursor.execute("SELECT store_id, locale FROM store")

    locations = _cursor.fetchall()

    print("\n  -- DISPLAYING STORE LOCATIONS --")

    for location in locations:
        print("  Locale: {}\n".format(location[1]))

def validate_user():
  """Validates the user's ID."""

  user_id = input("\nEnter a customer id (1-3): ")

  # Validate the user's ID.

  while not user_id.isdigit() or int(user_id) not in range(1, 4):
    print("Invalid customer number. Please enter a number from 1 to 3.")
    user_id = input("\nEnter a customer id (1-3): ")

  return int(user_id)

def show_account_menu():
  """Displays the customer account menu and gets the user's choice."""

  print("""

    ### Customer Menu ###

    1. Wishlist
    2. Add Book
    3. Main Menu

""")

  account_option = input("\n  Enter your choice: ")

  # Validate the user's choice.

  while not account_option.isdigit() or int(account_option) not in [1, 2, 3]:
    print("Invalid choice. Please enter a number from 1 to 3.")
    account_option = input("\n  Enter your choice: ")

  return int(account_option)

def show_wishlist(_cursor, _user_id):
    """ query the database for a list of books added to the users wishlist """

    _cursor.execute("SELECT user.user_id, user.first_name, user.last_name, book.book_id, book.book_name, book.author " + 
                    "FROM wishlist " + 
                    "INNER JOIN user ON wishlist.user_id = user.user_id " + 
                    "INNER JOIN book ON wishlist.book_id = book.book_id " + 
                    "WHERE user.user_id = {}".format(_user_id))
    
    wishlist = _cursor.fetchall()

    print("\n        -- Here is the requested wishlist --")

    for book in wishlist:
         print("        Book Name: {}\n        Author: {}\n".format(book[4], book[5]))

def show_books_to_add(_cursor, _user_id):
    """ query the database for a list of books not in the users wishlist """

    query = query = ("SELECT book_id, book_name, author, details "
            "FROM book "
            "WHERE book_id NOT IN (SELECT book_id FROM wishlist WHERE user_id = {})".format(_user_id))

    print(query)

    _cursor.execute(query)

    books_to_add = _cursor.fetchall()

    print("\n        -- Here are the available books --")

    for book in books_to_add:
        print("        Book Id: {}\n        Book Name: {}\n".format(book[0], book[1]))

def add_book_to_wishlist(_cursor, _user_id, _book_id):
    _cursor.execute("INSERT INTO wishlist(user_id, book_id) VALUES({}, {})".format(_user_id, _book_id))

try:
    """ try/catch block for handling potential MySQL database errors """ 

    db = mysql.connector.connect(**config) # connect to the WhatABook database 

    cursor = db.cursor() # cursor for MySQL queries

    print("\n  Hello, this is WhatABook! ")

    user_selection = ""

    # while the user's selection is not 4
    while user_selection != 4:
        user_selection = show_menu() # show the main menu
        # If the user selects option one, show_books method is activated
        if user_selection == 1:
            show_books(cursor)

        # If the user selects option two, show_locations method is activated
        if user_selection == 2:
            show_locations(cursor)

        # If the user selects option 3, validate_user method is activated
        if user_selection == 3:
            my_user_id = validate_user()
            account_option = show_account_menu() #Show the account settings menu


            # while the user's selection is not 3
            while account_option != 3:

                # If the use selects option 1, show_wishlist() method is activated to show the current users 
                # configured wishlist items 
                if account_option == 1:
                    show_wishlist(cursor, my_user_id)

                # if the user selects option 2, show_books_to_add function is activated to show the user 
                # the books not currently configured in the users wishlist
                if account_option == 2:

                    # show books that can be added to users wishlist
                    show_books_to_add(cursor, my_user_id)

                    # get the entered book_id 
                    book_id = int(input("\n       Enter book id you wish to add: "))
                    
                    # add the selected book the users wishlist
                    add_book_to_wishlist(cursor, my_user_id, book_id)

                    db.commit() # commit the changes to the database 

                    print("\n        Book id: {} has succesfully been added to your wishlist!".format(book_id))

                # if the selected option is less than 0 or greater than 3, display an invalid user selection 
                if account_option < 0 or account_option > 3:
                    print("\n      Invalid option, try again...")

                # show the account menu 
                account_option = show_account_menu()
        
        # if the user selection is less than 0 or greater than 4, display an invalid user selection
        if user_selection < 0 or user_selection > 4:
            print("\n      Invalid option, try again...")
            


    print("\n\n  Program terminated...")

except mysql.connector.Error as err:
    """ handle errors """ 

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
    