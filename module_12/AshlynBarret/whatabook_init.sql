"""create new user and assign password"""
CREATE USER 'whatabook_user'@'localhost' IDENTIFIED WITH mysql_native_password BY 'MySQL8IsGreat!';

"""grant all privileges to the whatabook database to user whatabook_user on localhost""" 
GRANT ALL PRIVILEGES ON whatabook.* TO'whatabook_user'@'localhost';

"""Create four tables"""
CREATE TABLE store (
    store_id    INT             NOT NULL    AUTO_INCREMENT,
    locale      VARCHAR(500)    NOT NULL,
    PRIMARY KEY(store_id)
);

CREATE TABLE book (
    book_id     INT             NOT NULL    AUTO_INCREMENT,
    book_name   VARCHAR(200)    NOT NULL,
    author      VARCHAR(200)    NOT NULL,
    details     VARCHAR(500),
    PRIMARY KEY(book_id)
);

CREATE TABLE user (
    user_id         INT         NOT NULL    AUTO_INCREMENT,
    first_name      VARCHAR(75) NOT NULL,
    last_name       VARCHAR(75) NOT NULL,
    PRIMARY KEY(user_id) 
);

CREATE TABLE wishlist (
    wishlist_id     INT         NOT NULL    AUTO_INCREMENT,
    user_id         INT         NOT NULL,
    book_id         INT         NOT NULL,
    PRIMARY KEY (wishlist_id),
    CONSTRAINT fk_book
    FOREIGN KEY (book_id)
        REFERENCES book(book_id),
    CONSTRAINT fk_user
    FOREIGN KEY (user_id)
        REFERENCES user(user_Id)
);

"""create store"""
INSERT INTO store(locale) VALUES('2120 Stemmons Fwy, Sanger, TX 76266'); 

"""create 9 books"""
INSERT INTO book(book_name, author) VALUES('Fourth Wing', 'Rebecca Yarros');

INSERT INTO book(book_name, author) VALUES('Crossed', 'Emily McIntire');

INSERT INTO book(book_name, author) VALUES('Holly', 'Stephen King');

INSERT INTO book(book_name, author) VALUES('The Outsiders', 'S.E. Hinton');

INSERT INTO book(book_name, author) VALUES('The Nightingale', 'Kristin Hannah');

INSERT INTO book(book_name, author) VALUES('Oppenheimer', 'Christopher Nolan');

INSERT INTO book(book_name, author) VALUES('The Housemaid', 'Freida McFadden');

INSERT INTO book(book_name, author) VALUES('Happiness: A Novel', 'Danielle Steel');

INSERT INTO book(book_name, author) VALUES('Remarkably Bright Creatures (Read with Jenna Pick)', 'Shelby Van Pelt');

"""create three users""" 
INSERT INTO user(first_name, last_name) VALUES('Austin', 'Leo');

INSERT INTO user(first_name, last_name) VALUES('Ashlyn', 'Danielle');

INSERT INTO user(first_name, last_name)VALUES('Miles', 'Edison');

"""create one wishlist per user"""
INSERT INTO wishlist(user_id, book_id)
  VALUES (
        (SELECT user_id FROM user WHERE first_name = 'Ashlyn'), 
        (SELECT book_id FROM book WHERE book_name = 'The Housemaid')
    );

INSERT INTO wishlist(user_id, book_id) 
 VALUES (
        (SELECT user_id FROM user WHERE first_name = 'Austin'),
        (SELECT book_id FROM book WHERE book_name = 'The Outsiders')
    );

INSERT INTO wishlist(user_id, book_id)
 VALUES (
        (SELECT user_id FROM user WHERE first_name = 'Miles'),
        (SELECT book_id FROM book WHERE book_name = 'Oppenheimer')
    );